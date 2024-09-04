from api.repositories.note_repository import get_notes_by_tag, get_notes_by_user

def fetch_notes_by_user(user_id: int) -> list:
    notes = get_notes_by_user(user_id)
    return [note.to_dict() for note in notes]


def fetch_notes_by_tag(tag_name: str) -> list:
    notes = get_notes_by_tag(tag_name)
    return [note.to_dict() for note in notes]


def get_all_tags_from_users_notes(user_id: int) -> list:

    notes = get_notes_by_user(user_id)

    tags = set()

    for note in notes:
        for tag in note.tags:
            tags.add(tag.name)
            
    return list(tags)