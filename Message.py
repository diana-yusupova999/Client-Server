from MARKER import MARKER


class Message:

    def __init__(self, author: str, date: str, text: str):
        self.text = text
        self.author = author
        self.date = date

    def __str__(self) -> str:
        return ("\nAUTHOR: {};\n"
                + "DATE: {};\n"
                + "TEXT: {};\n").format(self.author, self.date, self.text)


def parse_message(data: str) -> Message:
    msgsplit = data.replace(str(MARKER.MESSAGE), "").replace("\n", "").split(";")
    author = msgsplit[0].split(":")[1]
    date = msgsplit[1].split(":")[1]
    text = msgsplit[2].split(":")[1]
    return Message(author, date, text)
