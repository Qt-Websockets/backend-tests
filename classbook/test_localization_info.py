import json
import lib

db = lib.db()
ws = lib.ws()

def setup():
    with db.cursor() as cur:
        cur.execute("""INSERT INTO classbook VALUES(
             402, 401, 101, "098", "1f43f", "test2",
              "test2", "md5md5md5md5md5md5md5md5md5md5md", 
             "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")
        cur.execute("""INSERT INTO classbook_localization VALUES(
             403, 402, "uuid", "ru", "тест локализации", 
             "локализация", "md5md5md5md5md5md5md5md5md5md5md",
             "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")


def teardown():
    with db.cursor() as cur:
        cur.execute("""DELETE FROM classbook""")
        cur.execute("""DELETE FROM classbook_localization""")


def test_not_exist_localization_info():
    """Тестирует classbook_localization_info
    получение несуществующей локализации"""
    json_request = json.dumps({
        "classbook_localizationid": 402,
        "cmd": "classbook_localization_info",
        "m": "m8431"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % json.dumps(response))
    must_be = json.loads("""{
      "cmd": "classbook_localization_info",
      "code": 404,
      "error": "This localization doesn't exist",
      "m": "m8431",
      "result": "FAIL"
    }""")
    assert response == must_be


def test_localization_info():
    """Тестирует classbook_localization_info
    получение локализации"""
    json_request = json.dumps({
        "classbook_localizationid": 403,
        "cmd": "classbook_localization_info",
        "m": "m8431"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % json.dumps(response))
    must_be = json.loads("""{
      "cmd": "classbook_localization_info",
      "data": {
      "classbookid": 402,
      "classbook_localizationid": 403,
      "lang": "ru",
      "name": "тест локализации",
      "content": "локализация"
      },
      "m": "m8431",
      "result": "DONE"
    }""")
    assert response == must_be
