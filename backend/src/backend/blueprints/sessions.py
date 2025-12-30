from dataclasses import dataclass
from quart import Blueprint, ResponseReturnValue, g, request, render_template_string
from quart_auth import AuthUser, current_user, login_required, login_user, logout_user
from backend.models.member import select_member_by_email

blueprint = Blueprint("sessions", __name__)

@dataclass
class LoginData:
    email: str #EmailStr
    password: str #SecretStr
    remember: bool = False

class MyData:
    def __init__(self, d=None):
        if d is not None:
            for key, value in d.items():
                setattr(self, key, value)

# https://stackoverflow.com/questions/12399087/curl-to-access-a-page-that-requires-a-login-from-a-different-page
# test using: curl -X POST localhost:5050/sessions/ --json '{"email": "member@tozo.dev", "password": "password"}' --cookie-jar ~/Desktop/cookie.txt
@blueprint.post("/sessions/")
#async def login(data: LoginData) -> ResponseReturnValue:
async def login() -> ResponseReturnValue:
    mydict = await request.json # # https://mojoauth.com/parse-and-generate-formats/parse-and-generate-json-with-quart/
    data = MyData(mydict) # https://stackoverflow.com/questions/59250557/how-to-convert-a-python-dict-to-a-class-object

    member = await select_member_by_email(g.connection, data.email)

    if member is not None:
        password_hash = member.password_hash

    passwords_match = False
    if data.password == password_hash:
        passwords_match = True

    if passwords_match:
        assert member is not None  # nosec
        login_user(AuthUser(str(member.id))) #, data.remember)
        return {}, 200
    else:
        return {'error':"INVALID_CREDENTIALS"}, 401


@blueprint.delete("/sessions/")
async def logout() -> ResponseReturnValue:
    logout_user()
    return {}


@dataclass
class Status:
    member_id: int

# test using: curl localhost:5050/sessions/ --cookie ~/Desktop/cookie.txt
@blueprint.get("/sessions/")
@login_required
#async def status() -> Status:
async def status():
    assert current_user.auth_id is not None  # nosec
    #return Status(member_id=int(current_user.auth_id))
    return {'member_id': str(current_user.auth_id)}


# https://github.com/pgjones/quart-auth
@blueprint.route("/status/")
async def login_status():
  print(current_user) # AuthUser(auth_id=None, action=Action.PASS)
  return await render_template_string("{{ current_user.is_authenticated }}")
