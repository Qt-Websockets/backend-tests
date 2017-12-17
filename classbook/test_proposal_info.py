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
             105, 402, "uuid", "en", "proposal", 
             "test1", "md5md5md5md5md5md5md5md5md5md5md", 
             "2017-10-10 10:10:10")""")

def teardown():
    with db.cursor() as cur:
        cur.execute("""DELETE FROM classbook""")
        cur.execute("""DELETE FROM classbook_localization""")
        cur.execute("""DELETE FROM classbook_proposal""")


def test_not_exist_proposal_info():
    """Тестирует classbook_proposal_info
    получение несуществующего предложения"""
    json_request = json.dumps({
        "classbook_proposal_id": 1055,
        "cmd": "classbook_proposal_info",
        "m": "m8431"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % json.dumps(response))
    must_be = json.loads("""{
      "cmd": "classbook_proposal_info",
      "code": 404,
      "error": "This proposal doesn't exist",
      "m": "m8431",
      "result": "FAIL"
    }""")
    assert response == must_be


def test_proposal_info():
    """Тестирует classbook_proposal_info
    получение существующего предложения"""
    json_request = json.dumps({
        "classbook_proposal_id": 105,
        "cmd": "classbook_proposal_info",
        "m": "m8431"
    })
    ws.send(json_request)
    response = json.loads(ws.recv())
    print("Response: %s" % json.dumps(response))
    must_be = json.loads("""{
	  "cmd": "classbook_proposal_info",
	  "data": {
	    "classbookid": 402,
	    "content": "test1",
	    "id": 105,
	    "lang": "en",
	    "name": "proposal"
	  },
	  "m": "m8431",
	  "result": "DONE"
	}""")
    assert response == must_be
