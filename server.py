from all import *

IP = "0.0.0.0"
PORT = 8080

#TODO Generate a key on sign up
key = ""


def read_key():
    with open('key.key', 'rb') as filekey:
        global key
        key = filekey.read()

def check_user(name, passw): # check if user in the system
    if name == "ori" and passw == "ori":
        return "true"
    return "false"



def parse_protocol_message(msg):

    code = msg[:4]
    msg = msg[5:]
    text = msg.split("~")
    print(text)
    if code == 'ISSG':
        return 'SGIN' + '~' + check_user(text[0], text[1])
    elif code == 'CODE':
        read_key()
        print('GCOD' + '~' + key.decode())
        return 'GCOD' + '~' + key.decode()
    return "ERRO"




def handle_client(csock, addr):
    while True:
        msg = recv_one_message(csock)
        msg_send = parse_protocol_message(msg)
        send_one_message(csock, msg_send)


def main():
    s = socket.socket()
    print("-> " + str(key))
    s.bind((IP,PORT))
    s.listen()
    while True:
        cli_sock , addr = s.accept()
        t = threading.Thread(target = handle_client, args=(cli_sock, addr))
        t.start()



if __name__ == '__main__':
    main()