import socket
import os
import sys


class socket_raspi(object):
    """docstring forsocket_raspi as client."""

    def __init__(self, port, target, direktori_dataset):
        self.__port = port
        self.__host = target
        self.__dir = direktori_dataset

    def doInference(self, arg):
        pass

    def get_path_for_compress(self):
        path_zipping = []
        for root, directories, files in os.scandir(self.__dir):
            for filename in files:
                # join the two strings in order to form the full filepath.
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)

        return path_zipping

    def compress(self):
        dir = self.get_path_for_compress()
        filename = "dataset.zip"
        print('compressing...')
        for file_name in dir:
            with ZipFIle(filename, 'w') as zip:
                for file in dir:
                    print(file)
                    zip.write(file)
        print("Done Compress")

    def sendFile(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = self.__port
        host = socket.gethostbyname(self.__host)
        print(host, port)

        try:
            client_socket.connect((host, port))
        except Exception as e:
            print("Koneksi error : ", e)

        #do compression data
        self.compress()
        # step 1 kirim ukuran file ke server_socket
        filesize = os.path.getsize(self.__dir+"/dataset.zip")
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
                        print(sys.getsizeof(berkas))
                        client_socket.sendfile(berkas, 0)
                    # step 6 tunggu notifikasi dari server
                    buffer = client_socket.recv(1024).decode()
                    # step 7 DONE!!!!
                    if buffer=='Received':
                        client_socket.shutdown(socket.SHUT_WR)
            print("Selesai")
            client_socket.close()


# contoh penggunaan class socket_raspi
# ojek = socket_raspi(7000, "192.168.1.3")
dir = "/home/ahmadalfi/Training/python/socket-programming/dataset"
ojek = socket_raspi(7000, "127.0.0.1", dir)
ojek.sendFile()
