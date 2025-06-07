from mitmproxy import http
import re

class ProxyInterceptor:
    def request(self, flow: http.HTTPFlow) -> None:
        # 拦截Cursor AI请求
        if "cursor.so" in flow.request.pretty_host:
            print(f"拦截到Cursor请求: {flow.request.url}")
            
            # 修改目标地址为本地服务
            flow.request.host = "localhost"
            flow.request.port = 8000
            flow.request.scheme = "http"
            
            # 保留原始路径和参数
            print(f"转发到本地: http://localhost:8000{flow.request.path}")

addons = [ProxyInterceptor()]

if __name__ == "__main__":
    from mitmproxy.tools.main import mitmdump
    mitmdump(["-s", __file__])
