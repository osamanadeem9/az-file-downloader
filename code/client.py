import socket                   # Import socket module
import threading
import os
import sys
import time

def client(port, start, size, output_file, interval, index, global_socket):
    s = socket.socket()             # Create a socket object
    host = socket.gethostname()     # Get local machine name
    # port = 60000                    # Reserve a port for your service.

    s.connect((host, port))
    # s.send(b"Hello server!")
    # filesize = int(str(s.recv(1024).decode()))
    # print ("Filesize: "+str(filesize))
    
    with open(output_file, 'rb+') as f:
        f.seek(start)
        print("Start: "+str(f.tell()))
        # print ('file opened')
        start_time = time.time()
        total_time = time.time()
        count = 0
        count2=0
        while True:
            count = count+1024
            count2 = count2+1024
            data = s.recv(1024)

            if not data:
                break
         
            if (time.time()-start_time>=interval):
                time_passed = time.time()-start_time
                rate = count2/1000/time_passed
                print ("Server"+str(index)+": "+str(count/1000)+" / "+str(size/1000)+", download speed: "+str(rate)+"Kb/s")
                # print ("Server"+str(index)+"  Port: "+str(port)+"  Status: Alive"+"To Shutdown, Enter "+str(index)+" to pause, and then e"+str(index)+" to terminate this server. Enter r"+str(index)+" for resuming if paused")
                
                start_time = time.time()
                count2=0
           
            f.write(data)

        # print("End: "+str(f.tell()))
    f.close()

    print('Successfully got the file')
    print ("Server: ",index,"\tTotal data: ",(count-2048)/1000, "Kb\tTotal time: ",time.time()- total_time,"\tdownload speed: ",((count-2048)/1000)/(time.time()- total_time),"Kb/s")
    
    s.close()

def parseArguments():
    params = sys.argv[1 : ]
    numConn = int(params[params.index("-n") + 1])
    interval = float(params[params.index("-i") + 1])
    output_addr = str(params[params.index("-o") + 1])
    host = str(params[params.index("-a") + 1])
    
    ports = list()
    
    for i in range(0, numConn):
    	ports.append(int(params[params.index("-p") + i+1]))
        
    return host, interval, output_addr, ports

host, interval, filename, ports = parseArguments()

s = socket.socket()             # Create a socket object
# host = socket.gethostname()     # Get local machine name    
# interval = 2
# filename = "movie222.mp4"
s.bind(('', 62000))            # Bind to the port
s.listen(5)                     # Now wait for client connection.
print ('Client waiting for servers to connect....')

conn, addr = s.accept()     # Establish connection with client.
data = conn.recv(1024).decode()

f = open(filename,"wb")
filesize = int(data.split(' ')[0])
f.seek(filesize-1)
f.write(b"\0")
f.close()


print(data)

while (data!="Done"):
    
    if (data.find("Hello"))>=-1: 
        # ports = [60000,60002,60003,60004]
        # filename = "movie.mp4"
        for i, port in enumerate(ports):
            size = filesize-(filesize%(len(ports)*1024))
            size = int(size/len(ports))

            # print ("Start: "+str(i*size))
            threading.Thread(target = client,args=(port, i*size, size, filename, interval, i, conn)).start()
    data = conn.recv(1024).decode()
    print(data)
    if (data.find("Server")>-1):
        p = int(data.split(' ')[2])
        ports.remove(p)
        start = int(data.split(' ')[3])
        transferred = int(data.split(' ')[4])
        new_size = int(data.split(' ')[5])
        for i,port in enumerate(ports):
            print ("Client ",str(port)," waiting for connection again")
            threading.Thread(target = client,args=(port, start+transferred+(i*new_size), new_size, filename, interval, i, conn)).start()        

    data = "Done"
print ("\n\nFile transferred successfully!")