from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from controllers.schedule_controller import router as schedule_router

app = FastAPI()

\
origins = [
    "http://localhost:3000",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

app.include_router(schedule_router, prefix="/api")