import web

from systemStatusClass import *
from webLayout import *

systemStatusObj = sysStatus()

urls = (
    '/status', 'status',
    '/updateSocket', 'updateSocket',
    '/updateAnalysis', 'updateAnalysis',
)

class status:
    global systemStatusObj
    def GET(self):
        systemStat = {"overall": -1, "subSystem": {"IRIS seedlink Socket": systemStatusObj.isSocketActive(),
                                                   "IEWS Analysis System": systemStatusObj.isAnalysisActive(),
                                                   "IEWS Email Service": systemStatusObj.isEmailActive()}}

        if(systemStat["subSystem"]["IRIS seedlink Socket"] == 1 and
                systemStat["subSystem"]["IEWS Analysis System"] == 1 and
                systemStat["subSystem"]["IEWS Email Service"] == 1):
            systemStat["overall"] = 1
        else:
            systemStat["overall"] = 0

        return render.status(headerHtml, footerhtml, systemStat)

class updateSocket:
    global systemStatusObj
    def GET(self):
        systemStatusObj.seedlinkSocketHeartBeat()
        return "Socket Updated."

class updateAnalysis:
    global systemStatusObj
    def GET(self):
        systemStatusObj.analysisSysLastupdateHeartBeat()
        return "Analysis Updated."

app = web.application(urls, globals())
render = web.template.render('templates/')

if __name__ == "__main__":
    app.run()
