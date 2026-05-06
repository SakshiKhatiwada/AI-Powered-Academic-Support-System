from __future__ import annotations

import asyncio
import logging
from typing import Any

from app.adapters.llm.base import LLMAdapter
from app.prompts.notes_generation import get_notes_generation_prompt
from app.schemas.inference import GenerateNotesRequest, NotesLevel


class GenerationService:

    def __init__(
        self,
        llm_service: LLMAdapter,
        temperature: float = 0.25,
        timeout: int = 60,
        retries: int = 2,
        max_tokens: int = 3000,
        max_source_entries: int = 6,
    ):
        self.llm_service = llm_service
        self.temperature = temperature
        self.timeout = timeout
        self.retries = retries
        self.logger = logging.getLogger(__name__)
        self.max_tokens = max_tokens
        self.max_source_entries = max_source_entries

    async def generate_notes(
        self, context: GenerateNotesRequest, sources: list[dict[str, Any]]
    ) -> str:
        if context is None:
            raise ValueError("context is required")

        if not isinstance(sources, list):
            raise ValueError("sources must be a list of dicts")

        formatted_sources = self._prepare_sources(sources)

        if context.level == NotesLevel.CHAPTER:
            return await self.generate_chapter_notes(context, formatted_sources)

        if context.level == NotesLevel.TOPIC:
            return await self.generate_topic_notes(context, formatted_sources)

        raise ValueError("Invalid notes level")

    async def generate_chapter_notes(
        self,
        context: GenerateNotesRequest,
        sources: str,
    ) -> str:

        chapter_notes_prompt = get_notes_generation_prompt(category="", level="chapter")

        prompt = chapter_notes_prompt.format(
            university=context.university,
            program=context.program,
            subject=context.subject,
            chapter=context.chapter,
            credit_hours=context.chapter_credit_hours,
            learning_outcomes=self._format_list(context.learning_outcomes),
            topics=self._format_list(context.topics),
            sources=sources,
        )

        return await self._call_llm(prompt)

    async def generate_topic_notes(
        self,
        context: GenerateNotesRequest,
        sources: str,
    ) -> str:

        topic_notes_prompt = get_notes_generation_prompt(category="", level="topic")

        prompt = topic_notes_prompt.format(
            university=context.university,
            program=context.program,
            subject=context.subject,
            chapter=context.chapter,
            topic=context.topic_title,
            learning_outcomes=self._format_list(context.learning_outcomes),
            subtopics=self._format_list(context.subtopics),
            sources=sources,
        )

        return await self._call_llm(prompt)

    def _prepare_sources(self, sources: list[dict[str, Any]]) -> str:
        entries = self._dedupe_source_entries(sources)
        if not entries:
            return "No reference materials retrieved."

        return self._format_source_entries(entries)

    def _dedupe_source_entries(self, sources: list[dict[str, Any]]) -> list[dict[str, str]]:
        seen = set()
        entries: list[dict[str, str]] = []

        for src in sources:
            raw_text = (src.get("content") or src.get("text") or "").strip()
            if not raw_text:
                continue

            normalized = self._normalize_text(raw_text)
            if normalized in seen:
                continue

            seen.add(normalized)
            label = (
                src.get("document_id")
                or src.get("id")
                or (src.get("metadata") or {}).get("title")
                or f"source_{len(entries)+1}"
            )

            entries.append({"text": raw_text, "label": label})

            if len(entries) >= self.max_source_entries:
                break

        return entries

    def _format_source_entries(self, entries: list[dict[str, str]]) -> str:
        formatted = []
        for idx, entry in enumerate(entries, start=1):
            formatted.append(f"Source {idx} ({entry['label']}):\n{entry['text']}")
        return "\n\n".join(formatted)

    def _format_list(self, items: list[str] | None) -> str:
        if not items:
            return "Not specified"

        return "\n".join(f"- {item}" for item in items)

    def _normalize_text(self, text: str) -> str:
        return " ".join(text.split())

    async def _call_llm(self, prompt: str) -> str:
        for attempt in range(self.retries + 1):
            try:
                return await self.llm_service.generate_text(
                    prompt=prompt,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                )

            except Exception as e:
                self.logger.warning(f"LLM attempt {attempt+1} failed: {e}")

                if attempt >= self.retries:
                    raise

                await asyncio.sleep(2**attempt)
        raise RuntimeError("LLM generation failed after retries")
