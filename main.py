from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

app = FastAPI(title="Notes API", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/hello")
def hello():
    return {"message": "Hello from Notes API"}

class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=80)
    content: str = Field(min_length=1, max_length=500)

notes = []
next_id = 1

@app.get("/notes")
def get_notes():
    return notes


@app.post("/notes", status_code=201)
def create_note(note: NoteCreate):
    global next_id

    note_id = next_id
    next_id = note_id + 1

    new_note = {
        "id": note_id,
        "title": note.title,
        "content": note.content
    }

    notes.append(new_note)
    return new_note