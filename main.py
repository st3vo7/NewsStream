import os.path
import requests
import json
import pprint


import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.escape


url1 = ( 'https://newsapi.org/v2/top-headlines?'
        'country=rs&'
        #'category=technology&'
        #'q=bomba&'
        'apiKey=17060bbc869845deb9246555cd6f8e5d')


url3 = ( 'https://newsapi.org/v2/sources?'
        #'language=en&'
        'country=gb&'
        #'category=technology&'
        #'q=manchester city&'
        'apiKey=17060bbc869845deb9246555cd6f8e5d')


from tornado.options import define, options
define("port",default=8000, help="run on the given port", type=int)

class SourceHandler(tornado.web.RequestHandler):
    def get(self):

        '''
        print('u getu sam')
        
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
        
        '''

        
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
        
        '''
        items3 = podaci3['sources']
        for index in range(len(items3)):
            for key in items3[index]:
                if key == 'name':
                    izvori1.append(items3[index][key] + ' - ' + items3[index]['description'])
        

        
        self.render("sources.html",
                    izvori1=izvori1
                    )
        '''

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

        '''
        upit = self.request.body.decode("utf-8")
        print('+++'*20)
        print(upit)
        print('+++'*20)
        
        
        argumenti = self.request.arguments
        print(argumenti)
        print('---'*20)
        drzava_val = argumenti['country'][0].decode("utf-8") 
        kategorija_val =  argumenti['kategorija'][0].decode("utf-8")

        primljen = {
            'country1': drzava_val,
            'kategorija': kategorija_val
        }
        '''


        a=dic_data['country']
        b=dic_data['category']
        

        '''
        a=self.get_argument("drzava", None)
        b=self.get_argument("kategorija",None)
        print(a)
        print(b)
        '''
        
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
        
        '''
        items1 = podaci1['articles']
        for index in range(len(items1)):
            for key in items1[index]:
                if key == 'title':
                    naslovi1.append(items1[index][key])

        #umesto da renderujem celu stranu, vraticu ajaxu podatke, i on ce da mi izgenerise naslove
        self.write(json.dumps({'status': status1, 'sent': naslovi1}))
        '''

        self.write(json.dumps({'sent': podaci1}))



        '''
        #stari nacin, pre ajaksa
        self.render("index.html",
                    naslovi1=naslovi1,
                    zemlja = a,
                    kat = b,
                    )
        '''

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
