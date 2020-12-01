import tornado.web
from typing import Optional, Awaitable


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

