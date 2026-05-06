from langchain_core.prompts import PromptTemplate  # type: ignore[import]

from app.prompts.notes_generation.base import chapter_base_prompt, topic_base_prompt

ai_ml_chapter_prompt = PromptTemplate(
    input_variables=chapter_base_prompt.input_variables,
    template=chapter_base_prompt.template
    + """

Additional Instructions (AI/ML Subjects):

- Emphasize how topics relate to:
  - intelligent systems
  - data processing
  - learning mechanisms

- For each topic, briefly indicate:
  → purpose
  → where it is used

- Highlight relationships between topics such as:
  - data → model → output
  - input → transformation → result

- Where applicable, group topics into:
  - concepts
  - methods
  - applications

- Avoid mathematical detail at chapter level.
""",
)


ai_ml_topic_prompt = PromptTemplate(
    input_variables=topic_base_prompt.input_variables,
    template=topic_base_prompt.template
    + """

Additional Instructions (AI/ML Topics):

Content Focus:
- Clearly define all key terms.
- Explain:
  → what the concept is
  → why it is used
  → how it works

Structured Explanation Rules:
- If concept involves a system/model:
  → break into: Input → Process → Output

- If concept involves a pipeline:
  → present step-by-step flow

- If concept involves algorithm:
  → describe in ordered steps (not code unless essential)

- If concept involves comparison:
  → use table format

- If concept involves transformation (e.g., image/data):
  → show before → after idea clearly

Technical Representation:
- Use tables for:
  - comparisons
  - feature differences
  - evaluation metrics
- Use bullet sequences for flows and pipelines

Mathematics Handling:
- Include formulas ONLY if essential
- Do not derive unless explicitly required
- Keep formulas minimal and exam-relevant

Clarity Rules:
- Avoid vague wording like “improves performance”
- Be specific about:
  - inputs
  - outputs
  - purpose

Exam Focus Additions:
- Highlight commonly asked concepts such as:
  - definitions
  - model components
  - differences between methods
- Include edge distinctions (e.g., supervised vs unsupervised)

""",
)
