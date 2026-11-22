from .models import Device, Interface, StaticRoute
from pathlib import Path


class EnspCfgParser:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.lines = []
        self.device = Device(hostname="unknown")

    def load_file(self):
        with open(self.file_path, "r", encoding="utf-8", errors="ignore") as f:
            self.lines = [line.strip() for line in f if line.strip()]

    def parse(self):
        self.load_file()
        for line in self.lines:
            # 主机名 sysname
            if line.startswith("sysname "):
                self.device.hostname = line.split(" ", 1)[1]
            # 接口IP
            elif line.startswith("interface "):
                if_name = line.split(" ", 1)[1]
                current_if = Interface(name=if_name)
            elif line.startswith(" ip address "):
                parts = line.split()
                if len(parts) >=4:
                    current_if.ip = parts[2]
                    current_if.mask = parts[3]
                    self.device.interfaces.append(current_if)
            # 静态路由 ip route-static
            elif line.startswith("ip route-static "):
                parts = line.split()
                if len(parts)>=5:
                    dst = parts[2]
                    mask = parts[3]
                    nh = parts[4]
                    self.device.static_routes.append(StaticRoute(
                        destination=dst, mask=mask, next_hop=nh
                    ))
        return self.device
