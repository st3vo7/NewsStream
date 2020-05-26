import os.path
import requests
import json
import pprint
import asyncio

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.escape
import tornado.locks
import tornado.httpclient


from tornado.options import define, options
define("port",default=8000, help="run on the given port", type=int)


class MessageBuffer(object):
    def __init__(self):
        self.cond = tornado.locks.Condition()
        
        #lista ili dict?
        self.cache = {}
        #self.cache_size = 200
    
    def add_message(self, message):
        self.cache = json.dumps({'sent': message})
        self.cond.notify()
        
global_message_buffer = MessageBuffer()


class SourceHandler(tornado.web.RequestHandler):
    def get(self):

        self.render("sources.html",
                    )
        
        
    async def post(self):
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
        dic_data = tornado.escape.json_decode(self.request.body)
        print(dic_data)
        print('---'*26)

        #nakon što sam primio zahtev od klijenta, ovde
        #treba da vratim kontrolu ioloop-u dok potražujem podatke od apija.
        #tek po prispeću podataka od apija, "aktiviram klijenta" šaljući mu odgovor nazad

        a=dic_data['country']
        initial_request = dic_data['initial_request']

        if(not initial_request):
            print('cekaj malo dok proveris')
            await asyncio.sleep(600)
            print('gotovo cekanje')
        
        
       
        url = ( 'https://newsapi.org/v2/sources?'
                #'language=en&'
                'country='+a+'&'
                #'category=technology&'
                #'q=manchester city&'
                'pageSize=100&'
                'apiKey=17060bbc869845deb9246555cd6f8e5d')


        http_client = tornado.httpclient.AsyncHTTPClient()
        try:
            response1 = await http_client.fetch(url)
        except Exception as e:
            print('An error occurred: %s' %e)

        podaci1 = tornado.escape.json_decode(response1.body)
        pprint.pprint(podaci1)

        '''
        response3 = requests.get(url)
        podaci3 = response3.json()
        print(json.dumps(podaci3, indent=1))'
        '''
        
        status1 = podaci1['status']
        #print(status3)
        if status1=='error':
            print(status1)
            print(podaci1['code'])
            print(podaci1['message'])

        self.write(json.dumps({'sent': podaci1}))

        print('kraj posta u sauces')


class MainHandler(tornado.web.RequestHandler):

    def get(self):
         
        self.render("index.html",
                    )
        
    async def post(self):

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
        #print(self.request.body)
        dic_data = tornado.escape.json_decode(self.request.body)
        print(dic_data)
        print('---'*26)

        #nakon što sam primio zahtev od klijenta, ovde
        #treba da vratim kontrolu ioloop-u dok potražujem podatke od apija.
        #tek po prispeću podataka od apija, "aktiviram klijenta" šaljući mu odgovor nazad

    
        a=dic_data['country']
        b=dic_data['category']
        initial_request = dic_data['initial_request']
        #print(initial_request)
        
 
        if(not initial_request):
            #cekaj recimo pet minuta
            #10s sam stavio da vidim kako radi
            print('ceka odredjeno vreme na proveru')
            await asyncio.sleep(600)
            print("okay done now")
        


        url = ( 'https://newsapi.org/v2/top-headlines?'
                'country='+a+'&'
                'category='+b+'&'
                'pageSize=100&'
                #'q=bomba&'
                'apiKey=17060bbc869845deb9246555cd6f8e5d')
        print(url)

        http_client = tornado.httpclient.AsyncHTTPClient()
        try:
            response1 = await http_client.fetch(url)
        except Exception as e:
            print("An error occurred: %s" % e)
        #else:
            #print(response1.body)

        #response1 = requests.get(url)
        #podaci1 = response1.json()

        #umesto toga
        podaci1 = tornado.escape.json_decode(response1.body)
        pprint.pprint(podaci1)


        status1 = podaci1['status']
        
        if status1=='error':
            print(status1)
            print(podaci1['code'])
            print(podaci1['message'])
        

        #print('status:', status1)
        
        self.write(json.dumps({'sent': podaci1}))

        print('dosli smo do kraja puta')

    
    #Called in async handlers if the client closed the connection.
    #Override this to clean up resources associated with long-lived connections. Note that this method is called only
    #if the connection was closed during asynchronous processing; if you need to do cleanup after every request
    #override on_finish instead.
    '''
    def on_connection_close(self):
        #nije response1, jer je to odgovor od API-ja
        #meni treba da obradim slucaj kada klijent zatvori tab
        self.response1.cancel()
    '''
    
        
        

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/', MainHandler),
                  (r'/sources', SourceHandler),
                  ],
        template_path = os.path.join(os.path.dirname(__file__),"templates"),
        static_path = os.path.join(os.path.dirname(__file__),"static"),
        debug=True
    )
    http_server=tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
