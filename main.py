import socket
import threading
def receive(new_s, socket_list):
    try:
        nickname = new_s.recv(1024).decode().strip()
    except:
        new_s.close()
        socket_list.remove(new_s)

    for i in socket_list:
        i.send(f"\nWelcome {nickname} enter!".encode())
    while True:
        try:
            recv = new_s.recv(1024)
            recv = recv.decode()
            print(nickname + recv)
            for i in socket_list:
                i.send(f"\n{nickname}:{recv}".encode())
            if recv =="exit":
                new_s.close
                socket_list.remove(new_s)
                for i in socket_list:
                    i.send(f"\n {nickname} left!".encode())
        except:
            new_s.close()
            socket_list.remove(new_s)
            for i in socket_list:
                i.send(f"\n{nickname} 离开了".encode())

def sent(new_s):
    while True:
        msg = input(" ")
        new_s.send(msg.encode())

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(("127.0.0.1", 1109))  #下个版本改成变量
s.listen(5)
socket_list = []
while True:
    new_s,addr = s.accept()
    print("客户端来啦")
    socket_list.append(new_s)
    new_s.send("Your name?".encode())
    t1 = threading.Thread(target = receive, args = (new_s, socket_list,))
    t2 = threading.Thread(target = sent, args=(new_s,))
    t1.start()
    t2.start()