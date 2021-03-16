'''

目前汤总的意思是这样的，我们只保留最为稳定的那类数据，
不按照绝对值时间来删数据，按照比例来删，比如两次调整之间的时间是1个小时，那么我们只留中间20分钟的数据。
如果两次调整的间隔时间小于20分钟，就删掉这条数据。

汤总还说进一步缩减数据变化，使用30秒间隔、1分钟间隔，5分钟间隔的数据分别试试看。
30秒的看不出来，那就1分钟的数据，取一条，1分钟间隔就是1分钟取一条，5分钟取一条。取平均值吧

一分钟内就60个数的平均这样
所有的数值只要是数值类型 我就平均下

'''
import csv
from datetime import datetime, timedelta


targe_filename = "HBYC_Line2_Kiln_2021_Jan_12_28.csv"

path = "HXData/" + targe_filename

#实际处理 注释掉这行
# path = "HXDataSample/" + targe_filename

newpath = "HXProcessedData/" + targe_filename

bufsize = 65536*6*5
#实际处理 注释掉这行
# bufsize = 5000

#窑味料量
# Feeding_index = 28

# 本次只考虑使用头煤 HeadCoal_index
HeadCoal_index = 29

def process(lines):
    time_need_removed = []
    rows = []
    for i in range(0, len(lines)):

        items = lines[i].split(',')
        if items[0] not in ('timestamp'):
            d = datetime.strptime(items[0], "%Y/%m/%d %H:%M:%S")
            for span in filter_spans:
                if d >= span[0] and d <= span[1]:
                    rows.append(lines[i])
    return rows
     




time_points_of_changes = []
filter_spans = []

def scan_for_change(lines):
    global time_change

    for i in range(0, len(lines)):

        # print("窑喂料量Kiln_Feed_SP=", lines[i][28], 'Kiln_Burner_Coal_SP头煤=',lines[i][29])
        if i - 1 >= 0 and i + 1 < len(lines):
            # result = handleline(lines[i - 1], lines[i], lines[i + 1], lines[i + 2])
            items = lines[i].split(',')
            items_prev = lines[i-1].split(',')
            items_next = lines[i+1].split(',')
            if  (items_prev[HeadCoal_index] not in  ('Kiln_Burner_Coal_SP', '头煤') and \
                items_prev[HeadCoal_index] != items[HeadCoal_index] and  \
                items_prev[HeadCoal_index] != items_next[HeadCoal_index]):
                if items[0] not in time_points_of_changes:
                    time_points_of_changes.append(items[0])
                    print(items[0], ' changes!')

def main():
    global filter_spans

    with open(path, encoding="UTF-8") as infile:
        while True:
            lines = infile.readlines(bufsize)

            if not lines:
                break
            rows = scan_for_change(lines)
    print(len(time_points_of_changes), time_points_of_changes[0:10])

    
    # 找出想要保留的时间区间列表
    for i in range(0, len(time_points_of_changes)):
        if i + 1 < len(time_points_of_changes):
            d = datetime.strptime(time_points_of_changes[i], "%Y/%m/%d %H:%M:%S")
            d_next = datetime.strptime(time_points_of_changes[i+1], "%Y/%m/%d %H:%M:%S")
            # print(time_points_of_changes[i], time_points_of_changes[i+1])
            span = d_next - d
            print('#'*10, d, d_next)
            print(span, '@'*5, d+(span/3), d+(span*2/3))
            filter_spans.append((d+(span/3), d+(span*2/3)))

    print('\n')
    # print(filter_spans[0][0], filter_spans[0][1])
    with open(path, encoding="UTF-8") as infile:
        while True:
            lines = infile.readlines(bufsize)
            print('len(lines)=', len(lines))
            if not lines:
                break

            rows = process(lines)
            print('len(rows)=', len(rows))
            # print('process len(rows)=', len(rows), rows, '-'*10, '\n')
            # for r in rows:
            #     print(r, '#'*10, '\n')
            with open(newpath, "a", newline="") as csvfile:                            
                writer = csv.writer(csvfile) 

                # if write_count == 0:
                #     writer.writerow(header)
                # write_count += 1
                for row in rows:
                    writer.writerow(row.split(','))

if __name__ == "__main__":
    main()
