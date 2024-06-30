import typing
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.infraestructure.database.config.dynamodb import create_table, get_dynamodb_client


app = FastAPI()


client = get_dynamodb_client()
create_table(client)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health-check")
def health_check() -> typing.Dict:
    return {
        "name": "AI Feedback",
        "version": "0.0.1"
    }
