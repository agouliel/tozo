import os
from subprocess import call
from urllib.parse import urlparse
from quart import Quart
from quart_auth import QuartAuth
from quart_db import QuartDB
from backend.blueprints.control import blueprint as control_blueprint
from backend.blueprints.sessions import blueprint as sessions_blueprint

app = Quart(__name__)
app.config.from_prefixed_env(prefix='TOZO')
# directly: app.secret_key = 'secret key' # https://github.com/pgjones/quart-auth

auth_manager = QuartAuth(app) # previously AuthManager
quart_db = QuartDB(app)

app.register_blueprint(control_blueprint)
app.register_blueprint(sessions_blueprint)


@app.cli.command("recreate_db")
def recreate_db() -> None:
    db_url = urlparse(os.environ["TOZO_QUART_DB_DATABASE_URL"])
    call(  # nosec
        ["psql", "-U", "postgres", "-c", f"DROP DATABASE IF EXISTS {db_url.path.removeprefix('/')}",],
    )
    call(  # nosec
        ["psql", "-U", "postgres", "-c", f"DROP USER IF EXISTS {db_url.username}"],
    )
    call(  # nosec
        ["psql", "-U", "postgres", "-c", f"CREATE USER {db_url.username} LOGIN PASSWORD '{db_url.password}' CREATEDB",],  # noqa: E501
    )
    call(  # nosec
        ["psql", "-U", "postgres", "-c", f"CREATE DATABASE {db_url.path.removeprefix('/')}",],
    )
    call(  # nosec
        ["psql", "-U", "postgres", "-d", f"{db_url.path.removeprefix('/')}", "-c", f"GRANT ALL ON SCHEMA public TO {db_url.username}", ],
    )