import sys
from socket import *
import threading
import os
from os import listdir
from os.path import isfile, join
import mimetypes

print sys.version

hostName = 'localhost'
print(hostName)
portNo = int(sys.argv[1])   # sys.argv[0] is the program name
uploadDirectory = "Upload/"
filename = "index.html"
fN = ""
httpversion = ""

# separate thread for each client
class ClientHandler(threading.Thread):
    def __init__(self, clientsocket):
        threading.Thread.__init__(self)
        self.clientsocket = clientsocket
        print(self.name)
        print(self.clientsocket)

    def run(self):
        service(self.clientsocket)

def service(clientsocket):
    # read the http request
    request = clientsocket.recv(1024)  # returns bytes
    request = request.decode()  # decode to string
    # request = str(request).rstrip('\r\n')
    print("Http request: " + request)

    count = 0
    wholeRequest = request
    headers = []
    requestIndex = 0
    for index in range(0, len(wholeRequest)):
        if wholeRequest[index] == '\r' and wholeRequest[index + 1] == '\n':
            if count == 0:  # first line
                request = wholeRequest[0:index]
                print(request)
                count += 1
                requestIndex = index + 2
            else:  # other headers
                headers.append(wholeRequest[requestIndex:index])
                requestIndex = index + 2

    # print(headers)
    # Ensure well-formed request (return error otherwise)
    # Assuming first line of request in form of - GET / or GET /index.html or GET / HTTP/1.0 or GET /index.html HTTP/1.0
    isMalformedRequest = False
    requestSeparated = request.split(' ')
    # print(requestSeparated)
    if requestSeparated[0] != 'GET':
        isMalformedRequest = True
        # break

    if requestSeparated[1].startswith('/'):
        # Assuming only files exist in Upload directory, no directories are requested
        filename = requestSeparated[1].lstrip('/')
        if filename == '':
            filename = 'index.html'
        if len(requestSeparated) >= 3:
            if requestSeparated[2] == 'HTTP/1.0' or requestSeparated[2] == 'HTTP/1.1':
                httpversion = requestSeparated[2]
                isMalformedRequest = False
            else:
                isMalformedRequest = True
                # break
    else:
        isMalformedRequest = True
        # break

    if isMalformedRequest:
        print('Bad')
        BadRequest = "HTTP/1.0 400 Bad Request\r\n" + "Content-type: text/html\r\n" + "Content-length: 0\r\n\r\n" + \
                     "<html><head></head><body>" + "<h1>400 BAD REQUEST</h1>" + \
                     " request messsage not understood by server</body></html>\n"
        clientsocket.send(BadRequest)
        clientsocket.close()
    else:
        print(filename)

        # LOOK FOR the file in the Upload Directory - /Users/Salvi/Documents/Upload
        # print(os.getcwd())  # current directory
            # os.chdir(uploadDirectory)  # change directory
        fN = filename
        filename = uploadDirectory + filename
        # print(os.getcwd())  # current directory after change

        # onlyfiles = [f for f in listdir(uploadDirectory) if isfile(join(uploadDirectory, f))]
        # print(onlyfiles)

        if os.path.isfile(filename):
            # print("found")
            # Check for read access to foo.txt
            if os.access(filename, os.R_OK) == False:
                permissionDeniedMsg = "HTTP/1.0 403 Forbidden\r\n" + "Content-type: text/html\r\n" + \
                                      "Content-length: 0\r\n\r\n" + "<html><head></head><body>" + \
                                      "<h1>403 Permission Denied</h1></body></html>\n"
                clientsocket.send(permissionDeniedMsg)
                clientsocket.close()

            else:
                # Determine the MIME type and print HTTP header
                mimeType = "text/plain"
                if filename.endswith(".html") or filename.endswith(".htm"):
                    mimeType = "text/html"
                elif filename.endswith(".jpg") or filename.endswith(".jpeg"):
                    mimeType = "image/jpeg"
                elif filename.endswith(".gif"):
                    mimeType = "image/gif"
                elif filename.endswith(".class"):
                    mimeType = "application/octet-stream"

                mimeType, enc = mimetypes.guess_type(filename)
                if mimeType == "text/html" or mimeType == "text/plain":
                    f = open(filename, 'r')
                    size = os.path.getsize(filename)
                    content = "HTTP/1.0 200 OK\r\n" + "Content-type: " + mimeType + "\r\n" + \
                              "Content-length: " + str(size) + "\r\n\r\n"
                    clientsocket.send(content)
                    content = f.read()  # optional parameter for read is size, otherwise entire file
                    clientsocket.send(content)
                else:
                    f = open(filename, 'r')
                    print("Sending Image")
                    size = os.path.getsize(filename)
                    content = "HTTP/1.0 200 OK\r\n" + "Content-type: " + mimeType + "\r\n" + \
                              "Content-length: " + str(size) + "\r\n\r\n"
                    clientsocket.send(content)
                    imageRead = f.read()
                    imageContent = bytearray(imageRead)
                    clientsocket.send(imageContent)

                    print("Done Sending")
                    clientsocket.send('\r\n\r\n')
                clientsocket.close()

        else:
            print("not found")
            FileNotFoundMsg = "HTTP/1.0 404 Not Found\r\n" + "Content-type: text/html\r\n" + \
                              "Content-length: 0\r\n\r\n" + "<html><head></head><body>" + "<h1>404 NOT FOUND</h1>" + \
                              fN + \
                              " not found</body></html>\n"
            clientsocket.send(FileNotFoundMsg)
            clientsocket.close()



# create an INET, STREAMing socket
serversocket = socket(AF_INET, SOCK_STREAM)
serversocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

# bind the socket to a public host, and a well-known port
serversocket.bind((hostName, portNo))  # Permission denied with port 80, change port no with argv

# become a server socket
# queue up as many as 5 connect requests (the normal max) before refusing outside connections
serversocket.listen(5)

print(serversocket)

while True:
    # accept connections from outside
    (cs, address) = serversocket.accept()
    print cs, address
    thread1 = ClientHandler(cs)
    thread1.start()

    # thread1.join()

    # Why Google chrome sends two request, 2nd one being empty
    # http://stackoverflow.com/questions/4761913/
    # server-socket-receives-2-http-requests-when-i-send-from-chrome-and-receives-one