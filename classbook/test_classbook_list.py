import json
import lib

db = lib.db()
ws = lib.ws()


def setup():
    with db.cursor() as cur:
        cur.execute("""DELETE FROM classbook""")
        cur.execute("""DELETE FROM classbook_proposal""")
        cur.execute("""DELETE FROM classbook_localization""")
        cur.execute("""INSERT INTO classbook VALUES(
			 100, 0, 1, "098", "1f43f", "test1",
              "test1", "md5md5md5md5md5md5md5md5md5md5md", 
			 "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")
        cur.execute("""INSERT INTO classbook VALUES(
			 102, 0, 2, "098", "1f43f", "test2",
              "test2", "md5md5md5md5md5md5md5md5md5md5md", 
			 "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")
        cur.execute("""INSERT INTO classbook VALUES(
			 103, 0, 3, "098", "1f43f", "test2", 
             "test2", "md5md5md5md5md5md5md5md5md5md5md", 
			 "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")
        cur.execute("""INSERT INTO classbook VALUES(
			 104, 100, 2, "098", "1f43f", "test1test1", 
             "test1", "md5md5md5md5md5md5md5md5md5md5md", 
			 "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")
        cur.execute("""INSERT INTO classbook_proposal VALUES(
			 105, 102, "uuid", "en", "proposal", "name_before", 
             "test1", "content_before", "md5md5md5md5md5md5md5md5md5md5md", 
			 "2017-10-10 10:10:10")""")
        cur.execute("""INSERT INTO classbook_localization VALUES(
			 104, 104, "uuid", "ru", "тест локализации", 
             "локализация", "md5md5md5md5md5md5md5md5md5md5md",
			 "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")


def teardown():
    with db.cursor() as cur:
        cur.execute("""DELETE FROM classbook""")
        cur.execute("""DELETE FROM classbook_proposal""")
        cur.execute("""DELETE FROM classbook_localization""")


def test_with_default_parentid():
    """Testcase for classbook_list handler with default parentid=0"""
    json_request = json.dumps(
        {"parentid": 0, "cmd": "classbook_list", "m": "m7334"})
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % json.dumps(response))
    must_be = json.loads(
            """{"cmd":"classbook_list",
		"data":[
		{"childs":1,"classbookid":100,"name":"test1","parentid":0,"proposals":0},
		{"childs":0,"classbookid":102,"name":"test2","parentid":0,"proposals":1},
		{"childs":0,"classbookid":103,"name":"test2","parentid":0,"proposals":0}],
		"m":"m7334","result":"DONE"}""")
    assert response == must_be


def test_with_not_exists_parentid():
    """Testcase for classbook_list handler with not exists parentid"""
    json_request = json.dumps(
        {"parentid": 432, "cmd": "classbook_list", "m": "m7334"})
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % json.dumps(response))
    must_be = json.loads(
            """{
			    "cmd": "classbook_list",
			    "code": 404,
			    "error": "Not found the article with a given parentid",
			    "m": "m7334",
			    "result": "FAIL"
			}""")
    assert response == must_be


def test_with_not_default_parentid():
    """Testcase for classbook_list handler with not default parentid"""
    json_request = json.dumps(
        {"parentid": 100, "cmd": "classbook_list", "m": "m7334"})
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % json.dumps(response))
    must_be = json.loads(
            """{
			    "cmd": "classbook_list",
			    "data": [{
			        "childs": 0,
			        "classbookid": 104,
			        "name": "test1test1",
			        "parentid": 100,
			        "proposals": 0
			    }],
			    "m": "m7334",
			    "result": "DONE"
			}""")
    assert response == must_be


def test_with_exist_lang_default_parentid():
    """Testcase for classbook_list handler with exist localization
     lang=ru and default parentid"""
    json_request = json.dumps({"parentid": 100, "lang": "ru",
                               "cmd": "classbook_list", "m": "m7334"})
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % json.dumps(response))
    must_be = json.loads(
            """{
			    "cmd": "classbook_list",
			    "data": [{
			        "childs": 0,
			        "classbookid": 104,
			        "name": "тест локализации",
			        "parentid": 100,
			        "proposals": 0
			    }],
			    "m": "m7334",
			    "result": "DONE"
			}""")
    assert response == must_be
