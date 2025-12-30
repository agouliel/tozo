from quart_db import Connection


async def migrate(connection: Connection) -> None:
    await connection.execute(
        """CREATE TABLE members (
               id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
               created TIMESTAMP NOT NULL DEFAULT now(),
               email TEXT NOT NULL,
               email_verified TIMESTAMP,
               password_hash TEXT NOT NULL
           )""",
    )
    await connection.execute(
        """CREATE UNIQUE INDEX members_unique_email_idx ON members (LOWER(email))"""
    )