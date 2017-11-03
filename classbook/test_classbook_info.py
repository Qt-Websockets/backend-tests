import pytest
from fixtures import websocket
import json


import pymysql
db = pymysql.connect(user="root", passwd="root", db="freehackquest")

def setup():
	with db.cursor() as cur:
		cur.execute("""INSERT INTO classbook VALUES(
			 202, 0, 6, '098', '1f43f', 'test', 'test', '2017-10-10 10:10:10', '2017-10-10 10:10:10')""")
	db.commit()

def teardown():
	with db.cursor() as cur:
		cur.execute("""DELETE FROM classbook WHERE id=202""")
	db.commit()
	db.close()

def test_classbook_info_case1():
	"""Testcase for handler classbook_info without lang param"""
	ws = websocket()
	json_request = json.dumps({"classbookid":202,"cmd":"classbook_get_info","m":"m843"})
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