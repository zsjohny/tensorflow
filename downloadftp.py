from ftplib import FTP

ftp=FTP()                         #设置变量
ftp.set_debuglevel(2)             #打开调试级别2，显示详细信息
ftp.connect("ftp.kuick.cn","9021")          #连接的ftp sever和端口
ftp.login("haixue_data_a","FLf123456!@#")      #连接的用户名，密码
print ftp.getwelcome()            #打印出欢迎信息
ftp.cmd("/机会估值字段信息/")                #进入远程目录
bufsize=1024                      #设置的缓冲区大小
filename="机会乐语纪录2015-01.csv"           #需要下载的文件
file_handle=open(filename,"wb").write #以写模式在本地打开文件
ftp.retrbinaly("RETR filename.txt",file_handle,bufsize) #接收服务器上文件并写入本地文件
ftp.set_debuglevel(0)             #关闭调试模式
ftp.quit()                        #退出ftp