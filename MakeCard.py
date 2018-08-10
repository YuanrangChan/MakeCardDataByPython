#for python3
from time import *
import os
import ftplib  #用来FTP上传文件
import requests
import setting


class MakeCard():
    '''制卡流程包括制卡申请，制作卡数据，上传卡数据，发送反馈报文等'''
    #发送报文
    #def send_xml_request(self, url, data):
    def send_xml_request(self, url, xmlheader, **xmlbody)   # **代表可选参数
        data = xmlheader + xmlbody
        requests.post(url=url, data=data, timeout=3)    #xml内容是读取CardApply.xml文件并替换关键字段值

    def create_card_data(self, filename, oprseq, EIDorIMSI, **ICCID):
        if "UpdateKey" in filename:
            #wcp卡数据
            uname = open(filename, 'a')
            #写入头文件
            EID = EIDorIMSI
            uname.write(oprseq +'|2|'+ oprseq[0:3]+'|alibaba|' + conf.ApplicantPhone +'|'+\
                     oprseq[12:26]+'|MakeCardData|'+ EID +'|'+ sum(EID, conf.numbers)+'\n')
            #写入WCP卡数据文件
            for i in range(conf.numbers):
                uname.write(EID[:-7] + sum((EID[-7:]), i).zfill(7)+'|'+'3467012345abcde0456783232809'+\
                            str(i).zfill(4)+'|3467012345abcde0456873232809'+str(i).zfill(4)+'|3467012345abcde0457683232809'+\
                            str(i).zfill(4)+'\n')
                uname.close()
        else:
            #woqi卡数据
            uname = open(filename,'a')
            #写入头文件
            uname.write(oprseq + '|' + conf.CardMfrs + '|' + oprseq[0:3] + '|' +\
                        conf.Applicant + '|' + conf.ApplicantPhone + '|' + oprseq[12:20] + '|' +\
                        conf.ApplyReason + '|' + conf.MsisdnSection + '|' + conf.numbers +\
                        '|2~' + sum(conf.numbers, 1) + '\n')
            #写入IMSI和ICCID卡数据文件
            IMSI = EIDorIMSI
            for i in range(conf.numbers):
                IMSI = int(IMSI) + i
                ICCID = ICCID[:-7]+str(int(ICCID[-7:])+i).zfill(7)
                uname.write('')
                uname.close()


    def create_key_data(self, keyname):
        #密匙文件
        Kname = open(keyname, 'a')
        Kname.write('001|002\n')
        Kname.close()

    def encryption_card_data(self, USimMSName, USimMSNameEncryption):
        #文件加密
        #pwd = os.getcwd()  #获取当前路径    ..是相对路径
        #EncryptCardFile.jar文件是放在与主程序相同路径的加密工具
        encryption = 'java -jar EncryptCardFile.jar E4B044E830559B337AD15F2151A05AE8 B9A8C2FDA2378AA4A8EA9D028064FB3B' + ' ' +\
                     USimMSName + ' ' + USimMSNameEncryption
        os.system(encryption)

    #文件上传,传入主机名,上传路径以及文件名
    def upload_file(self, host, uploadDir, filename):
        f = ftplib.FTP(host)  #实例化FTP对象
        f.login(conf.username, conf.passwd)   #FTP登录主机
        '''以二进制形式上传文件'''
        pwd = os.getcwd()   #获取本地当前路径
        file_remote = uploadDir + filename
        file_local = pwd + filename
        bufsize = 1024   #设置缓冲器大小
        fp = open(file_local, 'rb')
        f.storbinary('STOR ' + file_remote, fp, bufsize)
        fp.close()

    def conn_orcale(self, province, oprseq):
        '''连接数据库查询号段对应的省份，以及查询APP表的状态是否满足上传wcp卡数据文件的条件'''
        hn = conf.hn
        hz = conf.hz
        hb = conf.hb
        if province in hn:
            #连接华南库
            pass
        elif province in hb:
            #连接华北库
            pass
        elif province in hz:
            #连接华中库
            pass


    def get_ICCIDandIMSIorEID(self, host, oprseq):
        connect(hostname=host, username=conf.username, passward=conf.passwd)   #连接
        if host == conf.hostwoqi:
            ICCID = ''
            IMSI = ''
            return ICCID,IMSI
        elif host == conf.hostWCP:
            EID = ''
            return EID

    #制作xml报文
    def create_xml_file(self, *xmldata):
        #*可传入任意多个参数
        xmldatas = [1, 2]   #列表接收参数
        #open文件
        #find字段
        #replace字段值
        xml = ''
        return xml
    xmldatas = [1, 2]
    create_xml_file(*xmldatas)

