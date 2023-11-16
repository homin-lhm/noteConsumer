import json
import os
import unittest

from common.yamlRead import YamlRead
import requests


class DeleteAllNotes(unittest.TestCase):
    envConfig = YamlRead().env_config()
    host = envConfig['host']

    def delete_all_notes(self, userid, sid):
        """
        清空用户下所有便签功能
        :param userid: 用户id
        :param sid: 用户的sid
        :return:None
        """
        get_note_url = self.host + f'/v3/notesvr/user/{userid}/home/startindex/0/rows/999/notes'
        delete_note_url = self.host + '/v3/notesvr/delete'
        clear_note_url = self.host + '/v3/notesvr/cleanrecyclebin'
        headers = {"X-User-Key": userid,
                   "cookie": "wps_sid=" + sid,
                   "Content-Type": "application/json;charset=utf-8"}
        noteIds = []
        # 1）获取首页便签接口 获取该用户的所有便签数据

        res = requests.get(get_note_url, headers=headers)
        for each in res.json()["webNotes"]:
            noteIds.append(each["noteId"])

        # 2）删除便签 循环删除的方式
        for noteId in noteIds:
            body = {
                "noteId": noteId
            }
            res = requests.post(delete_note_url, headers=headers, json=body)
            assert res.status_code == 200

        # 3）清空回收站
        clear_body = {
            "noteIds": ["-1"]
        }
        res = requests.post(clear_note_url, headers=headers, json=clear_body)
        assert res.status_code == 200

    def delete_notes(self, noteId, userid, sid):
        """
        清空用户下所有便签功能
        :param noteId:
        :param userid: 用户id
        :param sid: 用户的sid
        :return:None
        """
        delete_note_url = self.host + '/v3/notesvr/delete'
        clear_note_url = self.host + '/v3/notesvr/cleanrecyclebin'
        headers = {"X-User-Key": userid,
                   "cookie": "wps_sid=" + sid,
                   "Content-Type": "application/json;charset=utf-8"}
        # 2)删除便签
        body = {
            "noteId": noteId
        }
        res = requests.post(delete_note_url, headers=headers, json=body)
        assert res.status_code == 200

        # 3）清空回收站
        clear_body = {
            "noteIds": ["-1"]
        }
        res = requests.post(clear_note_url, headers=headers, json=clear_body)
        assert res.status_code == 200



