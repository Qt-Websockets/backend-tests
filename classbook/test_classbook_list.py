import json, lib

db = lib.db()
ws = lib.ws()

def setup():
	with db.cursor() as cur:
		cur.execute("""DELETE FROM classbook""")
		cur.execute("""DELETE FROM classbook_proposal""")
		cur.execute("""INSERT INTO classbook VALUES(
			 100, 0, 1, '098', '1f43f', 'test1', 'test1', 
			 '2017-10-10 10:10:10', '2017-10-10 10:10:10')""")
		cur.execute("""INSERT INTO classbook VALUES(
			 102, 0, 2, '098', '1f43f', 'test2', 'test2', 
			 '2017-10-10 10:10:10', '2017-10-10 10:10:10')""")
		cur.execute("""INSERT INTO classbook VALUES(
			 103, 0, 3, '098', '1f43f', 'test2', 'test2', 
			 '2017-10-10 10:10:10', '2017-10-10 10:10:10')""")
		cur.execute("""INSERT INTO classbook VALUES(
			 104, 100, 2, '098', '1f43f', 'test1test1', 'test1', 
			 '2017-10-10 10:10:10', '2017-10-10 10:10:10')""")
		cur.execute("""INSERT INTO classbook_proposal VALUES(
			 105, 102, 'en', 'proposal', 'test1', 
			 '2017-10-10 10:10:10')""")
	db.commit()

def teardown():
	with db.cursor() as cur:
		cur.execute("""DELETE FROM classbook""")
		cur.execute("""DELETE FROM classbook_proposal""")
	db.commit()


def test_with_parentid():
	"""Testcase for classbook_list handler with default parentid=0""" 
	json_request = json.dumps({"parentid":0,"cmd":"classbook_get_list","m":"m7334"})
	ws.send(json_request)
	response = json.loads(ws.recv())
	print("Response: %s" % response)
	must_be = json.loads(
		"""{"cmd":"classbook_get_list",
		"data":[
		{"childs":1,"classbookid":100,"name":"test1","parentid":0,"proposals":0},
		{"childs":0,"classbookid":102,"name":"test2","parentid":0,"proposals":1},
		{"childs":0,"classbookid":103,"name":"test2","parentid":0,"proposals":0}],
		"m":"m7334","result":"DONE"}""")
	assert response == must_be