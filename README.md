--------------------------------server.py-----------------------
Assumptions:
------------
1. First line is the "Http Request" Line, latter ones are the "Headers"

2. "Http Request" can be of any of the following four verisons -
	a. GET / 
	b. GET /index.html 
	c. GET / HTTP/1.0		OR		GET / HTTP/1.1  
	D. GET /index.html HTTP/1.0		OR		GET /index.html HTTP/1.1

3. Request "Headers" are parsed, but they are not used in anyway

4. Assuming only files exist in Upload directory, so only files are requested, no directories are requested

5. HTTP 1.0 is supported according to the requirement, but if server receives HTTP 1.1 request, it serves too

------------

5. Errors Handled - 
	400 - 	Bad Request
	403	-	Forbidden
	404 - 	Not Found
   
   Others
	200 -	OK

6. Types of file which are handled and tested -
	a. *.txt
	b. *.html
	C. *.jpg
	d. *.jpeg
	e. *.htm
	f. *.pdf
	g. *.gif

7. Works smoothly with Mozilla Firefox, Google Chrome

8. Command line arguments - Port No

9. To run, from terminal - 
		python socket.py portno


--------------------------------client.py-----------------------
1. Command line arguments - 
	a. HostName
	b. PortNo
	c. FileName (optional, default is 'index.html')	[Has to be the "exact same name and extension" as saved in server's \Download folder, otherwise file not found error is thrown]

2. To run, from terminal - 
		python client.py hostname portno filename

Assumptions:
------------

3. Using the filename, custom request are created of the form - 
		GET /index.html 
	
4. Files are saved in \Download folder

5. Response headers include - 
	|
	|-- Response Code
	|
	|-- Content-Type
	|
	|-- Content-Length	

6. Client side only saves file if it is a 200 OK response

7. If it is anything else other 200, only the 'html code' is printed with the error code


----------------------------Hierarchy---------------------
Assignment
	|----README
	|----Upload
	|----client.py
	|----Download
	|----server.py

----------------Python Version: 2.7.10 -------------------










