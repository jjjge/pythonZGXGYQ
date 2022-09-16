import re
import os
import xlwt

#获取数据
def getData1(data,):
    news=data
    # 新增确诊
    all_dict = {}
    all_dict['confirm_add'] = re.search('新增确诊病例(.*?)例',news).group(1)
    for k,v in all_dict.items():
        return v


def getData2(data):
    #获取新增无症状
    news=data
    all_dict = {}
    if re.search('新增无症状感染者(.*?)例', news) is None:
        all_dict['unnormal'] = 0
    else :all_dict['unnormal'] = re.search('新增无症状感染者(.*?)例', news).group(1)
    for k,v in all_dict.items():
        return v
def getData3(data):
    #获取时间
    news=data
    # 新增确诊
    all_dict = {}
    all_dict['pub_time'] = re.search('截至(.*?)24时', news).group(1)
    for k,v in all_dict.items():
        return v
#打开文件
if "__main__" == __name__:
    path = 'G:\develop/txtmmmm1'
    files = os.listdir(path)
    txts = []
    wb = xlwt.Workbook(encoding='uft-8')  # 新建一个Excel文件
    ws1 = wb.add_sheet('中国大陆')
    ws1.write(0, 0, '日期')
    ws1.write(0, 1, '新增确诊')
    ws1.write(0, 2, '新增无症状')
    #ws1.write(0, 3, '备注')
    # 创建各省新增病例表格
    ws2 = wb.add_sheet('各省确诊情况')
    ws3= wb.add_sheet('各省无症状情况')
    ws2.write(0, 0, '日期')
    ws3.write(0,0,'日期')
    provience=('河北','山西','辽宁','吉林','黑龙江','江苏','浙江','安徽','福建','江西','山东','河南','湖北','湖南','广东','海南','四川','贵州','云南','陕西','甘肃','青海','内蒙古','广西','西藏','宁夏','新疆','北京','天津','上海','重庆','香港','澳门','台湾')
    provience1 = ('河北', '山西', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南','广东', '海南', '四川', '贵州', '云南', '陕西', '甘肃', '青海', '内蒙古', '广西', '西藏', '宁夏', '新疆', '北京','天津', '上海', '重庆')
    row = 1  # 起始行
    col = 1 # 起始列
    temp = {}
    temp[32] = 0
    temp[33] = 0
    temp[34] = 0
    for pro in provience:
        #写入省份
        ws2.write(0,col,pro)
        ws3.write(0,col,pro)
        col = col + 1
    col = 1
    for file in files:  # 遍历
        position = path + '\\' + file
        with open(position, "r", encoding='utf-8') as f:
            data = f.read()  # 读取文件
            ws1.write(row,0,getData3(data))#写时间
            ws1.write(row,1,getData1(data))#写确诊
            ws1.write(row,2,getData2(data))#写无症状





            #各个省份新增确诊情况
            ws2.write(row, 0, getData3(data))  # 写时间
            ws3.write(row, 0, getData3(data))
            #截取新增确诊文本
            ind = data.find('本土病例')
            string = data[ind + 1:]
            ind = string.find('）')
            string = string[:ind]
            #截取无症状感染部分文本
            ind = data.find('新增无症状感染者')
            string1 = data[ind + 1:]
            ind = string1.find('）')
            string1 = string1[:ind]
            all_dict = {}
            all_dict1 = {}
            all_dict3 = {}

            #清空表
            all_dict.clear()
            all_dict1.clear()
            all_dict3.clear()

            for pro in provience1 :
                #遍历各省份确诊
                if re.search(pro+'(.*?)例，', string) is None:
                    all_dict[pro] = 0
                else:
                    all_dict[pro] = re.search(pro+'(.*?)例，', string).group(1)
                #遍历各省份无症状
                if re.search(pro+'(.*?)例，', string1) is None:
                    all_dict1[pro] = 0
                else:
                    all_dict1[pro] = re.search(pro+'(.*?)例，', string1).group(1)

            col = 1
            # 写确诊人数
            for k, v in all_dict.items():
                ws2.write(row, col, v)
                col = col + 1
            #写无症状人数
            col = 1
            for k, v in all_dict1.items():
                ws3.write(row, col, v)
                #print(k, v)#输出省份,人数
                #print(col,getData3(data))
                col = col + 1

            #读写港澳台人数
            col = 32

            if re.search('香港特别行政区(.*?)例（', data) is None:
                all_dict3['香港'] = 0
            else:
                all_dict3['香港'] = re.search( '香港特别行政区(.*?)例', data).group(1)
            if re.search('澳门特别行政区(.*?)例', data) is None:
                all_dict3['澳门'] = 0
            else:
                all_dict3['澳门'] = re.search( '澳门特别行政区(.*?)例', data).group(1)
            if re.search('台湾地区(.*?)例', data) is None:
                all_dict3['台湾'] = 0
            else:
                all_dict3['台湾'] = re.search( '台湾地区(.*?)例', data).group(1)

            for k, v in all_dict3.items():
                v=int(v)
                ws2.write(row, col, v-temp[col])
                #print(v, temp[col])
                temp[col]=v
                col = col + 1

            row = row + 1
    wb.save("疫情情况.xlsx")

