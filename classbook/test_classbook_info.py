import json
import lib

db = lib.db()
ws = lib.ws()

def setup():
	with db.cursor() as cur:
		cur.execute("""DELETE FROM classbook""")
		cur.execute("""DELETE FROM classbook_localization""")
		cur.execute("""INSERT INTO classbook VALUES(
			 202, 0, 6, '098', '1f43f', 'test', 
			 'test', '2017-10-10 10:10:10', '2017-10-10 10:10:10')""")
		cur.execute("""INSERT INTO classbook VALUES(
			 203, 0, 7, '098', '1f43f', 'test_with_lang', 
			 'test', '2017-10-10 10:10:10', '2017-10-10 10:10:10')""")
		cur.execute("""INSERT INTO classbook_localization VALUES(
			 204, 203, 'ru', 'тест локализации', 'локализация',
			 '2017-10-10 10:10:10', '2017-10-10 10:10:10')""")
	db.commit()

def teardown():
	with db.cursor() as cur:
		cur.execute("""DELETE FROM classbook""")
		cur.execute("""DELETE FROM classbook_localization""")
	db.commit()

def test_info_without_lang():
	"""Testcase for handler classbook_info without lang param"""
	json_request = json.dumps(
		{"classbookid":202,"cmd":"classbook_get_info","m":"m843"})
	ws.send(json_request)
	response = json.loads(ws.recv())
	print("Response: %s" % response)
	must_be = json.loads(
		"""{"cmd":"classbook_get_info",
		"data":
		{"classbookid":202,"content":"test","lang":"en",
		"langs":{},"name":"test","parentid":0,"uuid":"098"},
		"m":"m843","result":"DONE"}""")
	assert response == must_be

def test_info_with_lang():
	"""Тестирует classbook_infо с указанным языком, есть локализация"""
	json_request = json.dumps(
		{"classbookid":203, "lang":"ru", "cmd":"classbook_get_info","m":"m844"})
	ws.send(json_request)
	response = json.loads(ws.recv())
	print("Response: %s" % response)
	must_be = json.loads(
		"""{'cmd': 'classbook_get_info', 'data': 
		{'classbookid': 203, 'content': 'локализация', 'lang': 'ru', 
		'langs':
		 {'ru': 204}, 
		 'name': 'тест локализации', 'parentid': 0, 'uuid': '098'}, 
		'm': 'm844', 'result': 'DONE'}""".replace("'", "\""))
	assert response == must_be

def test_info_non_found():
	"""Тестирует classbook_infо на несуществующую статью"""
	json_request = json.dumps(
		{"classbookid":23232,"cmd":"classbook_get_info","m":"m8431"})
	ws.send(json_request)
	response = json.loads(ws.recv())
	print("Response: %s" % response)
	must_be = json.loads(
		"""{"cmd":"classbook_get_info",
		"code": 404,
		"error": "Not found the article",
		"m":"m8431","result":"FAIL"}""")
	assert response == must_be