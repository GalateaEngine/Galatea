from server import app
import json


# /classify tests
def test_classify_text():
    params={"text":"Hey there!"}
    request, response = app.test_client.get('/classify',params=params)
    assert response.status == 200
    assert type(response.text) == str

def test_classify_number():
    params={"text":32}
    request, response = app.test_client.get('/classify',params=params)
    assert response.status == 200
    assert type(response.text) == str

def test_classify_missing_parameters():
    params={"test":"test"}
    request, response = app.test_client.get('/classify',params=params)
    assert response.status == 401

def test_classify_wrong_method():
    request, response = app.test_client.post('/classify')
    assert response.status == 405

# /add tests
def test_add_partial():
    params={"text":"Im not feeling","emotions":{"anger":"0.0"}}
    request, response = app.test_client.post('/add',data=json.dumps(params))
    assert response.status == 200
    assert type(response.text) == str
    
def test_add_missing_text():
    params={"emotions":{"anger":"0.0"}}
    request, response = app.test_client.post('/add',data=json.dumps(params))
    assert response.status == 401    

def test_add_missing_emotion():
    params=({"text":"Hey there!"})
    request, response = app.test_client.post('/add',data=json.dumps(params))
    assert response.status == 401

def test_add_wrong_method():
    params=({"text":"Hey there!"})
    request, response = app.test_client.get('/add',data=json.dumps(params))
    assert response.status == 405

# /heartbeat

def test_heartbeat():
    request, response = app.test_client.get('/heartbeat')
    assert response.status == 200
    assert response.json == {"status":"alive"}

def test_heartbeat_wrong_method():
    request, response = app.test_client.post('/heartbeat')
    assert response.status == 405

