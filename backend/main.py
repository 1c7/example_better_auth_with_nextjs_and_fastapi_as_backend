from fastapi import Cookie, FastAPI, Request, Depends
from verify_session_token import verify_session_token
from models import User, UserSession
from sqlmodel import Session, select
from database import get_session

# 解释 root_path 参数：
#   因为 nginx 设定 /backend 转发给运行在 localhost:8000 的 FastAPI，
#   所以要设定 root_path='/backend'
app = FastAPI(root_path='/backend')

@app.get("/")
async def root(request: Request, db: Session = Depends(get_session)):
    '''
    整体思路：有 Cookie 就用 Cookie，没有就用 Authorization header，两个都没有就报错。
    '''
    cookies = request.cookies
    auth_header = request.headers.get('Authorization')
    token_to_query_db = None # 用于查询数据库的 token
    
    # 如果 Cookie 和 Authorization header 都不存在，返回错误
    if 'better-auth.session_token' not in cookies and not auth_header:
        print("No session token found in cookies or Authorization header.")
        return {"error": "未找到登录凭证，请先登录"}
    
    # 如果 Authorization header 存在，优先使用它
    if 'better-auth.session_token' in cookies:
        session_token = cookies['better-auth.session_token']
        token = session_token.split('.')[0]

        # 验证 session_token 是否有效
        hmac_key = "LcWr9US2bCHDNckxuXKJRAXLOr0a2d6c" # hmac_key 必须和 frontend/.env 里的 BETTER_AUTH_SECRET 一致。
        is_valid = verify_session_token(hmac_key, session_token)
        if not is_valid:
            print("Session token is invalid.")
            return {"error": "无效的登录凭证"}
        token_to_query_db = token
    elif auth_header: # 如果 Authorization header 存在，使用它
        token_to_query_db = auth_header.split(" ")[1]

    # 查询数据库表 `session` 的 token 字段
    statement = select(UserSession).where(UserSession.token == token_to_query_db)
    user_session = db.exec(statement).first()
    
    if not user_session:
        print(f"No session found for token: {token}")
        return {"error": "未找到对应的会话记录"}
    
    # 获取关联的用户信息
    user = user_session.user
    print(f"找到用户: {user.name} (ID: {user.id})")

    response = {
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "emailVerified": user.emailVerified,
            "image": user.image
        }
    }
    
    print(response)
    return response