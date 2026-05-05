from dataclasses import dataclass
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator

@dataclass
class TopicContext(BaseModel):
    syllabus_id: str | None = None
    subject: str
    topic: str
    subtopics: list[str]
    
class QueryResponse(BaseModel):
    answer: str
    
class NotesLevel(StrEnum):
    CHAPTER = "chapter"
    TOPIC = "topic"
class GenerateNotesRequest(BaseModel):
    subject_id: str | None = None
    document_id: str | None = None
    
    university: str
    program: str
    subject: str
    learning_outcomes: list[str] | None = None
    
    chapter: str
    chapter_credit_hours: int
    
    level: NotesLevel
    topic_title: str | None = Field(
        default=None,
        description="Title of the topic for which notes should be generated. "
        "Required when level='topic'. Optional or ignored when level='chapter'."
    )
    
    topics: list[str]
    subtopics: list[str] | None = Field(
        default=None,
        description="List of subtopics for topic-level notes. "
        "If absent, `topics` may be used as a fallback for backwards compatibility.",
    )
    
    @model_validator(mode="after")
    def validate_for_topic_level(cls, values):
        level = values.level
        topic_title = values.topic_title
        topics = values.topics or []
        subtopics = values.subtopics or topics
        
        if level == NotesLevel.TOPIC:
            if not topic_title:
                raise ValueError("topic_title is required when level is 'topic'")
            if not subtopics:
                raise ValueError("At least one subtopic is required for topic-level notes")
            
        if level == NotesLevel.CHAPTER and not topics:
            raise ValueError("At least one topic is required for chapter-level notes")
            
        values.subtopics = subtopics
        return values
                
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "subject_id": "ai-tu-001",
                "document_id": "ai-chapter-2",
                "university": "Tribhuvan University",
                "program": "BSc CSIT",
                "subject": "Artificial Intelligence",
                "learning_outcomes": [
                    "Introduce fundamental concepts of Artificial Intelligence and intelligent systems.",
                    "Design intelligent agents and apply AI techniques to solve real-world problems.",
                    "Understand knowledge representation, machine learning, neural networks and NLP applications.",
                ],
                "chapter": "2. Intelligent Agents",
                "chapter_credit_hours": 4,
                "level": "topic",
                "topic_title": "Environment Types",
                "topics": [
                    "Deterministic",
                    "Stochastic",
                    "Static",
                    "Dynamic",
                    "Observable",
                    "Semi-observable",
                    "Single Agent",
                    "Multi Agent",
                ],
                "subtopics": [
                    "Deterministic",
                    "Stochastic",
                    "Static",
                    "Dynamic",
                    "Observable",
                    "Semi-observable",
                    "Single Agent",
                    "Multi Agent",
                ],
            }
        }
    )
