class Request:
    marker: enumerate
    body: str

    def __init__(self, marker=None, body=""):
        self.marker = marker
        self.body = body

    def __str__(self) -> str:
        return "<{0}>{1}".format(str(self.marker), self.body)


