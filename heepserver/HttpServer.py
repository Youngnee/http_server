"""
Aid httpserver v3.0
"""

from socket import *
import sys
from threading import Thread
from config import *
import re
import json

# 服务器地址
ADDR = (HOST, PORT)

def connect_frame(env):
    s = socket()
    try:
        s.connect((frame_ip, frame_port)) # 连接WebFrom
    except Exception as e:
        print(e)
        return
    # 将请求字典转换为json数据发送
    data = json.dumps(env)
    s.send(data.encode())
    # 接收webframe数据,接收json
    msg = s.recv(4096*100).decode()
    # 返回数据字典
    return json.loads(msg)


# 封装httpserver基本功能
class HTTPServer(object):
    """
    httpserver功能封装类
    """

    def __init__(self, address):
        self.address = address
        self.create_socket()
        self.bind()

    def create_socket(self):
        """
        创建套接字
        """
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, DEBUG)

    def bind(self):
        """
        绑定地址
        """
        self.sockfd.bind(self.address)
        self.ip = self.address[0]
        self.port = self.address[1]

    def server_forever(self):
        """
        启动服务
        """
        self.sockfd.listen(5)
        print("Listen the port %d" % self.port)
        while True:
            connfd, addr = self.sockfd.accept()
            print("Connect From:", addr)
            client = Thread(target=self.handle, args=(connfd,))
            client.setDaemon(True)
            client.start()

    def handle(self,connfd):
        """
        处理具体客户端请求
        """
        request = connfd.recv(4096).decode()
        pattern = r"(?P<method>[A-Z]+)\s+(?P<info>/\S*)"
        try:
            env = re.match(pattern, request).groupdict()
        except:
            connfd.close()
            return
        else:
            data = connect_frame(env)
            if data:
                self.response(connfd,data)

    # 将数据整理为response格式发送给浏览器
    def response(self, connfd, data):
        """
        :param connfd:和网页交互的套接字
        :param data:服务器后端返回的内容
        """
        # data {"status":"200", "data":"content"}
        if data["status"] == "200":
            responseHeaders = "HTTP/1.1 200 OK\r\n"
            responseHeaders += "Content-Type:text/html\r\n"
            responseHeaders += "\r\n"
            responseBody = data["data"]

        elif data["status"] == "404":
            responseHeaders = "HTTP/1.1 404 NOT Found\r\n"
            responseHeaders += "Content-Type:text/html\r\n"
            responseHeaders += "\r\n"
            responseBody = data["data"]
        elif data["status"] == "500":
            pass

        # 将数据发送给浏览器
        response_data = responseHeaders + responseBody
        connfd.send(response_data.encode())







if __name__ == "__main__":
    httpd = HTTPServer(ADDR)
    httpd.server_forever()
