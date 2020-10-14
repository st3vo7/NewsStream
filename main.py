import os.path
import json
import pprint
import asyncio
from typing import Optional, Awaitable

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.escape
import tornado.httpclient

import motor.motor_tornado

from tornado.options import define, options

from user_handlers import *
from news_handlers import *


define("port", default=8000, help="run on the given port", type=int)

'''
class BaseHandler(tornado.web.RequestHandler):

    # suggested by pycharm for warning repression
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def prepare(self):
        if self.get_argument("btn1", None) is not None:
            print("detected click on btn Profile")
            self.redirect("/profile")
            return

        if self.get_argument("btn2", None) is not None:
            print("detected click on btn Sources")
            self.redirect("/sources")
            return

        if self.get_argument("logout", None) is not None:
            print("unutar if-a logout-a")
            self.clear_cookie("username")
            self.redirect("/")
            return

        if self.get_argument("btnSignIn", None) is not None:
            print("detected click on btnSignIn")
            self.redirect("/signin")
            return

    def get_current_user(self):
        a = self.get_secure_cookie("username")

        if a:
            print('***' * 15)
            print(a.decode("utf-8"))
            print('***' * 15)
            return a.decode("utf-8")
        return None



class ProfileHandler(BaseHandler):

    def prepare(self):
        super().prepare()

    @tornado.web.authenticated
    async def get(self):

        """
        my_db = self.settings['db']
        my_collection = my_db.test
        """
        username = self.current_user
        # print(username)
        # print("username: " + username)
        # find him in db
        v1 = await do_find_one(collection, username)
        # pprint.pprint(v1)

        if v1 is not None:

            # izvuci njegove vesti i renderuj ih na stranici
            headlines = v1['headlines']
            # pprint.pprint(headlines)

            await self.render('profile.html', user=self.current_user, headlines=headlines)

        else:
            print('Unknown client.')

    async def post(self):

        print('---' * 26)
        dic_data = tornado.escape.json_decode(self.request.body)
        # print(dic_data)
        print('---' * 26)

        if 'passOld' in dic_data:
            old_password = dic_data["passOld"]
            new_password1 = dic_data["passNew1"]
            new_password2 = dic_data["passNew2"]

            if new_password1 != new_password2:
                self.write(json.dumps({'sent': 'mismatched'}))
                return

            current_user_data = await do_find_one(collection, self.current_user)
            current_password = current_user_data['password']
            print("Current password: ", current_password)

            if old_password != current_password:
                self.write(json.dumps({'sent': 'current'}))
                return

            val = await do_alter_password(collection, self.current_user, new_password1)
            if val is not None:
                print('Password updated.')
                self.write(json.dumps({'sent': 'changed'}))
                return
            else:
                print('An error occurred while adjusting the timer')
            return

        if 'article' in dic_data:
            """
            my_db = self.settings['db']
            my_collection = my_db.test
            """

            username = self.current_user
            headline = dic_data['article']
            id_headline = dic_data['id_article']

            v1 = await do_delete_one(collection, username, headline)
            print("result %s" % repr(v1))
            self.write(json.dumps({'sent': id_headline}))
'''

'''
class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')

    def prepare(self):
        super().prepare()

    async def post(self):

        username = self.get_argument("username")
        password = self.get_argument("password")

        val = await do_check_one(collection, username, password)
        print('***' * 15)
        print(val)
        print('***' * 15)

        if val is not None:
            self.set_secure_cookie("username", username)
            self.redirect("/profile")
        else:
            self.write('<h1>Wrong credentials</h1>')


class SigninHandler(BaseHandler):
    def get(self):
        self.render('signin.html')

    def prepare(self):
        super().prepare()

    async def post(self):

        """
        my_db = self.settings['db']
        my_collection = my_db.test
        """

        username = self.get_argument("username")
        print(username)
        password = self.get_argument("password")
        print(password)
        # email = self.get_argument("email")

        if username == '' or password == '':
            self.write('Username and password must not be empty strings.')
            return

        val = await do_find_one(collection, username)

        if val:
            self.write('Username already exists. Please choose other one.')
            return

        val1 = await do_insert(collection, username, password)
        print("result %s" % repr(val1.inserted_id))

        if val1 is not None:
            self.set_secure_cookie("username", username)
            self.redirect("/profile")
        else:
            print("An error occurred while writing into a database.")
'''


