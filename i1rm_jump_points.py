import csv


targe_filename = "HBYC_Line2_Kiln_2021_Jan_12.csv"

path = "HXData/" + targe_filename

#实际处理 注释掉这行
path = "HXDataSample/" + targe_filename

newpath = "ProcessedData/" + targe_filename

bufsize = 65536


def process(lines):
    rows = []
    for i in range(0, len(lines)):
        if "两次不一致，进来..." in lines[i] and i - 1 >= 0 and i + 2 < len(lines):
            result = handleline(lines[i - 1], lines[i], lines[i + 1], lines[i + 2])
            if result is not None:
                rows.append(result)
    print("processing...", len(rows), " rows")
    return rows


def handleline(line0, line1, line2, line3):
    l0 = line0[line0.rfind("  ") + 2 :]
    if "s4=0" in l0:
        DI = l0[l0.find(":") + 1 : l0.find(",")]

        timediff = line2[line2.rfind("  ") + 2 : -1]

        bag_num = line3[line3.rfind("num:") + 4 : -1]

        # print(line0, line1, line2, line3)
        if (
            "警告，计算连包" in bag_num
            or "MyScreen" in timediff
            or "Thread" in timediff
            or "Thread" in bag_num
        ):
            return None
        else:
            return (DI, timediff, bag_num)


def main():
    with open(path, encoding="UTF-8") as infile:
        while True:
            lines = infile.readlines(bufsize)

            if not lines:
                break

            rows = process(lines)
            with open(newpath, "a", newline="") as csvfile:
                fieldnames = ["DI", "timediff", "bag_num"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                for row in rows:
                    writer.writerow(
                        {"DI": row[0], "timediff": row[1], "bag_num": row[2]}
                    )


if __name__ == "__main__":
    main()
