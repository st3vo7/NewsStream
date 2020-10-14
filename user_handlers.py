import json
import tornado.escape

from base_handler import *
from db_manip import *


class ProfileHandler(BaseHandler):

    def prepare(self):
        super().prepare()

    @tornado.web.authenticated
    async def get(self):

        my_db = self.settings['db']
        collection = my_db.test

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

        my_db = self.settings['db']
        collection = my_db.test

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


class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')

    def prepare(self):
        super().prepare()

    async def post(self):

        username = self.get_argument("username")
        password = self.get_argument("password")

        my_db = self.settings['db']
        collection = my_db.test

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

        my_db = self.settings['db']
        collection = my_db.test

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
