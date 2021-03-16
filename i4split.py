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


targe_filename = "HBYC_Line2_Kiln_2021_Jan_12_28sorted.csv"



#实际处理 注释掉这行
# path = "HXDataSample/" + targe_filename

path = "HXProcessedData/" + targe_filename

newpath_train = "HXProcessedData/HBYC_Line2_Kiln_2021_Jan_12_28train.csv"
newpath_test = "HXProcessedData/HBYC_Line2_Kiln_2021_Jan_12_28test.csv"

bufsize = 65536*6*5
#实际处理 注释掉这行
# bufsize = 5000

#窑味料量
# Feeding_index = 28

# 本次只考虑使用头煤 HeadCoal_index
HeadCoal_index = 29

def process(lines):
    rows0, rows1 = [], []
    for i in range(0, len(lines)):

        if i % 5 == 0:
            rows1.append(lines[i])
        else:
            rows0.append(lines[i])
    return rows0, rows1
     






def main():

    # print(filter_spans[0][0], filter_spans[0][1])
    with open(path, encoding="UTF-8") as infile:
        while True:
            lines = infile.readlines(bufsize)
            print('len(lines)=', len(lines))
            if not lines:
                break

            rows0, rows1 = process(lines)
            print('len(rows)=', len(rows0), len(rows1))
            # print('process len(rows)=', len(rows), rows, '-'*10, '\n')
            # for r in rows:
            #     print(r, '#'*10, '\n')
            with open(newpath_train, "a", newline="") as csvfile:                            
                writer = csv.writer(csvfile) 

                # if write_count == 0:
                #     writer.writerow(header)
                # write_count += 1
                for row in rows0:
                    writer.writerow(row.split(','))

            with open(newpath_test, "a", newline="") as csvfile:                            
                writer = csv.writer(csvfile) 

                # if write_count == 0:
                #     writer.writerow(header)
                # write_count += 1
                for row in rows1:
                    writer.writerow(row.split(','))

if __name__ == "__main__":
    main()
