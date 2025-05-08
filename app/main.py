from fastapi import FastAPI, Request, HTTPException
from app.models import Note, Base, engine, SessionLocal
from sqlalchemy.exc import SQLAlchemyError
import json

app = FastAPI()

# Crea las tablas si no existen
Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI application! You can use this API to manage your notes."}

@app.get("/notes")
async def get_notes():
    db = SessionLocal()
    try:
        notes = db.query(Note).all()
        return {"notes": [{"id": n.id, "title": n.title, "content": n.content} for n in notes]}
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        db.close()

@app.post("/notes")
async def create_note(request: Request):
    db = SessionLocal()
    try:
        data = await request.json()
        title = data.get("title")
        content = data.get("content")
        if not title or not content:
            raise HTTPException(status_code=400, detail="Title and content are required.")
        note = Note(title=title, content=content)
        db.add(note)
        db.commit()
        db.refresh(note)
        return {"message": "Note created successfully!", "note": {"id": note.id, "title": note.title, "content": note.content}}
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        db.close()
