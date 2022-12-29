from all import *

root = Tk()
driver_name = ""
dir_name = r"C:\temp\temp"

def delete_files(path): # delete all files in directory
    files = glob.glob(f'{path}\*.*')
    for f in files:
        print(f)
        os.remove(f)

def get_key(sock):
    build_protocol_message(sock, 'CODE', '')
    d = recv_one_message(sock)
    return parse_message_protocol(d)

def decrypt_zip(dec, path): # decrypt zip file content and save it 
    data = b''
    print(path)
    with open(path, 'rb') as f:
        data = f.read()
    os.remove(path)
    print(data)
    with open(path, 'wb') as f:
        f.write(dec.decrypt(data))
    print(path)
    shutil.unpack_archive(path, path) # extract the zip fileu

def encrypt_zip(enc, path): # encrypt zip file content and save it
    enc_data = b""
    with open(path, 'rb') as f:
        data = f.read()
        enc_data = enc.encrypt(data)
    with open(path, 'wb') as f:
        f.write(enc_data)

def build_protocol_message(sock, command, msg):

    full_msg = command + '~' + msg
    print(full_msg)
    send_one_message(sock, full_msg)

def gui_decrypt(sock): # lunch screen

    root.geometry("300x200")
    root.iconbitmap(r"img\favicon.ico")
    x = Label(root, text = "LOGIN", font = ('bold', 20)).place(x=90)
    username_text = Label(root, text = "Username: ", font = ('bold', 15)).place(y=50)
    password_text = Label(root, text = "Password: ", font = ('bold', 15)).place(y=100)
    utext = StringVar()
    ptext = StringVar()
    username = Entry(root, width = 15, textvariable=utext).place(x=100,y=55)
    password = Entry(root, show= "*", width = 15,textvariable=ptext).place(x = 100,y=105)

    submit = Button(root,height=1, width=15,text = "Login", command=lambda: app_system(sock)).place(x=60,y=155)
    
    root.mainloop()

def get_driveStatus():
    devices = []
    record_deviceBit = windll.kernel32.GetLogicalDrives()#The GetLogicalDrives function retrieves a bitmask
                                                         #representing the currently available disk drives.
    for label in string.ascii_uppercase : #The uppercase letters 'A-Z'
        if record_deviceBit & 1:
            devices.append(label)
        record_deviceBit >>= 1
    return devices

def secure_files(sock):
    
    print('stage 2')

    global dir_name
    shutil.make_archive(dir_name, 'zip', dir_name)
    delete_files(dir_name)
    key = get_key(sock)
    print(key)

    encrypter = Fernet(key.encode())
    origin = dir_name + '.zip'
    encrypt_zip(encrypter, origin)
    print(origin)

def decrypt_files(sock):
    global dir_name
    path = dir_name + '.zip'
    key = get_key(sock)
    decrypter = Fernet(key.encode())
    decrypt_zip(decrypter, path)
    print('d')




def app_system(sock): # the entire screen system

    global root
    root.destroy()

    root2 = Tk()
    root2.title("System")
    root2.iconbitmap(r"img\favicon.ico")
    root2.geometry("300x200")
    Button(root2, height=1, width=15, text="Secure my files!", command = lambda: secure_files(sock)).place(x=0)
    Button(root2, height=1, width=15, text="Decrypt my files!", command = lambda: decrypt_files(sock)).place(x=150)

    root2.mainloop()

def wait_until_plugged(sock):
    while True:

        

        # original = set(get_driveStatus())
        time.sleep(3)
        connected = True
        # add_device =  set(get_driveStatus())- original
        # subt_device = original - set(get_driveStatus())

        if connected:
            global driver_name
            gui_decrypt(sock)
        
        # if (len(add_device)):
        #     for drive in add_device:
        #             #print( "The drives added: %s." % (drive))
        #             global driver_name
        #             driver_name = drive
        #             gui_decrypt(sock)
                 
        # elif(len(subt_device)):
        #     #print ("There were %d"% (len(subt_device)))
        #     for drive in subt_device:
        #             #print ("The drives remove: %s." % (drive))
        #             pass

def parse_message_protocol(msg):
    code = msg[:4]
    msg = msg[5:]

    text = msg.split('~')
    print(text)
    if code == "SGIN":
        return "The user is in the system"
    elif code == "GCOD":
        return text[0]
    





def login_system(sock, username, password):
    
    msg = username + '~' + password
    build_protocol_message(sock, 'ISSG', msg)
    d = recv_one_message(sock)
    res = parse_message_protocol(d)
    if res == "The user is in the system":
        app_system(sock)
    




def main():
    c = socket.socket()
    c.connect(("127.0.0.1",8080))
    wait_until_plugged(c)


if __name__ == '__main__':
    main()