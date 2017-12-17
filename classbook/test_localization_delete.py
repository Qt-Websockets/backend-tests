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
        cur.execute("""INSERT INTO classbook VALUES(
             402, 401, 101, "098", "1f43f", "test2",
              "test2", "md5md5md5md5md5md5md5md5md5md5md", 
             "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")
        cur.execute("""INSERT INTO classbook_localization VALUES(
             402, 402, "uuid", "ru", "тест локализации", 
             "локализация", "md5md5md5md5md5md5md5md5md5md5md",
             "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")


def teardown():
    with db.cursor() as cur:
        cur.execute("""DELETE FROM classbook""")
        cur.execute("""DELETE FROM classbook_localization""")


def test_delete_exist_localization():
    """Тестирует classbook_localization_delete_record
    удаление существующей локализации"""
    json_request = json.dumps({
        "classbook_localizationid": 402,
        "cmd": "classbook_localization_delete_record",
        "m": "m8431"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % json.dumps(response))
    must_be = json.loads("""{
        "cmd": "classbook_localization_delete_record",
        "m": "m8431",
        "result": "DONE"
    }""")
    assert response == must_be
    with db.cursor() as cur:
        cur.execute("SELECT name FROM classbook_localization WHERE id=402")
        assert None == cur.fetchone()


def test_delete_not_exist_localization():
    """Тестирует classbook_localization_delete_record
    удаление несуществующей локализации"""
    json_request = json.dumps({
        "classbook_localizationid": 4022,
        "cmd": "classbook_localization_delete_record",
        "m": "m8431"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % json.dumps(response))
    must_be = json.loads("""{
        "cmd": "classbook_localization_delete_record",
        "m": "m8431",
        "code": 404,
        "error": "This localization doesn't exist",
        "result": "FAIL"
    }""")
    assert response == must_be