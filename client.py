import socket
import threading
import time as t
from datetime import *

from Request import *
from Message import *

HOST = '127.0.0.1'
PORT = 8001
ADDR = (HOST, PORT)
ADDR2 = (HOST, 8000)


class Client:
    last_msg_id = -1

    def send_request(self, request) -> str:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect(ADDR)
        except ConnectionRefusedError:
            client.connect(ADDR2)
        client.send(bytes(str(request).encode("UTF-8")))
        resp = client.recv(1024).decode("UTF-8")

        return resp

    def send_message(self, message: Message) -> str:
        return self.send_request(Request(MARKER.MESSAGE, str(message)))

    def parse_message(self, data: str) -> (int, str):
        datasplit = data.split("|")
        if len(datasplit) < 2:
            return None, ""
        else:
            return datasplit[0], datasplit[1]

    def updates(self, nickname: str) -> str:
        response = self.send_request(Request(MARKER.UPDATES, nickname.replace("|", "") + "|" + str(self.last_msg_id)))
        lmi, msgs = self.parse_message(response)
        if len(msgs) > 0 and lmi is not None:
            self.last_msg_id = lmi
        return msgs

    def print_to_console(self, text: str):
        print(text)
        print('Enter message:   ')

    def print_new_messages(self, nickname: str):
        while True:
            t.sleep(1)
            message_update = self.updates(nickname)
            if len(message_update) > 0 and message_update is not None and message_update != "None":
                self.print_to_console(str(message_update))

    def date(self) -> str:
        return datetime.strftime(datetime.now(), "%d-%m-%Y %T:%M%p")

    def start(self):
        print('Hello, stranger. Please, enter your nickname and start chatting now!')
        nick = input('Enter nickname:   ')
        self.send_message(Message(nick, self.date(), nick + " was connected!"))
        thread = threading.Thread(target=self.print_new_messages, args=(nick,))
        thread.start()
        while True:
            try:
                message_text = input()
                if message_text is not None:
                    self.send_message(Message(nick, self.date(), message_text))
            except Exception as e:
                print(e)
                continue


if __name__ == '__main__':
    Client().start()
