import socketserver

from Request import Request
from MARKER import MARKER
from Message import parse_message, Message

HOST = '127.0.0.1'
PORT = 8001
ADDR = (HOST, PORT)
ADDR2 = (HOST, 8000)

messages: dict = {}


def msg_request(data: str) -> Request:
    datasplit = data.replace("<", "").split(">")
    marker = datasplit[0]
    body = datasplit[1]
    return Request(marker, body)


def get_new_message(msgs: dict, nickname: str, lmi: int) -> (int, Message):
    print(msgs)
    for key, msg in msgs.items():
        if int(key) > lmi:
            if nickname != str.strip(msg.author):
                return key, msg
    return None, None


def parse_updates_request(data: str) -> (str, int):
    datasplit = data.replace("<{}>".format(str(MARKER.UPDATES)), "").split("|")
    nickname = datasplit[0]
    lmi = int(datasplit[1])
    return nickname, lmi


class ServerThreadHandler(socketserver.BaseRequestHandler):
    bufferSize = 1024
    last_msg_id = -1

    def handle(self):
        data = str(self.request.recv(self.bufferSize)).replace("'", "").replace("\n", "")[1:]
        print("data=" + data)
        request = msg_request(data)
        print(request.marker)
        addr = self.client_address
        if request.marker == str(MARKER.MESSAGE):
            lmi = len(messages)
            msg = parse_message(data)
            print("msg: " + str(msg))
            messages.update({lmi: msg})
        elif request.marker == str(MARKER.UPDATES):
            nickname, lmi = parse_updates_request(data)
            print("nick: " + nickname)
            print("lmi: " + str(lmi))
            key, new_message = get_new_message(messages, nickname, lmi)
            if key is not None and new_message is not None:
                messages_to_send = str(key) + "|" + str(new_message)
                print(messages_to_send)
                self.request.sendto(bytes(messages_to_send.encode("UTF-8")), addr)


if __name__ == "__main__":
    try:
        server = socketserver.TCPServer(ADDR, ServerThreadHandler)
        server.serve_forever()
    except OSError:
        server = socketserver.TCPServer(ADDR2, ServerThreadHandler)
        server.serve_forever()
