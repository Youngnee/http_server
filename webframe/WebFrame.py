"""
模拟网站后端应用程序工作
"""

from socket import *
import json
from settings import *
from select import select
from urls import *  # urls模块

frame_address = (frame_ip, frame_port)


# 应用类,将功能封装在类中
class Application(object):
    """
    功能实现类
    """

    def __init__(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, DEBUG)
        self.sockfd.bind(frame_address)

    def start(self):
        self.sockfd.listen(5)
        print("Listen the port: %d" % frame_port)
        rlist = [self.sockfd]
        wlist = []
        xlist = []

        # select IO多路复用监听请求
        while True:
            rs, ws, xs = select(rlist, wlist, xlist)
            for r in rlist:
                if r is self.sockfd:
                    connfd, addr = r.accept()
                    rlist.append(connfd)
                else:
                    self.handle(r)
                    rlist.remove(r)

    def handle(self, connfd):
        """
        处理请求回复
        :param connfd:连接套接字
        """
        request = connfd.recv(1024).decode()
        request = json.loads(request)  # 转换为请求字典
        # request ==> {"":"", "",""}
        if request["method"] == "GET":
            if request["info"] == "/" or request["info"][-5:] == ".html":
                response = self.get_html(request["info"])
            else:
                response = self.get_data(request["info"])
        elif request["method"] == "POST":
            pass

        response = json.dumps(response)
        connfd.send(response.encode())
        connfd.close()


    def get_html(self, info):
        if info == "/":
            filename = STATIC_DIR + "/index.html"
        else:
            filename = STATIC_DIR + info
        try:
            fd = open(filename)
        except Exception:
            with open(STATIC_DIR + "/404.html") as f:
                data = f.read()
                return {"status": "404", "data": data}
        else:
            return {"status": "200", "data": fd.read()}

    def get_data(self, info):
        for url, func in urls:
            if url == info:
                return {"status": "200", "data": func()}
        return {"status": "404", "data": "Sorry..."}


if __name__ == '__main__':
    app = Application()
    app.start()