'''
class SourceHandler(BaseHandler):

    def get(self):
        self.render("sources.html",
                    )

    def prepare(self):
        super().prepare()

    async def post(self):

        print('in POST request')
        print('---' * 26)
        dic_data = tornado.escape.json_decode(self.request.body)
        print(dic_data)
        print('---' * 26)

        # nakon što sam primio zahtev od klijenta, ovde
        # treba da vratim kontrolu ioloop-u dok potražujem podatke od apija.
        # tek po prispeću podataka od apija, "aktiviram klijenta" šaljući mu odgovor nazad

        a = dic_data['country']
        b = ''
        c = ''
        initial_request = dic_data['initial_request']

        if 'category' in dic_data:
            b = dic_data['category']
            print(b)
            print()

        if 'language' in dic_data:
            c = dic_data['language']
            print(c)
            print()

        if not initial_request:
            print('wait a little bit until checking')

            timer = 600
            if self.current_user is not None:
                # dakle ulogovan je, onda citaj tajmer iz baze
                # inace je 600

                """
                my_db = self.settings['db']
                my_collection = my_db.test
                """

                v1 = await do_find_one(collection, self.current_user)
                timer = v1['timer']

            try:
                await asyncio.sleep(timer)
            except asyncio.CancelledError:
                print('sleeping client terminated the connection')
                raise
            print('done waiting')

        url = ('https://newsapi.org/v2/sources?'
               'country=' + a + '&'
                                'category=' + b + '&'
                                                  'language=' + c + '&'
                                                                    'pageSize=100&'
                                                                    'apiKey=17060bbc869845deb9246555cd6f8e5d')

        http_client = tornado.httpclient.AsyncHTTPClient()
        try:
            response1 = await http_client.fetch(url)
        except Exception as e:
            print('An error occurred: %s' % e)

        my_data = tornado.escape.json_decode(response1.body)
        pprint.pprint(my_data)

        status1 = my_data['status']
        # print(status3)
        if status1 == 'error':
            print(status1)
            print(my_data['code'])
            print(my_data['message'])

        self.write(json.dumps({'sent': my_data}))

        print('End of POSS method in sauces.')

    def on_connection_close(self):

        try:
            print('***' * 15)
            asyncio.ensure_future(self.post()).cancel()
            print("A client has left the room.")
            print('***' * 15)

        except Exception as e:
            print("An error occurred: %s" % e)
            raise e


class MainHandler(BaseHandler):

    def get(self):
        self.render("index.html",
                    )

    def prepare(self):

        # print('U priperu sam')
        super().prepare()

    async def post(self):

        print('In POST method')
        # ovde treba da proverim da li sam dobio zahtev za vešću
        # ili zahtev za čuvanjem vesti

        print('---' * 26)
        # print(self.request.body)
        dic_data = tornado.escape.json_decode(self.request.body)
        print(dic_data)
        print('---' * 26)

        if "headline" in dic_data:
            print("Detected request for saving a news.")

            """
            my_db = self.settings['db']
            my_collection = my_db.test
            """

            username = self.current_user
            print(username)

            if username is None:
                print('There is no actively registered in client.')
                self.write(json.dumps({'sent': 'redirekt'}))
                return

            print('username: ' + username)

            headline = dic_data['headline']
            description = dic_data['description']
            url_headline = dic_data['url_headline']
            url_img = dic_data['url_img']

            val1 = await do_insert_headlines(collection, username, headline, description, url_headline, url_img)

            if val1 is not None:
                print('Updated list of news for currently registered client.')
            else:
                print("An error occurred while writing into a database.")

            self.write(json.dumps({'sent': 'upisano'}))

        elif 'timer' in dic_data:
            # print(dic_data['timer'])
            """
            my_db = self.settings['db']
            my_collection = my_db.test
            """

            timer = int(dic_data['timer'])

            username = self.current_user

            val = await do_alter_timer(collection, username, timer)

            if val is not None:
                print('Timer updated')
            else:
                print('An error occurred while updating a timer.')

        elif 'country' in dic_data:
            print("Request for the news is detected.")

            # nakon što sam primio zahtev od klijenta, ovde
            # treba da vratim kontrolu ioloop-u dok potražujem podatke od apija.
            # tek po prispeću podataka od apija, "aktiviram klijenta" šaljući mu odgovor nazad

            a = dic_data['country']
            b = dic_data['category']
            initial_request = dic_data['initial_request']
            c = ''

            if 'keyword' in dic_data:
                c = dic_data['keyword']
                # print(c)
                # print()

            # print(initial_request)

            if not initial_request:
                # cekaj recimo pet minuta
                # 10s sam stavio da vidim kako radi
                print('Wait a period of time before checking.')

                timer = 600

                if self.current_user is not None:
                    # dakle ulogovan je, onda citaj tajmer iz baze
                    # inace je 600
                    """
                    my_db = self.settings['db']
                    my_collection = my_db.test
                    """

                    v1 = await do_find_one(collection, self.current_user)
                    timer = v1['timer']
                    print(timer)

                try:
                    await asyncio.sleep(timer)
                except asyncio.CancelledError as e:
                    raise e
                finally:
                    print("okay done now1")

            url = ('https://newsapi.org/v2/top-headlines?'
                   'country=' + a + '&'
                                    'category=' + b + '&'
                                                      'pageSize=100&'
                                                      'q=' + c + '&'
                                                                 'apiKey=17060bbc869845deb9246555cd6f8e5d')
            print(url)

            http_client = tornado.httpclient.AsyncHTTPClient()
            try:
                response1 = await http_client.fetch(url)
            except Exception as e:
                print("Dogodila se greska: %s" % e)
            # else:
            # print(response1.body)

            my_data = tornado.escape.json_decode(response1.body)
            # pprint.pprint(my_data)

            status1 = my_data['status']

            if status1 == 'error':
                print(status1)
                print(my_data['code'])
                print(my_data['message'])

            # print('status:', status1)

            self.write(json.dumps({'sent': my_data, 'country': a, 'category': b, 'keyword': c}))

            print('We have reached the end.')

        else:
            print('Unknown request.')

    def on_connection_close(self):

        """
        Override this to clean up resources associated with long-lived connections.
        Note that this method is called only if the connection was closed during asynchronous processing;
        if you need to do cleanup after every request override on_finish instead.
        """

        # print(asyncio.isfuture(self.sleeping_client))  # False
        # print(asyncio.iscoroutine(self.sleeping_client)) # True
        # print(asyncio.isfuture(asyncio.ensure_future(self.sleeping_client))) # True

        try:
            print('***' * 15)
            asyncio.ensure_future(self.post()).cancel()
            print("A client has left the room.")
            print('***' * 15)

        except Exception as e:
            print("An error occurred: %s" % e)
            raise e
'''

if __name__ == '__main__':
    tornado.options.parse_command_line()

    client = motor.motor_tornado.MotorClient('localhost', 27017)
    db = client.test
    collection = db.test

    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "cookie_secret": "s8iJWyTeSQ+Hfgj59nTy4bFKahPdAEnbhsH5CRuUN1g=",
        "login_url": "/login",
        "db": db,
        "debug": True,
        "xsrf_cookies": True

    }

    app = tornado.web.Application(
        handlers=[(r'/', MainHandler),
                  (r'/sources', SourceHandler),
                  (r'/login', LoginHandler),
                  (r'/signin', SigninHandler),
                  (r'/profile', ProfileHandler),
                  (r'/favicon.ico', tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
                  ],
        **settings

    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print('Server has shut down.')
