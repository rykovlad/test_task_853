from sqlalchemy import Column, Integer, String, ForeignKey, Table, BIGINT
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm import DeclarativeBase

from create_db import engine


class Base(DeclarativeBase):
    pass


group_users = Table(
    "group_users",
    Base.metadata,
    Column("user_id", ForeignKey("users.tid"),
           primary_key=True),
    Column("group_id", ForeignKey("groups.tid"), primary_key=True),
)


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    tid = Column(BIGINT, unique=True)
    name = Column(String(128), nullable=False)
    username = Column(String(33), unique=True)

    users = relationship('User', secondary=group_users,
                         back_populates='groups')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    tid = Column(BIGINT, unique=True)
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64))
    username = Column(String(32), unique=True)

    groups = relationship('Group', secondary=group_users,
                          back_populates='users')

if __name__ == "__main__":
    Base.metadata.create_all(engine)

    # Creating a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()

    # An example of adding data to tables
    new_group = Group(tid=113211, username='group12', name='Group One')
    new_user = User(tid=33213, first_name='John', last_name='Doe',
                    username='je0hndoe')

    # Linking a user to a group
    # new_group.users.append(new_user)
    new_user.groups.append(new_group)


    # Saving changes in the database
    session.add(new_group)
    session.add(new_user)
    session.commit()

    # Closing the session
    session.close()
