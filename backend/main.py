from fastapi import Cookie, FastAPI, Request


app = FastAPI(root_path='/backend')

@app.get("/")
# return {"message": "Hello hi"} 
async def read_cookies(request: Request):
    cookies = request.cookies
    # print(cookies)
    session_token = cookies['better-auth.session_token']
    print(session_token)
    print(session_token.split('.')[0])
    return {"cookies": cookies}