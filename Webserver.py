from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
import cgi
import threading

PORT_NUMBER = 8080

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass

# This class will handles any incoming request from
# the browser
class myHandler(BaseHTTPRequestHandler):

    # Handler for the GET requests
    def do_GET(self):
        if self.path == "/": #did not define any page
            self.path="/HTMLFile.html" #set default

        try:
            # Check the file extension required and
            # set the right mime type

            sendReply = False
            if self.path.endswith(".html"):
                mimetype = 'text/html'
                sendReply = True
            if self.path.endswith(".jpg"):
                mimetype = 'image/jpg'
                sendReply = True
            if self.path.endswith(".gif"):
                mimetype = 'image/gif'
                sendReply = True
            if self.path.endswith(".js"):
                mimetype = 'application/javascript'
            if self.path.endswith(".css"):
                mimetype = 'text/css'
                sendReply = True

            if sendReply == True: #we defined the page
                #Saving Log Info
                logfile = open("logfile.txt", "a")
                IP = self.client_address[0]
                URLname= self.server.server_name
                URLport=str(self.server.server_port)
                URLpath=self.path
                address_ =''.join([URLname,':',URLport,'/',URLpath])
                # dateANDtime = self.log_date_time_string()
                dateANDtime = self.date_time_string(timestamp=None)
                logfile.write(" '%s' , '%s' ,[%s] \n" % (IP, address_, dateANDtime))
                logfile.close()
                f = open(curdir + sep + self.path) #seprator : text processing ==> cuurent directory
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(f.read().encode()) # send answer to client
                f.close()
            return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    # Handler for the POST requests
    def do_POST(self):
        if self.path == "/send":
            form = cgi.FieldStorage( #read form
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': self.headers['Content-Type'],
                         })

            print("Your name is: %s" % form["your_name"].value)
            print("Your family is: %s" % form["your_family"].value)
            self.send_response(200)
            self.end_headers()
            self.wfile.write("Thanks %s !" % form["your_name"].value)
            self.wfile.write("Thanks %s !" % form["your_family"].value)
            return



if __name__ == '__main__':
    try:
        # Create a web server and define the handler to manage the
        # incoming request
        server = ThreadingHTTPServer(('', PORT_NUMBER), myHandler)
        print('Started httpserver on port ', PORT_NUMBER)

        # Wait forever for incoming htto requests
        server.serve_forever()

    except KeyboardInterrupt:
        print('^C received, shutting down the web server')
        server.socket.close()
