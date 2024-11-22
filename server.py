import socket
from socket import *

serverPort = 5698
#define TCP server
serverSocket = socket(AF_INET, SOCK_STREAM)
#make binding with any ip address by ''
serverSocket.bind(('', serverPort))
# listen for requests
serverSocket.listen(50)
# print for the server is ready
print('Web Server is ready ...')

#opening all the files and images
#main_en.html
with open('main_en.html', 'r',encoding='utf-8') as f1:
    mainEn = f1.read()
#main_ar.html
with open('main_ar.html','r', encoding='utf-8') as f2:
    mainAr = f2.read()
#get img page
with open('supporting_material_en.html','r', encoding='utf-8') as f3:
    supporting_en = f3.read()
with open('supporting_material_ar.html','r', encoding='utf-8') as f4:
    supporting_ar = f4.read()

with open('Error.html','r', encoding='utf-8') as f13:
    Error = f13.read()

#style.css
with open('main.css','r', encoding='utf-8') as f6:
    css = f6.read()
#all the used images
with open('./images/background.png', 'rb') as f7:
    background=f7.read()
with open('./images/background2.png', 'rb') as f8:
    background2 = f8.read()
with open('./images/http.jpg', 'rb') as f9:
    http = f9.read()
with open('./images/Mohammed.png', 'rb') as f10:
    Mohammed = f10.read()
with open('./images/Mohammad.png', 'rb') as f11:
    Mohammad = f11.read()
with open('./images/Raseel.png', 'rb') as f12:
    Raseel = f12.read()
with open('countdown.mp4','rb') as f13:
    countdown = f13.read()
while True:
    #accept the connection
    connectionSocket, addr = serverSocket.accept()
    ip = addr[0]
    port = addr[1]
    print('Got connection from', "IP: " + ip + ", Port: " + str(port))
    #receve http reqeust
    sentence = connectionSocket.recv(4096).decode()
    #split the request to get the request line from user input
    match= sentence.split('\n')[0]
    print("match is: ", match)
    request = match.split(' ')[1]
    print("The Request is : "+request) # print http request intermanel
    print(sentence)

    #for any of this we handle the request depending on the url
    #for the base mian_en.gtml file :
    if(request =="/" or request =="/index.html" or request =="/main_en.html" or request =="/en"):
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
        connectionSocket.send("Content-Type: text/html; charset=utf-8\r\n".encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.send(mainEn.encode())
    #for the get img page :
    elif(request == "/ar" or request == "/main_ar.html"):
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
        connectionSocket.send("Content-Type: text/html; charset=utf-8\r\n".encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.send(mainAr.encode())

    elif(request == "/supporting_material_en.html"):
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
        connectionSocket.send("Content-Type: text/html; charset=utf-8\r\n".encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.send(supporting_en.encode())

    elif (request == "/supporting_material_ar.html"):
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
        connectionSocket.send("Content-Type: text/html; charset=utf-8\r\n".encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.send(supporting_ar.encode())

    #for the css file
    elif (request =="/main.css"):
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
        connectionSocket.send("Content-Type: text/css;\r\n".encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.send(css.encode())

    #if this statment(/request_handler?material) in the url then the user submit an img name in the html form
    elif 'request_handler?material' in request :
        var,type = request.split('=')[1], request.split('=')[2] #to get the image name alone
        object = var.split('&')[0]
        #if the requested file is image
        if (type == 'image'):
            images=['background','background2','mohammad','raseel','mohammed','http']
            images_h = [background, background2, Mohammad, Raseel, Mohammed, http]
            object = object.lower()
            if (object in images):
                connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
                for image in images:
                    if(object == image):
                        x = images.index(image)
                        if(images_h[x] != http):
                            connectionSocket.send("Content-Type: image/png;\r\n".encode())
                            connectionSocket.send("\r\n".encode())
                            connectionSocket.send(images_h[x])
                        else:
                            connectionSocket.send("Content-Type: image/jpg;\r\n".encode())
                            connectionSocket.send("\r\n".encode())
                            connectionSocket.send(images_h[x])
            else:
                connectionSocket.send("HTTP/1.1 307 Temporary Redirect\r\n".encode())
                connectionSocket.send('Content-Type: text/html; charset=utf-8\r\n'.encode())
                location = "Location:http://www.google.com/search?q="+object+"&udm=2\r\n"
                connectionSocket.send(location.encode())
                connectionSocket.send('\r\n'.encode())
                print("Redirect to google\r\n") 
        
        #if the requested file is video    
        elif (type == 'video'):
            video_name = 'countdown'
            video_file = countdown  
            object = object.lower()

            if object == video_name:
                connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
                connectionSocket.send("Content-Type: video/mp4;\r\n".encode()) 
                connectionSocket.send("\r\n".encode())
                connectionSocket.send(video_file) 
            else:
                connectionSocket.send("HTTP/1.1 307 Temporary Redirect\r\n".encode())
                connectionSocket.send('Content-Type: text/html; charset=utf-8\r\n'.encode())
                location = "Location:https://www.youtube.com/results?search_query=" + object + "\r\n"
                connectionSocket.send(location.encode())
                connectionSocket.send('\r\n'.encode())
                print("Redirect to YouTube\r\n")




        # with open(str(img1),'rb') as anyImg : # open the img
        #     img2 = anyImg.read()
        # #to check what the img type is , to send the correct http response
        # if (img1.endswith('.jpg')) :
        #     connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
        #     connectionSocket.send("Content-Type: image/jpg;\r\n".encode())
        #     connectionSocket.send("\r\n".encode())
        #     connectionSocket.send(img2)
        # else :
        #     connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
        #     connectionSocket.send("Content-Type: image/png;\r\n".encode())
        #     connectionSocket.send("\r\n".encode())
        #     connectionSocket.send(img2)

    #main_en page background img
    elif(request=="/images/background.png"):
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
        connectionSocket.send("Content-Type: image/png;\r\n".encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.send(background)
    #main_ar page background img
    elif (request =="/images/background2.png"):
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
        connectionSocket.send("Content-Type: image/png;\r\n".encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.send(background2)
    #http image in both pages
    elif (request =="/images/http.jpg"):
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
        connectionSocket.send("Content-Type: image/jpg;\r\n".encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.send(http)
    #our imgs in the both pages (en,ar)
    elif (request =="/images/Mohammed.png"):
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
        connectionSocket.send("Content-Type: image/png;\r\n".encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.send(Mohammed)
    elif (request =="/images/Raseel.png"):
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
        connectionSocket.send("Content-Type: image/png;\r\n".encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.send(Raseel)
    elif(request == "/images/Mohammad.png"):
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
        connectionSocket.send("Content-Type: image/png; charset=utf-8\r\n".encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.send(Mohammad)

    #if the client made any request that dose not exist
    else:
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
        connectionSocket.send("Content-Type: text/html; charset=utf-8\r\n".encode())
        connectionSocket.send("\r\n".encode())
        #connectionSocket.send(Error.encode())
        error = ('<!DOCTYPE html>'
                '<html lang="en">'
                '<style>'
                '*{text-align: center;padding:10px;}'
                'h1{font-size:50px;}'
                'p{font-size:20px;}'
                '</style>'
                '<head>'
                '<meta charset="UTF-8">'
                '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
                '<title>Error 404</title>'
                '</head>'
                '<body>'
                '<h1 style="color: red;">The file is not found!</h1>'
                '<p>IP Address: ' + str(ip) + ',Port Number: ' + str(port) + '</p>'
                '</body></html>'
        )
        connectionSocket.send(error.encode())
    connectionSocket.close()
