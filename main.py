from fastapi import FastAPI, HTTPException, Response
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

class NoteUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=80)
    content: str | None = Field(default=None, min_length=1, max_length=500)

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

@app.get("/notes/{note_id}")
def get_note(note_id: int):
    for note in notes:
        if note["id"] == note_id:
            return note

    raise HTTPException(status_code=404, detail="Note not found")

@app.head("/notes/{note_id}")
def head_note(note_id: int):
    for note in notes:
        if note["id"] == note_id:
            return Response(
                status_code=200,
                headers={"x-note-exists": "true"}
            )

    return Response(
        status_code=404,
        headers={"x-note-exists": "false"}
    )

@app.patch("/notes/{note_id}")
def update_note(note_id: int, note: NoteUpdate):
    for idx, existing_note in enumerate(notes):
        if existing_note["id"] == note_id:
            if note.title is not None:
                notes[idx]["title"] = note.title
            if note.content is not None:
                notes[idx]["content"] = note.content
            return notes[idx]

    raise HTTPException(status_code=404, detail="Note not found")

@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    for idx, note in enumerate(notes):
        if note["id"] == note_id:
            del notes[idx]
            return Response(status_code=204)

    raise HTTPException(status_code=404, detail="Note not found")