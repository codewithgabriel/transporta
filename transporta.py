#!/usr/bin/python3
import sys
sys.path.append('bin/')
import time
import termcolor as tc
import socket
import threading
import argparse
import host
import client
import os





class transporta():   
    def arg_parser(self):    
        parser = argparse.ArgumentParser(description='transporta.')
        parser.add_argument('-H', '--host' ,action='store_true',   help='start transporta as host.')
        parser.add_argument('-C', '--client',action='store_true',   help='start transporta as client.')
        parser.add_argument('-s', '--send' , action='store_true', help='send bytes or buffer.')
        parser.add_argument('-st', '--set' , action='store_true', help='set byte size to be send or recv per time stamp for host.')
        parser.add_argument('-t', '--transport', action='store_true', help='transport buffer/bytes from a remote machine to your machine.')
        parser.add_argument('-d', '--drag', action='store_true', help='drag bytes/buffer from your machine to a remote  machine.')

        parser.add_argument('ip', type=str  , help='ip.')
        parser.add_argument('port', type=int  , help='port.')
        parser.add_argument('byte', type=str , help='bytes to send/ bytes sent can be use to config communication protocol.')
       
        args = parser.parse_args()

        

        self.HOST =  args.host
        self.CLIENT = args.client
        self.IP = args.ip
        self.PORT = args.port
        self.SEND = args.send
        self.SEND_BYTE = args.byte.encode()
        self.TRANSPORT = args.transport
        self.DRAG = args.drag
        self.SET = args.set
        self.handle_args()
        
    def handle_args(self):
        if self.HOST:
            if self.TRANSPORT:
                print('[!] host can not use --transport on intializing use --host-transport instead.')
                sys.exit()
            
            if self.SEND_BYTE == b'MIN' or self.SEND_BYTE == b'MAX' or self.SEND_BYTE == b'DEF':
                if self.SET:
                    self.handle_host(self.SEND_BYTE, 'send', 'host')
                elif self.TRANSPORT:
                    self.handle_host(self.SEND_BYTE, 'transport', 'host')
            else:
                print('[!] invalid byte config it can either be:\nMAX(100 000 000)\nMIN(100 000)\nDEF(1000)')
                sys.exit()

        elif self.CLIENT:
            if self.SEND_BYTE != b'MIN' or self.SEND_BYTE != b'MAX' or self.SEND_BYTE != b'DEF':
                if self.SEND:
                    self.send_bytes(self.SEND_BYTE , 'client')
                elif self.TRANSPORT:
                  self.handle_transport(self.SEND_BYTE, 'client')
                elif self.DRAG:
                    self.handle_drag(self.SEND_BYTE, 'client')
                
    def handle_host(self, byte_size,CMD,USER):
        __host__ = host.__host__(self.IP, self.PORT, byte_size, CMD, USER)
        __host__.start_connection()
    def handle_client(self, CMD , VALUE, USER):
        __client__ = client.__client__(self.IP, self.PORT, CMD, VALUE, USER)
        __client__.start_connection()

    def send_bytes(self, value, USER):
        self.handle_client('send', value,USER)
    def handle_transport(self, byte_value, USER):
        self.handle_client('transport', byte_value , USER)
    def handle_drag(self, byte_value, USER):
        self.handle_client('drag', byte_value , USER)



TRANSPORTA = transporta()
TRANSPORTA.arg_parser()