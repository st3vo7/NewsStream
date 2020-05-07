import os.path
import requests
import json
import pprint


import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.escape


from tornado.options import define, options
define("port",default=8000, help="run on the given port", type=int)

class SourceHandler(tornado.web.RequestHandler):
    def get(self):

        self.render("sources.html",
                    )
        
        
    def post(self):
        print('u postu sam')
        izvori1 = []
        
        
        if self.get_argument("btn1",None) != None:
            self.redirect("/")
            return
        print('prosao redirect na home')
        
        if self.get_argument("btn2",None) != None:
            self.redirect("/sources")
            return
        print('prosao redirect na sources')
            
        #a=self.get_argument("drzava",None)
        #print(a)

        print('---'*26)
        a = tornado.escape.json_decode(self.request.body)
        print(a)
        print('---'*26)
        

       
        url = ( 'https://newsapi.org/v2/sources?'
                #'language=en&'
                'country='+a+'&'
                #'category=technology&'
                #'q=manchester city&'
                'apiKey=17060bbc869845deb9246555cd6f8e5d')
        
        response3 = requests.get(url)
        podaci3 = response3.json()
        print(json.dumps(podaci3, indent=1))
        
        status3 = podaci3['status']
        #print(status3)
        if status3=='error':
            print(status3)
            print(podaci3['code'])
            print(podaci3['message'])

        self.write(json.dumps({'sent': podaci3}))


class MainHandler(tornado.web.RequestHandler):
    def get(self):
         
        self.render("index.html",
                    )
        
    def post(self):

        print('u postu sam')
        if self.get_argument("btn2",None) != None:
            self.redirect("/sources")
            return
        print('prosao redirect na sauces')
       
        if self.get_argument("btn1",None) != None:
            self.redirect("/")
            return

        print('prosao redirect na home')

        print('---'*26)
        dic_data = tornado.escape.json_decode(self.request.body)
        print(dic_data)
        print('---'*26)


        a=dic_data['country']
        b=dic_data['category']
        

        
        url = ( 'https://newsapi.org/v2/top-headlines?'
                'country='+a+'&'
                'category='+b+'&'
                #'q=bomba&'
                'apiKey=17060bbc869845deb9246555cd6f8e5d')
        print(url)

        
        naslovi1 = []
        response1 = requests.get(url)
        podaci1 = response1.json()
        pprint.pprint(podaci1)


        status1 = podaci1['status']
        
        if status1=='error':
            print(status1)
            print(podaci1['code'])
            print(podaci1['message'])
        

        #print('status:', status1)
        

        self.write(json.dumps({'sent': podaci1}))

        print('dosli smo do kraja puta')
        
        

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/',MainHandler),
                  (r'/sources', SourceHandler),
                  ],
        template_path = os.path.join(os.path.dirname(__file__),"templates"),
        static_path = os.path.join(os.path.dirname(__file__),"static"),
        debug=True
    )
    http_server=tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
