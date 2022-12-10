import os
import time
from random import randrange
from typing import Optional, List

# import psycopg2
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Response, status, Depends
from fastapi.params import Body
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from sqlalchemy import update

from app.utils import FilePrinter, Logger, TerminalPrinter
from app import models
from app.database import engine, get_db
from . import schemas
from .database import DatabaseConnector

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# logger = Logger()

# DatabaseConnector.create_connection()


@app.get("/")
def root():
    return {"message": "welcome to my API"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)) -> List[models.Post]:
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)) -> models.Post:
    # cursor.execute(
    #     """
    #     SELECT * 
    #     FROM posts 
    #     WHERE id = %s
    #     """,
    #     (str(id))
    # )
    # post = cursor.fetchone()
    post = db.query(models.Post).get(id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"post with the id: {id} not found"
        )

    return post


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.InputPost, 
                db: Session = Depends(get_db)) -> models.Post:
    # cursor.execute(
    #     """
    #     INSERT INTO posts (title, content, is_published) 
    #     VALUES (%s, %s, %s) 
    #     RETURNING *
    #     """, 
    #     (post.title, post.content, post.is_published)
    # )
    # new_post = cursor.fetchone()
    # connection.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)) -> None:
    # cursor.execute(
    #     """
    #     DELETE FROM posts 
    #     WHERE id = %s 
    #     RETURNING *
    #     """, 
    #     (str(id))
    # )
    # post = cursor.fetchone()
    # connection.commit()
    post = db.query(models.Post).get(id)

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"post with id: {id} does not exists"
        )
    db.delete(post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, updated_post: schemas.InputPost, 
                db: Session = Depends(get_db)) -> models.Post:
    # cursor.execute(
    #     """
    #     UPDATE posts
    #     SET title=%s, content=%s, is_published=%s
    #     WHERE id = %s
    #     RETURNING *
    #     """,
    #     (post.title, post.content, post.is_published, str(id))
    # )
    # updated_post = cursor.fetchone()
    # connection.commit()
    # post_query = db.query(models.Post).get(id)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exists"
        )
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
