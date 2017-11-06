import pytest
from websocket import create_connection
import json


def ws():
    ws = create_connection("ws://localhost:1234")
    token = json.dumps({
        "email": "admin",
        "password": "admin",
        "cmd": "login",
        "m": "m5123"
    })
    ws.send(token)
    result = ws.recv()
    return ws


def db():
    import pymysql
    db = pymysql.connect(
        user="root",
        passwd="root",
        db="test",
        use_unicode=True,
        charset="utf8",
        autocommit=True)
    return db