"""
Server entry point, it connects everything together. 
"""

from fastapi import  FastAPI
from src.api.routes import router
from dotenv import load_dotenv
load_dotenv()


app = FastAPI(
    title = "Multi Agent System using Azure Services",
    description = "Production-grade agentc solution for stock analysis",
    version = "1.0.0"
)

app.include_router(router, prefix = "/api/v1")

@app.get("/")
def health_check():
    "simple health check to verify if the server is running"
    return {"status" : "healthy", "service" : "Multi agent crew"}
