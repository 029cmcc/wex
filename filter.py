import json
import urllib.request
import os


# ==========================
# 源接口地址
# ==========================

SOURCE = "https://9280.kstore.vip/aiwex.json"


# 输出文件

CONFIG_FILE = "config.json"

OUTPUT_FILE = "fish.json"



# ==========================
# 读取JSON
# ==========================

def load_json(file):

    with open(
        file,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



# ==========================
# 保存JSON
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

            "源接口没有sites数据"

        )



    # 排序列表

    order = cfg.get(

        "sites_order",

        []

    )



    # 名称替换

    rename = cfg.get(

        "rename",

        {}

    )



    site_map = {}



    print()

    print(

        "开始过滤站点..."

    )



    # ======================
    # 过滤+改名
    # ======================

    for site in source_sites:


        key = site.get(

            "key"

        )


        if not key:

            continue



        if key not in order:

            continue



        # 复制对象

        new_site = site.copy()



        # 改名字

        if key in rename:

            new_site["name"] = rename[key]



        site_map[key] = new_site




    # ======================
    # 按顺序输出
    # ======================

    sites = []



    for key in order:


        if key in site_map:


            sites.append(

                site_map[key]

            )



    if len(sites) == 0:

        raise Exception(

            "没有匹配到任何站点，请检查key"

        )



    # ======================
    # 保留源接口全部字段
    # ======================

    result = data.copy()


    result["sites"] = sites



    save_json(

        OUTPUT_FILE,

        result

    )



    print()

    print("====================")

    print(

        "生成完成"

    )

    print(

        "站点数量:",

        len(sites)

    )

    print("====================")



    for i, s in enumerate(

        sites,

        1

    ):

        print(

            f"{i:02d}. {s.get('name','')}"

            f"  [{s.get('key','')}]"

        )


    print("====================")

    print(

        f"输出文件: {OUTPUT_FILE}"

    )



if __name__ == "__main__":

    main()
