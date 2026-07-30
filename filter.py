import json
import urllib.request

CONFIG_FILE = "config.json"
OUTPUT_FILE = "fish.json"


def load_json(file):
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def download(url):
    print("=" * 40)
    print("正在下载接口：")
    print(url)
    print("=" * 40)

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(
                r.read().decode("utf-8")
            )
    except Exception as e:
        raise Exception(f"下载失败：{e}")


def main():

    cfg = load_json(CONFIG_FILE)

    data = download(cfg["source"])

    if "sites" not in data:
        raise Exception("接口异常：没有 sites 字段")

    sites = data["sites"]

    print(f"接口站点数量：{len(sites)}")

    keep_keys = set(cfg.get("keep_keys", []))
    rename = cfg.get("rename", {})
    order = cfg.get("order", [])

    site_map = {}

    # 保留指定站点
    for site in sites:

        key = site.get("key")

        if key not in keep_keys:
            continue

        new_site = site.copy()

        if key in rename:
            new_site["name"] = rename[key]

        site_map[key] = new_site

    # 按顺序输出
    new_sites = []

    for key in order:
        if key in site_map:
            new_sites.append(site_map[key])

    data["sites"] = new_sites

    save_json(OUTPUT_FILE, data)

    print("=" * 40)
    print(f"最终保留：{len(new_sites)} 个站点")
    print("=" * 40)

    for i, site in enumerate(new_sites, 1):
        print(
            f"{i:02d}. {site['name']} ({site['key']})"
        )

    print("=" * 40)
    print(f"已生成 {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
