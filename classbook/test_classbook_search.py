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
             100, 0, 1, '098', '1f43f', 'test1', 'tefindme',
             'md5md5md5md5md5md5md5md5md5md5md', 
             '2017-10-10 10:10:10', '2017-10-10 10:10:10')""")
        cur.execute("""INSERT INTO classbook VALUES(
             102, 0, 2, '098', '1f43f', 'test', 'test2',
             'md5md5md5md5md5md5md5md5md5md5md',
             '2017-10-10 10:10:10', '2017-10-10 10:10:10')""")
        cur.execute("""INSERT INTO classbook VALUES(
             103, 0, 3, '098', '1f43f', 'tutsearch', 'test2',
             'md5md5md5md5md5md5md5md5md5md5md',
             '2017-10-10 10:10:10', '2017-10-10 10:10:10')""")
        cur.execute("""INSERT INTO classbook VALUES(
             104, 100, 2, '098', '1f43f', 'test1test1', 'test1',
             'md5md5md5md5md5md5md5md5md5md5md',
             '2017-10-10 10:10:10', '2017-10-10 10:10:10')""")
        cur.execute("""INSERT INTO classbook_proposal VALUES(
             105, 102, 'sdsd', 'en', 'proposal', 'test1',
             'md5md5md5md5md5md5md5md5md5md5md', NOW())""")
        cur.execute("""INSERT INTO classbook_localization VALUES(
             104, 104, 'uuid', 'ru', 'тест локализации', 'локализация',
             'md5md5md5md5md5md5md5md5md5md5md', NOW(), NOW())""")
        cur.execute("""INSERT INTO classbook_localization VALUES(
             106, 0, 'uuid', 'ru', 'поиск', 'найди меня',
             'md5md5md5md5md5md5md5md5md5md5md', NOW(), NOW())""")

def teardown():
    with db.cursor() as cur:
        cur.execute("""DELETE FROM classbook""")
        cur.execute("""DELETE FROM classbook_proposal""")
        cur.execute("""DELETE FROM classbook_localization""")


def test_search_in_en_name_default_parentid():
    """Testcase for classbook_search handler with default parentid=0
    check search in English name"""
    json_request = json.dumps({
        "parentid": 0,
        "cmd": "classbook_list",
        "search": "search",
        "m": "m7334"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % response)
    must_be = json.loads("""{"cmd":"classbook_list",
        "data":[
        {"childs":0,"classbookid":103,"name":"tutsearch","parentid":0,"proposals":0}],
        "m":"m7334","result":"DONE"}""")
    assert response == must_be


def test_search_in_ru_name_default_parentid():
    """Testcase for classbook_search handler with default parentid=0
    check search in Russian name"""
    json_request = json.dumps({
        "parentid": 0,
        "cmd": "classbook_list",
        "search": "пои",
        "lang": "ru",
        "m": "m7334"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % response)
    must_be = json.loads("""{"cmd":"classbook_list",
        "data":[
        {"childs":0,"classbookid":106,"name":"поиск","parentid":0,"proposals":0}],
        "m":"m7334","result":"DONE"}""")
    assert response == must_be
