#coding=utf-8
import requests
import argparse
import datetime
import re
from prettytable import PrettyTable
now = datetime.datetime.now()

tomorrow = now+datetime.timedelta(days=1)
tomorrow = tomorrow.strftime('%Y-%m-%d')
print tomorrow

argument = argparse.ArgumentParser()
argument.add_argument('--fromcity','-f',default='hangzhoudong')
argument.add_argument('--tocity','-t',default='xiamen')
argument.add_argument('--date','-d',default=tomorrow)
# argument.add_argument('-d',action='store_true')
args =argument.parse_args()

from_station =  args.fromcity
to_station = args.tocity
Date = args.date

stationlist_url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
r = requests.get(stationlist_url, verify=False)
stationlist = r.content

ToStation = ''
FromStation = ''

placea = stationlist.find(from_station)
placeb = stationlist.find(to_station)

for i in range(-4,-1):
	FromStation += stationlist[placea+i]
for i in range(-4,-1):
	ToStation += stationlist[placeb+i]

query_url='https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate='+Date+'&from_station='+FromStation+'&to_station='+ToStation
r = requests.get(query_url,verify=False)


with open('json.txt','w') as fp:
	 fp.write(str(r.json()))

if 'datas' in r.json()["data"]:
	rj = r.json()["data"]["datas"]
	pt = PrettyTable()

	header = '车次 车站 到站时间 时长 一等座 二等座 软卧 硬卧 硬座 无座'.split()
	pt._set_field_names(header)

	for x in rj:
		ptrow = []
		ptrow.append(x["station_train_code"])
		ptrow.append('\n'.join([x["from_station_name"],x["to_station_name"]]))
		ptrow.append('\n'.join([x["start_time"], x["arrive_time"]]))
		ptrow.append(x["lishi"].replace(':','h')+'m')
		ptrow.append(x['zy_num'])
		ptrow.append(x['ze_num'])
		ptrow.append(x['rw_num'])
		ptrow.append(x['yw_num'])
		ptrow.append(x['yz_num'])
		ptrow.append(x['wz_num'])
		pt.add_row(ptrow)
	print pt
else :
	print '这两个站点没有直达列车'