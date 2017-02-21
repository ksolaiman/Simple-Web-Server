import sys
from socket import *
import io

serverName = sys.argv[1]
serverPort = int(sys.argv[2])
downloadFolder = "Download/"
try:
    fN = sys.argv[3]
except IndexError:
    fN = "index.html"

# create an INET, STREAMing socket
sc = socket(AF_INET, SOCK_STREAM)
# now connect to the web server on port 80
sc.connect((serverName, serverPort))
# request = input()
request = "GET /" + fN + "\r\n"
noOfByteSent = sc.send(request)   # returns the number of bytes sent


# Receive the header informations
readReply = sc.recv(1024)
content = readReply
print(content)


# parse the data / header
content = str(content).split('\r\n')
firstLine = content[0].split(' ')
secondLine = content[1].split(' ')
responseCode = firstLine[1]
contentTypeSplit = secondLine[1].split('/')
contentType = contentTypeSplit[0]
contentExtension = contentTypeSplit[1]
if (responseCode == "200"):
    if contentType.startswith('image'):
        imageContent = bytes()
        content = sc.recv(1024)
        imageContent += content
        while content:
            content = sc.recv(1024)
            imageContent += content

        filename = downloadFolder + str(fN)
        f = open(filename, 'w')
        f.write(imageContent)
        f.close()

        print ("File Saved as " + str(fN))


    elif contentType.startswith('text'):
        content = sc.recv(1024)
        txtContent = content
        while content:
            content = sc.recv(1024)
            txtContent += content

        if contentExtension == "plain":
            contentExtension = "txt"

        filename = downloadFolder + str(fN)
        f = open(filename, 'w')
        f.write(txtContent)
        f.close()

        print ("File Saved as " + str(fN))

    else:
        content = sc.recv(1024)
        txtContent = content
        while content:
            content = sc.recv(1024)
            txtContent += content

        if contentExtension == "plain":
            contentExtension = "txt"

        filename = downloadFolder + str(fN)
        f = open(filename, 'w')
        f.write(txtContent)
        f.close()

        print ("File Saved as " + str(fN))