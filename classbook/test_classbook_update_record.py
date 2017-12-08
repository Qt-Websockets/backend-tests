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
             301, 0, 1, "098", "1f43f", "test1", 
             "test1", "5a105e8b9d40e1329780d62ea2265d8a", 
             "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")
        cur.execute("""INSERT INTO classbook VALUES(
             302, 0, 2, "098as", "1f43f", "test1", 
             "test1", "5a105e8b9d40e1329780d62ea2265d8a", 
             "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")
        cur.execute("""INSERT INTO classbook VALUES(
             303, 0, 3, "09a8as", "1fsd43f", "tesast1", 
             "test1", "5a105e8b9d40e1329780d62ea2265d8a", 
             "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")
        cur.execute("""INSERT INTO classbook VALUES(
             304, 0, 4, "09a8as", "1fsd43f", "tesast1", 
             "test1", "5a105e8b9d40e1329780d62ea2265d8a", 
             "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")
        cur.execute("""INSERT INTO classbook VALUES(
             305, 0, 5, "09a8as", "1fsd43f", "tesast1", 
             "test1", "5a105e8b9d40e1329780d62ea2265d8a", 
             "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")
        cur.execute("""INSERT INTO classbook VALUES(
             306, 0, 6, "09a8as", "1fsd43f", "tesast1", 
             "test1", "5a105e8b9d40e1329780d62ea2265d8a", 
             "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")

def teardown():
    with db.cursor() as cur:
        cur.execute("""DELETE FROM classbook""")
        cur.execute("""DELETE FROM classbook_proposal""")
        cur.execute("""DELETE FROM classbook_localization""")


def test_update_exists_article():
    """Testcase for classbook_update_record handler
    Проверям обновление сущестующей статьи,
    обновление name, parentid=0=>0, content, ordered"""
    json_request = json.dumps({
        "parentid": 0,
        "classbookid": 301,
        "name": "update_test",
        "content": "update_content",
        "ordered": 10,
        "cmd": "classbook_update_record",
        "m": "m7334"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % response)
    must_be = json.loads("""{
        "cmd": "classbook_update_record",
        "data": {
            "classbookid": 301,
            "content": "update_content",
            "md5_content": "a98452078e39848d80cfca70306d2a77",
            "name": "update_test",
            "ordered": 10,
            "parentid": 0
        },
        "m": "m7334",
        "result": "DONE"
    }""")
    assert response == must_be


def test_update_exists_article_woutpid():
    """Testcase for classbook_update_record handler
    Проверям обновление сущестующей статьи,
    обновление name, content, ordered"""
    json_request = json.dumps({
        "classbookid": 302,
        "name": "update_test",
        "content": "update_content",
        "ordered": 10,
        "cmd": "classbook_update_record",
        "m": "m7334"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % response)
    must_be = json.loads("""{
        "cmd": "classbook_update_record",
        "data": {
            "classbookid": 302,
            "content": "update_content",
            "md5_content": "a98452078e39848d80cfca70306d2a77",
            "name": "update_test",
            "ordered": 10,
            "parentid": 0
        },
        "m": "m7334",
        "result": "DONE"
    }""")
    assert response == must_be


def test_update_exists_article_name():
    """Testcase for classbook_update_record handler
    Проверям обновление сущестующей статьи,
    обновление name"""
    json_request = json.dumps({
        "cmd": "classbook_update_record",
        "classbookid": 303,
        "name": "update_test",
        "m": "m7321"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % response)
    must_be = json.loads("""{
        "cmd": "classbook_update_record",
        "data": {
            "classbookid": 303,
            "content": "test1",
            "md5_content": "5a105e8b9d40e1329780d62ea2265d8a",
            "name": "update_test",
            "ordered": 3,
            "parentid": 0
        },
        "m": "m7321",
        "result": "DONE"
    }""")
    assert response == must_be


def test_update_without_params():
    """Testcase for classbook_update_record handler
    Проверям обновление сущестующей статьи,
    обновление без параметров"""
    json_request = json.dumps({
        "cmd": "classbook_update_record",
        "classbookid": 303,
        "m": "m7321"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % response)
    must_be = json.loads("""{
        "cmd": "classbook_update_record",
        "code": 403,
        "error": "Not found a charges. Not enough parameters",
        "m": "m7321",
        "result": "FAIL"
    }""")
    assert response == must_be


def test_update_not_exist_article():
    """Testcase for classbook_update_record handler
    Проверям обновление несущестующей статьи"""
    json_request = json.dumps({
        "cmd": "classbook_update_record",
        "classbookid": 30321,
        "m": "m7321"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % response)
    must_be = json.loads("""{
        "cmd": "classbook_update_record",
        "code": 404,
        "error": "Not found a article with a given classbookid",
        "m": "m7321",
        "result": "FAIL"
    }""")
    assert response == must_be


def test_update_exist_article_content():
    """Testcase for classbook_update_record handler
    Проверям обновление сущестующей статьи
    обновление content"""
    json_request = json.dumps({
        "cmd": "classbook_update_record",
        "content": "update_content",
        "classbookid": 304,
        "m": "m7321"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % response)
    must_be = json.loads("""{
        "cmd": "classbook_update_record",
        "data": {
            "classbookid": 304,
            "content": "update_content",
            "md5_content": "a98452078e39848d80cfca70306d2a77",
            "name": "tesast1",
            "ordered": 4,
            "parentid": 0
        },
        "m": "m7321",
        "result": "DONE"
    }""")
    assert response == must_be


def test_update_exist_article_ordered():
    """Testcase for classbook_update_record handler
    Проверям обновление сущестующей статьи
    обновление ordered"""
    json_request = json.dumps({
        "cmd": "classbook_update_record",
        "ordered": 100,
        "classbookid": 305,
        "m": "m7321"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % response)
    must_be = json.loads("""{
        "cmd": "classbook_update_record",
        "data": {
            "classbookid": 305,
            "content": "test1",
            "md5_content": "5a105e8b9d40e1329780d62ea2265d8a",
            "name": "tesast1",
            "ordered": 100,
            "parentid": 0
        },
        "m": "m7321",
        "result": "DONE"
    }""")
    assert response == must_be


def test_update_exist_article_parentid():
    """Testcase for classbook_update_record handler
    Проверям обновление сущестующей статьи
    обновление существующего parentid"""
    json_request = json.dumps({
        "cmd": "classbook_update_record",
        "parentid": 301,
        "classbookid": 306,
        "m": "m7321"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % response)
    must_be = json.loads("""{
        "cmd": "classbook_update_record",
        "data": {
            "classbookid": 306,
            "content": "test1",
            "md5_content": "5a105e8b9d40e1329780d62ea2265d8a",
            "name": "tesast1",
            "ordered": 6,
            "parentid": 301
        },
        "m": "m7321",
        "result": "DONE"
    }""")
    assert response == must_be


def test_update_exist_article_with_not_exist_parentid():
    """Testcase for classbook_update_record handler
    Проверям обновление сущестующей статьи
    обновление не существующего parentid"""
    json_request = json.dumps({
        "cmd": "classbook_update_record",
        "parentid": 1,
        "classbookid": 306,
        "m": "m7321"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % response)
    must_be = json.loads("""{
        "cmd": "classbook_update_record",
        "code": 404,
        "error": "Not found a article with a given parentid",
        "m": "m7321",
        "result": "FAIL"
    }""")
    assert response == must_be


def test_update_root_article():
    """Testcase for classbook_update_record handler
    Проверям обновление корневой статьи"""
    json_request = json.dumps({
        "cmd": "classbook_update_record",
        "parentid": 301,
        "classbookid": 0,
        "m": "m7321"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % response)
    must_be = json.loads("""{
        "cmd": "classbook_update_record",
        "code": 403,
        "error": "Not today. It's root article id",
        "m": "m7321",
        "result": "FAIL"
    }""")
    assert response == must_be
