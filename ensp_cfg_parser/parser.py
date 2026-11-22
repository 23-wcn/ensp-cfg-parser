from pathlib import Path
from typing import List, Dict, Optional
from pydantic import BaseModel


class Interface(BaseModel):
    name: str
    description: Optional[str] = None
    ip: Optional[str] = None
    mask: Optional[str] = None
    status: Optional[str] = None


class Route(BaseModel):
    destination: str
    mask: str
    next_hop: Optional[str] = None
    out_interface: Optional[str] = None
    protocol: Optional[str] = None


class EnspCfgInfo(BaseModel):
    device_name: Optional[str] = None
    interfaces: List[Interface] = []
    routes: List[Route] = []


class EnspCfgParser:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.info = EnspCfgInfo()

    def parse(self) -> EnspCfgInfo:
        if not self.file_path.exists():
            raise FileNotFoundError(f"文件不存在：{self.file_path}")
        lines = self.file_path.read_text(encoding="utf-8", errors="ignore").splitlines()

        current_intf: Optional[Interface] = None
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 设备名称 sysname
            if line.startswith("sysname "):
                self.info.device_name = line.split(" ", 1)[1]
                continue

            # 进入接口视图
            if line.startswith("interface "):
                intf_name = line.split(" ", 1)[1]
                current_intf = Interface(name=intf_name)
                self.info.interfaces.append(current_intf)
                continue

            # 接口IP地址
            if current_intf and line.startswith(" ip address "):
                parts = line.split()
                if len(parts) >= 4:
                    current_intf.ip = parts[2]
                    current_intf.mask = parts[3]
                continue

            # 接口描述
            if current_intf and line.startswith(" description "):
                current_intf.description = line.split(" ", 1)[1]
                continue

            # 接口shutdown
            if current_intf and line == " shutdown":
                current_intf.status = "shutdown"
                continue

            # 静态路由 ip route-static
            if line.startswith("ip route-static "):
                parts = line.split()
                if len(parts) >= 4:
                    rt = Route(
                        destination=parts[2],
                        mask=parts[3],
                        next_hop=parts[4] if len(parts)>=5 else None,
                        protocol="static"
                    )
                    self.info.routes.append(rt)
                continue
        return self.info


if __name__ == "__main__":
    p = EnspCfgParser("test.cfg")
    res = p.parse()
    print("设备名称：", res.device_name)
    print("\n====接口信息====")
    for i in res.interfaces:
        print(f"{i.name} | {i.ip}/{i.mask} | {i.description} | {i.status}")
    print("\n====路由信息====")
    for r in res.routes:
        print(f"{r.destination}/{r.mask} -> {r.next_hop}")
