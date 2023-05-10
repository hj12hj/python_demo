from suds.client import Client

url = "http://localhost:333/ws/user?wsdl"  # 注意入参url为接口的wsdl地址
client = Client(url)
# 输出接口的结构化描述
# 调用接口方法，非常简单
result = client.service.userList({"name": "张三", "age": "18"})
