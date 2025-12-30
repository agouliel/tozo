from dataclasses import dataclass
from datetime import datetime
from quart_db import Connection


@dataclass
class Member:
    id: int
    email: str
    password_hash: str
    created: datetime
    email_verified: datetime | None
    last_totp: str | None
    totp_secret: str | None


async def select_member_by_email(db: Connection, email: str) -> Member | None:
    result = await db.fetch_one(
        """SELECT id, email, password_hash, created, email_verified
             FROM members
            WHERE LOWER(email) = LOWER(:email)""",
        {"email": email},
    )
    return None if result is None else Member(**result)


async def select_member_by_id(db: Connection, id: int) -> Member | None:
    result = await db.fetch_one(
        """SELECT id, email, password_hash, created, email_verified
             FROM members
            WHERE id = :id""",
        {"id": id},
    )
    return None if result is None else Member(**result)