import socket
import sys
import io
import shutil
import os

"""script untuk server-side"""


class socket_backend(object):
    """docstring for socket_backend."""

    def __init__(self, port, root_dir=None):
        # self.__host = '0.0.0.0'
        self.__host = '127.0.0.1'
        self.__port = port
        self.__sizeFile = 0
        self.__root_dir = root_dir
        self.__nameFile = os.path.join(root_dir, 'dataSet.zip')

    def disconnect(self):
        self.__koneksiClient.close()

    def checksumDat(self, arg):
        pass

    """This will send inference file from deep learning classification"""

    def doInference(self, arg):
        # import toolset Deep Learning Class
        pass

    def sendFile(self, arg):
        self.__koneksiClient.send(str('want2send').encode)

    def doTrain(self):
        # import toolset Deep Learning Class
        pass

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

            self.__koneksiClient.send(command.encode())
            print("Menerima data")

            with open(self.__nameFile, 'wb') as file:
                while True:
                    berkas = self.__koneksiClient.recv(self.__sizeFile)
                    if not berkas:
                        break
                    file.write(berkas)
                file.close()

            self.__koneksiClient.shutdown(socket.SHUT_RD)
            self.UnzipDataset()
            print("Data Sudah terekstrak")

    def UnzipDataset(self):

        shutil.unpack_archive(self.__nameFile, self.__root_dir)
        os.remove(self.__nameFile)

    """""begin socket communication,the role play of this method is listen to incoming file"""""

    def beginSocketComm(self):
        port = self.__port
        # initialize instace of socket server
        self.__server_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.__server_socket.bind((self.__host, port))

        """
            jumlah client (untuk kasus Proyek Akhir,jumlah client 1 aja..
            bisa bangkrut gue nyewa cloud nya -_-")
        """
        self.__server_socket.listen(1)
        print("Begin Listening...")
        while True:

            self.__koneksiClient, identity = self.__server_socket.accept()
            self.__ipclient,self.__socketclient=identity
            print("Koneksi Masuk, dari : ", str(
                self.__ipclient), str(self.__socketclient)
            )
            command = self.__koneksiClient.recv(1024).decode()

            if command == "do_train":
                print("Data masuk : " + str(command))
                self.recvFile()

                self.doTrain()

            elif command == "inference":
                print("Data masuk : " + str(command))
                self.recvFile(self.__koneksiClient)

                self.doInference()

            if not command:
                print("This is not Data!!!")
                self.__koneksiClient.shutdown(socket.SHUT_RD)


dir = "/home/ahmadalfi/Training/python/socket-programming/server"
ojek = socket_backend(7000, root_dir=dir)
ojek.beginSocketComm()
