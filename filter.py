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
    print("================")
    print("下载接口：")
    print(url)

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
        raise Exception(f"接口获取失败：{e}")


def main():
    cfg = load_json(CONFIG_FILE)

    data = download(cfg["source"])

    if "sites" not in data:
        raise Exception("接口异常，没有 sites 字段")

    sites = data["sites"]

    print("================")
    print("原始站点：", len(sites))

    keep_keys = set(cfg.get("keep_keys", []))
    remove_keywords = cfg.get("remove_keywords", [])
    rename = cfg.get("rename", {})
    order = cfg.get("order", [])

    result = []

    for site in sites:
        key = site.get("key", "")
        name = site.get("name", "")

        # 优先保留
        if key in keep_keys:
            new_site = site.copy()

            if key in rename:
                new_site["name"] = rename[key]

            result.append(new_site)
            continue

        # 关键词过滤
        text = key + name

        remove = False

        for word in remove_keywords:
            if word in text:
                remove = True
                break

        if remove:
            continue

    # 建立映射
    site_map = {
        site["key"]: site
        for site in result
    }

    new_sites = []
    used = set()

    # 按配置排序
    for key in order:
        if key in site_map:
            new_sites.append(site_map[key])
            used.add(key)

    # 没写到 order 的放最后
    for key, site in site_map.items():
        if key not in used:
            new_sites.append(site)

    data["sites"] = new_sites

    print("================")
    print("过滤后站点：", len(new_sites))
    print("================")

    for site in new_sites:
        print(
            site.get("key"),
            "|",
            site.get("name")
        )

    print("================")

    save_json(OUTPUT_FILE, data)

    print("生成完成：", OUTPUT_FILE)


if __name__ == "__main__":
    main()
