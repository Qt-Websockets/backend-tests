import json
import lib

db = lib.db()
ws = lib.ws()


def setup():
    with db.cursor() as cur:
        cur.execute("""DELETE FROM classbook""")
        cur.execute("""DELETE FROM classbook_localization""")
        cur.execute("""INSERT INTO classbook VALUES(
             202, 0, 6, "098", "1f43f", "test", 
             "test", "md5md5md5md5md5md5md5md5md5md5md", 
             "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")
        cur.execute("""INSERT INTO classbook VALUES(
             203, 0, 7, "098", "1f43f", "test_with_lang", 
             "test", "md5md5md5md5md5md5md5md5md5md5md", 
             "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")
        cur.execute("""INSERT INTO classbook_localization VALUES(
             204, 203, "098", "ru", "тест локализации", 
             "локализация", "md5md5md5md5md5md5md5md5md5md5md",
             "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")
        cur.execute("""INSERT INTO classbook VALUES(
             205, 0, 7, "098", "1f43f", "test_path", 
             "test", "md5md5md5md5md5md5md5md5md5md5md", 
             "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")
        cur.execute("""INSERT INTO classbook VALUES(
             206, 205, 7, "098", "1f43f", "test_path", 
             "test", "md5md5md5md5md5md5md5md5md5md5md", 
             "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")
        cur.execute("""INSERT INTO classbook VALUES(
             207, 206, 7, "098", "1f43f", "test_path", 
             "test", "md5md5md5md5md5md5md5md5md5md5md", 
             "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")
        cur.execute("""INSERT INTO classbook VALUES(
             208, 207, 7, "098", "1f43f", "test_path", 
             "test", "md5md5md5md5md5md5md5md5md5md5md", 
             "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")
        cur.execute("""INSERT INTO classbook VALUES(
             209, 208, 7, "098", "1f43f", "test_path", 
             "test", "md5md5md5md5md5md5md5md5md5md5md", 
             "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")
        cur.execute("""INSERT INTO classbook VALUES(
             210, 209, 7, "098", "1f43f", "test_path", 
             "test", "md5md5md5md5md5md5md5md5md5md5md", 
             "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")
        cur.execute("""INSERT INTO classbook VALUES(
             211, 210, 7, "098", "1f43f", "test_path", 
             "test", "md5md5md5md5md5md5md5md5md5md5md", 
             "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")
        cur.execute("""INSERT INTO classbook VALUES(
             212, 213, 7, "098", "1f43f", "test_path", 
             "test", "md5md5md5md5md5md5md5md5md5md5md", 
             "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")
        cur.execute("""INSERT INTO classbook VALUES(
             213, 212, 7, "098", "1f43f", "test_path", 
             "test", "md5md5md5md5md5md5md5md5md5md5md", 
             "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")
        cur.execute("""INSERT INTO classbook VALUES(
             214, 215, 7, "098", "1f43f", "test_path", 
             "test", "md5md5md5md5md5md5md5md5md5md5md", 
             "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")
        cur.execute("""INSERT INTO classbook VALUES(
             215, 216, 7, "098", "1f43f", "test_path", 
             "test", "md5md5md5md5md5md5md5md5md5md5md", 
             "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")
        cur.execute("""INSERT INTO classbook VALUES(
             216, 214, 7, "098", "1f43f", "test_path", 
             "test", "md5md5md5md5md5md5md5md5md5md5md", 
             "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")
        cur.execute("""INSERT INTO classbook VALUES(
             217, 215, 7, "098", "1f43f", "test_path", 
             "test", "md5md5md5md5md5md5md5md5md5md5md", 
             "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")


def teardown():
    with db.cursor() as cur:
        cur.execute("""DELETE FROM classbook""")
        cur.execute("""DELETE FROM classbook_localization""")


def test_info_non_found():
    """Тестирует classbook_infо на несуществующую статью"""
    json_request = json.dumps({
        "classbookid": 23232,
        "cmd": "classbook_info",
        "m": "m8431"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % response)
    must_be = json.loads("""{
        "cmd": "classbook_info",
        "code": 404,
        "error": "Not found the article",
        "m": "m8431",
        "result": "FAIL"
    }""")
    assert response == must_be


def test_info_without_lang():
    """Testcase for handler classbook_info without lang param"""
    json_request = json.dumps({
        "classbookid": 202,
        "cmd": "classbook_info",
        "m": "m843"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % response)
    must_be = json.loads("""{
            "cmd": "classbook_info",
            "data": {
                "classbookid": 202,
                "content": "test",
                "lang": "en",
                "langs": {},
                "name": "test",
                "parentid": 0,
                "parents": [
                    {
                        "classbookid": 0,
                        "name": "Root",
                        "parentid": 0
                    }
                ],
                "uuid": "098"
            },
            "m": "m843",
            "result": "DONE"
        }""")
    assert response == must_be


def test_info_with_lang_with_local():
    """Тестирует classbook_infо с указанным языком, есть локализация"""
    json_request = json.dumps({
        "classbookid": 203,
        "lang": "ru",
        "cmd": "classbook_info",
        "m": "m844"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % response)
    must_be = json.loads("""{
                    "cmd": "classbook_info",
                    "data": {
                        "classbookid": 203,
                        "content": "локализация",
                        "lang": "ru",
                        "langs": {
                            "ru": 204
                        },
                        "name": "тест локализации",
                        "parentid": 0,
                        "parents": [
                            {
                                "classbookid": 0,
                                "name": "Root",
                                "parentid": 0
                            }
                        ],
                        "uuid": "098"
                    },
                    "m": "m844",
                    "result": "DONE"
                }""")
    assert response == must_be


def test_info_with_lang_with_out_local():
    """Тестирует classbook_infо с указанным языком, отсутствует локализация"""
    json_request = json.dumps({
        "classbookid": 202,
        "lang": "ru",
        "cmd": "classbook_info",
        "m": "m82"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % response)
    must_be = json.loads("""{
                "cmd": "classbook_info",
                "data": {
                    "classbookid": 202,
                    "content": "test",
                    "lang": "en",
                    "langs": {},
                    "name": "test",
                    "parentid": 0,
                    "uuid": "098",
                    "parents": [
                        {
                            "classbookid": 0,
                            "name": "Root",
                            "parentid": 0
                        }
                    ]
                },
                "m": "m82",
                "result": "DONE"
            }""")
    assert response == must_be


def test_info_with_lang_not_exists_article():
    """Тестирует classbook_infо с указанным языком, несуществующей статьей"""
    json_request = json.dumps({
        "classbookid": 2022,
        "lang": "ru",
        "cmd": "classbook_info",
        "m": "m82"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % response)
    must_be = json.loads("""{"cmd": "classbook_info", "code": 404, 
        "error": "Not found the article", 
        "m": "m82", "result": "FAIL"}""")
    assert response == must_be


def test_info_with_unsupported_lang():
    """Тестирует classbook_infо с неподдерживаемым языком"""
    json_request = json.dumps({
        "classbookid": 202,
        "lang": "er",
        "cmd": "classbook_info",
        "m": "m82"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % response)
    must_be = json.loads("""{
            "cmd": "classbook_info",
            "code": 404,
            "error": "Language is not support",
            "m": "m82",
            "result": "FAIL"}""")
    assert response == must_be


def test_info_with_unsupported_lang_not_exists_article():
    """Тестирует classbook_infо с неподдерживаемым языком
    несуществующей статьи"""
    json_request = json.dumps({
        "classbookid": 20222,
        "lang": "er",
        "cmd": "classbook_info",
        "m": "m82"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % response)
    must_be = json.loads("""{
            "cmd": "classbook_info",
            "code": 404,
            "error": "Not found the article",
            "m": "m82",
            "result": "FAIL"
            }""")
    assert response == must_be


def test_info_parents_path_2():
    """Тестирует classbook_infо
    Проверка родительского пути 2 род"""
    json_request = json.dumps({
        "classbookid": 206,
        "cmd": "classbook_info",
        "m": "m82"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % response)
    must_be = json.loads("""{
        "cmd": "classbook_info",
        "data": {
            "classbookid": 206,
            "content": "test",
            "lang": "en",
            "langs": {},
            "name": "test_path",
            "parentid": 205,
            "parents": [
                {
                    "classbookid": 205,
                    "name": "test_path",
                    "parentid": 0
                },
                {
                    "classbookid": 0,
                    "name": "Root",
                    "parentid": 0
                }
            ],
            "uuid": "098"
        },
        "m": "m82",
        "result": "DONE"
    }""")
    assert response == must_be


def test_info_parents_path_3():
    """Тестирует classbook_infо
    Проверка родительского пути 3 род"""
    json_request = json.dumps({
        "classbookid": 207,
        "cmd": "classbook_info",
        "m": "m82"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % response)
    must_be = json.loads("""{
        "cmd": "classbook_info",
        "data": {
            "classbookid": 207,
            "content": "test",
            "lang": "en",
            "langs": {},
            "name": "test_path",
            "parentid": 206,
            "parents": [
                {
                    "classbookid": 206,
                    "name": "test_path",
                    "parentid": 205
                },
                {
                    "classbookid": 205,
                    "name": "test_path",
                    "parentid": 0
                },
                {
                    "classbookid": 0,
                    "name": "Root",
                    "parentid": 0
                }
            ],
            "uuid": "098"
        },
        "m": "m82",
        "result": "DONE"
    }""")
    assert response == must_be


def test_info_parents_path_4():
    """Тестирует classbook_infо
    Проверка родительского пути 4 род"""
    json_request = json.dumps({
        "classbookid": 208,
        "cmd": "classbook_info",
        "m": "m82"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % response)
    must_be = json.loads("""{
        "cmd": "classbook_info",
        "data": {
            "classbookid": 208,
            "content": "test",
            "lang": "en",
            "langs": {},
            "name": "test_path",
            "parentid": 207,
            "parents": [
                {
                    "classbookid": 207,
                    "name": "test_path",
                    "parentid": 206
                },
                {
                    "classbookid": 206,
                    "name": "test_path",
                    "parentid": 205
                },
                {
                    "classbookid": 205,
                    "name": "test_path",
                    "parentid": 0
                },
                {
                    "classbookid": 0,
                    "name": "Root",
                    "parentid": 0
                }
            ],
            "uuid": "098"
        },
        "m": "m82",
        "result": "DONE"
    }""")
    assert response == must_be


def test_info_parents_path_5():
    """Тестирует classbook_infо
    Проверка родительского пути 5 род"""
    json_request = json.dumps({
        "classbookid": 209,
        "cmd": "classbook_info",
        "m": "m82"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % response)
    must_be = json.loads("""{
        "cmd": "classbook_info",
        "data": {
            "classbookid": 209,
            "content": "test",
            "lang": "en",
            "langs": {},
            "name": "test_path",
            "parentid": 208,
            "parents": [
                {
                    "classbookid": 208,
                    "name": "test_path",
                    "parentid": 207
                },
                {
                    "classbookid": 207,
                    "name": "test_path",
                    "parentid": 206
                },
                {
                    "classbookid": 206,
                    "name": "test_path",
                    "parentid": 205
                },
                {
                    "classbookid": 205,
                    "name": "test_path",
                    "parentid": 0
                },
                {
                    "classbookid": 0,
                    "name": "Root",
                    "parentid": 0
                }
            ],
            "uuid": "098"
        },
        "m": "m82",
        "result": "DONE"
    }""")
    assert response == must_be


def test_info_parents_path_6():
    """Тестирует classbook_infо
    Проверка родительского пути 6 род"""
    json_request = json.dumps({
        "classbookid": 210,
        "cmd": "classbook_info",
        "m": "m82"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % response)
    must_be = json.loads("""{
        "cmd": "classbook_info",
        "data": {
            "classbookid": 210,
            "content": "test",
            "lang": "en",
            "langs": {},
            "name": "test_path",
            "parentid": 209,
            "parents": [
                {
                    "classbookid": 209,
                    "name": "test_path",
                    "parentid": 208
                },
                {
                    "classbookid": 208,
                    "name": "test_path",
                    "parentid": 207
                },
                {
                    "classbookid": 207,
                    "name": "test_path",
                    "parentid": 206
                },
                {
                    "classbookid": 206,
                    "name": "test_path",
                    "parentid": 205
                },
                {
                    "classbookid": 205,
                    "name": "test_path",
                    "parentid": 0
                }
            ],
            "uuid": "098"
        },
        "m": "m82",
        "result": "DONE"
    }""")
    assert response == must_be


def test_info_parents_path_cicle():
    """Тестирует classbook_infо
    Проверка родительского пути простой цикл"""
    json_request = json.dumps({
        "classbookid": 213,
        "cmd": "classbook_info",
        "m": "m82"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % response)
    must_be = json.loads("""{
        "cmd": "classbook_info",
        "data": {
            "classbookid": 213,
            "content": "test",
            "lang": "en",
            "langs": {},
            "name": "test_path",
            "parentid": 212,
            "parents": [
                {
                    "classbookid": 212,
                    "name": "test_path",
                    "parentid": 213
                }
            ],
            "uuid": "098"
        },
        "m": "m82",
        "result": "DONE"
    }""")
    assert response == must_be


def test_info_parents_path_hard_cicle_1():
    """Тестирует classbook_infо
    Проверка родительского пути сложный цикл
    214 -> 215 -> 216 -\> 214"""
    json_request = json.dumps({
        "classbookid": 214,
        "cmd": "classbook_info",
        "m": "m82"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % response)
    must_be = json.loads("""{
        "cmd": "classbook_info",
        "data": {
            "classbookid": 214,
            "content": "test",
            "lang": "en",
            "langs": {},
            "name": "test_path",
            "parentid": 215,
            "parents": [
                {
                    "classbookid": 215,
                    "name": "test_path",
                    "parentid": 216
                },
                {
                    "classbookid": 216,
                    "name": "test_path",
                    "parentid": 214
                }
            ],
            "uuid": "098"
        },
        "m": "m82",
        "result": "DONE"
    }""")
    assert response == must_be


def test_info_parents_path_hard_cicle_2():
    """Тестирует classbook_infо
    Проверка родительского пути сложный цикл
    217 -> 215-> 216 -> 214
            ^-/--/---/---|  """
    json_request = json.dumps({
        "classbookid": 217,
        "cmd": "classbook_info",
        "m": "m82"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % response)
    must_be = json.loads("""{
        "cmd": "classbook_info",
        "data": {
            "classbookid": 217,
            "content": "test",
            "lang": "en",
            "langs": {},
            "name": "test_path",
            "parentid": 215,
            "parents": [
                {
                    "classbookid": 215,
                    "name": "test_path",
                    "parentid": 216
                },
                {
                    "classbookid": 216,
                    "name": "test_path",
                    "parentid": 214
                },
                {
                    "classbookid": 214,
                    "name": "test_path",
                    "parentid": 215
                }
            ],
            "uuid": "098"
        },
        "m": "m82",
        "result": "DONE"
    }""")
    assert response == must_be