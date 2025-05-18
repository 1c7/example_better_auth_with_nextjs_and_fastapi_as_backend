## 演示：使用 `Better Auth`（Next.js） + FastAPI
关键点：演示在 FastAPI 中获得 better auth 用户身份。  

## 为什么要用 FastAPI？明明 Next.js 可以做全栈（用 ORM 操作数据库）
因为需要 AI 功能，AI 大多基于 Python 生态圈，很多库是 Python 库。   

所以选用 Next.js 主要作为前端，发 HTTP 请求调用 Python FastAPI 后端。     

## 这个仓库对你的价值
`better-auth` 专注 Typescript 生态，短期内不会做对接其他语言。     
通过这个示例，你就知道在 FastAPI 里如何获取用户身份    
better-auth 没有提供对接其他语言的官方文档，这个方案是我自己摸索出来的  [参考资料](https://github.com/better-auth/better-auth/issues/2685)

## 运行前的准备
在本地开发环境用 nginx 做转发（以下命令假设操作系统是 macOS）    

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

改成：  
```
server {
    listen       8080;
    server_name  localhost;

    location / {
        proxy_pass http://localhost:9000; # 前端 Next.js
    }

    location /backend {
        proxy_pass http://localhost:8000; # 后端 FastAPI
    }
}
```
解释如下：  
入口是 8080 端口，     
`/` 指向 Next.js 运行的 9000 端口   
`/backend` 指向 FastAPI 运行的 8000 端口   

用以下命令，启用或者重启 nginx（使配置生效）
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

### 创建一个空的 PostgreSQL 数据库
```
createdb demo_better_auth_fastapi
```

设置环境变量，`frontend/.env` 文件内设置 `CONNECTION_STRING`

先创建 .env 文件：  
```
cp .env.example .env
```

例子：用 neon.tech 的 PostgreSQL 数据库
```
CONNECTION_STRING="postgresql://neondb_owner:npg_QnvkFf2iPeN0@ep-curly-base-a168l333-pooler.ap-southeast-1.aws.neon.tech/zheng2025?sslmode=require"
```

例子：连接本地 PostgreSQL 数据库
```
CONNECTION_STRING="postgresql://postgres:password@localhost:5432/demo_better_auth_fastapi"
```

## 创建 Better Auth 所需的数据库表
```
npx @better-auth/cli migrate
```
会创建 4 张表：user, account, session, verification  
参考 `frontend/better-auth_migrations/`   


### 运行后端
```bash
cd backend

# 安装依赖
uv sync

# 运行
uv run uvicorn main:app --reload
```

## 注册账号，访问 http://localhost:8080/sign-up
注册后会自动跳转首页 `/`

## 登录账号，访问 http://localhost:8080/sign-in
登录后会自动跳转首页 `/`

## 访问首页： http://localhost:8080/
首页会发请求给 http://localhost:8080/backend     

请阅读以下 2 个文件：  
- `frontend/app/page.tsx`
- `backend/main.py`

## 概述 `frontend/app/page.tsx`
因为这个页面是 Next.js Server Component，发请求是从服务器一侧发出，不是用户的浏览器，所以不带 Cookie，我们就直接带一个 `Authorization: Bearer [token]`   
如果是 Next.js Client Component 就会默认携带 Cookie。  

## 概述 `backend/main.py`
代码逻辑：从 Cookie 中获取 `better-auth.session_token`，或者从 HTTP Header `Authorization` 里获取 token。    

如果是从 Cookie 里用 `better-auth.session_token`，你有两种选择：
1. 直接使用，不验证签名，用 `split(".")[0]` 拿到 token, 去查询数据库表 `session` 的 `token` 字段
2. 先验证签名，用 `backend/verify_session_token.py` 如果 valid（有效）再去查数据库表 `session` 的 `token` 字段

## 备注：Python 生态做 Authentication 没有好的选择，   
FastAPI 的生态里没有类似 Ruby on Rails 的 devise gem 那么好用。  
FastAPI 里最好的选项是 `FastAPI Users`，但还是太难用了。  

[Awesome Python 的 Authentication](https://github.com/vinta/awesome-python?tab=readme-ov-file#authentication) 都是一些简单的代码库，还是需要自己大量写代码。  

## 解释：为什么我想用 `better-auth` 作为 Authentication 方案
2. 网上很多夸赞 better auth（文字评论或 Youtube 视频），[`better-auth`](https://github.com/better-auth/better-auth) 的 Github Star 有 13.5k
3. better auth 是 YC "2025春季批次" 的被投企业（算是认可和背书）
4. better auth 的文档清晰
5. 我实际试用 better auth 觉得体验不错。   
6. `FastAPI Users` 使用体验极差，我不想忍受。  

## 参考资料
1. [YC > Companies ›Better Auth](https://www.ycombinator.com/companies/better-auth)
1. [YC > Launches > Better Auth - The Authentication Framework for TypeScript](https://www.ycombinator.com/launches/NUm-better-auth-the-authentication-framework-for-typescript)
1. [Youtube: Auth is HARD... this makes it EASY - Ras Mic](https://www.youtube.com/watch?v=QurjwJHCoHQ)

## 注意
1. `Next.js` 区分 Server Component 和 Client Component
2. `Better-Auth` 也区分 server 和 client
写代码时不要弄混了。     

## 文件夹结构

- `frontend/` 是 Next.js 项目
- `backend/` 是 FastAPI 项目

两个文件夹都是在新项目的基础上用尽可能少的代码演示功能，代码越少，干扰越少。   
