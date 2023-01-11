#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        # Request path
        request_path = self.data.decode().split(" ")[1]

        # Check which files to server
        if request_path == "/" or request_path == "/index.html":
            html_path = "./www/index.html"
        elif request_path == "/deep/index.html":
            html_path = "./www/deep/index.html"
        else:
            html_path = ""

        # Check if the file exists and send the file
        if html_path != "" and os.path.isfile(html_path):
            # Open the files
            html_file = open(html_path, "r")
            file_content = html_file.read()
            headers = "HTTP/1.1 200 OK\n"
            headers += "Content-Type: text/html; charset=utf-8\n"
            response = headers + file_content
            self.request.sendall(response.encode())
        else:
            self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r", "utf-8"))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
