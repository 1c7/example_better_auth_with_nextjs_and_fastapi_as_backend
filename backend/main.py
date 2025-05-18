from fastapi import Cookie, FastAPI, Request

# 解释 root_path：因为用 nginx 设定 /backend 转发给运行在 localhost:8000 的这个 FastAPI，所以要设定 root_path='/backend'
app = FastAPI(root_path='/backend')

@app.get("/")
async def read_cookies(request: Request):
    cookies = request.cookies
    session_token = cookies['better-auth.session_token']
    token = session_token.split('.')[0]
    signture = session_token.split('.')[1]
    return {"token": token}