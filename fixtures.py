import pytest
from websocket import create_connection
import json

@pytest.fixture()
def websocket():
	ws = create_connection("ws://localhost:1234")
	print("Websocket connection was created")
	token = json.dumps({"cmd":"token","token":"97A16219-0FD0-4624-8CC5-958644DAAA04","m":"m1"})
	ws.send(token)
	result = ws.recv()
	return ws