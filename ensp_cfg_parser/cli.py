import click
from .parser import EnspCfgParser
import json


@click.command()
@click.argument("cfg_file")
@click.option("--json", "-j", is_flag=True, help="输出json格式")
def main(cfg_file, json):
    parser = EnspCfgParser(cfg_file)
    res = parser.parse()
    if json:
        click.echo(res.model_dump_json(indent=2, ensure_ascii=False))
    else:
        click.echo(f"设备主机名: {res.hostname}")
        click.echo("===接口列表===")
        for iface in res.interfaces:
            click.echo(f"{iface.name}  IP:{iface.ip}/{iface.mask}")
        click.echo("===静态路由===")
        for rt in res.static_routes:
            click.echo(f"{rt.destination}/{rt.mask} -> {rt.next_hop}")


if __name__ == "__main__":
    main()
