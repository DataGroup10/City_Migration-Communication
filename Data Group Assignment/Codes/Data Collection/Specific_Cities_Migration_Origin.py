# -*- coding: utf-8 -*-
import requests
import json
import time
import xlrd
import xlwt
from ChineseAdminiDivisionsDict import CitiesCode, ProvinceCode

def migration_all_date(areaname, classname, no, direction): #定义生成不同时期，不同城市，不同迁徙方向
    if no == -1 :
        no = CitiesCode[str(areaname)]
    #######创建一个workbook########
    workbook = xlwt.Workbook(encoding = 'utf-8')    # 创建一个workbook 设置编码
    worksheet = workbook.add_sheet('Sheet', cell_overwrite_ok=True)    # 创建一个worksheet
    #################写入行头各城市代码及其城市名###############
    if direction == 'in' :
        nameofdire = '迁入来源地'
    if direction == 'out':
        nameofdire = '迁出目的地'
    CitiesOrder = {}                         #存放城市序号的空字典
    worksheet.write(0 , 0 , label='城市代码')                      #写入行头
    worksheet.write(0 , 1 , label=str(nameofdire))                 #写入行头
    times = 1
    for key , value in CitiesCode.items():
        worksheet.write(times , 0 , label=str(value))                #写入城市代码
        worksheet.write(times , 1 , label=str(key))                  #写入城市名
        CitiesOrder[str(key)] = times                           #写入城市序号字典
        times += 1
    ########################设定日期##############################
    datelist = []                                    #日期列表
    counter_data = 2                                 #日期计数器
    # for date1 in range(20230101,20230132):           #一月份
    #     datelist.append(date1)
    # for date2 in range(20230201,20230229):           #二月份
    #     datelist.append(date2)
    # for date3 in range(20230301,20230332):           #三月份
    #     datelist.append(date3)
    for date4 in range(20230401,20230431):           #四月份
        datelist.append(date4)
    for date5 in range(20230501,20230532):           #五月份
        datelist.append(date5)
    for date6 in range(20230601,20230631):           #六月份
        datelist.append(date6)
    # for date7 in range(20230701,20230732):           #七月份
    #     datelist.append(date7)
    # for date8 in range(20230801,20230832):           #八月份
    #     datelist.append(date8)
    # for date9 in range(20230901,20230931):           #九月份
    #     datelist.append(date9)
    # for date10 in range(20231001,20231032):           #十月份
    #     datelist.append(date10)
    for date in datelist:                            #遍历所有日期
        datename = date
        time.sleep(1)
        url=f'http://huiyan.baidu.com/migration/cityrank.jsonp?dt={classname}&id={no}&type=move_{direction}&date={date}'
        print(url)
        response=requests.get(url, timeout=2) #发出请求并json化处理
        time.sleep(1)
        r=response.text[4:-1] #去头去尾
        data_dict=json.loads(r) #字典化
        if data_dict['errmsg']=='SUCCESS':
            data_list=data_dict['data']['list']
            time.sleep(1)
            ################写入###############
            worksheet.write(0 , counter_data , label=datename)             #写入表头————日期
            for a in range(len(CitiesCode)):
                worksheet.write(a+1 , counter_data , label=0)              #先把当前日期下该列所有城市值置0
            ############获取数据###########
            for i in range (len(data_list)):
                city_name=data_list[i]['city_name'] #城市名
                value=data_list[i]['value']         #当日迁徙量所占百分比值
            ##############写入#############
                worksheet.write(CitiesOrder[str(city_name)] , counter_data , label=value)             #查找城市序号字典，在对应的行里写入相应的值
            counter_data += 1                                 #日期计数器自加一
    workbook.save(f"{areaname}-{nameofdire}.xls")      #保存


def circu_exe_direction(areaname,classname,no):
    mukous = ['in','out']
    for mukou in mukous:
        migration_all_date(areaname,classname,no,mukou)
    print(str(areaname)+'---','完成')


if __name__=="__main__":
    # circu_exe_direction('淄博市','city',-1)
    circu_exe_direction('天津市', 'city', -1)
    # circu_exe_direction('江门市', 'city', -1)
    # circu_exe_direction('黔西南州', 'city', -1)

    print('全部完成')
