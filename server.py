import socketserver
import threading
import json
import time
import sqlite3

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(2024).strip()
        print("{} wrote:".format(self.client_address[0]))
        status, self.data = json.loads(self.data)
        if status == "entery":
            addRowDb(self.data)
            for i in self.data:
                print(i)
        elif status == "request":
            print(self.data)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def addRowDb(modif_files):
    conn = sqlite3.connect('files.db')
    try:
        cur = conn.cursor()
        cur.execute("""create table if not exists files (
                        id      integer     primary key AUTOINCREMENT,
                        path    text        not null,
                        size    int         not null,
                        status  char(10)    not null,
                        source  text        not null,
                        [timestamp] timestamp DEFAULT CURRENT_TIMESTAMP)
                    """)
        cur.executemany("insert into files(path, size, status, source) values (?,?,?,?)", modif_files)
    except sqlite3.DatabaseError as err:
        print("Error: ", err)
    else:
        conn.commit()
        conn.close()

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    server = ThreadedTCPServer((HOST, PORT), MyTCPHandler)
    with server:
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        try:
            while True:
                time.sleep(0.1)
        except (KeyboardInterrupt, SystemExit):
            server.shutdown()