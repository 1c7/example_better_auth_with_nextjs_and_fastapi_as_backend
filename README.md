# 演示：如何使用 `Better Auth` + Next.js + FastAPI
关键点：在 FastAPI 中获得当前用户身份。  

## 为什么要用 FastAPI？明明 Next.js 可以做全栈（用 ORM 操作数据库）
因为需要 AI 功能，AI 大多基于 Python 生态圈，很多库是 Python 库。   

所以选择用 Next.js 主要作为前端，发 HTTP 请求调用 Python 后端。     

## 这个仓库对你的价值
`better-auth` 官方专注于 Typescript 生态圈，短期内不会做任何其他语言的对接。   
我跑通了这个例子，你就知道如何在 FastAPI 里获取用户的身份（current user）  
better-auth 没有提供对接其他语言的官方文档，这个方案是我自己摸索出来的。   

[参考](https://github.com/better-auth/better-auth/issues/2685)

## 备注
Python 生态做 Authentication 没有好的选择，   
因为我们选了 FastAPI，最好的选项是 `FastAPI Users`，但是依然太难用了。

[Awesome Python 的 Authentication](https://github.com/vinta/awesome-python?tab=readme-ov-file#authentication) 都是一些简单的代码库，还是需要自己大量写代码。  

## 结论：我希望用 better auth 作为 Authentication 方案


<!-- # Demo: use `better-auth`(Next.js) with FastAPI

## Why Next.js + FastAPI? instead of just using Next.js alone
a lot of AI lib are in Python ecosystem, I want to build a "AI Chatbot Web App",   
so using Python would be a great idea.   

## Value
 -->
