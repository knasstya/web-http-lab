from fastapi import FastAPI, HTTPException, Response
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

import os
from dotenv import load_dotenv
import psycopg

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg.connect(DATABASE_URL)

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

@app.get("/notes")
def get_notes():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM notes")
            rows = cursor.fetchall()

            notes = []

            for row in rows:
                id = row[0]
                title = row[1]
                content = row[2]

                note = {
                    "id": id,
                    "title": title,
                    "content": content
                }

                notes.append(note)

    return notes


@app.post("/notes", status_code=201)
def create_note(note: NoteCreate):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO notes (title, content)
                VALUES (%s, %s)
                RETURNING id, title, content
                """,
                (note.title, note.content)
            )
            row = cursor.fetchone()

    return {
        "id": row[0],
        "title": row[1],
        "content": row[2]
    }

@app.get("/notes/{note_id}")
def get_note(note_id: int):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, title, content
                FROM notes
                WHERE id = %s
                """,
                (note_id,)
            )

            row = cursor.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return {
        "id": row[0],
        "title": row[1],
        "content": row[2]
    }

@app.head("/notes/{note_id}")
def head_note(note_id: int):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id
                FROM notes
                WHERE id = %s
                """,
                (note_id,)
            )

            row = cursor.fetchone()

    if row is not None:
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
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE notes
                SET title = COALESCE(%s, title),
                    content = COALESCE(%s, content)
                WHERE id = %s
                RETURNING id, title, content
                """,
                (note.title, note.content, note_id)
            )

            row = cursor.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return {
        "id": row[0],
        "title": row[1],
        "content": row[2]
    }

@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM notes
                WHERE id = %s
                """,
                (note_id,)
            )

            deleted_count = cursor.rowcount

    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Note not found")

    return Response(status_code=204)