# backend/app.py
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import fun, yaml, tdesign

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://127.0.0.1:3002"],  # 测试环境
    allow_origins=["http://10.95.14.174:5173"],  # 测试环境
    allow_credentials=True,  # 允许携带认证信息
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)

app.include_router(fun.router)
app.include_router(yaml.router)
app.include_router(tdesign.router)

if __name__ == "__main__":
    uvicorn.run("backend.app:app", host="0.0.0.0", port=8012, reload=True)
