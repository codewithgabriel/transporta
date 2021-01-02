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
import tqdm

class transport():
    def __init__(self,conn,remote_file_dest , local_file_dest):
        self.conn = conn
        self.REMOTE_FILE_DEST = remote_file_dest.strip()
        self.LOCAL_FILE_DEST = local_file_dest.strip()
    def send(self):
        try:
            file_name = self.REMOTE_FILE_DEST.split('/')
            file_name = file_name[-1]
            file_size = os.path.getsize(self.REMOTE_FILE_DEST)

            
            progress = tqdm.tqdm(range(file_size), f'[+] transporting {file_name}...' , unit='B', unit_scale=True)
            with open(self.REMOTE_FILE_DEST, 'rb') as _file_:
                for _ in progress:
                    _bytes_ = _file_.read()
                    if not _bytes_:
                        break
                    self.conn.sendall(_bytes_)
                    progress.update(file_size)
                self.conn.close()
                print('[#] done!.')
                

        except FileNotFoundError:
            self.allocation_resources_error()
        except Exception:
           self.error_encountered()

    def allocation_resources_error(self):
        tc.cprint(f'[!] unable to allocate data resources!')
        self.exit()
    def error_encountered(self):
        tc.cprint('[!] transporta is unable to trasport data!')
        self.exit()
    def exit(self):
        print('[#] done!.')
        sys.exit()
