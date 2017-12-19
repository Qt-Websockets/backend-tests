import json
import lib

db = lib.db()
ws = lib.ws()

def setup():
    with db.cursor() as cur:
        cur.execute("""INSERT INTO classbook VALUES(
             401, 0, 100, "098", "1f43f", "test1",
              "test1", "md5md5md5md5md5md5md5md5md5md5md", 
             "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")
        cur.execute("""INSERT INTO classbook_proposal VALUES(
             105, 401, "uuid", "en", "proposal", "test1", "before",
             "before", "md5md5md5md5md5md5md5md5md5md5md", 
             "2017-10-10 10:10:10")""")

def teardown():
    with db.cursor() as cur:
        cur.execute("""DELETE FROM classbook""")
        cur.execute("""DELETE FROM classbook_proposal""")


def test_delete_proposal():
    """Тестирует classbook_proposal_delete_record
    удаление существующего предложения"""
    json_request = json.dumps({
        "classbook_proposal_id": 105,
        "cmd": "classbook_proposal_delete_record",
        "m": "m8431"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % json.dumps(response))
    must_be = json.loads("""{
        "cmd": "classbook_proposal_delete_record",
        "m": "m8431",
        "result": "DONE"
    }""")
    assert response == must_be
    with db.cursor() as cur:
        cur.execute("SELECT name FROM classbook WHERE id=105")
        assert None == cur.fetchone()


def test_delete_not_exist_proposal():
    """Тестирует classbook_proposal_delete_record
    удаление несуществующего предложения"""
    json_request = json.dumps({
        "classbook_proposal_id": 4011,
        "cmd": "classbook_proposal_delete_record",
        "m": "m8431"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % json.dumps(response))
    must_be = json.loads("""{
        "cmd": "classbook_proposal_delete_record",
        "code": 404,
        "error": "This proposal doesn't exist",
        "m": "m8431",
        "result": "FAIL"
    }""")
    assert response == must_be
    with db.cursor() as cur:
        cur.execute("SELECT name FROM classbook WHERE id=401")
        assert "test1" == cur.fetchone()[0]