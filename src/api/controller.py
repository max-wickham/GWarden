import os
import subprocess

from src.api.passer import read_from_str, Item

class UnauthenticatedError(Exception):
    pass

class Controller:
    api_key: str | None

    def __init__(self, username, password) -> None:
        self.file_path = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[:-1])
        result = subprocess.run(f"{self.file_path}/bw logout".split(' '), capture_output=True)
        result = subprocess.run(f"{self.file_path}/bw login {username} {password} --raw".split(' '), capture_output=True)
        if result.returncode != 0:
            raise UnauthenticatedError
        api_key = result.stdout.decode("utf-8")
        self.username = username
        self.password = password
        self.api_key = api_key

    def logout(self):
        os.system("./bw logout")
        self.api_key = None
        self.username = None
        self.password = None

    def get_items(self) -> list[Item]:
        if self.api_key is None:
            raise UnauthenticatedError
        result = subprocess.run(f"{self.file_path}/bw list items --session {self.api_key}".split(' '), capture_output=True)
        if result.returncode != 0:
            raise UnauthenticatedError
        return read_from_str(result.stdout.decode("utf-8"))

    def logged_in(self) -> bool:
        return self.api_key is not None
