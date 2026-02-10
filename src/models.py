from typing import List, Optional
import datetime
from sqlmodel import SQLModel, Field, Relationship


class ActivityStudent(SQLModel, table=True):
    activity_name: str = Field(foreign_key="activity.name", primary_key=True)
    student_email: str = Field(foreign_key="student.email", primary_key=True)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)


class Activity(SQLModel, table=True):
    name: str = Field(primary_key=True)
    description: str
    schedule: str
    max_participants: int
    participants: List["Student"] = Relationship(back_populates="activities", link_model=ActivityStudent)


class Student(SQLModel, table=True):
    email: str = Field(primary_key=True)
    name: Optional[str] = None
    grade: Optional[int] = None
    activities: List[Activity] = Relationship(back_populates="participants", link_model=ActivityStudent)
