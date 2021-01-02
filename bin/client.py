#!/usr/bin/python3
import sys
sys.path.append('bin/')
import time
import termcolor as tc
import socket
import threading
import argparse
import os
import host
import transport
import tqdm



class __client__():
    def __init__(self, ip, port, cmd,value, USER):
        self.IP = ip
        self.PORT = port
        self.ADDR = (ip , port)
        self.CONN_NO = []
        self.BYTE_SIZE_MAX = 100000000
        self.BYTE_SIZE_MIN = 100000
        self.BYTE_SIZE_DEF = 1000
        self.CMD = cmd
        self.VALUE = value
        self.USER = USER

    def start_connection(self):
        try:
            with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as server:
                print(f'[+] connecting to {self.IP} on port {self.PORT}')
                print('[+] connected!.')
                self.connected = True
                self.conn = server
                server.connect(self.ADDR)
                self.handle_connection(self.conn)
                # thread = threading.Thread(target=self.handle_connection , args=(self.conn , ))
                # thread.start()
                # thread._stop()
        except KeyboardInterrupt:
            self.conn.send(b'exit')
            self.exit()
        except socket.gaierror:
            self.server_error()
        except ConnectionRefusedError:
            tc.cprint(f'[!] {self.IP} is down on port {self.PORT}!', 'red')
            sys.exit()
    def handle_connection(self, conn):
        if self.CMD == 'send':
            self.__send__(self.conn, self.VALUE)
            self.send_transport_info(self.VALUE)
        elif self.CMD == 'drag':
            self.send_drag_info(self.VALUE)
        elif self.CMD == 'transport' or self.CMD == 'recv':
            self.send_transport_info(self.VALUE)
            #self.__recv__()

        
           

    def handle_active_conn_count(self):
        self.CONN_NO = host.__host__(self.IP, self.PORT).CONN_NO

    def __recv__(self, conn , __data__):
        
            try:
                print(f'[+] {__data__}')
                tc.cprint(f'[+] {len(__data__)} byte(s) is recv!.', 'yellow')
                print('[#] done!')
                self.conn.close()
                self.exit()
            except OSError:
                self.exit()

    def __send__(self, conn, __data__):
        data_len = len(__data__)
        try:
            tc.cprint(f'[+] sending bytes..', 'green' )
            self.conn.send(__data__)
            tc.cprint(f'[+] {data_len} bytes(s) sent.', 'yellow')
            __data__ = self.conn.recv(self.BYTE_SIZE_MAX)
            self.__recv__(self.conn , __data__)

        except KeyboardInterrupt:
            self.conn.send(b'exit')
            self.conn.close()
            self.exit()
    def send_transport_info(self, INFO):
        try:
            tc.cprint('[+] sending resources info...', 'green')
            self.conn.send(INFO)
            tc.cprint('[+] info is sent!...' , 'yellow')
            print('[#] done sending info!')
            FILE = INFO.decode().split(',')
            file_size = os.path.getsize(FILE[0].strip())
            file_name = FILE[0].split('/')
            file_name = file_name[-1]
            file_name = FILE[1] + '/' + file_name 
            
            progress = tqdm.tqdm(range(file_size) ,  f'[+] transporting {file_name}...' , unit='B' , unit_scale=True)
            with open(file_name.strip(), 'wb') as f:
                for _ in progress:
                    incoming_bytes = self.conn.recv(self.BYTE_SIZE_MAX)
                    if not incoming_bytes:
                        break
                    f.write(incoming_bytes)
                    progress.update(file_size)
            tc.cprint(f'[+] {file_name} is successfully transported', 'yellow')
            self.close_connection()
        except FileNotFoundError:
            tc.cprint(f'[!] error allocating resources')
            self.exit()
        except Exception:
            self.exit()
    def send_drag_info(self, INFO):
        try:
            tc.cprint('[+] sending resources info...', 'green')
            FILE = INFO.decode().split(',')
            file_size = os.path.getsize(FILE[0].strip())
            file_name = FILE[0].strip()
            
            self.conn.send(INFO + b',' + bytes(str(file_size) , 'utf-8')+ ',<DRAG>'.encode())
            # incoming_bytes = self.conn.recv(self.BYTE_SIZE_MAX)
            # print(incoming_bytes)
            progress = tqdm.tqdm(range(file_size) ,  f'[+] dragging {file_name}...' , unit='B' , unit_scale=True)
            with open(file_name.strip(), 'rb') as f:
                for _ in progress:
                    outgoing_bytes = f.read(file_size)
                    if not outgoing_bytes:
                        break
                    self.conn.sendall(outgoing_bytes)
                    progress.update(file_size)
            tc.cprint(f'[+] {file_name} is successfully dragged to remote dest {FILE[1]}', 'yellow')
            self.close_connection()
        except FileNotFoundError:
            tc.cprint(f'[!] error allocating resources')
            self.exit()
        except Exception:
            self.exit()

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
            self.exit()
        except AttributeError:
            self.exit()
        except Exception:
            self.exit()
            