if __name__ == '__main__':
    conf = setting.Setting()
    oprseq = conf.province + conf.bipcode + conf.timesec + conf.tailnum
    applyxmldatas = []
    cardApplyHeader = MakeCard.create_xml_file()   #制卡申请报文头
    cardApplyBody = MakeCard.create_xml_file()    #制卡申请报文体
    pbossfeedback = MakeCard.create_xml_file(cc, dd)  #pboss反馈报文
    wcpfeedback = MakeCard.create_xml_file(ee, ff)    #wcp反馈报文
    #发送制卡申请报文
    MakeCard.send_xml_request(conf.cardApplyURL, cardApplyHeader, cardApplyBody)

    sleep(60)   #等待手动审批   可以优化成自动审批。。。
    #获取ICCID和IMSI
    getResult = MakeCard.get_ICCIDandIMSIorEID(conf.hostwoqi, oprseq)
    ICCID = getResult[1]
    IMSI = getResult[2]
    #制作woqi卡数据文件
    woqiUSimMSName = 'MW_USimMS_'+ oprseq +'_'+ conf.CardMfrs +'_'+ str(conf.province) +'_1_'+ str(conf.timesec) +'.dat'   #woqi卡数据文件名
    MakeCard.create_card_data(woqiUSimMSName, oprseq, IMSI, ICCID)
    #制作woqi索引文件
    woqiKeyName = 'KeyData_'+ oprseq + '_' + conf.CardMfrs + '_' + oprseq[0:3] + '_1_' +\
                  oprseq[12:26]+'.IDX'   #woqi索引文件名
    MakeCard.create_key_data(woqiKeyName)
    #加密
    woqiUSimMSNameEncryption = woqiUSimMSName[3:]
    MakeCard.encryption_card_data(woqiUSimMSName, woqiUSimMSNameEncryption)
    #上传woqi卡数据文件
    MakeCard.upload_file(conf.hostwoqi, conf.uploadDirwoqi, woqiUSimMSNameEncryption)
    #pboss发送反馈报文
    MakeCard.send_xml_request(conf.pbossfeedbackURL, pbossfeedback)

    #获取EID
    EID = MakeCard.get_ICCIDandIMSIorEID(conf.hostWCP, oprseq)
    #制作wcp卡数据文件
    wcpUSimMSName = 'MW_USimMS_UpdateKey_'+oprseq+'_2_'+oprseq[0:3]+'_'+oprseq[12:26]+'.dat'
    MakeCard.create_card_data(wcpUSimMSName, oprseq, EID)
    #制作wcp索引文件
    wcpKeyName = ''
    MakeCard.create_key_data(wcpKeyName)
    #加密
    wcpUSimMSNameEncryption = wcpUSimMSName[3:]
    MakeCard.encryption_card_data(wcpUSimMSName, wcpUSimMSNameEncryption)
    #上传wcp卡数据文件
    MakeCard.upload_file(conf.hostWCP, conf.uploadDirWCP, wcpUSimMSNameEncryption)
    #wcp发送反馈报文
    MakeCard.send_xml_request(conf.wcpfeedbackURL, wcpfeedback)















