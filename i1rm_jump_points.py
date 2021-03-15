import csv
from datetime import datetime, timedelta

'''
根据csv原始数据中： 窑味料量、头煤的变化 去掉一定前后区间的间跃值

 10秒
 10分
 1小时

 https://stackoverflow.com/questions/16286991/converting-yyyy-mm-dd-hhmmss-date-time

'''
targe_filename = "HBYC_Line2_Kiln_2021_Jan_12_28.csv"

path = "HXData/" + targe_filename

#实际处理 注释掉这行
# path = "HXDataSample/" + targe_filename

newpath = "HXProcessedData/" + targe_filename

bufsize = 65536*6*3
#实际处理 注释掉这行
# bufsize = 5000

#窑味料量
Feeding_index = 28
HeadCoal_index = 29

def process(lines):
    time_need_removed = []

    for i in range(0, len(lines)):

        # print("窑喂料量Kiln_Feed_SP=", lines[i][28], 'Kiln_Burner_Coal_SP头煤=',lines[i][29])
        if i - 1 >= 0 and i + 1 < len(lines):
            # result = handleline(lines[i - 1], lines[i], lines[i + 1], lines[i + 2])
            items = lines[i].split(',')
            items_prev = lines[i-1].split(',')
            items_next = lines[i+1].split(',')
            
            '''
            排除掉文件开始2行，
            并且保证数值开始的这一行，之后的一行，和变化前的一行都不同（只有1行变化也许是异常)
            '''
            if  (items_prev[Feeding_index] not in  ('Kiln_Feed_SP', '窑喂料量') and \
                items_prev[Feeding_index] != items[Feeding_index] and  \
                items_prev[Feeding_index] != items_next[Feeding_index]) or \
                (items_prev[HeadCoal_index] not in  ('Kiln_Burner_Coal_SP', '头煤') and \
                items_prev[HeadCoal_index] != items[HeadCoal_index] and  \
                items_prev[HeadCoal_index] != items_next[HeadCoal_index]):
                d = datetime.strptime(items[0], "%Y/%m/%d %H:%M:%S")
                if d not in time_need_removed:
                    time_need_removed.append(d)
                    print(i, items_prev[Feeding_index],items[Feeding_index],items_next[Feeding_index], 
                        items_prev[HeadCoal_index],items[HeadCoal_index],items_next[HeadCoal_index],items[0])
                # 删除变化前后1分钟的值
                # d0 = d - timedelta(hours=0, minutes=1)
                # d1 = d + timedelta(hours=0, minutes=1)               
                # print('rm data between' , '>>'*5, items[0], d,'\n',  d0, d1)
    
    if len(time_need_removed) >= 1:
        print('time_need_removed', '>>'*10, time_need_removed)
        rows = []
        rm_count = 0
        for i in range(0, len(lines)):
            items = lines[i].split(',')
            if items[0] not in ('timestamp', '_Temp_f'):
                i_time = datetime.strptime(items[0], "%Y/%m/%d %H:%M:%S")
                for d in time_need_removed:
                    d0 = d - timedelta(hours=0, minutes=15)
                    d1 = d + timedelta(hours=0, minutes=15)
                    if i_time >= d0 and i_time <= d1:
                        rm_count += 1
                        print(i_time)
                    else:
                        rows.append(lines[i])
        print('after rm ', rm_count, 'len(rows)=', len(rows))
        return rows
    else:
        # rows = []
        # for i in range(0, len(lines)):
        #     rows.append(lines[i])
        # return rows
        return lines






# def get_header(path):
#     with open(path, 'r') as f:
#         d_reader = csv.DictReader(f)

#         #get fieldnames from DictReader object and store in list
#         headers = d_reader.fieldnames
#     return headers


def main():
    # header = get_header(path)
    # print('header=', header)
    # write_count = 0
    with open(path, encoding="UTF-8") as infile:
        while True:
            lines = infile.readlines(bufsize)
            print('len(lines)=', len(lines))
            if not lines:
                break

            rows = process(lines)
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
