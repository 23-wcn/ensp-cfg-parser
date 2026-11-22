```
# ensp-cfg-解析器
华为eNSP .cfg配置文件解析工具

## ✨ 功能
- 解析华为设备cfg配置，自动提取设备名称
- 提取接口信息：接口名、IP地址、掩码、描述、shutdown状态
- 提取静态路由：目标网段、掩码、下一跳
- 命令行直接打印结果，支持导出Excel表格

## 📦 安装依赖
```bash
py -m pip install -r requirements.txt
```

# 🚀 使用示例

直接在控制台打印解析结果

py -m ensp_cfg_parser.cli r1.cfg


- 解析并导出Excel

py -m ensp_cfg_parser.cli r1.cfg -o result.xlsx



# 📁 目录结构

ensp-cfg-parser/

├── ensp_cfg_parser/      # 源码包

│   ├── __init__.py

│   ├── parser.py         # 解析核心

│   └── cli.py            # 命令行入口

├── examples/             # 示例cfg文件

├── tests/                # 测试用例

├── requirements.txt      # 依赖

└── README.md



# ⚠️ 说明

目前只支持华为 VRP 静态路由、基础接口配置解析，后续持续扩展 OSPF、ACL 等功能。
