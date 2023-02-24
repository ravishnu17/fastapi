import pytest

def test_getAllPost(authorized_client ,testPost):
    res = authorized_client.get('/get/posts')
    print(res.json())
    assert res.status_code == 200