import json
import os
import unittest
import time

from common.caseLog import info
from common.yamlRead import YamlRead
import requests


class GetAllNotes:
    """
            根据用户获取所有便签
            返回所有便签的id
    """
    yamlRead = YamlRead()
    envConfig = YamlRead().env_config()
    host = envConfig['host']

    def get_all_notes(self, userid, sid):
        header = {"X-User-Key": userid, "cookie": "wps_sid=" + sid,
                  "Content-Type": "application/json;charset=utf-8"}
        noteIds = []
        # 1）获取首页便签接口 获取该用户的所有便签数据
        path = f'/v3/notesvr/user/{userid}/home/startindex/0/rows/99999/notes'
        url = self.host + path
        res = requests.get(url, headers=header)
        for each in res.json()["webNotes"]:
            noteIds.append(each["noteId"])
        info(f"用户{userid}首页所有便签id:{noteIds}")
        return noteIds

