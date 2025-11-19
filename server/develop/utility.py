import uuid


def compose_unique_identifier() -> str:
    unique_identifier: uuid.UUID = uuid.uuid4()
    result: str = str(unique_identifier)
    return result