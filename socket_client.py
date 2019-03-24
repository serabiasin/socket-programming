import socket
import os
import sys
import shutil

class socket_raspi(object):
    """docstring forsocket_raspi as client."""

    def __init__(self, port, target,
                 direktori_dataset=None,
                 direktori_wav=None):
        self.__port = port
        self.__host = target
        self.__dirDat = direktori_dataset
        self.__dirWav = direktori_wav

    def disconnect(self):
        self.client_socket.close()
    def doInference(self):
        pass

    def compress(self):
        # dir = self.get_path_for_compress()
        filename = "dataset"
        print("masuk")
        shutil.make_archive(filename,'zip',self.__dirDat)
        namaZip=os.path.basename(self.__dirDat[:-1])+'.zip'
        return namaZip

    def doTrain(self):
        namaZip=self.compress()
        self.sendFile(namaZip)


    """
    TODO:
    method ini kalau bisa flexibel, bisa buat ngirim zip,
    atau send wav(buat inference)
    """
    def sendFile(self,namaFile):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = self.__port
        host = socket.gethostbyname(self.__host)
        print(host, port)

        try:
            self.client_socket.connect((host, port))
        except Exception as e:
            print("Koneksi error : ", e)

        # contoh implementasi send file ( untuk train model )
        # do compression data
        # self.compress()
        # step 1 kirim ukuran file ke server_socket
        filesize = os.path.getsize(namaFile)
        command = "send_file"
        dataSize = str(filesize)
        self.client_socket.send(command.encode())
        # step 2 tunggu balasan dari server
        buffer = self.client_socket.recv(1024).decode()
        # step 3 kirim file
        if buffer == 'ready':
            command = "ok"
            self.client_socket.send(command.encode())
            buffer = self.client_socket.recv(1024).decode()
            if buffer == 'do_it':
                # simpan ukuran file (karena socket harus tau ukuran file nya dulu)
                self.client_socket.send(dataSize.encode())
                # step 5 send file
                buffer = self.client_socket.recv(1024).decode()
                if buffer == 'whereisfile':
                    with open(namaFile, 'rb') as berkas:
                        self.client_socket.sendfile(berkas, 0)
                    # step 6 DONE!!!!
                    berkas.close()
                    self.client_socket.shutdown(socket.SHUT_WR)

            print("Selesai")

    def recvFile(self):
        pass


        # contoh penggunaan class socket_raspi
        # ojek = socket_raspi(7000, "192.168.1.3")
dir = "/home/ahmadalfi/Training/python/speech_processing/dataset/"
ojek = socket_raspi(7000, "127.0.0.1", direktori_dataset=dir)
# ojek.sendFile()
# ojek.doTrain()
