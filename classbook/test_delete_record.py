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


def test_delete_record():
	"""Тестирует classbook_delete_record
	удаление статьи без потомков"""
	json_request = json.dumps({
		"classbookid": 402,
		"cmd": "classbook_delete_record",
		"m": "m8431"
	})
	ws.send(json_request)
	response = json.loads(ws.recv())
	print("Response: %s" % json.dumps(response))
	must_be = json.loads("""{
		"cmd": "classbook_delete_record",
		"m": "m8431",
		"result": "DONE"
	}""")
	assert response == must_be
	with db.cursor() as cur:
		cur.execute("SELECT ordered FROM classbook WHERE id=402")
		assert None == cur.fetchone()


def test_delete_record_with_childs():
	"""Тестирует classbook_delete_record
	удаление статьи с потомками"""
	json_request = json.dumps({
		"classbookid": 401,
		"cmd": "classbook_delete_record",
		"m": "m8431"
	})
	ws.send(json_request)
	response = json.loads(ws.recv())
	print("Response: %s" % json.dumps(response))
	must_be = json.loads("""{
		"cmd": "classbook_delete_record",
		"code": 403,
		"error": "Could not delete, because childs exists. Please remove childs first.",
		"m": "m8431",
		"result": "FAIL"
	}""")
	assert response == must_be
	with db.cursor() as cur:
		cur.execute("SELECT name FROM classbook WHERE id=401")
		assert "test1" == cur.fetchone()[0]

def test_delete_record_with_lang():
	"""Тестирует classbook_delete_record
	удаление статьи без потомков с локализацией"""
	json_request = json.dumps({
		"classbookid": 402,
		"cmd": "classbook_delete_record",
		"m": "m8431"
	})
	ws.send(json_request)
	response = json.loads(ws.recv())
	print("Response: %s" % json.dumps(response))
	must_be = json.loads("""{
		"cmd": "classbook_delete_record",
		"m": "m8431",
		"result": "DONE"
	}""")
	assert response == must_be
	with db.cursor() as cur:
		cur.execute("SELECT ordered FROM classbook WHERE id=402")
		assert None == cur.fetchone()
		cur.execute("""SELECT name FROM classbook_localization
			WHERE classbookid=402""")
		assert None == cur.fetchone()