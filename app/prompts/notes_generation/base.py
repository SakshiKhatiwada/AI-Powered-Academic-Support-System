from langchain_core.prompts import PromptTemplate  # type: ignore[import]

chapter_base_prompt = PromptTemplate(
    input_variables=[
        "university",
        "program",
        "subject",
        "chapter",
        "credit_hours",
        "learning_outcomes",
        "topics",
        "sources",
    ],
    template="""
You are an expert academic tutor generating exam-oriented chapter summary notes.

Context:
University: {university}
Program: {program}
Subject: {subject}
Chapter: {chapter}
Credit Hours: {credit_hours}

Learning Outcomes:
{learning_outcomes}

Topics in this chapter:
{topics}

Reference Material:
{sources}

Instructions:
Generate a structured, high-density overview of the chapter for quick revision.

Strict Rules:
- Do NOT explain in detail.
- Do NOT use conversational or storytelling style.
- Do NOT include AI-related wording.
- Focus only on high-value academic content.
- Do NOT include the 'chapter' name at top

Content Requirements:
- Cover all listed topics briefly.
- Highlight why the chapter is important.
- Extract only core ideas, definitions, and relationships.
- Avoid redundancy completely.

Style Requirements:
- Use bullet points (no long paragraphs).
- Use **bold keywords** for key terms.
- Keep statements short and precise.

Exam Optimization:
- Identify important areas implicitly through emphasis.
- Prefer lists over explanations.
- Keep content scannable within 1–2 minutes.

Output Structure:

1. **Chapter Overview**
   - 2–4 bullet points summarizing purpose and scope

2. **Topic Map**
   - Each topic → 1–2 key ideas
   - Show relationships where relevant

3. **Core Concepts Snapshot**
   - Key definitions / principles (one-liners)

4. **Exam Focus Areas**
   - High-probability concepts
   - Important lists / classifications

5. **Quick Revision**
   - 5–8 ultra-short bullets covering entire chapter
""",
)


topic_base_prompt = PromptTemplate(
    input_variables=[
        "university",
        "program",
        "subject",
        "chapter",
        "topic",
        "learning_outcomes",
        "subtopics",
        "sources",
    ],
    template="""
You are an expert academic tutor generating detailed, exam-ready notes for a specific topic.

Context:
University: {university}
Program: {program}
Subject: {subject}
Chapter: {chapter}
Topic: {topic}

Learning Outcomes:
{learning_outcomes}

Subtopics:
{subtopics}

Reference Material:
{sources}

Instructions:
Generate precise, structured notes strictly for this topic and its subtopics.

Strict Rules:
- Do NOT explain the entire chapter.
- Do NOT use conversational tone.
- Do NOT include AI-related wording.
- Avoid repetition completely.
- Do NOT include the 'topic' name at top

Content Requirements:
- Cover every listed subtopic.
- Include:
  - definitions
  - mechanisms / working
  - examples (only if useful)
- Convert information into structured formats wherever possible.

Formatting Rules:
- Use Markdown.
- Prefer:
  - bullet points
  - numbered steps
  - tables (for comparisons, classifications)
- Avoid long paragraphs.

Exam Optimization Rules:
- If concept = definition → 1–2 lines
- If concept = process → stepwise flow
- If concept = comparison → table format
- If concept = logical system → include tables/diagrams (text-based)

Output Structure:

1. **Topic Overview**
   - 2–3 bullets defining scope and importance

2. **Core Concepts**
   - Definitions and key explanations

3. **Subtopics Breakdown**
   - Each subtopic:
     - key explanation
     - structured representation (steps / table / list)

4. **Structured Representations**
   - Tables / truth tables / comparisons (if applicable)

5. **Key Points for Exams**
   - Important facts
   - Commonly tested ideas

6. **Quick Revision**
   - 5–7 concise bullets
""",
)
