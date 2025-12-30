from quart import Quart
from quart_auth import QuartAuth
from backend.blueprints.control import blueprint as control_blueprint

app = Quart(__name__)
app.config.from_prefixed_env(prefix='TOZO')

auth_manager = QuartAuth(app)

app.register_blueprint(control_blueprint)
