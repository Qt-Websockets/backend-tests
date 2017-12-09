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


def test_export_html():
    """Тестирует classbook_export
    экспорт учебника в html"""
    json_request = json.dumps({
        "output": "html",
        "lang": "en",
        "cmd": "classbook_export",
        "m": "m8431"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % response)
    must_be = json.loads("""{
        "cmd": "classbook_export",
        "data": "<!DOCTYPE HTML><html><head><title>Freehackquest classbook</title>\n<meta charset=\"utf-8\"></head>\n<body><h1> Freehackquest Classbook</h1>\n<h2>Table of contents</h2>\n<h3><a href=#401>test1</a></h3>\n<h3><a href=#402>test2</a></h3>\n<article id=401><h2>test1</h2>\n<p>test1</p></article>\n<article id=402><h2>test2</h2>\n<p>test2</p></article>\n</body></html>\n",
        "m": "m8431",
        "result": "DONE"
    }""")
    assert response == must_be
