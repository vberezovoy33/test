import time
import socket
import json
import sys

from pathlib import Path

def start_client(p_string, HOST, PORT, source):
    old_dict_path = {}

    while True:
        dir_path = Path(p_string).expanduser().resolve(strict=True)
        dict_path = {x : (x.stat().st_size, x.stat().st_mtime, x.stat().st_ctime)
                        for x in dir_path.rglob('*') if x.is_file()}

        if not old_dict_path:
            old_dict_path = dict_path
        else:
            old_set_pathname = set(old_dict_path.keys())
            set_pathname = set(dict_path.keys())
            creted_files = set_pathname - old_set_pathname
            removed_files = old_set_pathname - set_pathname
            chacking_files = set_pathname & old_set_pathname

            modif_files = []
            modif_files += [(str(x), dict_path[x][0], 'created', source) for x in creted_files]
            modif_files += [(str(x), old_dict_path[x][0], 'removed', source) for x in removed_files]
            modif_files += [(str(x), dict_path[x][0], 'changed', source) for x in chacking_files
                                if dict_path[x] != old_dict_path[x]]


            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                if modif_files:
                    sock.connect((HOST, PORT))
                    sock.sendall(bytes(json.dumps(("entery", modif_files)), "utf-8"))

                    received = str(sock.recv(2024), "utf-8")
                    print(json.dumps(modif_files));
            old_dict_path = dict_path

        time.sleep(2)

if __name__ == "__main__":


    p_string = sys.argv[1]
    HOST, PORT = sys.argv[2], int(sys.argv[3])
    source = sys.argv[4]

    start_client(p_string, HOST, PORT, source)
