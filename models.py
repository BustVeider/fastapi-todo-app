from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, ForeignKeyConstraint
from database import Base
from sqlalchemy.orm import relationship

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    tasks = relationship("TaskModel", back_populates="owner")

class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(
        Integer, primary_key=True, index=True
    )
    title = Column(String, nullable=False)
    is_completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("UserModel", back_populates="tasks")
    description = Column(String, nullable=True)
