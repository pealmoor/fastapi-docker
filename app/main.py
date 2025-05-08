from fastapi import FastAPI, Request
import json
import os

app = FastAPI()


@app.get("/")
async def root():
    return {
        "message": "Welcome to the FastAPI application! "
        "You can use this API to manage your notes."
    }


@app.get("/notes")
async def get_notes():

    # TODO: Implementar
    return {"notes": []}


@app.post("/notes")
async def create_note(request: Request):
    # TODO: Implementar
    return {"message": "Note created successfully!"}
