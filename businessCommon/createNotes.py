import json
import os
import unittest
import time
from common.yamlRead import YamlRead
import requests
from common.caseLog import info, error, step


class SetNoteContentAndNoteInfo:
    yamlRead = YamlRead()
    envConfig = yamlRead.env_config()
    host = envConfig['host']

    def set_note_content_and_note_info(self, userid, sid, num, remindTime=None):
        """
        创建没有用户分组的便签
        :param remindTime:
        :param userid: 用户名
        :param sid: wps_sid
        :param num: 数量
        :return: 返回字典格式，包含所有创建的便签id
        """
        info_url = self.host + '/v3/notesvr/set/noteinfo'
        content_url = self.host + '/v3/notesvr/set/notecontent'

        headers = {"X-User-Key": userid,
                   "cookie": "wps_sid=" + sid,
                   "Content-Type": "application/json;charset=utf-8"}

        noteIds = []
        note_content_info_list = []
        for i in range(num):
            # 新增便签主体
            noteId = str(int(time.time() * 1000)) + "_noteId"
            if remindTime is None:
                body_info = {"noteId": noteId, "star": 0, "remindTime": 0, "remindType": 0}
            else:
                body_info = {"noteId": noteId, "star": 0, "remindTime": 1700186400000, "remindType": 1}
            res = requests.post(info_url, headers=headers, json=body_info)
            infoVersion = res.json()['infoVersion']
            # 新增便签内容
            body_content = {"title": "oZIyHTsF3CyIESOiGvuiEQ==",
                            "summary": "R/RUQ/JH1ma9R2FVaaUzAphoLyPYh3RVXs45PBwgMOA=",
                            "body": "R/RUQ/JH1ma9R2FVaaUzAtwlXImqcX++1wS1GmEpgL8=",
                            "localContentVersion": infoVersion,
                            "noteId": noteId,
                            "bodyType": 0}  # "thumbnail": null,
            res = requests.post(content_url, headers=headers, json=body_content)
            note_content_info = {"noteId": noteId, "title": body_content["title"], "body": body_content["body"],
                                 "summary": body_content["summary"]}
            note_content_info_list.append(note_content_info)
        info(note_content_info_list)
        return note_content_info_list

    def set_note_info(self, userid, sid, num):
        """
        创建没有用户分组的主体
        :param userid: 用户名
        :param sid: wps_sid
        :param num: 数量
        :return: 返回字典格式，包含所有创建的便签id
        """
        info_url = self.host + '/v3/notesvr/set/noteinfo'
        headers = {"X-User-Key": userid,
                   "cookie": "wps_sid=" + sid,
                   "Content-Type": "application/json;charset=utf-8"}
        note_info = []
        for i in range(num):
            # 新增便签主体
            noteId = str(int(time.time() * 1000)) + "_noteId"
            body_info = {"noteId": noteId, "star": 0}
            res = requests.post(info_url, headers=headers, json=body_info)
            infoVersion = res.json()['infoVersion']
            note_info.append({"noteId": noteId, "infoVersion": infoVersion})
        return note_info
