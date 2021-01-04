#!/usr/bin/python3
import sys
sys.path.append('bin/')
import time
import termcolor as tc
import socket
import threading
import argparse
import os
import transport
import drag



class __host__():
    def __init__(self, ip, port, byte_size,cmd,user):
        self.IP = ip
        self.PORT = port
        self.ADDR = (ip , port)
        self.CONN_NO = []
        self.CMD = cmd
        self.USER = user

        if byte_size == b'MAX':
            self.BYTE_SIZE = 100000000
        elif  byte_size == b'MIN':
            self.BYTE_SIZE = 100000
        elif byte_size == b'DEF':
            self.BYTE_SIZE = 1000
        self.conn = None


    def start_connection(self):
        try:
            with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as server:
                print(f'[+] binding {self.IP} to port {self.PORT}')
                server.bind(self.ADDR)
                print(f'[+] listening to port {self.PORT}')
                server.listen()
                print('[+] connection established!.')
                self.connected = True
                while self.connected:
                    conn , addr =  server.accept()
                    self.conn = conn
                    self.CONN_NO.append(addr)


                    thread =  threading.Thread(target=self.handle_connection , args=(conn,addr))
                    thread.start()
                thread._stop()
                conn.close()
        except KeyboardInterrupt:
            self.exit()
        except socket.gaierror:
            self.server_error()
        except OverflowError:
            self.server_error()
            self.exit()
        except OSError:
            self.server_error()
    def handle_connection(self, conn, addr):
        try:
            tc.cprint(f'[*] {addr} connected', 'green')
            tc.cprint(f'[*] {len(self.CONN_NO)} process handled', 'yellow')
            self.__recv__(conn,addr)
            # self.__send__(conn,addr)
        except KeyboardInterrupt:
            self.exit()



    def __recv__(self, conn, addr):
            __data__ = conn.recv(self.BYTE_SIZE)
            self.reply_bytes(conn, addr, __data__)
            self.reply_buffer(conn, addr , __data__)
    def reply_buffer(self, conn , addr, __data__):
        check_transport = b',' in  __data__ and b'/' in __data__ and b'<DRAG>' not in __data__
        check_drag = b'<DRAG>' in __data__
        if check_transport:
            INFO = __data__.decode().split(',')
            local_file_dest = INFO[0]
            remote_file_dest = INFO[1]
            TRANSPORT = transport.transport(conn, local_file_dest, remote_file_dest)
            TRANSPORT.send()
        elif check_drag:
            INFO = __data__.decode().split(',')
            INFO.remove('<DRAG>')

            remote_file_name = INFO[0].strip()
            remote_file_name = remote_file_name.split('/')

            remote_file_dest = INFO[1] + '/' + remote_file_name[-1]
            local_file_dest = INFO[0]
            file_size = INFO[2]
            DRAG = drag.drag(conn, remote_file_dest, local_file_dest, file_size)
            DRAG.recv()
        else:
            pass
    def reply_bytes(self,conn,addr, __data__):
        check_transport = b',' in  __data__ and b'/' in __data__
        if __data__ == b'exit':
            tc.cprint(f'[!] {addr} diconnected!.')
            self.CONN_NO.remove(addr)
            tc.cprint(f'{ len(self.CONN_NO)} is active process')
            self.conn.send(b'byee')
        elif __data__ == b'hello':
            conn.send(b'I am up on port ' + bytes(str(self.PORT) , 'utf-8'))
        elif __data__ == b'':
            conn.send(b'recv!')
        else:
            if check_transport:
                pass
            else:
                tc.cprint(f'[+] {addr} says {__data__}' , 'green')
                conn.send(b'recv!')


    # def __send__(self, conn , addr, cmd):
    #     if cmd == 'send':
    #         self.conn.send(b'recv!')
    #     else:
    #         pass

    def exit(self):
        tc.cprint('[!] exit.!', 'red')
        sys.exit()
    def server_error(self):
        tc.cprint('[!] unable to create server!')
        sys.exit()
    def close_connection(self):
        try:
            self.conn.shutdown(socket.SHUT_WR)
            self.conn.close()
        except AttributeError:
            self.exit()
        except Exception:
            self.exit()
