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

    def doInference(self, arg):
        pass

    def compress(self):
        # dir = self.get_path_for_compress()
        filename = "dataset"
        print("masuk")
        shutil.make_archive(filename,'zip',self.__dirDat)


    """
    TODO:
    method ini kalau bisa flexibel, bisa buat ngirim zip,
    atau send wav(buat inference)
    """
    def sendFile(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = self.__port
        host = socket.gethostbyname(self.__host)
        print(host, port)

        try:
            client_socket.connect((host, port))
        except Exception as e:
            print("Koneksi error : ", e)

        # contoh implementasi send file ( untuk train model )
        # do compression data
        self.compress()
        # step 1 kirim ukuran file ke server_socket
        filesize = os.path.getsize("dataset.zip")
        command = "send_file"
        dataSize = str(filesize)
        client_socket.send(command.encode())
        # step 2 tunggu balasan dari server
        buffer = client_socket.recv(1024).decode()
        # step 3 kirim file
        if buffer == 'ready':
            command = "ok"
            client_socket.send(command.encode())
            buffer = client_socket.recv(1024).decode()
            if buffer == 'do_it':
                # simpan ukuran file (karena socket harus tau ukuran file nya dulu)
                client_socket.send(dataSize.encode())
                # step 5 send file
                buffer = client_socket.recv(1024).decode()
                if buffer == 'whereisfile':
                    with open('dataset.zip', 'rb') as berkas:
                        client_socket.sendfile(berkas, 0)
                    # step 6 DONE!!!!
                    berkas.close()
                    client_socket.shutdown(socket.SHUT_WR)

            print("Selesai")
            client_socket.close()



        # contoh penggunaan class socket_raspi
        # ojek = socket_raspi(7000, "192.168.1.3")
dir = "/home/ahmadalfi/Training/python/speech_processing/dataset/"
ojek = socket_raspi(7000, "127.0.0.1", direktori_dataset=dir)
ojek.sendFile()
