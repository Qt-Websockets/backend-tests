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


def test_localization_add_record():
    """Тестирует classbook_localization_info
    добавление не созданной локализации"""
    json_request = json.dumps({
        "classbookid": 402,
        "lang": "de",
        "name": "doich",
        "content": "doiche",
        "cmd": "classbook_localization_add_record",
        "m": "m8431"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % json.dumps(response))
    classbook_localizationid = None
    with db.cursor() as cur:
        cur.execute("""SELECT id FROM classbook_localization WHERE name='doich'""")
        #TypeError: 'NoneType' object is not subscriptable
        #Означает что нет записи в БД
        classbook_localizationid = cur.fetchone()[0]
    assert classbook_localizationid != None
    must_be = json.loads("""{
        "cmd": "classbook_localization_add_record",
        "data": {
            "classbookid": 402,
            "classbook_localizationid": 1,
            "lang": "de",
            "name": "doich",
            "content": "doiche",
            "md5_content": "6ea18a2bade6f5b2bcb889a9c05bbac3"
        },
        "m": "m8431",
        "result": "DONE"
    }""")
    must_be["data"]["classbook_localizationid"] = classbook_localizationid
    assert response == must_be


def test_localization_add_record_exist_localization():
    """Тестирует classbook_localization_info
    добавление созданной локализации"""
    json_request = json.dumps({
        "classbookid": 402,
        "lang": "ru",
        "name": "rus",
        "content": "russian",
        "cmd": "classbook_localization_add_record",
        "m": "m8431"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % json.dumps(response))
    classbook_localizationid = None
    with db.cursor() as cur:
        cur.execute("""SELECT id FROM classbook_localization WHERE name='rus'""")
        classbook_localizationid = cur.fetchone()
    assert classbook_localizationid == None
    must_be = json.loads("""{
        "cmd": "classbook_localization_add_record",
        "code": 403,
        "error": "This lang already exist",
        "m": "m8431",
        "result": "FAIL"
    }""")
    assert response == must_be