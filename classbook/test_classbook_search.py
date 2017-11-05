import json, lib

db = lib.db()
ws = lib.ws()

def setup():
	with db.cursor() as cur:
		cur.execute("""DELETE FROM classbook""")
		cur.execute("""DELETE FROM classbook_proposal""")
		cur.execute("""DELETE FROM classbook_localization""")
		cur.execute("""INSERT INTO classbook VALUES(
			 100, 0, 1, '098', '1f43f', 'test1', 'tefindme', 
			 '2017-10-10 10:10:10', '2017-10-10 10:10:10')""")
		cur.execute("""INSERT INTO classbook VALUES(
			 102, 0, 2, '098', '1f43f', 'test', 'test2', 
			 '2017-10-10 10:10:10', '2017-10-10 10:10:10')""")
		cur.execute("""INSERT INTO classbook VALUES(
			 103, 0, 3, '098', '1f43f', 'tutsearch', 'test2', 
			 '2017-10-10 10:10:10', '2017-10-10 10:10:10')""")
		cur.execute("""INSERT INTO classbook VALUES(
			 104, 100, 2, '098', '1f43f', 'test1test1', 'test1', 
			 '2017-10-10 10:10:10', '2017-10-10 10:10:10')""")
		cur.execute("""INSERT INTO classbook_proposal VALUES(
			 105, 102, 'en', 'proposal', 'test1', 
			 '2017-10-10 10:10:10')""")
		cur.execute("""INSERT INTO classbook_localization VALUES(
			 104, 104, 'ru', 'тест локализации', 'локализация',
			 '2017-10-10 10:10:10', '2017-10-10 10:10:10')""")
		cur.execute("""INSERT INTO classbook_localization VALUES(
			 106, 0, 'ru', 'поиск', 'найди меня',
			 '2017-10-10 10:10:10', '2017-10-10 10:10:10')""")


def teardown():
	with db.cursor() as cur:
		cur.execute("""DELETE FROM classbook""")
		cur.execute("""DELETE FROM classbook_proposal""")
		cur.execute("""DELETE FROM classbook_localization""")

def test_search_in_en_name_default_parentid():
	"""Testcase for classbook_search handler with default parentid=0
	check search in English name""" 
	json_request = json.dumps({"parentid":0,"cmd":"classbook_search", 
		"search": "1","m":"m7334"})
	ws.send(json_request)
	response = json.loads(ws.recv())
	print("Response: %s" % response)
	must_be = json.loads(
		"""{"cmd":"classbook_search",
		"data":[
		{"childs":1,"classbookid":100,"name":"test1","parentid":0,"proposals":0}],
		"m":"m7334","result":"DONE"}""")
	assert response == must_be

def test_search_in_ru_name_default_parentid():
	"""Testcase for classbook_search handler with default parentid=0
	check search in Russian name""" 
	json_request = json.dumps({"parentid":0,"cmd":"classbook_search", 
		"search": "пои", "lang":"ru","m":"m7334"})
	ws.send(json_request)
	response = json.loads(ws.recv())
	print("Response: %s" % response)
	must_be = json.loads(
		"""{"cmd":"classbook_search",
		"data":[
		{"childs":0,"classbookid":106,"name":"поиск","parentid":0,"proposals":0}],
		"m":"m7334","result":"DONE"}""")
	assert response == must_be