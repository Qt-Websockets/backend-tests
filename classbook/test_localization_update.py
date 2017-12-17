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
             402, 405, "uuid", "ru", "тест локализации", 
             "локализация", "md5md5md5md5md5md5md5md5md5md5md",
             "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")


def teardown():
    with db.cursor() as cur:
        cur.execute("""DELETE FROM classbook""")
        cur.execute("""DELETE FROM classbook_localization""")


def test_update_exist_localization():
    """Тестирует classbook_localization_update_record
    обновление существующей локализации"""
    json_request = json.dumps({
        "classbook_localizationid": 402,
        "name": "обновление локализации",
        "content": "обновление локализации",
        "cmd": "classbook_localization_update_record",
        "m": "m8431"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % json.dumps(response))
    must_be = json.loads("""{
        "cmd": "classbook_localization_update_record",
        "data": {
            "classbook_localizationid": 402,
            "classbookid": 405,
            "content": "обновление локализации",
            "lang": "ru",
            "md5_content": "3eede0f11699fd69a4831e70ed8062ae",
            "name": "обновление локализации"
        },
        "m": "m8431",
        "result": "DONE"
    }""")
    assert response == must_be
    with db.cursor() as cur:
        cur.execute("SELECT name FROM classbook_localization WHERE id=402")
        assert "обновление локализации" == cur.fetchone()[0]


def test_update_not_exist_localization():
    """Тестирует classbook_localization_update_record
    обновление несуществующей локализации"""
    json_request = json.dumps({
        "classbook_localizationid": 4022,
        "name": "обновление локализации",
        "content": "обновление локализации",
        "cmd": "classbook_localization_update_record",
        "m": "m8431"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % json.dumps(response))
    must_be = json.loads("""{
        "cmd": "classbook_localization_update_record",
        "code": 404,
        "error": "This localization doesn't exist",
        "m": "m8431",
        "result": "FAIL"
    }""")
    assert response == must_be