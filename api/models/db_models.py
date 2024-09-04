from sqlalchemy import Column, ForeignKey, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from db import db

# Association table for the many-to-many relationship between Notes and Tags
note_tags_association_table = db.Table(
    'note_tags', db.Model.metadata,
    Column('note_id', db.Integer, ForeignKey('notes.note_id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', db.Integer, ForeignKey('tags.tag_id', ondelete='CASCADE'), primary_key=True)
)


class User(db.Model):
    """
    User model for the database interactions.
    """
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(db.String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(db.String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(db.String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(db.DateTime, nullable=False, default=func.now())

    # One-to-many relationship with Note model
    notes = relationship('Note', back_populates='user', cascade="all, delete-orphan")

    def to_dict(self):
        """Convert the user object to a dictionary, excluding sensitive data."""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat()
        }


class Note(db.Model):
    """
    Note model for the database interactions.
    """
    __tablename__ = 'notes'

    note_id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(db.String(200))
    content: Mapped[str] = mapped_column(db.Text)
    created_at: Mapped[datetime] = mapped_column(db.DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(db.DateTime, default=func.now(), onupdate=func.now())
    user_id: Mapped[int] = mapped_column(db.Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)

    # Many-to-one relationship with User model
    user = relationship('User', back_populates='notes')

    # Many-to-many relationship with Tag model using note_tags_association_table
    tags = relationship('Tag', secondary=note_tags_association_table, back_populates='notes')

    def to_dict(self):
        return {
            "note_id": self.note_id,
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "user_id": self.user_id,
            "tags": [tag.to_dict() for tag in self.tags]
        }


class Tag(db.Model):
    __tablename__ = 'tags'

    tag_id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String(50), unique=True, nullable=False)

    # Many-to-many relationship with Note model using note_tags_association_table
    notes = relationship('Note', secondary=note_tags_association_table, back_populates='tags')

    def to_dict(self):
        return {
            "tag_id": self.tag_id,
            "name": self.name,
            "notes": [note.note_id for note in self.notes]
        }
