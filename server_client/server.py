"""
    This file takes part of the server side of the peer to peer network
    This file deals with uploading of the song for other peers
"""

from server_client.constants import *

__author__ = "Aman Nagpal"

class Server: 


    def __init__(self, msg):
        try:
            # the message to upload in bytes
            self.msg = msg

            # define a socket
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            self.connections = []

            # make a list of peers 
            self.peers = []

            # bind the socket
            self.s.bind((HOST, PORT))

            # listen for connection
            self.s.listen(1)

            print("-" * 12+ "Server Running"+ "-" *21)
            
            self.run()
        except Exception as e:
            sys.exit()



    """
    This method deals with sending info to the clients 
    This methods also closes the connection if the client has left
    :param: connection -> The connection server is connected to 
    :param: a -> (ip address, port) of the system connected
    """
    def handler(self, connection, a):
        
        try:
            while True:
                # server recieves the message
                data = connection.recv(BYTE_SIZE)
                for connection in self.connections:
    
                    # The peer that is connected wants to disconnect
                    if data and data.decode('utf-8')[0].lower() == 'q':

                        # disconnect the peer 
                        self.disconnect(connection, a)
                        return
                    elif data and data.decode('utf-8') == REQUEST_STRING:
                        print("-" * 21 + " UPLOADING " + "-" * 21)
                        # if the connection is still active we send it back the data
                        # this part deals with uploading of the file
                        connection.send(self.msg)
                        #convert_to_music(self.msg)
        except Exception as e:
            sys.exit()


    """
        This method is run when the user disconencts
    """
    def disconnect(self, connection, a):
        self.connections.remove(connection)
        self.peers.remove(a)
        connection.close()
        self.send_peers()
        print("{}, disconnected".format(a))
        print("-" * 50)



    """
        This method is use to run the server
        This method creates a different thread for each client
    """
    def run(self):
        # constantly listeen for connections
        while True:
            connection, a = self.s.accept()

            # append to the list of peers 
            self.peers.append(a)
            print("Peers are: {}".format(self.peers) )
            self.send_peers()
            # create a thread for a connection
            c_thread = threading.Thread(target=self.handler, args=(connection, a))
            c_thread.daemon = True
            c_thread.start()
            self.connections.append(connection)
            print("{}, connected".format(a))
            print("-" * 50)



    """
        send a list of peers to all the peers that are connected to the server
    """
    def send_peers(self):
        peer_list = ""
        for peer in self.peers:
            peer_list = peer_list + str(peer[0]) + ","

        for connection in self.connections:
            # we add a byte '\x11' at the begning of the our byte 
            # This way we can differentiate if we recieved a message or a a list of peers
            data = PEER_BYTE_DIFFERENTIATOR + bytes(peer_list, 'utf-8')
            connection.send(PEER_BYTE_DIFFERENTIATOR + bytes(peer_list, 'utf-8'))

