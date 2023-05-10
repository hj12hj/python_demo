from mitmproxy import http


def request(flow: http.HTTPFlow) -> None:
    # 获取请求的 URL
    url = flow.request.pretty_url

    # 判断请求的 URL 是否为本地请求并包含所需路径
    if url.startswith("http://10.7.4.10:9000") and "/reportCustomConfig/getDataSourceMap" in url:
        # 打印请求信息
        print(f"Intercepted request to {url}")
        print(f"Request headers: {flow.request.headers}")
        print(f"Request content: {flow.request.text}")


def response(flow: http.HTTPFlow) -> None:
    # 获取响应的 URL
    print(flow.response.content, type(flow.response.content))
    flow.response.content = b'{"code": 0, "msg": "success", "data": "1"}'
