# File downloader over local servers

This is a project for my Computer Networks class. The task to build a file downloader which downloads a large size from multiple servers at the same time, and each server possesses a separate copy of that file. All the servers then simultaneously send their due portion of the file to the client.

Major concepts used are: multi-threading, socket programming, file handling and segmentation etc
## Working steps:

Following is the sequence of steps on which the file downloader is made:
  *	The client sends the request to download file, from specific number of file servers
  *	The request is accepted by all the servers, and file metadata (like file size) is shared with the client.
  *	Load balancing takes place, and each server starts sharing equal portion of the file with client simultaneously.
  *	Any server can be paused, and resumed during the file transfer process. The file transfer will stay paused unless the server is resumed.
  *	If a server (6000) is aborted / fails during file transmission, its parameters are shared with other servers (6002, 6003, 6004). And when they finish downloading their individual parts, the remaining data from the failed server (6000) is divided equally and is transmitted over the other servers.
  *	The client and server connections terminate after the file is completely transferred.

## How to use:

Firstly we have to initiate the client request. In Windows, open command prompt and enter the following command

```
python client.py -i 1 -o oned_copy.mp4 -n 4 -a 127.0.0.1 -p 60000 60002 60003 60004

where
    i = interval for displaying results (like amount of data downloaded from each server, average download speed)
    o = name of the output file
    n = number of virtual servers
    a = IP address of the server (file is sent to a different location on same computer, so IP is same. Can be different local IP)
    p = port numbers on which server connection is going to be established (or server IPs)
```

After that, run the server file to start the socket connection

```
python server.py -i 1 -f oned.mp4 -n 4 -a 127.0.0.1 -p 60000 60002 60003 60004

where
    i = interval for displaying results (like status of each server whether it's alive or dead)
    f = name of the input file
    n = number of virtual servers
    a = IP address of the client
    p = port numbers on which server connection is going to be established (or server IPs)
```

## Important Points:
  *	To pause the server anytime during file transmission, enter server index on the server side. For example, enter “1” to pause Server1
  *	To resume the paused server, enter “r”+server index. For example, enter ”r1” to resume Server1
  *	To abort a server, first pause the server (by entering server index) and then “e”+server index to terminate the server.

## Features Implemented:

A short detail of the implementation process of the main features is given below:

  * **Server-Client implementation:**<br/>
      TCP is used for this process, and is done using sockets. Server listens to client connections, and the client connection is established.
      
  *	**Implementation of multiple servers:**<br/>
      This is done through multi-threading. Loop is used to initialize the thread over a number of ports.
      
  *	**Handling server failure and load balancing:**<br/>
      Whenever a server is aborted, the server stops transmission from that server and stores and transmits the information of remaining data to all the other servers. That data is divided equally among those servers and completed file is transferred to the client.

## How it works:

### Simple Transfer:
The following shows a successful transfer between server and client (no server failure)

#### server.py:
![output](/output/simple_transfer%20(server%20side).JPG)
<br/>
#### client.py:
![output](/output/simple_transfer%20(client%20side).JPG)
