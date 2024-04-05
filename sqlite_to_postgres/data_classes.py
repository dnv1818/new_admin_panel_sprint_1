from dataclasses import dataclass
import decimal
from uuid import UUID
from datetime import datetime, date
from typing import Optional


@dataclass
class Filmwork:
    id: UUID
    title: str
    description: Optional[str]
    creation_date: Optional[date]
    file_path: Optional[str]
    rating: Optional[decimal.Decimal]
    type: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[str]


@dataclass
class Genre:
    id: UUID
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class Person:
    id: UUID
    full_name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class GenreFilmwork:
    id: UUID
    genre_id: UUID
    film_work_id: UUID
    created_at: Optional[datetime]


@dataclass
class PersonFilmwork:
    id: UUID
    person_id: UUID
    film_work_id: UUID
    role: str
    created_at: Optional[datetime]
