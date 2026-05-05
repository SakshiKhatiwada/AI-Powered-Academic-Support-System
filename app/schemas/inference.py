from pydantic import BaseModel, ConfigDict, Field

class TopicContext(BaseModel):
    syllabus_id: str | None = None
    university: str
    program: str
    subject: str
    chapter: str | None = None
    topic: str
    subtopics: list[str]
    hours: int | None = None
    learning_outcomes: list[str] | None = None
    
class QueryRequest(BaseModel):
    context: TopicContext
    
class QueryResponse(BaseModel):
    answer: str
    
class ChapterTopic(BaseModel):
    name: str
    subtopics: list[str] = Field(default_factory = list)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
               "name": "Clustering Techniques",
                "subtopics": [
                    "Partitioning (k-means, k-means++, Mini-Batch k-means, k-medoids)",
                    "Hierarchical (Agglomerative and Divisive)",
                    "Density based (DBSCAN)",
                    "Outlier analysis",
                ],
            }
        }
    )
    
class ChapterNoteContext(BaseModel):
    syllabus_id: str | None = None
    university: str
    program: str
    subject: str
    chapter: str
    chapter_hours: int
    topics: list[ChapterTopic]
    learning_outcomes: list[str] | None = None
    
class ChapterQueryRequest(BaseModel):
    context: ChapterNoteContext
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "context": {
                     "syllabus_id": "dm-unit-7",
                    "university": "TU",
                    "program": "BSc CSIT",
                    "subject": "Data Mining",
                    "chapter": "7. Cluster Analysis",
                    "chapter_hours": 8,
                    "topics": [
                        {
                            "name": "7.1. Clustering Basics",
                            "subtopics": [
                                "Types of data in cluster analysis",
                                "Similarity and dissimilarity between objects",
                            ],
                        },
                        {
                            "name": "7.2. Clustering Techniques",
                            "subtopics": [
                                "Partitioning (k-means, k-means++, Mini-Batch k-means, k-medoids)",
                                "Hierarchical (Agglomerative and Divisive)",
                                "Density based (DBSCAN)",
                                "Outlier analysis",
                            ],
                        },
                    ],
                    "learning_outcomes": [
                        "Explain major clustering approaches and their tradeoffs",
                        "Apply clustering algorithms to exam-style problems",
                    ],
                }
            }
        }
    )