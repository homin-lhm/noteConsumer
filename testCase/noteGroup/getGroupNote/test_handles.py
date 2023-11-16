import re
import unittest
from common.caseLog import info, error, step
from common.outputCheck import OutputCheck
from common.yamlRead import YamlRead
from businessCommon.re import Re
from businessCommon.clearNotes import DeleteAllNotes
from businessCommon.createGroup import CreateGroup
from businessCommon.createNotes import SetNoteContentAndNoteInfo


class GetGroupNote(unittest.TestCase):
    re = Re()
    envConfig = YamlRead().env_config()
    dataConfig = YamlRead().data_config()
    sid1 = envConfig["sid1"]
    userId1 = envConfig["userId1"]
    host = envConfig["host"]
    x_user_Key1 = envConfig["x_user_Key1"]
    url = host + dataConfig["interface"]["GetGroupNote"]["path"]
    base = dataConfig["interface"]["GetGroupNote"]["base"]
    assertBase = {
        'responseTime': int,
        'webNotes': [
            {
                'noteId': '',
                'createTime': int,
                'star': 0,
                'remindTime': 0,
                'remindType': 0,
                'infoVersion': int,
                'infoUpdateTime': int,
                'groupId': '',
                'title': 'oZIyHTsF3CyIESOiGvuiEQ==',
                'summary': 'R/RUQ/JH1ma9R2FVaaUzAphoLyPYh3RVXs45PBwgMOA=',
                'thumbnail': None,
                'contentVersion': int,
                'contentUpdateTime': int
            }
        ]
    }

    def setUp(self):
        DeleteAllNotes().delete_all_notes(self.x_user_Key1, self.sid1)

    def tearDown(self) -> None:
        pass

    def testCase01(self):
        """查看分组下便签 handles校验-输入不存在的的groupId"""
        step("STEP: 查看分组下便签的接口请求")
        body = self.base
        body["groupId"] = "1111111111111111111111111111"

        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(200, res.status_code)
        expr = {"responseTime": 0, "webNotes": []}
        OutputCheck().assert_output(expr, res.json())

    def testCase02(self):
        """查看分组下便签 handles校验-校验一页返回的数据<=rows"""
        step("PRE-STEP：新增一个分组")
        groupIds = CreateGroup().create_group(self.userId1, self.sid1, 1)
        step("PRE-STEP：在分组下新增一个便签")
        group_note_content_info = CreateGroup().create_group_note(groupIds[0], self.userId1, self.sid1, 1)
        step("STEP: 查看分组下便签的接口请求")
        body = {
            'startIndex': 0,
            'rows': 1,
            "groupId": groupIds[0]
        }

        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(200, res.status_code)
        expr = self.assertBase
        expr['webNotes'][0]['noteId'] = group_note_content_info["noteIds"][0]
        expr['webNotes'][0]['groupId'] = groupIds[0]
        assert len(res.json()["webNotes"]) == body["rows"]
        OutputCheck().assert_output(expr, res.json())

    def testCase03(self):
        """查看分组下便签 handles校验-只创建了一个便签，startIndex为1时，rows为1时，返回数据不会显示这条便签"""
        step("PRE-STEP：新增一个分组")
        groupIds = CreateGroup().create_group(self.userId1, self.sid1, 1)
        step("PRE-STEP：在分组下新增一个便签")
        group_note_content_info = CreateGroup().create_group_note(groupIds[0], self.userId1, self.sid1, 1)
        step("STEP: 查看分组下便签的接口请求")
        body = {
            'startIndex': 1,
            'rows': 1,
            "groupId": groupIds[0]
        }

        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(200, res.status_code)
        expr = {"responseTime": 0, "webNotes": []}
        OutputCheck().assert_output(expr, res.json())

    def testCase04(self):
        """查看分组下便签 handles校验-A用户不可查看B用户的便签"""
        step("PRE-STEP：新增一个分组")
        groupIds = CreateGroup().create_group(self.userId1, self.sid1, 1)
        step("PRE-STEP：在分组下新增一个便签")
        group_note_content_info = CreateGroup().create_group_note(groupIds[0], self.userId1, self.sid1, 1)
        step("STEP: 查看分组下便签的接口请求")
        body = {
            'startIndex': 0,
            'rows': 1,
            "groupId": groupIds[0]
        }

        res = self.re.post(self.url, body, sid="V02SkXpn9EteCABt3NL8cLlvU-p3y_w00ad2fc70000d111849834", userId="22679353")
        assert group_note_content_info[0]["noteId"] not in res.json()
        assert groupIds[0] not in res.json()


