"""Data models for course structure and summaries."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class SummaryType(str, Enum):
    FULL = "full"
    TOPIC = "topic"
    KEY_CONCEPTS = "key_concepts"
    EXAM_PREP = "exam_prep"


class Language(str, Enum):
    HEBREW = "he"
    ENGLISH = "en"


@dataclass
class Topic:
    name: str
    description: str = ""
    subtopics: list[str] = field(default_factory=list)
    key_concepts: list[str] = field(default_factory=list)
    learning_objectives: list[str] = field(default_factory=list)


@dataclass
class Course:
    name: str
    description: str = ""
    instructor: str = ""
    topics: list[Topic] = field(default_factory=list)
    target_audience: str = ""
    prerequisites: list[str] = field(default_factory=list)
    language: Language = Language.HEBREW

    @classmethod
    def from_dict(cls, data: dict) -> "Course":
        language = Language(data.get("language", "he"))
        topics = [
            Topic(
                name=t["name"],
                description=t.get("description", ""),
                subtopics=t.get("subtopics", []),
                key_concepts=t.get("key_concepts", []),
                learning_objectives=t.get("learning_objectives", []),
            )
            for t in data.get("topics", [])
        ]
        return cls(
            name=data["name"],
            description=data.get("description", ""),
            instructor=data.get("instructor", ""),
            topics=topics,
            target_audience=data.get("target_audience", ""),
            prerequisites=data.get("prerequisites", []),
            language=language,
        )
