import tornado.web
import tornado.ioloop
from tornado_helper import *
from token_helper import generate_token
from db_helper import *


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        token, user_id = get_session_cookies(self)
        if user_id is None or token is None:
            self.redirect('/signin')
            return
        if check_token(token, user_id):
            self.render('templates/dashboard.html', data=get_user_data(user_id))
        else:
            self.redirect('/login')


class DeleteUserRecord(tornado.web.RequestHandler):
    def get(self):
        token, user_id = get_session_cookies(self)
        if check_token(token, user_id):
            delete_user_data(user_id, self.get_argument('id'))
        self.redirect('/')


class AddUserDataHandler(tornado.web.RequestHandler):
    def post(self):
        token, user_id = get_session_cookies(self)
        if check_token(token, user_id):
            add_user_data(user_id, self.get_body_argument('data'))
        self.redirect('/')


class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(open('static/login.html', 'rb').read())
        self.flush()

    def post(self):
        if process_session_request(self):
            return
        if (ls := process_body_arguments(self))[0]:
            return
        login = ls[1]
        password = ls[2]
        user = get_user(login)
        if user and user.password == password:
            self.set_secure_cookie('token', create_token(generate_token(), user.id))
            self.set_secure_cookie('user-id', str(user.id))
            self.redirect('/')
            return
        else:
            self.redirect('/login')


class SignInHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(open('static/signin.html', 'rb').read())
        self.flush()

    def post(self):
        if process_session_request(self):
            return
        if (ls := process_body_arguments(self))[0]:
            return
        login = ls[1]
        password = ls[2]
        if not check_username(login):
            self.redirect('/signin')
            return
        user = create_user(login, password)
        self.set_secure_cookie('token', create_token(generate_token(), user.id))
        self.set_secure_cookie('user-id', str(user.id))
        self.redirect('/')


def create_app() -> tornado.web.Application:
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/add_user_record", AddUserDataHandler),
        (r"/delete_user_record", DeleteUserRecord),
        (r"/signin", SignInHandler),
        (r"/login", LoginHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {'path': 'static'})
    ], cookie_secret='ukCYdbP7:BrcmkAGsbRZxSbexMRnMFB2P3anjR*'
                     'NB4uus5$8lvQMXxVw8oS0tsM98_Fi0q7JdnLTUk'
                     'Lfz8VXa7:xpcKJYw3OslC1Bi4QyzewQGm9ngeRH'
                     'nBqgV02AovuXqh7BtS0$7AnV5pdTG0aTRTvrJcd')


if __name__ == '__main__':
    app = create_app()
    app.listen(1111)
    tornado.ioloop.IOLoop.current().start()
