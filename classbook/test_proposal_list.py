import json
import lib

db = lib.db()
ws = lib.ws()

def setup():
	with db.cursor() as cur:
		cur.execute("""INSERT INTO classbook VALUES(
			 402, 401, 101, "098", "1f43f", "test2",
			  "test2", "md5md5md5md5md5md5md5md5md5md5md", 
			 "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")
		cur.execute("""INSERT INTO classbook VALUES(
			 403, 402, 102, "uuid", "1gdfgdfа", "tasd",
			  "test2", "md5md5md5md5md5md5md5md5md5md5md", 
			 "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")
		cur.execute("""INSERT INTO classbook_localization VALUES(
			 104, 402, "uuid", "ru", "тест локализации", 
			 "локализация", "md5md5md5md5md5md5md5md5md5md5md",
			 "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")
		cur.execute("""INSERT INTO classbook VALUES(
			 404, 402, 102, "uuid", "1gdfgdfа", "tasd",
			  "test2", "md5md5md5md5md5md5md5md5md5md5md", 
			 "2017-10-10 10:10:10", "2017-10-10 10:10:10")""")
		cur.execute("""INSERT INTO classbook_proposal VALUES(
			 105, 402, "uuid", "en", "proposal", "before", 
			 "test1", "before", "md5md5md5md5md5md5md5md5md5md5md", 
			 "2017-10-10 10:10:10")""")
		cur.execute("""INSERT INTO classbook_proposal VALUES(
			 106, 403, "uuid", "ru", "ru_proposal", "before", 
			 "test1", "before", "md5md5md5md5md5md5md5md5md5md5md", 
			 "2017-10-10 10:10:10")""")
		cur.execute("""INSERT INTO classbook_proposal VALUES(
			 107, 402, "uuid", "de", "deproposal", "before", 
			 "test1", "before", "md5md5md5md5md5md5md5md5md5md5md", 
			 "2017-10-10 10:10:10")""")
		cur.execute("""INSERT INTO classbook_proposal VALUES(
			 108, 403, "uuid", "en", "proposal", "before", 
			 "test1", "before", "md5md5md5md5md5md5md5md5md5md5md", 
			 "2017-10-10 10:10:10")""")



def teardown():
	with db.cursor() as cur:
		cur.execute("""DELETE FROM classbook""")
		cur.execute("""DELETE FROM classbook_localization""")
		cur.execute("""DELETE FROM classbook_proposal""")


def test_proposal_list_without_params():
	"""Тестирует classbook_proposal_list
	получение без параметров"""
	json_request = json.dumps({
		"cmd": "classbook_proposal_list",
		"m": "m8431"
	})
	ws.send(json_request)
	response = json.loads(ws.recv())
	print("Response: %s" % json.dumps(response))
	must_be = json.loads("""{
		"cmd": "classbook_proposal_list",
		"data": [
			{
				"classbookid": 0,
				"id": 105,
				"lang": "en",
				"name": "proposal"
			},
			{
				"classbookid": 0,
				"id": 106,
				"lang": "ru",
				"name": "ru_proposal"
			},
			{
				"classbookid": 0,
				"id": 107,
				"lang": "de",
				"name": "deproposal"
			},
			{
				"classbookid": 0,
				"id": 108,
				"lang": "en",
				"name": "proposal"
			}
		],
		"m": "m8431",
		"result": "DONE"
	}""")
	assert response == must_be


def test_proposal_list_with_classbookid():
	"""Тестирует classbook_proposal_list
	получение с заданным classbookid"""
	json_request = json.dumps({
		"classbookid": 402,
		"cmd": "classbook_proposal_list",
		"m": "m8431"
	})
	ws.send(json_request)
	response = json.loads(ws.recv())
	print("Response: %s" % json.dumps(response))
	must_be = json.loads("""{
		"cmd": "classbook_proposal_list",
		"data": [
			{
				"classbookid": 402,
				"id": 105,
				"lang": "en",
				"name": "proposal"
			},
			{
				"classbookid": 402,
				"id": 107,
				"lang": "de",
				"name": "deproposal"
			}
		],
		"m": "m8431",
		"result": "DONE"
	}""")
	assert response == must_be


def test_proposal_list_with_en_lang():
	"""Тестирует classbook_proposal_list
	получение с english языком"""
	json_request = json.dumps({
		"lang": "en",
		"cmd": "classbook_proposal_list",
		"m": "m8431"
	})
	ws.send(json_request)
	response = json.loads(ws.recv())
	print("Response: %s" % json.dumps(response))
	must_be = json.loads("""{
		"cmd": "classbook_proposal_list",
		"data": [
			{
				"classbookid": 0,
				"id": 105,
				"lang": "en",
				"name": "proposal"
			},
			{
				"classbookid": 0,
				"id": 108,
				"lang": "en",
				"name": "proposal"
			}
		],
		"m": "m8431",
		"result": "DONE"
	}""")
	assert response == must_be


def test_proposal_list_with_de_lang():
	"""Тестирует classbook_proposal_list
	получение с de языком"""
	json_request = json.dumps({
		"lang": "de",
		"cmd": "classbook_proposal_list",
		"m": "m8431"
	})
	ws.send(json_request)
	response = json.loads(ws.recv())
	print("Response: %s" % json.dumps(response))
	must_be = json.loads("""{
		"cmd": "classbook_proposal_list",
		"data": [
			{
				"classbookid": 0,
				"id": 107,
				"lang": "de",
				"name": "deproposal"
			}
		],
		"m": "m8431",
		"result": "DONE"
	}""")
	assert response == must_be


def test_proposal_list_with_lang_classbookid():
	"""Тестирует classbook_proposal_list
	получение с ru языком и classbookid"""
	json_request = json.dumps({
		"lang": "ru",
		"classbookid": 403,
		"cmd": "classbook_proposal_list",
		"m": "m8431"
	})
	ws.send(json_request)
	response = json.loads(ws.recv())
	print("Response: %s" % json.dumps(response))
	must_be = json.loads("""{
		"cmd": "classbook_proposal_list",
		"data": [
			{
				"classbookid": 403,
				"id": 106,
				"lang": "ru",
				"name": "ru_proposal"
			}
		],
		"m": "m8431",
		"result": "DONE"
	}""")
	assert response == must_be


def test_proposal_list_with_not_exist_lang_classbookid():
	"""Тестирует classbook_proposal_list
	получение с несуществующим языком и classbookid"""
	json_request = json.dumps({
		"lang": "ur",
		"classbookid": 4033,
		"cmd": "classbook_proposal_list",
		"m": "m8431"
	})
	ws.send(json_request)
	response = json.loads(ws.recv())
	print("Response: %s" % json.dumps(response))
	must_be = json.loads("""{
		"cmd": "classbook_proposal_list",
		"code": 404,
		"error": "This article doesn't exist",
		"m": "m8431",
		"result": "FAIL"
	}""")
	assert response == must_be

