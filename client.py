from all import *

root = Tk()
driver_name = ""

def build_protocol_message(sock, command, msg):

    full_msg = command + '~' + msg
    send_one_message(sock, full_msg)

def gui_decrypt(sock):

    root.geometry("300x200")

    x = Label(root, text = "LOGIN", font = ('bold', 20)).place(x=90)
    username_text = Label(root, text = "Username: ", font = ('bold', 15)).place(y=50)
    password_text = Label(root, text = "Password: ", font = ('bold', 15)).place(y=100)
    utext = StringVar()
    ptext = StringVar()
    username = Entry(root, width = 15, textvariable=utext).place(x=100,y=55)
    password = Entry(root, show= "*", width = 15,textvariable=ptext).place(x = 100,y=105)

    submit = Button(root,height=1, width=15,text = "Login", command= lambda: login_system(sock,utext.get(), ptext.get()), ).place(x=60,y=155)
    
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

    dir_name = r'C:\temp\temp'
    shutil.make_archive(dir_name, 'zip', dir_name)
    build_protocol_message(sock, 'CODE', '')
    d = recv_one_message(sock)
    key = parse_message_protocol(d)
    print(key)

    print("COMPLETE")

def app_system(sock):
    global root
    root.destroy()

    root = Tk()
    root.title("System")
    root.geometry("300x200")
    Button(root, height=1, width=15, text="Secure my files!", command = lambda: secure_files(sock)).place(x=0)
    Button(root, height=1, width=15, text="Decrypt my files!").place(x=150)

    root.mainloop()

def wait_until_plugged(sock):
    while True:

        

        original = set(get_driveStatus())
        time.sleep(3)
        add_device =  set(get_driveStatus())- original
        subt_device = original - set(get_driveStatus())

        if (len(add_device)):
            for drive in add_device:
                    #print( "The drives added: %s." % (drive))
                    global driver_name
                    driver_name = drive
                    gui_decrypt(sock)
                 
        elif(len(subt_device)):
            #print ("There were %d"% (len(subt_device)))
            for drive in subt_device:
                    #print ("The drives remove: %s." % (drive))
                    pass

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