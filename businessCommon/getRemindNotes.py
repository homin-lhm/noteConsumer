import json
import os
import unittest
import time

from common.caseLog import info
from common.yamlRead import YamlRead
import requests


class GetRemindNotes:
    """
            根据用户获取所有便签
            返回所有便签的id
    """
    yamlRead = YamlRead()
    envConfig = YamlRead().env_config()
    host = envConfig['host']

    def get_remind_notes(self, userid, sid):
        header = {"X-User-Key": userid, "cookie": "wps_sid=" + sid,
                  "Content-Type": "application/json;charset=utf-8"}
        body = {
            "rows": 300,
            "startIndex": 0,
            "remindStartTime": 32503651200000,
            "remindEndTime": 946656000000
        }
        noteIds = []
        # 1）获取首页便签接口 获取该用户的所有便签数据
        path = '/v3/notesvr/web/getnotes/remind'
        url = self.host + path
        res = requests.get(url, headers=header, json=body)
        print(res)
        for each in res.json()["webNotes"]:
            noteIds.append(each["noteId"])
        info(f"用户{userid}所有日历便签id:{noteIds}")
        return noteIds
