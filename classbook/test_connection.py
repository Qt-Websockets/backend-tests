import lib

ws = lib.ws()

def test_conection():
	assert ws.status == 101