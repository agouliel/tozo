from quart import Blueprint, ResponseReturnValue

blueprint = Blueprint('control', __name__)

# # curl http://127.0.0.1:5050/control/ping/
@blueprint.get('/control/ping/')
async def ping() -> ResponseReturnValue:
    return {'ping': 'pong'}
