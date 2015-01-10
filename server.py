import SocketServer
import os.path

# coding: utf-8

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
#           2014 Konrad Lindenbach, Ben Dubois
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright c 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):

    def get200Header(self, fileRequested, fileStr):
        header = "HTTP/1.1 200 OK\n" + \
                 "Date: Mon, 21 Jan 2008 18:06:16 GMT\n" + \
                 "Content-Type: text/%s\n" % \
                 ( "css" if fileRequested.endswith(".css") else "html") + \
                 "Content-Length: %d\n\n" % len(fileStr)

        return header

    def get404Header(self):
        header = "HTTP/1.1 404 Not Found\n" + \
                "Date: Mon, 21 Jan 2008 18:06:16 GMT\n" + \
                "Content-Type: text/html\n" + \
                "Content-Length: 117\n\n" + \
                "<html><body>\n" + \
                "<h2>Document not found</h2>\n" + \
                "You asked for a document that doesn't exist. " + \
                "That is so sad.\n" + \
                "</body></html>\n"

        return header

    def pathIsValid(self, path):
        if "/../" in  path or path.startswith("../") or path.endswith("/.."):
            return False

        return  os.path.isfile(path)
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        fileRequested = "./www" + self.data.split()[1]

        if fileRequested.endswith("/"):
            fileRequested += "index.html"

        response = ""
        if self.pathIsValid(fileRequested):
            fileStr = open(fileRequested, "r").read()
            header = self.get200Header(fileRequested, fileStr)
            response = header + fileStr
        else:
            response = self.get404Header()

        self.request.sendall(response)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
