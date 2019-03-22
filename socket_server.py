import socket
import sys
from zipfile import ZipFile
import zipfile
import io
"""script untuk server-side"""


class socket_backend(object):
    """docstring for socket_backend."""

    def __init__(self, port):
        # self.__host = '0.0.0.0'
        self.__host = '127.0.0.1'
        self.__port = port
        self.__sizeFile = 0

    """This will send inference file from deep learning classification"""

    def checksumDat(self, arg):
        pass

    """This will send inference file from deep learning classification"""

    def sendFile(self, arg):
        pass

    def recvFile(self):
        # self.__koneksiClient.
        # self.__sizeFile = int(data)
        pass

    def UnzipDataset(self):
        source_filename = '/home/ahmadalfi/Training/python/socket-programming/server/dataset.zip'
        dest = '/home/ahmadalfi/Training/python/socket-programming/server/'
        if zipfile.is_zipfile(source_filename):
            print('Extracting..')
            with ZipFile(source_filename) as zf:
                zf.extractall(dest)
                # zf.read()
                zf.close()

    """""begin socket communication,the role play of this method is listen to incoming file"""""

    def beginSocketComm(self):
        port = self.__port
        # initialize instace of socket server
        self.__server_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.__server_socket.bind((self.__host, port))
        Format_file = "dataSuara.zip"

        """
            jumlah client (untuk kasus Proyek Akhir,jumlah client 1 aja..
            bisa bangkrut gue nyewa cloud nya -_-")
        """
        self.__server_socket.listen(1)
        print("Begin Listening...")
        while True:

            koneksi_client, ipaddress = self.__server_socket.accept()
            self.__koneksiClient = koneksi_client
            print("Koneksi Masuk, dari : ", str(
                ipaddress[0]), str(ipaddress[1]))
            self.__ipClient = ipaddress
            command = koneksi_client.recv(1024).decode()
            if command == "send_file":
                print("Data masuk : " + str(command))
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
                        self.__koneksiClient.recv(1024).decode())
                    self.__koneksiClient.send(command.encode())
                    print("Menerima data")
                    self.__path_raw = '/home/ahmadalfi/Training/python/socket-programming/server/dataset.zip'

                    # berkas = koneksi_client.recv(self.__sizeFile)

                    with open(self.__path_raw, 'wb') as file:
                        while True:
                            berkas = koneksi_client.recv(self.__sizeFile)
                            if not berkas:
                                print("Selesai")
                                break
                            file.write(berkas)
                        file.seek(0)
                        file.close()

                    koneksi_client.shutdown(socket.SHUT_RD)
                    # LAH INI LIST FILE NYA MUNCUL!? KOK CORRUPT?!
                    self.UnzipDataset()

                    print("file diterima")
                    koneksi_client.close()

            elif command == "inference":
                pass
            if not command:
                print("This is not Data!!!")
                break


ojek = socket_backend(7000)
ojek.beginSocketComm()
