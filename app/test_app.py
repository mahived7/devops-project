import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_loads(client):
    res = client.get('/')
    assert res.status_code == 200
    assert b'Task Manager' in res.data

def test_add_task(client):
    res = client.post('/add', data={'title': 'Test task'})
    assert res.status_code == 200
    assert b'Test task' in res.data

def test_health_check(client):
    res = client.get('/health')
    assert res.status_code == 200
    assert b'healthy' in res.data

def test_metrics_endpoint(client):
    res = client.get('/metrics')
    assert res.status_code == 200

def test_delete_task(client):
    client.post('/add', data={'title': 'To be deleted'})
    res = client.post('/delete/1')
    assert res.status_code == 200