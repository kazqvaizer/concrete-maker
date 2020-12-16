from io import StringIO

import pytest
from django.contrib.auth import BACKEND_SESSION_KEY, HASH_SESSION_KEY, SESSION_KEY
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.handlers.wsgi import WSGIRequest
from rest_framework_simplejwt.tokens import AccessToken

from app.middleware import JWTAuthMiddleware, TokenAuthMiddleware

pytestmark = [
    pytest.mark.django_db,
]


@pytest.fixture
def session_user(mixer):
    return mixer.blend("auth.User")


@pytest.fixture
def token_user(mixer):
    return mixer.blend("auth.User")


@pytest.fixture
def anon_user():
    return AnonymousUser()


@pytest.fixture
def req(anon_user):
    req = WSGIRequest(
        {
            "REQUEST_METHOD": "GET",
            "PATH_INFO": "/",
            "wsgi.input": StringIO(),
        }
    )
    req.user = anon_user

    middleware = SessionMiddleware(get_response=lambda r: None)
    middleware.process_request(req)
    req.session.save()

    return req


@pytest.fixture
def setup_session(session_user, req):
    req.session[SESSION_KEY] = session_user.pk
    req.session[BACKEND_SESSION_KEY] = "django.contrib.auth.backends.ModelBackend"
    req.session[HASH_SESSION_KEY] = session_user.get_session_auth_hash()


@pytest.fixture
def setup_jwt(token_user, req):
    payload = AccessToken.for_user(token_user)
    req.META["HTTP_AUTHORIZATION"] = f"JWT {payload}"


@pytest.fixture
def setup_drf(token_user, req, mixer):
    token = mixer.blend("authtoken.Token", user=token_user)
    req.META["HTTP_AUTHORIZATION"] = f"Token {token}"


@pytest.mark.usefixtures("setup_session", "setup_jwt")
def test_if_request_has_token_user_it_will_be_set_for_jwt_auth(token_user, req):
    fake_request = JWTAuthMiddleware(lambda r: r)(req)

    assert fake_request.user == token_user


@pytest.mark.usefixtures("setup_session", "setup_drf")
def test_if_request_has_token_user_it_will_be_set_for_drf_auth(token_user, req):
    fake_request = TokenAuthMiddleware(lambda r: r)(req)

    assert fake_request.user == token_user


@pytest.mark.usefixtures("setup_session")
def test_if_request_has_no_token_user_then_session_user_will_set_for_jwt(
    session_user, req
):
    fake_request = JWTAuthMiddleware(lambda r: r)(req)

    assert fake_request.user == session_user


@pytest.mark.usefixtures("setup_session")
def test_if_request_has_no_token_user_then_session_user_will_set_for_drf(
    session_user, req
):
    fake_request = TokenAuthMiddleware(lambda r: r)(req)

    assert fake_request.user == session_user


def test_if_request_has_no_jwt_or_another_user_anonymoous_will_set_for_jwt(
    req, anon_user
):
    fake_request = JWTAuthMiddleware(lambda r: r)(req)

    assert fake_request.user == anon_user


def test_if_request_has_no_jwt_or_another_user_anonymoous_will_set_for_drf(
    req, anon_user
):
    fake_request = TokenAuthMiddleware(lambda r: r)(req)

    assert fake_request.user == anon_user


def test_broken_token_is_okay_for_jwt(req, anon_user):
    req.META["HTTP_AUTHORIZATION"] = "JWT brokenz!"

    fake_request = JWTAuthMiddleware(lambda r: r)(req)

    assert fake_request.user == anon_user


def test_broken_token_is_okay_for_drf(req, anon_user):
    req.META["HTTP_AUTHORIZATION"] = "Token brokenz!"

    fake_request = TokenAuthMiddleware(lambda r: r)(req)

    assert fake_request.user == anon_user
