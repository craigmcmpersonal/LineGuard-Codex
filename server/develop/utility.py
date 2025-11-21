from datetime import datetime, timezone
import uuid


def compose_unique_identifier() -> str:
    unique_identifier: uuid.UUID = uuid.uuid4()
    result: str = str(unique_identifier)
    return result

def coordinated_universal_time() -> datetime:
    result: datetime = datetime.now(
        timezone.utc
    )
    return result

def now() -> str:
    result: str = coordinated_universal_time().strftime(
        constants.DATETIME_FORMAT_ROUNDTRIP
    )
    return result