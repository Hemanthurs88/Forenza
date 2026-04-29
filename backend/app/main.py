from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth_proxy, export, generate, history, nlp, refine, sessions

app = FastAPI(title="ForensicAI Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in [sessions, generate, refine, nlp, export, history, auth_proxy]:
    app.include_router(router.router, prefix="/api")
