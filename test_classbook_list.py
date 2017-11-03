import pytest
from fixtures import websocket
import json

def test_conection():
	ws = websocket()
	assert ws.status == 101

def test_with_parentid():
	"""Testcase for classbook_list handler with default parentid=0""" 
	ws = websocket()
	json_request = json.dumps({"parentid":0,"cmd":"classbook_get_list","m":"m7334"})
	ws.send(json_request)
	response = json.loads(ws.recv())
	print("Response: %s" % response)
	must_be = json.loads(
		"""{"cmd":"classbook_get_list",
		"data":[
		{"childs":0,"classbookid":1,"name":"Intro","parentid":0,"proposals":0},
		{"childs":0,"classbookid":2,"name":"Second","parentid":0,"proposals":0},
		{"childs":0,"classbookid":3,"name":"Third","parentid":0,"proposals":0}],
		"m":"m7334","result":"DONE"}""")
	assert response == must_be