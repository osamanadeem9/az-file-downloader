import socket                   # Import socket module
import os
import threading
import time
import keyboard
import sys

def server(ports, port, filename, start, size, interval, index, global_socket):
    # num_ports = len(ports)
    index = index+1
    s = socket.socket()             # Create a socket object
    # host = socket.gethostname()     # Get local machine name
    
    s.bind(('', port))            # Bind to the port
    s.listen(5)                     # Now wait for client connection.

    # print ('Server listening....')
    conn, addr = s.accept()     # Establish connection with client.
    # conn.send(str(size).encode())
    while True:
        # count = 1024
        # print ('Got connection from', addr)
        f = open(filename,'rb')
        f.seek(start)
        print("Start",index,": "+str(start)+" "+ str(f.tell()))
        l = f.read(1024)
    
        count = 0
        count2=0
        transferred = 0
        start_time = time.time()
        total_time = time.time()
        while (l):
            count = count+1024
            count2+=1024
            transferred=transferred+1024
            conn.send(l)
            l = f.read(1024)
            
            if (time.time()-start_time>=interval):
                time_passed = time.time()-start_time
                rate = count2/1000/time_passed
                # print ("Server"+str(index)+"\tStatus: Available\tData received: "+str(count2/1000)+"    Download speed: "+str(rate)+"Kb/s\t Enter "+str(index)+" to pause, r"+str(index)+" to resume, and e"+str(index)+" to terminate this server")
                print ("Server"+str(index)+"  Port: "+str(port)+"  Status: Alive"+"\tTo Shutdown, Enter "+str(index)+" to pause, and then e"+str(index)+" to terminate this server. Enter r"+str(index)+" for resuming if paused")
                
                start_time = time.time()
                count2=0
            
            if (count>=size):
                break
            
            # print("Index",index," ",count/1000)
            if (keyboard.is_pressed(str(index))):
                print("Server"+ str(index)+ "\tStatus: Paused \t Enter r"+str(index)+" anytime to resume")
                inp = input()            

                if(inp=="r"+str(index)):
                    print("Server"+str(index)+ " resumed\n")
                
                elif(inp=="e"+str(index)):
                    print ("Server"+str(index)+"  Port: "+str(port)+"  Status: Dead"+"\tTo Shutdown, Enter "+str(index)+" to pause, and then e"+str(index)+" to terminate this server. Enter r"+str(index)+" for resuming if paused")

                    print("Server",index, " aborted\n")
                    # ports=[60004,60005,60006]
                    ports.remove(port)
                    status = "Server"+str(index)+" paused"+" "+str(port)+" "+str(start)+" "+str(transferred)+" "+str(int(((size-transferred)-(size-transferred)%(len(ports)*1024))/len(ports)))
                    global_socket.send(str.encode(status))

                    conn.close()
                    for i,port in enumerate(ports):
                        new_file = filename[:-5]+str(i)+filename[-4:]
                        if new_file not in os.listdir('.'):
                            shutil.copyfile(filename, new_file)
                        
                        new_size = (size-transferred)-(size-transferred)%(len(ports)*1024)
                        new_size = int(new_size/len(ports))
                        
                        print("\nAvailable Servers: ",ports)
                        # print("Total: ",size," Transferred: ",transferred," Remaining: ",new_size*len(ports))
                        print("Distribtuting data equally among the available servers: ")
                        # print("Ranges: ",start+transferred+(i*new_size), new_size)
                        while True:
                            try:
                                print ("Server"+str(index)+"  Port: "+str(port)+"  Status: Dead"+"\tTo Shutdown, Enter "+str(index)+" to pause, and then e"+str(index)+" to terminate this server. Enter r"+str(index)+" for resuming if paused")
                                print("On Server ", port, ", data of ",new_size, " being transferred")
                                threading.Thread(target = server, args = (ports, port, new_file, start+transferred+(i*new_size), new_size, interval, i, global_socket)).start()
                                
                                break
                            except:
                                time.sleep(interval)
                                # print("Inside while loop")               
                    exit()
        print ("\nEnd",index,": "+str(f.tell()-1024)+" Transferred: ",str(transferred))
        f.close()
        print ("Server: ",index,"\tTotal data: ",count/1000, "\tTotal time: ",time.time()- total_time)
        print('\nDone sending')

        conn.close() 
        break


def parseArguments():
    params = sys.argv[1 : ]
    numConn = int(params[params.index("-n") + 1])
    interval = float(params[params.index("-i") + 1])
    input_addr = str(params[params.index("-f") + 1])
    host = str(params[params.index("-a") + 1])
    
    ports = list()
    
    for i in range(0, numConn):
    	ports.append(int(params[params.index("-p") + i+1]))
        
    return host, interval, input_addr, ports




host, interval, filename, ports = parseArguments()

s = socket.socket()             # Create a socket object
# host = socket.gethostname()     # Get local machine name
print(host)
# filename = "oned.mp4"
# interval = 2

s.connect((host, 62000))
s.send((str(os.path.getsize(filename))+' Hello client, connected on 62000').encode())

# ports = [60000, 60002,60003,60004]
import shutil
for i,port in enumerate(ports):
    new_file = filename[:-4]+str(i)+filename[-4:]
    if new_file not in os.listdir('.'):
        shutil.copyfile(filename, new_file)
    size = os.path.getsize(new_file)-os.path.getsize(new_file)%(len(ports)*1024)
    size = int(size/len(ports))

    # print ("Ranges: "+ str(i*size) +" to "+ str((i+1)*size))
    threading.Thread(target = server, args = (ports, port, new_file, i*size, size, interval, i, s)).start()


 
