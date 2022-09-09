import pytest

def test_getAllPost(authorized_client ,testPost):
    res = authorized_client.get('/posts')
    
    assert res.status_code == 200