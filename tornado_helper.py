import tornado.web
from db_helper import *
from typing import Union


# return None or str by cookie name
def get_secure_cookie(self: tornado.web.RequestHandler, name: str) -> Union[None, str]:
    return None if (v := self.get_secure_cookie(name)) is None else v.decode('utf-8')


# update all tokens and return token and user-id cookie
def get_session_cookies(self) -> tuple[str | None, int | None]:
    update_tokens()
    return get_secure_cookie(self, 'token'), get_secure_cookie(self, 'user-id')


# process session cookies. return True if cookies valid and redirected to /
def process_session_request(self):
    token, user_id = get_session_cookies(self)
    if check_token(token, user_id):
        self.redirect('/')
        return True
    return False


# process body arguments. return (True, None, None) if login and password fields is NOT valid.
# return (True, login, password) if not.
def process_body_arguments(self) -> tuple[bool, Union[None, str], Union[None, str]]:
    login = self.get_body_argument('login')
    password = self.get_body_argument('password')
    if not login or login == '' or not password or password == '':
        self.redirect('/login')
        return True, None, None
    return False, login, password
