import json
import lib

db = lib.db()
ws = lib.ws()

def setup():
    with db.cursor() as cur:
        cur.execute("""INSERT INTO classbook VALUES(
             401, 100, 100, "098", "1f43f", "test1",
              "test1", "md5md5md5md5md5md5md5md5md5md5md", 
             "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")
        cur.execute("""INSERT INTO classbook VALUES(
             402, 0, 101, "098", "1f43f", "test2",
              "test2", "md5md5md5md5md5md5md5md5md5md5md", 
             "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")


def teardown():
    with db.cursor() as cur:
        cur.execute("""DELETE FROM classbook""")
        cur.execute("""DELETE FROM classbook_localization""")


def test_add_basic_record_pareintid_0():
    """Тестирует classbook_add_record
    добавляет статью с parentid = 0, name, content"""
    json_request = json.dumps({
        "parentid": 0,
        "cmd": "classbook_add_record",
        "name": "add_test",
        "content": "add_content",
        "m": "m8431"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % json.dumps(response))
    if response.get("data"):
        classbookid = response["data"]["classbookid"]
    else:
        classbookid = 0
    must_be = json.loads("""{
        "cmd": "classbook_add_record",
        "data": 
            {"classbookid": 410, 
            "content": "add_content",
            "md5_content":
            "aa1bcaabfb81fb580cb9b97787fc4671",
            "name": "add_test",
            "parentid": 0},
        "m": "m8431",
        "result": "DONE"
    }""") 
    must_be["data"]["classbookid"] = classbookid
    assert response == must_be
    with db.cursor() as cur:
        cur.execute(f"SELECT name FROM classbook WHERE id={classbookid}")
        assert "add_test" == cur.fetchone()[0]


def test_add_basic_record_parentid_not_0():
    """Тестирует classbook_add_record
    добавляет статью с parentid not 0, name, content"""
    json_request = json.dumps({
        "parentid": 401,
        "cmd": "classbook_add_record",
        "name": "add_test",
        "content": "add_content",
        "m": "m8431"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % json.dumps(response))
    classbookid = response["data"]["classbookid"]
    must_be = json.loads("""{
        "cmd": "classbook_add_record",
        "data": 
            {"classbookid": 410, 
            "content": "add_content",
            "md5_content":
            "aa1bcaabfb81fb580cb9b97787fc4671",
            "name": "add_test",
            "parentid": 401},
        "m": "m8431",
        "result": "DONE"
    }""")
    must_be["data"]["classbookid"] = classbookid
    assert response == must_be
    with db.cursor() as cur:
        cur.execute(f"SELECT ordered FROM classbook WHERE id={classbookid}")
        assert 101 == cur.fetchone()[0]

def test_add_record_with_uuid():
    """Тестирует classbook_add_record
    добавляет статью с parentid, name, content, uuid"""
    json_request = json.dumps({
        "parentid": 401,
        "cmd": "classbook_add_record",
        "name": "add_test",
        "content": "add_content",
        "uuid": "ccadd04a-dc2c-11e7-9296-cec278b6b50a",
        "m": "m8431"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % json.dumps(response))
    classbookid = response["data"]["classbookid"]
    must_be = json.loads("""{
        "cmd": "classbook_add_record",
        "data": 
            {"classbookid": 410, 
            "content": "add_content",
            "md5_content":
            "aa1bcaabfb81fb580cb9b97787fc4671",
            "name": "add_test",
            "parentid": 401},
        "m": "m8431",
        "result": "DONE"
    }""")
    must_be["data"]["classbookid"] = classbookid
    assert response == must_be
    with db.cursor() as cur:
        cur.execute(f"SELECT uuid FROM classbook WHERE id={classbookid}")
        assert "ccadd04a-dc2c-11e7-9296-cec278b6b50a" == cur.fetchone()[0]


def test_add_record_with_ordered():
    """Тестирует classbook_add_record
    добавляет статью с parentid, name, content, ordered"""
    json_request = json.dumps({
        "parentid": 401,
        "cmd": "classbook_add_record",
        "name": "add_test",
        "content": "add_content",
        "ordered": 345,
        "m": "m8431"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % json.dumps(response))
    classbookid = response["data"]["classbookid"]
    must_be = json.loads("""{
        "cmd": "classbook_add_record",
        "data": 
            {"classbookid": 410, 
            "content": "add_content",
            "md5_content":
            "aa1bcaabfb81fb580cb9b97787fc4671",
            "name": "add_test",
            "parentid": 401},
        "m": "m8431",
        "result": "DONE"
    }""")
    must_be["data"]["classbookid"] = classbookid
    assert response == must_be
    with db.cursor() as cur:
        cur.execute(f"SELECT ordered FROM classbook WHERE id={classbookid}")
        assert 345 == cur.fetchone()[0]

def test_add_record_with_not_exist_article():
    """Тестирует classbook_add_record
    добавляет статью с parentid, name, content"""
    json_request = json.dumps({
        "parentid": 4111,
        "cmd": "classbook_add_record",
        "name": "add_test",
        "content": "add_content",
        "m": "m8431"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % json.dumps(response))
    must_be = json.loads("""{
        "cmd": "classbook_add_record",
        "code": 404,
        "error": "Not found article with this id",
        "m": "m8431",
        "result": "FAIL"
    }""")
    assert response == must_be

