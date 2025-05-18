from sqlmodel import create_engine, Session
from dotenv import load_dotenv
import os

# 加载 .env 文件
load_dotenv()

# 从环境变量获取数据库连接字符串，如果没有则使用默认值
DATABASE_URL = os.getenv("CONNECTION_STRING")
engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session