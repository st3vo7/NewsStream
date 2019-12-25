import os.path
import requests
import json


import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web


url1 = ( 'https://newsapi.org/v2/top-headlines?'
        'country=rs&'
        #'category=technology&'
        #'q=bomba&'
        'apiKey=')


url3 = ( 'https://newsapi.org/v2/sources?'
        #'language=en&'
        'country=gb&'
        #'category=technology&'
        #'q=manchester city&'
        'apiKey=')


from tornado.options import define, options
define("port",default=8000, help="run on the given port", type=int)

class SourceHandler(tornado.web.RequestHandler):
    def get(self):
        
        izvori1 = []
        
        #self.render("sources.html")
        response3 = requests.get(url3)
        podaci3 = response3.json()
        
        status3 = podaci3['status']
        print(status3)
        
        #print(json.dumps(podaci3, indent=1))
        
        items3 = podaci3['sources']
        for index in range(len(items3)):
            for key in items3[index]:
                if key == 'name':
                    izvori1.append(items3[index][key] + ' - ' + items3[index]['description'])
        
        
        
        
        self.render("sources.html",
                    izvori1=izvori1
                    )
        
        
    def post(self):
        
        izvori1 = []
        
        
        if self.get_argument("btn1",None) != None:
            self.redirect("/")
        
        if self.get_argument("btn2",None) != None:
            self.redirect("/sources")
            
        a=self.get_argument("drzava",None)
        #print(a)
        
        url = ( 'https://newsapi.org/v2/sources?'
                #'language=en&'
                'country='+a+'&'
                #'category=technology&'
                #'q=manchester city&'
                'apiKey=')
        
        response3 = requests.get(url)
        podaci3 = response3.json()
        
        status3 = podaci3['status']
        print(status3)
        
        #print(json.dumps(podaci3, indent=1))
        
        items3 = podaci3['sources']
        for index in range(len(items3)):
            for key in items3[index]:
                if key == 'name':
                    izvori1.append(items3[index][key] + ' - ' + items3[index]['description'])
        

        
        self.render("sources.html",
                    izvori1=izvori1
                    )


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        
        naslovi1 = []
        #naslovi2 = []
        
        
        
        response1 = requests.get(url1)
        podaci1 = response1.json()
        #print(json.dumps(podaci1, indent=1))
        
        status1 = podaci1['status']
        
        
        if status1=='error':
            print(status1)
            print(podaci1['code'])
            print(podaci1['message'])
        
        
        print(status1)
            
        
        items1 = podaci1['articles']
        for index in range(len(items1)):
            for key in items1[index]:
                if key == 'title':
                    naslovi1.append(items1[index][key])
        
        
        
        
        
        self.render("index.html",
                    naslovi1=naslovi1,
                    zemlja = "rs",
                    kat = "all")
        
    def post(self):
        
        if self.get_argument("btn2",None) != None:
            self.redirect("/sources")
       
        if self.get_argument("btn1",None) != None:
            self.redirect("/")
       
        
        a=self.get_argument("drzava",None)
        b=self.get_argument("kategorija",None)
        print(b)
        
        #print(a)
        
        url = ( 'https://newsapi.org/v2/top-headlines?'
                'country='+a+'&'
                'category='+b+'&'
                #'q=bomba&'
                'apiKey=')
        #print(url)

        
        naslovi1 = []
        response1 = requests.get(url)
        podaci1 = response1.json()
        status1 = podaci1['status']
        
        if status1=='error':
            print(status1)
            print(podaci1['code'])
            print(podaci1['message'])
        
        
        print(status1)
        
        items1 = podaci1['articles']
        for index in range(len(items1)):
            for key in items1[index]:
                if key == 'title':
                    naslovi1.append(items1[index][key])
        
        
        self.render("index.html",
                    naslovi1=naslovi1,
                    zemlja = a,
                    kat = b,
                    )
        
        
        
        
            
        

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/',MainHandler),
                  (r'/sources', SourceHandler),
                  ],
        template_path=os.path.join(os.path.dirname(__file__),"templates"),
        debug=True
    )
    http_server=tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
