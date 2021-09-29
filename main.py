#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pygerrit2 import GerritRestAPI, HTTPBasicAuth
import time

# gerrit根域名
yourhost = "http://your-gerrit-domain.com/"
# 登录审核人员的账号
loginUserAccount = 'zhangsan'
loginUserPassword = '123456'
# 需要自动加分的人员
yourTeamUserNames = "三 张,四 李,五 王"

def action():
    print('开始')
    auth = HTTPBasicAuth(loginUserAccount, loginUserPassword)
    rest = GerritRestAPI(url=yourhost, auth=auth)
    changes = rest.get("/changes/?O=881&S=0&n=25&q=status%3Aopen%20-is%3Awip&o=CURRENT_REVISION&o=CURRENT_COMMIT&o=DETAILED_LABELS")
    filterChanges = [x for x in changes if x['owner']['name'] in yourTeamUserNames]

    for change in filterChanges:
        print(change)
        # 需要跳过的分支
        if (change['branch'] == 'master'):
            continue
        if((change['labels'] is None) or (change['labels']['Code-Review'] is None)):
            break
        if 'approved' not in change['labels']['Code-Review'] or change['labels']['Code-Review']['approved'] is None:
            json = '{"drafts":"PUBLISH_ALL_REVISIONS","labels":{"Code-Review":2,"Verified":1},"message":"","reviewers":[]}'
            url = '/changes/{}/revisions/{}/review'.format(change['id'], change['current_revision'])
            rest.post(url, data=str(json), headers={"Content-Type": "application/json"})
    print('结束')

# 10秒执行一次
while True:
    action()
    time.sleep(10)
