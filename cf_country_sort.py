import re
import os

INPUT_FILE = "nodes.txt"
OUTPUT_DIR = "country_nodes"


def main():

    if not os.path.exists(INPUT_FILE):
        print(f"错误：找不到 {INPUT_FILE}")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    counters = {}
    country_lines = {}

    with open(INPUT_FILE, "r", encoding="utf-8") as f:

        for line in f:
            line = line.strip()

            if not line:
                continue

            # 删除末尾的 [域名 延迟]
            # 例如：
            # [cf.877774.xyz 68ms]
            line = re.sub(r"\s*\[.*?\]\s*$", "", line)

            # 提取国家代码
            # 例如：#JP 电信优选
            match = re.search(
                r"#([A-Z]{2})\s+电信优选",
                line
            )

            if not match:
                print(f"跳过无法识别的行：{line}")
                continue

            country = match.group(1)

            # 初始化该国家
            if country not in counters:
                counters[country] = 0
                country_lines[country] = []

            # 该国家编号 +1
            counters[country] += 1
            number = counters[country]

            # 直接使用函数替换，避免 \11 这种问题
            line = re.sub(
                r"#[A-Z]{2}\s+电信优选",
                lambda m: m.group(0) + str(number),
                line,
                count=1
            )

            country_lines[country].append(line)

    # 输出分类文件
    for country, lines in country_lines.items():

        output_file = os.path.join(
            OUTPUT_DIR,
            f"{country}.txt"
        )

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
            f.write("\n")

        print(
            f"{country}: {len(lines)} 个节点 -> {output_file}"
        )


if __name__ == "__main__":
    main()
