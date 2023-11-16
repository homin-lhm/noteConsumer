import json
import os
import unittest
import time

from common.caseLog import info
from common.yamlRead import YamlRead
import requests


class CreateGroup(unittest.TestCase):
    envConfig = YamlRead().env_config()
    host = envConfig['host']

    def create_group(self, userid, sid, num):
        """
        创建便签分组
        :param userid: 用户id
        :param sid: wps_sid
        :param num: 笔记分组数量
        :return:分组列表
        """
        url = self.host + f'/v3/notesvr/set/notegroup'
        headers = {"X-User-Key": userid,
                   "cookie": "wps_sid=" + sid,
                   "Content-Type": "application/json;charset=utf-8"}
        group_list = []
        for i in range(num):
            time.time()
            groupId = str(int(time.time() * 1000)) + '_groupId'
            body = {
                'groupId': groupId,
                'groupName': 'Test'
            }
            res = requests.post(url, headers=headers, json=body)
            assert res.status_code == 200
            group_list.append(groupId)
        info(f'创建的分组：{group_list}')
        return group_list

    def create_group_note(self, groupId, userid, sid, num):
        """
        创建分组下的便签
        :param groupId: 用户分组
        :param userid: 用户id
        :param sid: wps_id
        :param num: 数量
        :return: 分组下的便签列表
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
            body_info = {"noteId": noteId, "star": 0, "remindTime": 0, "remindType": 0, "groupId": groupId}

            res = requests.post(info_url, headers=headers, json=body_info)
            infoVersion = res.json()['infoVersion']
            # 新增便签内容
            body_content = {"title": "oZIyHTsF3CyIESOiGvuiEQ==",
                            "summary": "R/RUQ/JH1ma9R2FVaaUzAphoLyPYh3RVXs45PBwgMOA=",
                            "body": "R/RUQ/JH1ma9R2FVaaUzAtwlXImqcX++1wS1GmEpgL8=", "localContentVersion": infoVersion,
                            "noteId": noteId, "bodyType": 0}  # "thumbnail": null,
            res = requests.post(content_url, headers=headers, json=body_content)
            noteIds.append(noteId)
            note_content_info = {"noteId": noteId, "title": body_content["title"], "body": body_content["body"],
                                 "summary": body_content["summary"], "groupId": groupId}
            note_content_info_list.append(note_content_info)
        info(f'在分组下创建的便签数据是{note_content_info_list}')
        return note_content_info_list

    def get_group(self, userid, sid):
        """
        获取分组列表
        :param userid: 用户id
        :param sid: wps_sid
        :return:分组列表
        """
        url = self.host + f'/v3/notesvr/get/notegroup'
        headers = {"X-User-Key": userid,
                   "cookie": "wps_sid=" + sid,
                   "Content-Type": "application/json;charset=utf-8"}
        body = {"lastRequestTime":0,"excludeInValid":True}
        res = requests.post(url, headers=headers, json=body)
        self.assertEqual(200, res.status_code)
        group_list = []
        for i in res.json()["noteGroups"]:
            groupId = i["groupId"]
            group_list.append(groupId)
        info(f'获取分组列表：{group_list}')
        return group_list

    def delete_group(self, userid, sid, groupId):
        """
        删除分组
        :param groupId: 要删除的分组Id
        :param userid: 用户id
        :param sid: wps_sid
        """
        detete_group_url = self.host + f'/v3/notesvr/delete/notegroup'
        headers = {"X-User-Key": userid,
                   "cookie": "wps_sid=" + sid,
                   "Content-Type": "application/json;charset=utf-8"}

        detete_group_body = {"groupId": groupId}
        res = requests.post(detete_group_url, headers=headers, json=detete_group_body)
        self.assertEqual(200, res.status_code, msg=f'状态码异常，返回体{res.text}')

    def get_group_note(self, groupId, userid, sid):
        """
        获取分组下的便签
        :param groupId: 用户分组
        :param userid: 用户id
        :param sid: wps_id
        :return: 分组下的便签列表
        """
        url = self.host + '/v3/notesvr/web/getnotes/group'

        headers = {"X-User-Key": userid,
                   "cookie": "wps_sid=" + sid,
                   "Content-Type": "application/json;charset=utf-8"}

        body = {"groupId": groupId, "startIndex": 0, "rows": 10}
        res = requests.post(url, headers=headers, json=body)
        self.assertEqual(200, res.status_code)
        group_note_list = []
        for i in res.json()["webNotes"]:
            noteId = i["noteId"]
            group_note_list.append(noteId)
        info(f'获取分组下的便签：{group_note_list}')
        return group_note_list

