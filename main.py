import os.path
# import requests
import json
import pprint
import asyncio
from typing import Optional, Awaitable

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.escape
import tornado.locks
import tornado.httpclient

import motor.motor_tornado

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)


async def do_find_one(my_collection, value1):
    document = await my_collection.find_one({"name": value1})
    return document


async def do_check_one(my_collection, value1, value2):
    document = await my_collection.find_one({"name": value1, "password": value2})
    return document


async def do_insert(my_collection, value1, value2):
    document = {"name": value1, "password": value2, "headlines": [], "timer": 600}
    result = await my_collection.insert_one(document)
    return result


async def do_insert_headlines(my_collection, name, value1, value2, value3, value4):
    document = {"headline": value1, "description": value2, "url_headline": value3, "url_img": value4}
    result = await my_collection.update_one({"name": name}, {'$push': {"headlines": document}})
    return result


async def do_delete_one(my_collection, name, headline):
    result = await my_collection.update_one({"name": name}, {'$pull': {"headlines": {"headline": headline}}})
    return result


async def do_alter_timer(my_collection, name, timer_value):
    result = await my_collection.update_one({"name": name}, {'$set': {"timer": timer_value}})
    return result


class BaseHandler(tornado.web.RequestHandler):

    # ovo mi predlaze tornado za uklanjanje warninga
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get_current_user(self):
        a = self.get_secure_cookie("username")

        if a:
            print('***' * 15)
            print(a.decode("utf-8"))
            print('***' * 15)
            return a.decode("utf-8")
        return None


class ProfileHandler(BaseHandler):

    @tornado.web.authenticated
    async def get(self):

        """
        my_db = self.settings['db']
        my_collection = my_db.test
        """
        username = self.current_user

        print(username)
        # print("username: " + username)

        # nadji ga u bazi
        v1 = await do_find_one(collection, username)
        # pprint.pprint(v1)

        if v1 is not None:

            # izvuci njegove vesti i renderuj ih na stranici
            headlines = v1['headlines']
            # pprint.pprint(headlines)

            await self.render('profile.html', user=self.current_user, headlines=headlines)

        else:
            print('Nepostojeci klijent.')

    async def post(self):

        if self.get_argument("btn1", None) is not None:
            print("detektovan klik na btn Profile")
            self.redirect("/profile")
            return

        if self.get_argument("btn2", None) is not None:
            print("detektovan klik na btn Sources")
            self.redirect("/sources")
            return

        if self.get_argument("logout", None) is not None:
            print("unutar if-a logout-a")
            self.clear_cookie("username")
            self.redirect("/")
            return

        print('---' * 26)
        dic_data = tornado.escape.json_decode(self.request.body)
        print(dic_data)
        print('---' * 26)

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


class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')

    async def post(self):

        if self.get_argument("btnSignIn", None) is not None:
            print("detektovan klik na btnSignIn")
            self.redirect("/signin")
            return

        if self.get_argument("btn1", None) is not None:
            print("detektovan klik na btn Profile")
            self.redirect("/profile")
            return

        if self.get_argument("btn2", None) is not None:
            print("detektovan klik na btn Sources")
            self.redirect("/sources")
            return

        username = self.get_argument("username")
        password = self.get_argument("password")

        self.set_secure_cookie("username", username)

        val = await do_check_one(collection, username, password)
        print('***' * 15)
        print(val)
        print('***' * 15)

        if val is not None:
            self.redirect("/profile")
        else:
            self.write('<h1>Pogresni kredencijali</h1>')


class SigninHandler(BaseHandler):
    def get(self):
        self.render('signin.html')

    async def post(self):

        if self.get_argument("btn1", None) is not None:
            print("detektovan klik na btn Profile")
            self.redirect("/profile")
            return

        if self.get_argument("btn2", None) is not None:
            print("detektovan klik na btn Sources")
            self.redirect("/sources")
            return

        """
        my_db = self.settings['db']
        my_collection = my_db.test
        """

        username = self.get_argument("username")
        password = self.get_argument("password")
        # email = self.get_argument("email")

        val = await do_find_one(collection, username)

        if val:
            self.write('Username already exists. Please choose other one.')
            return

        val1 = await do_insert(collection, username, password)
        print("result %s" % repr(val1.inserted_id))

        self.set_secure_cookie("username", username)

        if val1 is not None:
            self.redirect("/profile")
        else:
            print("greska pri upisu u bazu")


