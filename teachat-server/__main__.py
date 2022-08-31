# -*- coding: utf-8 -*-
import socket
import threading
import logging
import argparse
import asyncio
import os
import traceback

usable_sockets = []


def receive(user_sock):
    """

    :param user_sock:
    :return:
    """
    global usable_sockets
    while True:
        try:
            #####################################################
            # 看我看我！！！
            # 这都是经验！！！！
            # 你只使用一个接收消息的地方就行
            # 就是下面这个就行！！！
            # 然后你可以格式化一下客户端的消息
            # 用json最好，我举个荔枝，例如：
            # {"type": "auth", "user": user}
            # 这样就可以用原生json库解码了
            # 接下来判断type里的内容是啥就可以做对应操作了
            #####################################################
            # 向服务端发送信息
            msg = user_sock.recv(1024).decode()
        except socket.timeout:  # 响应超时
            user_sock.close()
            usable_sockets.remove(user_sock)
            break
        except:
            logger.error('发生了一个非致命错误！')
            traceback.print_exc()
            user_sock.close()
            usable_sockets.remove(user_sock)
            break

    # for i in usable_sockets:
    #     i.send(f"\nWelcome {nickname} enter!".encode())
    # while True:
    #     try:
    #         recv = user_sock.recv(1024)
    #         recv = recv.decode()
    #         print(nickname + recv)
    #         for i in usable_sockets:
    #             i.send(f"\n{nickname}:{recv}".encode())
    #         if recv == "exit":
    #             # 关闭用户socket，并从连接表中丢弃
    #             user_sock.shutdown(socket.SHUT_RDWR)
    #             user_sock.close()
    #
    #             usable_sockets.remove(user_sock)
    #             for i in usable_sockets:
    #                 i.send(f"\n {nickname} left!".encode())
    #     except:
    #         user_sock.close()
    #         usable_sockets.remove(user_sock)
    #         for i in usable_sockets:
    #             i.send(f"\n{nickname} 离开了".encode())


def server_input():
    global usable_sockets
    while True:
        msg = input('>')
        if len(usable_sockets) == 0:
            print('注意！当前没有任何用户连接到本服务器，本次发送消息无效')
        else:
            for sock in usable_sockets:
                sock.send(msg.encode())


async def main(logger: logging.Logger, bind: tuple = ('127.0.0.1', 1107), socket_timeout: float = 15,
               allow_server_input: bool = False):
    global usable_sockets

    # 绑定socket主机和端口
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(bind)  # ~~下个版本改成变量~~ 已经改了
    s.listen()

    logger.info('服务端已绑定至{}'.format(bind))

    if allow_server_input:
        logger.debug('已允许服务端输入，现在你可以在服务端聊天了')
        sent_thread = threading.Thread(target=server_input, daemon=False)
        sent_thread.start()

    # 开始主循环
    while True:
        sock, addr = s.accept()
        logger.debug('新客户端连接！{}'.format(addr))

        sock.settimeout(socket_timeout)
        usable_sockets.append(sock)
        t1 = threading.Thread(target=receive, args=(sock,))
        t1.start()


if __name__ == '__main__':
    # 设置输入参数
    parser = argparse.ArgumentParser()
    parser.add_argument('-D, --debug', help='启用调试模式', action='store_true')
    parser.add_argument('-p, --port', help='设置绑定端口', type=int, action='store', default=1107)
    parser.add_argument('-H, --host', help='设置绑定主机', type=str, action='store', default='127.0.0.1')
    parser.add_argument('-t, --timeout', help='设置单个socket超时的时间', type=float, action='store', default=15)
    parser.add_argument('-I, --stdin', help='启用服务端聊天功能', action='store_true')
    args = parser.parse_args()

    # 创建logger
    if args._get_kwargs()[0][1] is True:
        logger_level = logging.DEBUG
    else:
        logger_level = logging.INFO

    # 初始化logger
    logging.basicConfig(format='[%(asctime)s][%(levelname)s]@[Thread:%(threadName)s(%(thread)d),Function:%(funcName)s,'
                               'Line:%(lineno)d] %(message)s', level=logger_level)
    logger = logging.getLogger('TeachatServer')
    logger.info('日志初始化完成')
    logger.info('服务端正在运行(pid:{pid})'.format(pid=os.getpid()))

    # 异步运行主函数
    asyncio.run(main(
        bind=(args._get_kwargs()[2][1], args._get_kwargs()[1][1]),  # -H host -p port
        logger=logger,
        socket_timeout=args._get_kwargs()[3][1],  # -t(timeout) <float>
        allow_server_input=args._get_kwargs()[4][1]
    ))
