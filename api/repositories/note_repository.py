from api.models.db_models import Note, Tag

def get_notes_by_user(user_id: int) -> list:
    return Note.query.filter_by(user_id=user_id).all()

def get_notes_by_tag(tag_name: str) -> list:
    tag = Tag.query.filter_by(name=tag_name).first()
    if tag:
        return tag.notes
    return []