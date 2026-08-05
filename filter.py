import json
import urllib.request
import os
from datetime import datetime, timezone, timedelta


# ==========================
# 原作者源接口（固定）
# ==========================

SOURCE = "https://9280.kstore.vip/aiwex.json"


# 文件

CONFIG_FILE = "config.json"

OUTPUT_FILE = "fish.json"



# ==========================
# 读取 JSON
# ==========================

def load_json(file):

    with open(
        file,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



# ==========================
# 保存 JSON
# ==========================

def save_json(file, data):

    with open(
        file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )



# ==========================
# 获取源接口
# ==========================

def fetch_source():

    print()
    print("====================")
    print("正在获取接口:")
    print(SOURCE)
    print("====================")


    req = urllib.request.Request(

        SOURCE,

        headers={
            "User-Agent":
            "Mozilla/5.0"
        }

    )


    try:

        with urllib.request.urlopen(

            req,

            timeout=30

        ) as response:


            text = response.read().decode(

                "utf-8-sig"

            )


            return json.loads(text)



    except Exception as e:

        raise Exception(

            f"接口获取失败: {e}"

        )



# ==========================
# 主程序
# ==========================

def main():


    start_time = datetime.now()



    if not os.path.exists(CONFIG_FILE):

        raise Exception(

            "找不到 config.json"

        )



    cfg = load_json(CONFIG_FILE)



    data = fetch_source()



    source_sites = data.get(

        "sites",

        []

    )



    if not source_sites:

        raise Exception(

            "源接口没有 sites 数据"

        )



    order = cfg.get(

        "sites_order",

        []

    )



    rename = cfg.get(

        "rename",

        {}

    )



    site_map = {}



    print()

    print("====================")

    print("开始过滤站点...")

    print("====================")



    for site in source_sites:


        key = site.get(

            "key"

        )


        if not key:

            continue



        if key not in order:

            continue



        if key in site_map:

            print(

                "发现重复 key:",

                key

            )



        new_site = site.copy()



        if key in rename:

            new_site["name"] = rename[key]



        site_map[key] = new_site




    sites = []

    missing = []



    for key in order:


        if key in site_map:

            sites.append(

                site_map[key]

            )

        else:

            missing.append(key)



    if missing:

        print()

        print("====================")

        print("以下站点未找到:")

        for m in missing:

            print("-", m)

        print("====================")



    if len(sites) == 0:

        raise Exception(

            "没有匹配到任何站点，请检查 config.json"

        )



    result = data.copy()

    result["sites"] = sites



    save_json(

        OUTPUT_FILE,

        result

    )



    # ==========================
    # UTC+8 时间
    # ==========================

    end_time = datetime.now(
        timezone(
            timedelta(hours=8)
        )
    )


    print()

    print("====================")

    print("生成完成")

    print(

        "站点数量:",

        len(sites)

    )

    print(

        "耗时:",

        str(datetime.now() - start_time)

    )

    print(

        "时间:",

        end_time.strftime(

            "%Y-%m-%d %H:%M:%S"

        )

    )

    print("====================")



    for i, s in enumerate(

        sites,

        1

    ):

        print(

            f"{i:02d}. "

            f"{s.get('name','')}"

            f" [{s.get('key','')}]"

        )



    print("====================")

    print(

        "输出文件:",

        OUTPUT_FILE

    )

    print("====================")




if __name__ == "__main__":

    main()