class SourceHandler(BaseHandler):

    def get(self):
        self.render("sources.html",
                    )

    async def post(self):
        print('u postu sam')

        if self.get_argument("btn1", None) is not None:
            self.redirect("/profile")
            return
        print('prosao redirect na profile')

        if self.get_argument("btn2", None) is not None:
            self.redirect("/sources")
            return
        print('prosao redirect na sources')

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
            print('cekaj malo dok proveris')

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

            self.sleeping_client = asyncio.sleep(timer)
            await self.sleeping_client
            print('gotovo cekanje')

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
            print('Dogodila se greska: %s' % e)

        my_data = tornado.escape.json_decode(response1.body)
        pprint.pprint(my_data)

        status1 = my_data['status']
        # print(status3)
        if status1 == 'error':
            print(status1)
            print(my_data['code'])
            print(my_data['message'])

        self.write(json.dumps({'sent': my_data}))

        print('kraj posta u sauces')

    def on_connection_close(self):

        print('***' * 15)
        asyncio.ensure_future(self.sleeping_client).cancel()
        print("A client has left the room.")
        print('***' * 15)


class MainHandler(BaseHandler):

    def get(self):
        self.render("index.html",
                    )

    async def post(self):
        print('u postu sam')

        if self.get_argument("btn2", None) is not None:
            self.redirect("/sources")
            return
        print('prosao redirect na sauces')

        if self.get_argument("btn1", None) is not None:
            self.redirect("/profile")
            return
        print('prosao redirect na profile')

        # ovde treba da proverim da li sam dobio zahtev za vešću
        # ili zahtev za čuvanjem vesti

        print('---' * 26)
        # print(self.request.body)
        dic_data = tornado.escape.json_decode(self.request.body)
        print(dic_data)
        print('---' * 26)

        if "headline" in dic_data:
            print("detektovao sam zahtev za cuvanjem jedne vesti")

            """
            my_db = self.settings['db']
            my_collection = my_db.test
            """

            username = self.current_user
            print(username)

            if username is None:
                print('nemam trenutno aktivnog klijenta')
                self.write(json.dumps({'sent': 'redirekt'}))
                return

            print('username: ' + username)

            headline = dic_data['headline']
            description = dic_data['description']
            url_headline = dic_data['url_headline']
            url_img = dic_data['url_img']

            val1 = await do_insert_headlines(collection, username, headline, description, url_headline, url_img)

            if val1 is not None:
                print('azurirana lista vesti trenutnog klijenta')
            else:
                print("greska pri upisu u bazu")

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
                print('azuriran tajmer')
            else:
                print('greska pri azuriranju tajmera')

        elif 'country' in dic_data:
            print("detektovao sam zahtev za potragom vesi")

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
                print('ceka odredjeno vreme na proveru')

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

                self.sleeping_client = asyncio.sleep(timer)
                await self.sleeping_client
                print("okay done now")

            url = ('https://newsapi.org/v2/top-headlines?'
                   'country=' + a + '&'
                                    'category=' + b + '&'
                                                      'pageSize=100&'
                                                      'q=' + c + '&'
                                                                 'apiKey=17060bbc869845deb9246555cd6f8e5d')
            print(url)

            http_client = tornado.httpclient.AsyncHTTPClient()
            try:
                print("+++++++++++++++++++++++++++++++++iznad response1 await+++++++++++++++++++++++++++++++++++++++")
                response1 = await http_client.fetch(url)
                print("+++++++++++++++++++++++++++++++++ispod response1 await+++++++++++++++++++++++++++++++++++++++")
            except Exception as e:
                print("Dogodila se greska: %s" % e)
            # else:
            # print(response1.body)

            print("--------------------------------------iznad my_data-----------------------------------------------")
            my_data = tornado.escape.json_decode(response1.body)
            print("--------------------------------------ispod my data-----------------------------------------------")
            pprint.pprint(my_data)

            status1 = my_data['status']

            if status1 == 'error':
                print(status1)
                print(my_data['code'])
                print(my_data['message'])

            # print('status:', status1)

            self.write(json.dumps({'sent': my_data, 'country': a, 'category': b, 'keyword': c}))

            print('dosli smo do kraja puta')

        else:
            print('nepoznat zahtev')

    def on_connection_close(self):

        """
        Override this to clean up resources associated with long-lived connections.
        Note that this method is called only if the connection was closed during asynchronous processing;
        if you need to do cleanup after every request override on_finish instead.
        """

        # nije response1, jer je to odgovor od API-ja
        # meni treba da obradim slucaj kada klijent zatvori tab
        # self.response1.cancel()
        # self.sleeping_client.cancel()

        # print(asyncio.isfuture(self.sleeping_client))
        # print(asyncio.iscoroutine(self.sleeping_client))
        # print(asyncio.isfuture(asyncio.ensure_future(self.sleeping_client)))

        try:
            print('***' * 15)
            asyncio.ensure_future(self.sleeping_client).cancel()
            print("A client has left the room.")
            print('***' * 15)

        except asyncio.CancelledError as e:
            print("An error occurred: %s" % e)


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
                  (r'/profile', ProfileHandler)
                  ],
        **settings

    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
