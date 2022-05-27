#!/usr/bin/env python3
"""
Main file
"""
from db import DB
from user import User

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


my_db = DB()

def up(user_id: int) -> None:
    user = my_db._session.query(User).filter_by(id=user_id).first()
    user.session_id = "1q2w3e4r5t6y"
    my_db._session.commit()

user1 = my_db.add_user('email@1.com', 'hashed_password')
up(int(user1.id))
#user1.session_id = "1q2w3e4r5t6y"
#my_db._session.commit()
print(user1.id)
print(user1.email)
print(user1.hashed_password)
print(user1.session_id)
print(user1.reset_token)
user2 = my_db._session.query(User).filter_by(session_id='1q2w3e4r5t6y').first()
print(user1 is user2)
print(user2.session_id)
#try:
#    my_db.update_user(user1.id, session_id='1N2e3w4P5w6d')
#    print("session_id updated to:")
#    print(user.session_id)
#    my_user = my_db._session.query(User).filter_by(session_id='1N2e3w4P5w6d').first()
#    print(my_user.email)
#    print(user1 is my_user)
#except ValueError:
#    print("Error")
