#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb
import time
import datetime
#判断字段数据是否为时间格式
def is_valid_time(str):
	try:
		time.strptime(str,"%Y-%m-%d %H:%M:%S")
		return True
	except:
		return False

db = MySQLdb.connect(host="localhost",user="root",passwd="captain",db="testDB",charset='utf8')
cursor = db.cursor()
selectAll = "select * from example"
try:
	cursor.execute(selectAll)
	results = cursor.fetchall()
	str2 = "2015-06-01 09:52:15"
	t2 = time.strptime(str2,"%Y-%m-%d %H:%M:%S")
	y2,m2,d2,h2,n2,s2 = t2[0:6]
	datet2 = datetime.datetime(y2,m2,d2,h2,n2,s2)
	for rows in results:
		customerId = rows[0]
		chanceId = rows[1]
		birthday = rows[2]
		createDate = rows[3]
		registerPlace = rows[4]
		school = rows[5]
		testArea = rows[6]
		position = rows[7]
		education = rows[8]
		loginTime = rows[9]
		createtime = rows[10]
		netPayMoney = rows[11]
		couponMoney = rows[12]
		onlinePayType = rows[13]
		orderFromUrl = rows[14]
		webFrom = rows[15]
		location = rows[16]
		chanceSoruce = rows[19]
		flowSource = rows[20]
		crmChanceAssignId = rows[21]
		communicationStatus = rows[22]
		advisoryStatus = rows[23]
		callTime = rows[24]
		hasAnswer = rows[25]
		majorRemark = rows[26]
		startDateTime = rows[27]
		assignFlag = rows[28]
		crmChanceId = rows[30]
		createBy = rows[32]
		bespeakTime = rows[33]
		crmCommunicationId = rows[34]
		SDATE = rows[35]
		TOTALLEN = rows[36]
		AdvisoryStatus = rows[37]


		#修改字符串，若为空=0，不为空=1
		i = 3
		list = [1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3]
		while (i < 38):
			list[i] = rows[i]
			if list[i] == '':
				list[i] = 0
			else:
				list[i] = 1
			i+=1
		#修改数据库里面的字符串数据
		resetString = "update example set %s = %d,%s = %d,%s = %d,%s = %d,%s = %d,%s = %d,%s = %d,\
		%s = %d,%s = %d,%s = %d,%s = %d,%s = %d,%s = %d,%s = %d,%s = %d\
		where customerId = %d"%('birthday',list[2],'school',list[5],'testArea',list[6],
			'position',list[7],'education',list[8],'orderFromUrl',list[14],'webfrom',list[15],
			'location',list[16],'chanceSoruce',list[19],'flowSource',list[20],'communicationStatus',
			list[22],'majorRemark',list[26],'assignFlag',list[28],'crmCommunicationId',list[34],
			'advisoryStatus',list[37],customerId)
		cursor.execute(resetString)

		#修改时间字段与2015-06-01做时间差
		str1 = createDate
		str3 = loginTime
		str4 = createtime
		str5 = startDateTime
		str6 = bespeakTime
		if(is_valid_time(str1)):
			t1 = time.strptime(str1,"%Y-%m-%d %H:%M:%S")
			y1,m1,d1,h1,n1,s1 = t1[0:6]
			datet1 = datetime.datetime(y1,m1,d1,h1,n1,s1)
			timex = (datet1 - datet2).days

			resetCreatedate = "update example set createDate = %d where customerId = %d"%(timex3,customerId)
			cursor.execute(resetCreatedate)
		else:
			continue
		if(is_valid_time(str3)):
			t3 = time.strptime(str3,"%Y-%m-%d %H:%M:%S")
			y3,m3,d3,h3,n3,s3 = t3[0:6]
			datet3 = datetime.datetime(y3,m3,d3,h3,n3,s3)
			timex3 = (datet3 - datet2).days

			resetCreatedate3 = "update example set loginTime = %d where customerId = %d"%(timex3,customerId)
			cursor.execute(resetCreatedate3)
		else:
			continue
		if(is_valid_time(str4)):
			t4 = time.strptime(str4,"%Y-%m-%d %H:%M:%S")
			y4,m4,d4,h4,n4,s4 = t4[0:6]
			datet4 = datetime.datetime(y4,m4,d4,h4,n4,s4)
			timex4 = (datet4 - datet2).days

			resetCreatedate4 = "update example set createtime = %d where customerId = %d"%(timex4,customerId)
			cursor.execute(resetCreatedate4)
		else:
			continue
		if(is_valid_time(str5)):
			t5 = time.strptime(str5,"%Y-%m-%d %H:%M:%S")
			y5,m5,d5,h5,n5,s5 = t5[0:6]
			datet5 = datetime.datetime(y5,m5,d5,h5,n5,s5)
			timex5 = (datet5 - datet2).days

			resetCreatedate5 = "update example set startDateTime = %d where customerId = %d"%(timex5,customerId)
			cursor.execute(resetCreatedate5)
		else:
			continue
		if(is_valid_time(str6)):
			t6 = time.strptime(str6,"%Y-%m-%d %H:%M:%S")
			y6,m6,d6,h6,n6,s6 = t6[0:6]
			datet6 = datetime.datetime(y6,m6,d6,h6,n6,s6)
			timex6 = (datet6 - datet2).days

			resetCreatedate6 = "update example set bespeakTime = %d where customerId = %d"%(timex6,customerId)
			cursor.execute(resetCreatedate6)
		else:
			continue
	db.commit()

except:
	print "error"
	
db.close()
