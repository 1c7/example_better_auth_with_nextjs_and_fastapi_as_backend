from fastapi import Cookie, FastAPI, Request
from verify_session_token import verify_session_token

# 解释 root_path 参数：
#   因为 nginx 设定 /backend 转发给运行在 localhost:8000 的 FastAPI，
#   所以要设定 root_path='/backend'
app = FastAPI(root_path='/backend')

@app.get("/")
async def read_cookies(request: Request):
    cookies = request.cookies
    session_token = cookies['better-auth.session_token']
    token = session_token.split('.')[0]

    # we use this token to query database table "session", query the "token" column
    # and check if the token exists in the database.

    # verify session_token
    # hmac_key 必须和 frontend/.env 里的 BETTER_AUTH_SECRET 一致。
    hmac_key = "LcWr9US2bCHDNckxuXKJRAXLOr0a2d6c"
    is_valid = verify_session_token(hmac_key, session_token)
    if is_valid:
        print("Session token is valid.")
    else:
        print("Session token is invalid.")

    return {"token": token}