## 演示：使用 `Better Auth`（Next.js） + FastAPI
关键点：演示在 FastAPI 中获得 better auth 用户身份。  

## 为什么要用 FastAPI？明明 Next.js 可以做全栈（用 ORM 操作数据库）
因为需要 AI 功能，AI 大多基于 Python 生态圈，很多库是 Python 库。   

所以选用 Next.js 主要作为前端，发 HTTP 请求调用 Python FastAPI 后端。     

## 这个仓库对你的价值
`better-auth` 官方专注于 Typescript 生态，短期内不会做任何其他语言的对接。   
我跑通了这个例子，你就知道如何在 FastAPI 里获取用户的身份（current user）  
better-auth 没有提供对接其他语言的官方文档，这个方案是我自己摸索出来的。   

[参考](https://github.com/better-auth/better-auth/issues/2685)

## 如何运行
整体结构：本地用 nginx 做转发。  

查看 nginx 配置文件路径：
```
nginx -t
```

输出:
```
nginx: the configuration file /opt/homebrew/etc/nginx/nginx.conf syntax is ok
nginx: configuration file /opt/homebrew/etc/nginx/nginx.conf test is successful
```

编辑此文件
```
code /opt/homebrew/etc/nginx/nginx.conf
```

关键点
```json
server {
    listen       8080;
    server_name  localhost;

    location / {
        proxy_pass http://localhost:9000; # 前端 Next.js
    }

    location /backend {
        proxy_pass http://localhost:8000; # 后端 FastAPI
    }
```

让 nginx 启动或重启（使得配置生效）
```
- 启动：`brew services start nginx`
- 停止：`brew services stop nginx`
- 重启：`brew services restart nginx`
- 重新加载配置：`nginx -s reload` （可能需要 `sudo`）
```

### 运行前端
```bash
cd frontend/

# 安装依赖
pnpm install 

# 启动服务器
pnpm run dev
```

### 配置 PostgreSQL 数据库
```
cp .env.example .env
```

.env 文件设置 `CONNECTION_STRING`
```
CONNECTION_STRING="postgresql://neondb_owner:npg_QnvkFf2iPeN0@ep-curly-base-a168l333-pooler.ap-southeast-1.aws.neon.tech/zheng2025?sslmode=require"
```

## 设置 Better Auth 所需的数据库表
```
npx @better-auth/cli generate
```

```
npx @better-auth/cli migrate
```
这会创建 4 张表：user, account, session, verification


### 运行后端
```bash
cd backend

# 安装依赖
uv sync

# 运行
uv run uvicorn main:app --reload
```

## 注册账号，访问 http://localhost:8080/sign-up

## 登录账号，访问 http://localhost:8080/sign-in

## 访问首页
首页会发请求给 http://localhost:8080/backend   
会自动带上 Cookie，

`backend/main.py` 文件里：

```python
@app.get("/")
async def read_cookies(request: Request):
    cookies = request.cookies
    session_token = cookies['better-auth.session_token']
    token = session_token.split('.')[0]
    signture = session_token.split('.')[1]
    return {"token": token}
```

就拿到了 token，如有需要可以用 `backend/verify_session_token.py` 进行验证。

用这个 token 去数据库表 `session` 里查询即可。   

## 备注
Python 生态做 Authentication 没有好的选择，   
没有 Ruby on Rails 的 devise gem 或者类似 gem 那么易用。  
因为我们选了 FastAPI，最好的选项是 `FastAPI Users`，但是依然太难用了。

[Awesome Python 的 Authentication](https://github.com/vinta/awesome-python?tab=readme-ov-file#authentication) 都是一些简单的代码库，还是需要自己大量写代码。  

## 结论：我希望用 better auth 作为 Authentication 方案
1. Github Star 有 13.5k
2. 网上对于 better auth 的夸赞有很多
3. better auth 是 YC 2025 春季被投企业（算是一种认可和背书）
4. better auth 的文档清晰直接
5. 我实际试用 better auth 之后觉得体验不错。   

## 参考资料
1. [YC > Companies ›Better Auth](https://www.ycombinator.com/companies/better-auth)
1. [YC > Launches > Better Auth - The Authentication Framework for TypeScript](https://www.ycombinator.com/launches/NUm-better-auth-the-authentication-framework-for-typescript)
1. [Youtube: Auth is HARD... this makes it EASY - Ras Mic](https://www.youtube.com/watch?v=QurjwJHCoHQ)

<!-- # Demo: use `better-auth`(Next.js) with FastAPI

## Why Next.js + FastAPI? instead of just using Next.js alone
a lot of AI lib are in Python ecosystem, I want to build a "AI Chatbot Web App",   
so using Python would be a great idea.   

## Value
 -->
