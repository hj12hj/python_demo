from mitmproxy import http, ctx
from multiprocessing import Lock


class Filter:
    def __init__(self, filter_info):
        self.log_info = ""
        self.mutex = Lock()
        self.filter_info = filter_info
        self.response_file = None
        self.switch_on = False
        self.log_file = "log.txt"

    def log(self, info) -> None:
        self.log_info += f"{info}\n\n"

    def write_log(self, mode="w+") -> None:
        self.mutex.acquire()
        with open(self.log_file, mode) as f:
            f.write(self.log_info)
        self.mutex.release()

    def is_target_flow(self, flow: http.HTTPFlow) -> bool:
        for info in self.filter_info:
            if info["str_in_url"] in flow.request.url:
                self.log_file = info["log_file"]
                self.switch_on = info["switch_on"]
                if info["response_file"] != None:
                    self.response_file = info["response_file"]
                return True
        else:
            return False

    def modify_response(self, flow: http.HTTPFlow) -> http.HTTPFlow:
        if self.switch_on and self.response_file:
            with open(self.response_file, "r", encoding="utf-8") as f:
                flow.response.content = f.read().encode()
        return flow

    def request(self, flow: http.HTTPFlow) -> None:
        if self.is_target_flow(flow):
            self.log_info = ""
            self.log(f"——METHOD——\n{flow.request.method}")
            self.log(f"——HOST——\n{flow.request.pretty_host}")
            self.log(f"——URL——\n{flow.request.pretty_url}")
            query = [i + ":" + flow.request.query[i] + "\n" for i in flow.request.query]
            self.log(f"——QUERY STRING——\n{''.join(query)}")
            if flow.request.urlencoded_form:
                form = [i + ":" + flow.request.urlencoded_form[i] + "\n" for i in flow.request.urlencoded_form]
                self.log(f"——FORM——\n{''.join(form)}")
            self.write_log()

    def response(self, flow: http.HTTPFlow) -> None:
        if self.is_target_flow(flow):
            self.log_info = ""
            self.log(f"——RESPONSE before modified——\n{flow.response.content.decode(encoding='UTF-8')}")
            flow = self.modify_response(flow)
            self.log(f"——RESPONSE after modified——\n{flow.response.content.decode(encoding='UTF-8')}")
            self.write_log(mode="a")


filter_info = [
    {
        "str_in_url": "getSimpleNews",
        "log_file": "getSimpleNews_log.txt",
        "switch_on": True,
        "response_file": "getSimpleNews_response.txt",
    },
    {
        "str_in_url": "getQQNewsComment",
        "log_file": "getQQNewsComment_log.txt",
        "switch_on": True,
        "response_file": None,
    }
]
addons = [
    Filter(filter_info)
]


if __name__ == '__main__':
    pass