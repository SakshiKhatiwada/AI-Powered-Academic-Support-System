from app.prompts.notes_generation.base import chapter_base_prompt, topic_base_prompt

from .ai_ml import ai_ml_chapter_prompt, ai_ml_topic_prompt


def get_notes_generation_prompt(category: str = "", level: str = "chapter", type: str = "logical"):
    if type == "logical":
        if category == "ai_ml":
            if level == "chapter":
                return ai_ml_chapter_prompt
            else:
                return ai_ml_topic_prompt

        if level == "chapter":
            return chapter_base_prompt
        else:
            return topic_base_prompt
