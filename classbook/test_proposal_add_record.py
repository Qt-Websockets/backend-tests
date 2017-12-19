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
		cur.execute("""INSERT INTO classbook_proposal VALUES(
			 105, 402, "uuid", "en", "proposal", "before", 
			 "test1", "before", "md5md5md5md5md5md5md5md5md5md5md", 
			 "2017-10-10 10:10:10")""")

def teardown():
	with db.cursor() as cur:
		cur.execute("""DELETE FROM classbook""")
		cur.execute("""DELETE FROM classbook_localization""")
		cur.execute("""DELETE FROM classbook_proposal""")


def test_proposal_add_record_exsist_article():
	"""Тестирует classbook_proposal_add_record
	добавление предложения для существующей статьи"""
	json_request = json.dumps({
		"classbookid": 402,
		"name": "add proposal",
		"content": "exist article",
		"lang": "en",
		"cmd": "classbook_proposal_add_record",
		"m": "m8431"
	})
	ws.send(json_request)
	response = json.loads(ws.recv())
	print("Response: %s" % json.dumps(response))
	classbook_proposal_id = None
	with db.cursor() as cur:
		cur.execute("""SELECT id FROM classbook_proposal WHERE content='exist article'""")
		#TypeError: 'NoneType' object is not subscriptable
		#Означает что нет записи в БД
		classbook_proposal_id = cur.fetchone()[0]
	must_be = json.loads("""{
	  "cmd": "classbook_proposal_add_record",
	  "data": {
		"classbook_proposal_id": 111,
		"classbookid": 402,
		"content": "exist article",
		"content_before": "test2",
		"lang": "en",
		"md5_content": "e682fa1c72d936f876d566cfbf3a5d23",
		"name": "add proposal",
		"name_before": "test2"
	  },
	  "m": "m8431",
	  "result": "DONE"
	}""")
	must_be["data"]["classbook_proposal_id"] = classbook_proposal_id
	assert response == must_be


def test_proposal_add_record_not_exist_article():
	"""Тестирует classbook_proposal_add_record
	добавление предложения для существующей статьи"""
	json_request = json.dumps({
		"classbookid": 4022,
		"name": "add proposal",
		"content": "not exist article",
		"lang": "en",
		"cmd": "classbook_proposal_add_record",
		"m": "m8431"
	})
	ws.send(json_request)
	response = json.loads(ws.recv())
	print("Response: %s" % json.dumps(response))
	must_be = json.loads("""{
		"cmd": "classbook_proposal_add_record",
		"code": 404,
		"error": "This article or localization doesn't exist",
		"m": "m8431",
		"result": "FAIL"
	}""")
	assert response == must_be
