"""

PROGRAMMED BY           : AHMAD ALFI ADZ-DZIKRI
DATE PRGORAMMED         : BANDUNG, MARCH 26 2019
PURPOSE                 : CLOUD DEEP LEARNING BASED EXPERIMENT

"""

import socket
import os
import sys
import shutil


class socketClient(object):

    """
    port
    Server Port number

    target
    is a ip target, or the DNS target (which is server)

    direktori_dataset
    the directory of dataset

    direktori_wav
    the directory of wav file (sample voice)

    root_dir
    this variable used to be a place where incoming file stored
    """
    def __init__(self, port, target,
                 direktori_dataset=None,
                 direktori_wav=None,
                 root_dir=None):

        self.__port = port
        self.__host = target
        self.__dirDat = direktori_dataset
        self.__dirWav = direktori_wav
        self.__root_dir = root_dir

        self.__client_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        port = self.__port
        host = socket.gethostbyname(self.__host)
        print(host, port)

        try:
            self.__client_socket.connect((host, port))
        except Exception as e:
            print("Koneksi error : ", e)

    """
    disconnectClient()

    this method is use to disconnect the client and close the socket
    Connection
    """
    def disconnectClient(self):
        self.__client_socket.shutdown(socket.SHUT_RDWR)
        self.__client_socket.close()
        print("Socket Closed")

    """
    doInference()

    this will do a inference and send data wav to server and
    do deep learning inference
    """
    def doInference(self):
        self.__command = "inference"
        self.sendFile(self.__dirWav)

        print("begin hearing data...")
        # mulai process receive
        self.recvFile()

    """
    compress()

    an utility to make directory become archive
    """
    def compress(self):
        # dir = self.get_path_for_compress()
        filename = "dataset"
        shutil.make_archive(filename, 'zip', self.__dirDat)
        namaZip = os.path.basename(self.__dirDat[:-1]) + '.zip'
        return namaZip


    """
    doTrain()

    send instruction to do a training for deep learning
    and send archive that compress() do to the server
    """
    def doTrain(self):
        namaZip = self.compress()
        self.__command = "do_train"
        self.sendFile(namaZip)


    """
    sendFile()

    this method is an utility to send file to the server
    """
    def sendFile(self, namaFile):

        # step 1 kirim ukuran file ke server_socket
        filesize = os.path.getsize(namaFile)
        command = self.__command

        dataSize = str(filesize)
        self.__client_socket.send(command.encode())
        # step 2 tunggu balasan dari server
        buffer = self.__client_socket.recv(1024).decode()
        # step 3 kirim file
        if buffer == 'ready':
            command = "ok"
            self.__client_socket.send(command.encode())
            buffer = self.__client_socket.recv(1024).decode()
            if buffer == 'do_it':
                # simpan ukuran file (karena socket harus tau ukuran file nya dulu)
                self.__client_socket.send(dataSize.encode())
                response = self.__client_socket.recv(1024).decode()
                if response == 'whatname':
                    #  step 7 send namafile
                    namafile_temp = os.path.basename(namaFile)
                    self.__client_socket.send(namafile_temp.encode())
                    buffer = self.__client_socket.recv(1024).decode()
                    if buffer == 'whereisfile':
                        # step 6 send file
                        with open(namaFile, 'rb') as berkas:
                            self.__client_socket.sendfile(berkas, 0)
                            # step 7 DONE!!!!
                            berkas.close()

            print("Selesai")

    """
    recvFile()

    this method is an utility to receive file from server
    """
    def recvFile(self):
        # Pertama kita 'handshake' dulu untuk memberi informasi
        # alamat IP, dan port yang kita pakai setelah
        # itu server akan mengirim hasil inferensi

        # step 1 menerima respon dari server
        response = self.__client_socket.recv(1024).decode()
        # step 2 dapat response dan meminta size data
        if response == 'want2send':
            self.__client_socket.sendall(str("sizeFirst").encode())
        # step 3 simpan filesize
            sizeFile = int(self.__client_socket.recv(1024).decode())
        # step 4 beritahu server,bahwa client siap
            self.__client_socket.send(str('ready').encode())
        # step 5 menerima file
            namafile = os.path.join(self.__root_dir, 'result.json')
            with open(namafile, 'wb') as file:
                while True:
                    berkas = self.__client_socket.recv(sizeFile)
                    if not berkas:
                        break
                    file.write(berkas)
                file.close()
        else:
            print("Wrong response")


# contoh penggunaan class socket_raspi

# ojek = socketClient(7000, "192.168.1.3")
# dir = "/home/ahmadalfi/Training/python/speech_processing/dataset/"
# wav = "/home/ahmadalfi/Training/python/socket-programming/client/[class1]00003_0.wav"
# root = '/home/ahmadalfi/Training/python/socket-programming/client'
#
# ojek = socketClient(7000, "127.0.0.1", direktori_dataset=dir,
#                     direktori_wav=wav, root_dir=root)
#
# ojek.doTrain()
# ojek.disconnectClient()
# ojek = socketClient(7000, "127.0.0.1", direktori_dataset=dir,
#                     direktori_wav=wav, root_dir=root)
# ojek.doInference()
# ojek.disconnectClient()
