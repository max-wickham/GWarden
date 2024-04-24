from enum import Enum
import os
import subprocess
from multiprocessing import Process, Queue

from gi.repository import GLib

from src.api.passer import read_from_str, Item

class UnauthenticatedError(Exception):
    pass


class Controller:
    api_key: str | None
    file_path = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[:-1])

    def __init__(self) -> None:
        self.login_callback = lambda x : None
        self.get_items_callback = lambda x: None
        self.sync_callback = lambda x : None

        self.login_queue = Queue()
        self.get_items_queue = Queue()
        self.sync_queue = Queue()

        self.sync_process = None


    def login(self, username, password, callback):
        self.login_callback = callback

        def producer(queue):
            print('logging in')
            result = subprocess.run(f"{self.file_path}/bw logout".split(' '), capture_output=True)
            result = subprocess.run(f"{self.file_path}/bw login {username} {password} --raw".split(' '), capture_output=True)
            print('donw in')
            print(result.returncode)
            print(result)
            if result.returncode != 0:
                queue.put(None)
            else:
                queue.put(result.stdout.decode("utf-8"))
        Process(target=producer, args=(self.login_queue,), daemon=True).start()

    def get_items(self, callback):
        self.get_items_callback = callback
        def producer(queue):
            result = subprocess.run(f"{self.file_path}/bw list items --session {self.api_key}".split(' '), capture_output=True)
            if result.returncode != 0:
                queue.put(None)
            queue.put(result.stdout.decode("utf-8"))
        Process(target=producer, args=(self.get_items_queue,), daemon=True).start()

    # def start_sync_loop(self, interval, callback):
    #     self.sync_callback = callback
    #     def producer(queue):
    #         import time
    #         while True:
    #             result = subprocess.run(f"{self.file_path}/bw list items --session {self.api_key}".split(' '), capture_output=True)
    #             if result.returncode != 0:
    #                 queue.put(None)
    #             queue.put(read_from_str(result.stdout.decode("utf-8")))
    #             time.sleep(interval)
    #     self.sync_process = Process(target=producer, args=(self.get_items_queue,), daemon=True).start()

    def stop_sync_loop(self):
        if self.sync_process is not None:
            self.sync_process.terminate()

    def run(self):
        if self.login_queue.qsize() > 0:
            item = self.login_queue.get()
            print('logging in finished')
            print(item)
            if item is not None:
                self.api_key = item
            self.login_callback(item)
        GLib.timeout_add(100, self.run)
        if self.get_items_queue.qsize() > 0:
            print('received items')
            item = self.get_items_queue.get()
            print(item)
            if item is not None:
                self.get_items_callback(read_from_str(item))
        # if self.get_items_queue.qsize() > 0:
        #     print('received items')
        #     item = self.get_items_queue.get()
        #     print('Item',item)
        #     if item is not None:
        #         self.sync_callback(item)

    #     self.file_path = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[:-1])
    #     result = subprocess.run(f"{self.file_path}/bw logout".split(' '), capture_output=True)
    #     result = subprocess.run(f"{self.file_path}/bw login {username} {password} --raw".split(' '), capture_output=True)
    #     if result.returncode != 0:
    #         raise UnauthenticatedError
    #     api_key = result.stdout.decode("utf-8")
    #     self.username = username
    #     self.password = password
    #     self.api_key = api_key

    # def sync(self):
    #     result = subprocess.run(f"{self.file_path}/bw sync".split(' '), capture_output=True)
    #     if result.returncode != 0:
    #         raise UnauthenticatedError

    # def logout(self):
    #     os.system("./bw logout")
    #     self.api_key = None
    #     self.username = None
    #     self.password = None

    # def get_items(self) -> list[Item]:
    #     if self.api_key is None:
    #         raise UnauthenticatedError
    #     result = subprocess.run(f"{self.file_path}/bw list items --session {self.api_key}".split(' '), capture_output=True)
    #     if result.returncode != 0:
    #         raise UnauthenticatedError
    #     return read_from_str(result.stdout.decode("utf-8"))

    # def logged_in(self) -> bool:
    #     return self.api_key is not None



    # def run(self):
    #     # should be run in the main loop
