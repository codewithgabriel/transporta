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

class drag():
    def __init__(self,conn,remote_file_dest , local_file_dest, file_size):
        self.conn = conn
        self.REMOTE_FILE_DEST = remote_file_dest.strip()
        self.LOCAL_FILE_DEST = local_file_dest.strip()
        self.FILE_SIZE = int(file_size)
    def recv(self):
        try:
            progress = tqdm.tqdm(range(self.FILE_SIZE), f'[+] dragging {self.REMOTE_FILE_DEST}...' , unit='B', unit_scale=True)
            with open(self.REMOTE_FILE_DEST, 'wb') as _file_:
                for _ in progress:
                    _bytes_ = self.conn.recv(self.FILE_SIZE)
                    if not _bytes_:
                        break
                    _file_.write(_bytes_)
                    progress.update(self.FILE_SIZE)
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
        tc.cprint('[!] draga is unable to trasport data!')
        self.exit()
    def exit(self):
        print('[#] done!.')
        sys.exit()