from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import crud
import models
from create_db import SessionLocal, engine
from schemas import User, Group, PatchUser, PatchGroup

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="my apishka", description="deskriPshiOn",
              summary="my_summary",
              contact={"name": "url", "phone": "102"})


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/")
def read_all_users(skip: int = 0, limit: int = 100,
                   db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)


@app.get("/users/{user_tid}")
def read_user(user_tid: int | None, db: Session = Depends(get_db)):
    return crud.get_users(db, user_tid=user_tid)


@app.get("/groups/")
def read_all_groups(skip: int = 0, limit: int = 100,
                    db: Session = Depends(get_db)):
    return crud.get_groups(db, skip=skip, limit=limit)


@app.get("/groups/{group_tid}")
def read_group(group_tid, db: Session = Depends(get_db)):
    return crud.get_groups(db, group_tid=group_tid)


@app.post("/users/")
def create_user(user: User, db: Session = Depends(get_db)):
    '''text in desc to create user'''
    try:
        return crud.create_user(db, user.tid, user.first_name, user.last_name,
                                user.username, user.groups)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="так це ж було вже")


@app.post("/groups/")
def create_group(group: Group, db: Session = Depends(get_db)):
    try:
        return crud.create_group(db, group.tid, group.name,
                                 group.username, group.users)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="так це ж було вже")


@app.patch("/users/{tid}")
def update_user(tid: int, user: PatchUser, db: Session = Depends(get_db)):
    try:
        return crud.update_user(db, tid, user.first_name, user.last_name,
                                user.username, user.groups)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="так це ж було вже")


@app.patch("/groups/{tid}")
def update_group(tid: int, group: PatchGroup, db: Session = Depends(get_db)):
    try:
        return crud.update_group(db, tid, group.name,
                                 group.username, group.users)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="так це ж було вже")


@app.delete("/users/")
def delete_user(tid: int, db: Session = Depends(get_db)):
    if not crud.delete_user(db, tid):
        raise HTTPException(status_code=400, detail="немає такого")


@app.delete("/groups/")
def delete_groups(tid: int, db: Session = Depends(get_db)):
    if not crud.delete_group(db, tid):
        raise HTTPException(status_code=400, detail="немає такого")

