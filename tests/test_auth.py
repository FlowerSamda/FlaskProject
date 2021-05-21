import pytest
from flask import g, session
from flaskr.db import get_db


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200  # get 요청 후 Response 반환
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a'}
    )  # client.post는 data dict를 form data로 post
    #  register view가 로그인 뷰로 리다이렉트 할 때, header에 Location이 생긴다네?
    assert 'http://localhost/auth/login' == response.headers['Location']

    with app.app_context():
        assert get_db().execute(
            "select * from user where username = 'a'",
        ).fetchone() is not None


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    # response.data는 response body를 바이트로 반환하기에, 위에 parameterize에 b''로 되있음)
    assert message in response.data  # 반대로, response.get_data(as_text=True) 사용도 가능

def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        # session에 유저 아이디가 있으면 안됨(로그아웃 했으니까!, session 은 flask의 글로벌 변수)
        assert 'user_id' not in session