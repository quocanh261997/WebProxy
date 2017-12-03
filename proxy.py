"""
Name: Quoc Anh Nguyen, Andre Le
Class: CSE 283 - Section A
Date: 12/02/2017
Assignment: Project 2 - Net Nonny: A Web Proxy Based Service
"""

#Import necessary module for the program
import socket
import sys
import thread
import gzip
import struct

HTTP_PORT = 80
HOST = ""
port_num = int(sys.argv[1])
MAX_CONNECTIONS = 1000
BUFFER_SIZE = 16384
BAD_URL_HOST = "http://ceclnx01.eas.miamioh.edu/~gomezlin/error.html"
BAD_CONTENT_HOST = "http://ceclnx01.eas.miamioh.edu/~gomezlin/error2.html"
SUFFIXES = [".png", ".jpg", ".jpeg", ".js", ".cs", ".gif"]
BAD_KEYWORD = ["spongebob","britney spears","paris hilton"]

#The main function that runs everything
def main():
    #Socket configuration
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        server.bind((HOST,port_num))
        server.listen(MAX_CONNECTIONS)
        print "Ready to serve, listening at port ", port_num
    except socket.error, message:
        print "Failed to connect, error code: ", str(message[0]), ", Error message: ", str(message[1])
        sys.exit(1)
    #Start the thread
    while 1:
        connection, address = server.accept()
        thread.start_new_thread(serve_connection, (connection, address))
    server.close()

#Parse first line of request to get the url
def get_url(first_line):
    url = ""
    try:
        url = first_line.split(" ")[1]
    except IndexError:
        print "IndexError in line: ", first_line
    finally:
        return url

#Parse the url to a web server
#Ex: "http://www.google.com/index.html" => "www.google.com"
def url_to_web_server(url):
    http_pos = url.find("://")
    if http_pos == -1:
        temp = url
    else:
        temp = url[(http_pos+3):]
    web_server_pos = temp.find("/")
    if web_server_pos == -1:
        web_server_pos = len(temp)
    return temp[:web_server_pos].split(":")[0]

#Check if file content suffixes that isn't going to be inspected
def check_for_content(url):
    if any (url.endswith(suffix) for suffix in SUFFIXES):
        return False
    return True

#Return if the line contains any keyword
def contains_keywords(line, keywords):
    keywords.append("badtest")
    for seq in keywords:
        if len(seq.split(" "))>1:
            if all(s in line.lower() for s in seq.split(" ")):
                return True
    if any (s in line.lower() for s in keywords):
        return True
    keywords.remove("badtest")
    return False

#Print the info the request to the console
def print_info(type, request, address):
    print address[0], "\t", type.upper(), "\t", request

#Redirect the user back to a webpage
def redirect_response(url):
    return "HTTP/1.1 302 Found\r\nLocation: " + url + "\r\nHost: " + url_to_web_server(url) + "\r\nConnection: close\r\n\r\n"

#Establish the connection
def serve_connection(connection, address):
    #Receive a request from the user
    data = connection.recv(BUFFER_SIZE)
    first_line = data.split("\n")[0]
    url = get_url(first_line)
    web_server = url_to_web_server(url)
    badUrl = False

    #Serve "GET" request only
    if "GET" in first_line:
        print_info("request", first_line, address)
        badUrl = contains_keywords(url, BAD_KEYWORD)
        #Check if the url contains block keywords
        if badUrl:
            print_info("blacklisted", url, address)

    content_check_needed = check_for_content(url)
    try:
        served_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        served_socket.connect((web_server,HTTP_PORT))
        #If the url contains bad keyword(s), shut down the connection and
        #redirect the users to the error webpage
        if badUrl:
            served_socket.shutdown(socket.SHUT_RDWR)
            connection.shutdown(socket.SHUT_RD)
            connection.send(redirect_response(BAD_URL_HOST))
        else:
            served_socket.send(data)
            badContent = False
            while 1:
                new_chunk = served_socket.recv(BUFFER_SIZE)
                if len(new_chunk)>0:
                    if content_check_needed:
                        for line in new_chunk.split("\n"):
                            badContent = contains_keywords(line, BAD_KEYWORD)
                            if badContent:
                                print_info("bad content",url, address)
                                break
                    #If the content contains bad keywords, redirect the users
                    if badContent:
                        served_socket.shutdown(socket.SHUT_RDWR)
                        connection.shutdown(socket.SHUT_RD)
                        connection.send(redirect_response(BAD_CONTENT_HOST))
                    else:
                        connection.send(new_chunk)
                else:
                    break
        served_socket.close()
    except socket.error, (value, message):
        print_info("peer reset", first_line, address)
    finally:
        connection.close()
        print "\t> Connection closed. Thread exiting..."
        thread.exit()

#Run the main function
if __name__ == "__main__":
    try:
        print "Forbidden keywords:", BAD_KEYWORD
        main()
    except KeyboardInterrupt:
        print "Stopping server..."
        sys.exit(1)
