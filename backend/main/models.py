from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from flask_bcrypt import generate_password_hash, check_password_hash
from uuid import uuid4
import enum
import datetime

from backend.database import db, Base


class RecipeComplexity(enum.Enum):
    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'

    @classmethod
    def values(cls) -> list:
        return [cls.EASY.value, cls.MEDIUM.value, cls.HARD.value]


class Recipe(db.Model, Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(80), nullable=False)
    description = Column(Text, nullable=False)
    complexity = Column(Enum(RecipeComplexity), nullable=False)
    cooking_time = Column(Integer, nullable=False)
    instruction = Column(Text, nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, user_id: int, title: str, description: str,
                 complexity: str, cooking_time: int, instruction: str):
        self.user_id = user_id
        self.title = title
        self.description = description
        self.complexity = RecipeComplexity(complexity)
        self.cooking_time = cooking_time
        self.instruction = instruction
        self.upload()

    def __repr__(self):
        return f"recipe: {self.id}"

    @property
    def info(self) -> dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'complexity': self.complexity.value,
            'cooking_time': self.cooking_time,
            'instruction': self.instruction,
            'time_created': self.time_created.isoformat()
        }

    @classmethod
    def find_by_id(cls, _id: int) -> db.Model:
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> list:
        return cls.query.all()

    def set_complexity(self, complexity: str) -> None:
        self.complexity = RecipeComplexity(complexity)
        self.update()
        return
