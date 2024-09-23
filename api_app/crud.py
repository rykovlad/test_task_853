from sqlalchemy.orm import Session

import models


def get_users(db: Session, user_tid: list | int | None = None,
              skip: int = 0, limit: int = 100):
    if isinstance(user_tid, list):
        return db.query(models.User) \
            .filter(models.User.tid.in_(user_tid)) \
            .offset(skip).limit(limit).all()
    elif isinstance(user_tid, int):
        return db.query(models.User) \
            .filter(models.User.tid == user_tid).first()
    else:
        return db.query(models.User).offset(skip).limit(limit).all()


def get_groups(db: Session, group_tid: list | int | None = None,
               skip: int = 0, limit: int = 100):
    if isinstance(group_tid, list):
        return db.query(models.Group) \
            .filter(models.Group.tid.in_(group_tid)) \
            .offset(skip).limit(limit).all()
    elif isinstance(group_tid, int):
        return db.query(models.Group) \
            .filter(models.Group.tid == group_tid).first()
    else:
        return db.query(models.Group).offset(skip).limit(limit).all()


def create_user(db: Session, user_tid: int, first_name: str,
                last_name: str | None = None,
                username: str | None = None,
                groups: list[int] | int | None = None):
    db_user = models.User(tid=user_tid, first_name=first_name,
                          last_name=last_name, username=username)
    db.add(db_user)
    if groups:
        if isinstance(groups, list):
            groups = get_groups(db, group_tid=groups)
            for group in groups:
                group.users.append(db_user)
                db.add(group)
        elif isinstance(groups, int):
            group = get_groups(db, group_tid=groups)
            group.users.append(db_user)
            db.add(group)
    db.commit()
    return db_user


def create_group(db: Session, group_tid: int, name: str,
                 username: str | None = None,
                 users: list[int] | int | None = None):
    db_group = models.Group(tid=group_tid, name=name, username=username)
    db.add(db_group)
    if users:
        if isinstance(users, list):
            users = get_users(db, user_tid=users)
            for user in users:
                user.groups.append(db_group)
                db.add(user)
        elif isinstance(users, int):
            user = get_users(db, user_tid=users)
            user.groups.append(db_group)
            db.add(user)
    db.commit()
    return db_group


def add_user_2_group(db: Session, user_tid: int, group_tid: int):
    user = get_users(db, user_tid=user_tid)
    group = get_groups(db, group_tid=group_tid)
    user.groups.append(group)
    db.add(user)
    db.commit()


def delete_user(db: Session, user_tid: int):
    user = get_users(db, user_tid=user_tid)
    if user:
        db.delete(user)
        db.commit()
        return True
    return False


def delete_group(db: Session, group_tid: int):
    group = get_groups(db, group_tid=group_tid)
    if group:
        db.delete(group)
        db.commit()
        return True
    return False


def update_user(db: Session, user_tid: int, first_name: str | None = None,
                last_name: str | None = None,
                username: str | None = None,
                groups: list[int] | int | None = None):
    user = get_users(db, user_tid=user_tid)
    if user:
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if username:
            user.username = username
        if groups:
            for g in user.groups:
                db.delete(g)
            if isinstance(groups, list):
                groups = get_groups(db, group_tid=groups)
                for group in groups:
                    group.users.append(user)
                    db.add(group)
            elif isinstance(groups, int):
                group = get_groups(db, group_tid=groups)
                group.users.append(user)
                db.add(group)
        db.commit()
        return user
    return None


def update_group(db: Session, group_tid: int, name: str | None = None,
                 username: str | None = None,
                 users: list[int] | int | None = None):
    group = get_groups(db, group_tid=group_tid)
    if group:
        if name:
            group.name = name
        if username:
            group.username = username
        if users:
            for u in group.users:
                db.delete(u)
            if isinstance(users, list):
                users = get_users(db, user_tid=users)
                for user in users:
                    user.groups.append(group)
                    db.add(user)
            elif isinstance(users, int):
                user = get_users(db, user_tid=users)
                user.groups.append(group)
                db.add(user)
        db.commit()
        db.refresh(group)
        return group
    return None
