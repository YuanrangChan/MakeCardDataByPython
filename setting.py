import os
import random
from time import *
class Setting():
    def __init__(self):
        self.bipcode ='1BIP2B950'
        self.cardApplyURL = "http://192.168.127.110:9083/huawei-test3/http/tsn_boss_call_pboss/send.jsp"
        self.pbossfeedbackURL = ''
        self.wcpfeedbackURL = ''
        self.numbers = 500
        self.uploadDirwoqi = '/home/pboss/file/pboss/cardinfo/'
        self.localDir = os.getcwd()
        self.hostwoqi = '192.168.106.107'
        self.username = 'pboss'
        self.passwd = 'P_BOSS$2017'
        self.uploadDirWCP = '/home/.......'
        self.hostWCP = '192.168.119.130'
        self.province = 200
        self.tailnum = str(random.randint(000000, 999999)).zfill(6)
        self.timesec = strftime('%Y%m%d%H%M%S', localtime(time()))
        self.applyxmldatas = []
        self.CardMfrs = 2
        self.hz = []
        self.hn = []
        self.hb = []
        self.ApplicantPhone = ''
        self.Applicant = ''
        self.ApplyReason = ''
        self.MsisdnSection = ''
		self.Address='http://192.168.122.39:8080/interface4iomp/iompActionServlet'