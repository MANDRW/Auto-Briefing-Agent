from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class Article(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    url: str = Field(unique=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_processed: bool = Field(default=False)
