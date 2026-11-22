import click
from .parser import EnspCfgParser
import pandas as pd


@click.command()
@click.argument("cfg_file")
@click.option("--out", "-o", default=None, help="导出excel文件路径")
def main(cfg_file, out):
    """华为eNSP cfg配置解析工具"""
    try:
        parser = EnspCfgParser(cfg_file)
        data = parser.parse()
        click.echo(f"✅ 设备名称：{data.device_name}")

        # 打印接口
        click.echo("\n【接口列表】")
        intf_rows = []
        for i in data.interfaces:
            row = {"接口": i.name, "IP": i.ip, "掩码": i.mask, "描述": i.description, "状态": i.status}
            click.echo(f"{i.name:12} {i.ip or '-':15} {i.description or ''}")
            intf_rows.append(row)

        # 打印路由
        click.echo("\n【路由表】")
        route_rows = []
        for rt in data.routes:
            row = {"目标": rt.destination, "掩码": rt.mask, "下一跳": rt.next_hop, "出接口": rt.out_interface, "协议": rt.protocol}
            click.echo(f"{rt.destination}/{rt.mask} -> {rt.next_hop}")
            route_rows.append(row)

        # 导出Excel
        if out:
            with pd.ExcelWriter(out) as writer:
                pd.DataFrame(intf_rows).to_excel(writer, sheet_name="接口", index=False)
                pd.DataFrame(route_rows).to_excel(writer, sheet_name="路由", index=False)
            click.echo(f"\n📄 已导出到：{out}")
    except Exception as e:
        click.echo(f"❌ 错误：{e}", err=True)


if __name__ == "__main__":
    main()
