"""

PROGRAMMED BY           : AHMAD ALFI ADZ-DZIKRI
DATE PRGORAMMED         : BANDUNG, MARCH 26 2019
PURPOSE                 : (FINAL PROJECT) CLOUD DEEP LEARNING BASED EXPERIMENT

"""
import socket
import sys
import io
import shutil
import os

class socketServer(object):
    """

    port
    choose a port to be open (remember! , if you configured a firewall..open the port you choose first!)

    root_dir
    path for placeholder to store an incoming file from client


    """

    def __init__(self, port, root_dir=None):
        # self.__host = '0.0.0.0'
        self.__host = '127.0.0.1'
        self.__port = port
        self.__sizeFile = 0
        self.__root_dir = root_dir

        self.__inference = False
        self.__doTrain = False

    """
    disconnectServer()

    this method will close connection and shutdown the socket
    """
    def disconnectServer(self):
        self.__koneksiClient.shutdown(socket.SHUT_RDWR)
        self.__koneksiClient.close()

    """
    doInference()

    This will receive wav file for inference
    and will do an inference with deep learning classification
    """

    def doInference(self):
        # import toolset Deep Learning Class
        filename = "/home/ahmadalfi/Training/python/socket-programming/server/inference/halo.txt"
        self.recvFile()
        self.sendFile(filename)

    """
    sendFile()

    this method is an utility to send deep learning result
    """
    def sendFile(self, filename):
        # step 1 mengirim instruksi agar 'siap-siap'
        self.__koneksiClient.sendall(str('want2send').encode())
        # step 2 mendapat permintaan mengetahui filesize
        response = self.__koneksiClient.recv(1024).decode()
        if response == 'sizeFirst':
            # step 3 mengirim ukuran file
            dataSize = str(os.path.getsize(filename))
            self.__koneksiClient.send(dataSize.encode())
            response = self.__koneksiClient.recv(1024).decode()
            if response == 'ready':
                with open(filename, 'rb') as berkas:
                    self.__koneksiClient.sendfile(berkas, 0)
                berkas.close()
                self.__koneksiClient.shutdown(socket.SHUT_WR)
        else:
            print("Invalid response")

    """
    doTrain()

    After receive file, this routine will takes to another classes
    to begin deep learning model training

    """
    def doTrain(self):
        self.recvFile()
        print("Do Train")
        # import toolset Deep Learning Class here

    """
    recvFile()

    this method will receive file from client
    """
    def recvFile(self):
        # send command back to say 'we ready'
        buffer = 'ready'
        self.__koneksiClient.send(buffer.encode())
        # wait response again
        response = self.__koneksiClient.recv(1024).decode()
        # receive file
        if response == "ok":
            saya_siap = 'do_it'
            self.__koneksiClient.send(saya_siap.encode())
            command = 'whereisfile'

            self.__sizeFile = int(
                self.__koneksiClient.recv(1024).decode()
            )
            self.__koneksiClient.send(str('whatname').encode())

            namafile = self.__koneksiClient.recv(1024).decode()

            self.__nameFile = os.path.join(self.__root_dir, namafile)
            self.__koneksiClient.send(command.encode())

            print("Menerima data")

            with open(self.__nameFile, 'wb') as file:
                while True:
                    berkas = self.__koneksiClient.recv(self.__sizeFile)
                    if not berkas:
                        break
                    file.write(berkas)
                file.close()

            if self.__doTrain and not self.__inference:
                self.UnzipDataset()
            elif self.__inference and not self.__doTrain:
                print("inference")

    """
    UnzipDataset()

    this method is an utility to extract archive file
    """
    def UnzipDataset(self):

        shutil.unpack_archive(self.__nameFile, self.__root_dir)
        os.remove(self.__nameFile)

    """""
    beginSocketComm()

    begin socket communication,
    the role play of this method is listen to incoming file"""""

    def beginSocketComm(self):
        port = self.__port
        # initialize instace of socket server
        self.__server_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)

        # reference:
        # https://stackoverflow.com/questions/44387712/python-sockets-how-to-shut-down-the-server
        self.__server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.__server_socket.bind((self.__host, port))

        """
            jumlah client (untuk kasus Proyek Akhir,jumlah client 1 aja..
            bisa bangkrut gue nyewa cloud nya -_-")
        """
        self.__server_socket.listen(1)
        print("Begin Listening...")
        while True:

            self.__koneksiClient, identity = self.__server_socket.accept()
            self.__ipclient, self.__socketclient = identity
            print("Koneksi Masuk, dari : ", str(
                self.__ipclient), str(self.__socketclient)
            )
            command = self.__koneksiClient.recv(1024).decode()

            if command == "do_train":
                print("Data masuk : " + str(command))
                self.__inference = False
                self.__doTrain = True

                self.doTrain()

            elif command == "inference":
                print("Data masuk : " + str(command))
                self.__inference = True
                self.__doTrain = False
                self.doInference()

            if not command:
                print("This is not Data!!!")
                self.__koneksiClient.shutdown(socket.SHUT_RD)


# dir = "/home/ahmadalfi/Training/python/socket-programming/server/"
# ojek = socketServer(7000, root_dir=dir)
# ojek.beginSocketComm()
