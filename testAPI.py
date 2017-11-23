import socket
import json


HOST, PORT = "localhost", 9999
def getChangeData(dateStart, dateEnd, source):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(bytes(json.dumps(("request", (dateStart, dateEnd, source))), "utf-8"))

        received = str(sock.recv(2024), "utf-8")
        result = json.loads(received)
        print(result)

if __name__ == "__main__":
    dateStart = "2017-11-21T13:37:32"
    dateEnd = "2017-11-22T07:11:00"
    source = None
    getChangeData(dateStart, dateEnd, source)
