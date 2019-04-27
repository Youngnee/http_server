## 项目分析

1. 功能:
    httpserver
        * 获取http请求
        * 解析http请求
        * 将请求发送给WebFrame
        * 从WebFrame获取反馈数据
        * 将数据组织为Response格式发送给客户

    WebFrame
        * 从 httpserver获取请求
        * 根据请求处理逻辑或者是数据
            1. 静态网页
            2. 其他数据
        * 将数据反馈给httpserver

2. 升级点
    * 采用httpserver和应用分离的模式, 降低耦合
    * 采用了用户配置文件确定软件功能的思路
    * 在数据处理端,仿照后端框架的处理思想

3. 技术点分析
    * httpserver需要建立两个套接字,分别和两端通信
    * WenFrame部分采用了多路复用接收请求

4. 项目结构

5. 交互数据格式协议
    httpserver --> webframe {method:"GET", info:"/"}

    webframe --> httpserver {status:"200", data:"cccc"}



cookie:
    import json()

    json.dumps()将python字典转换为json字符串
    json.loads()将json字符串解析为python字典

    json.dumps(dict)-->'{"a":1, b:"abcd"}'
    json.loads()







