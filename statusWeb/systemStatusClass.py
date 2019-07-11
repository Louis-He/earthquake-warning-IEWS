import datetime
import time

class sysStatus:
    def __init__(self):
        self.seedlinkSocketLastupdate = -1
        self.analysisSysLastupdate = -1
        self.emailSysLastupdate = 1

    def seedlinkSocketHeartBeat(self):
        self.seedlinkSocketLastupdate = int(time.mktime(datetime.datetime.utcnow().timetuple()))

    def analysisSysLastupdateHeartBeat(self):
        self.analysisSysLastupdate = int(time.mktime(datetime.datetime.utcnow().timetuple()))

    def isSocketActive(self):
        now = int(time.mktime(datetime.datetime.utcnow().timetuple()))
        if abs(now - self.seedlinkSocketLastupdate) < 60:
            return 1
        else:
            return 0

    def isAnalysisActive(self):
        now = int(time.mktime(datetime.datetime.utcnow().timetuple()))
        if abs(now - self.analysisSysLastupdate) < 60:
            return 1
        else:
            return 0

    def isEmailActive(self):
        return self.emailSysLastupdate