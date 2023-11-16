import re
import unittest

from parameterized import parameterized

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
    mustKey = dataConfig["interface"]["GetGroupNote"]["mustKey"]
    optionKeys = dataConfig["interface"]["GetGroupNote"]["optionKeys"]
    input_startIndex_empty_list = dataConfig["interface"]["GetGroupNote"]["input_startIndex_empty_list"]
    input_rows_empty_list = dataConfig["interface"]["GetGroupNote"]["input_rows_empty_list"]
    input_startIndex_list = dataConfig["interface"]["GetGroupNote"]["input_startIndex_list"]
    input_rows_list = dataConfig["interface"]["GetGroupNote"]["input_rows_list"]
    input_groupId_list = dataConfig["interface"]["GetGroupNote"]["input_groupId_list"]

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
        """查看分组下便签的必填项校验"""
        step("STEP: 查看分组下便签的接口请求")
        body = {
            'startIndex': 0,
            'rows': 10
        }
        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase02(self):
        """查看分组下便签的noteId值为空字符串"""
        step("STEP: 查看分组下便签的接口请求")
        body = {
            'groupId': '',
            'startIndex': 0,
            'rows': 10
        }
        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase03(self):
        """查看分组下便签的noteId值为None"""
        step("STEP: 查看分组下便签的接口请求")
        body = {
            'groupId': None,
            'startIndex': 0,
            'rows': 10
        }
        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(optionKeys)
    def testCase04(self, key):
        """查看分组下便签的非必填项校验"""
        step("PRE-STEP：新增一个分组")
        groupIds = CreateGroup().create_group(self.userId1, self.sid1, 1)
        step("PRE-STEP：在分组下新增一个便签")
        group_note_content_info = CreateGroup().create_group_note(groupIds[0], self.userId1, self.sid1, 1)
        step("STEP: 查看分组下便签的接口请求")
        body = self.base
        body["groupId"] = groupIds[0]
        body.pop(key)

        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(200, res.status_code)
        expr = self.assertBase
        expr['webNotes'][0]['noteId'] = group_note_content_info["noteIds"][0]
        expr['webNotes'][0]['groupId'] = groupIds[0]
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(input_startIndex_empty_list)
    def testCase05(self, input_value, code):
        print(input_value)
        """查看分组下便签的startIndex值为None或空"""
        step("PRE-STEP：新增一个分组")
        groupIds = CreateGroup().create_group(self.userId1, self.sid1, 1)
        step("PRE-STEP：在分组下新增一个便签")
        group_note_content_info = CreateGroup().create_group_note(groupIds[0], self.userId1, self.sid1, 1)
        step("STEP: 查看分组下便签的接口请求")
        body = {
            'groupId': groupIds[0],
            'startIndex': input_value,
            'rows': 10
        }
        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(code, res.status_code)
        expr = self.assertBase
        expr['webNotes'][0]['noteId'] = group_note_content_info["noteIds"][0]
        expr['webNotes'][0]['groupId'] = groupIds[0]
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(input_rows_empty_list)
    def testCase06(self, input_value, code):
        """查看分组下便签的startIndex值为None或空"""
        step("PRE-STEP：新增一个分组")
        groupIds = CreateGroup().create_group(self.userId1, self.sid1, 1)
        step("PRE-STEP：在分组下新增一个便签")
        group_note_content_info = CreateGroup().create_group_note(groupIds[0], self.userId1, self.sid1, 1)
        step("STEP: 查看分组下便签的接口请求")
        body = {
            'groupId': groupIds[0],
            'startIndex': 0,
            'rows': input_value
        }
        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(code, res.status_code)
        expr = self.assertBase
        expr['webNotes'][0]['noteId'] = group_note_content_info["noteIds"][0]
        expr['webNotes'][0]['groupId'] = groupIds[0]
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(input_startIndex_list)
    def testCase07(self, input_value, code):
        """查看分组下便签的startIndex 入参校验"""
        step("PRE-STEP：新增一个分组")
        groupIds = CreateGroup().create_group(self.userId1, self.sid1, 1)
        step("PRE-STEP：在分组下新增一个便签")
        group_note_content_info = CreateGroup().create_group_note(groupIds[0], self.userId1, self.sid1, 1)
        step("STEP: 查看分组下便签的接口请求")
        body = {
            'groupId': groupIds[0],
            'startIndex': input_value,
            'rows': 10
        }
        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(code, res.status_code)

    @parameterized.expand(input_rows_list)
    def testCase08(self, input_value, code):
        """查看分组下便签的startIndex 入参校验"""
        step("PRE-STEP：新增一个分组")
        groupIds = CreateGroup().create_group(self.userId1, self.sid1, 1)
        step("PRE-STEP：在分组下新增一个便签")
        group_note_content_info = CreateGroup().create_group_note(groupIds[0], self.userId1, self.sid1, 1)
        step("STEP: 查看分组下便签的接口请求")
        body = {
            'groupId': groupIds[0],
            'startIndex': input_value,
            'rows': 10
        }
        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(code, res.status_code)

    @parameterized.expand(input_groupId_list)
    def testCase09(self, input_value, code):
        """查看分组下便签的startIndex 入参校验"""
        step("PRE-STEP：新增一个分组")
        groupIds = CreateGroup().create_group(self.userId1, self.sid1, 1)
        step("PRE-STEP：在分组下新增一个便签")
        group_note_content_info = CreateGroup().create_group_note(groupIds[0], self.userId1, self.sid1, 1)
        step("STEP: 查看分组下便签的接口请求")
        body = {
            'groupId': input_value,
            'startIndex': 0,
            'rows': 10
        }
        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(code, res.status_code)

    def testCase10(self):
        """查看分组下便签 X - user - key 入参校验:X-user-key不存在"""
        step("PRE-STEP：新增一个分组")
        groupIds = CreateGroup().create_group(self.userId1, self.sid1, 1)
        step("PRE-STEP：在分组下新增一个便签")
        group_note_content_info = CreateGroup().create_group_note(groupIds[0], self.userId1, self.sid1, 1)
        step("STEP: 查看分组下便签的接口请求")
        body = {
            'groupId': groupIds[0],
            'startIndex': 0,
            'rows': 10
        }
        res = self.re.post(self.url, body, self.sid1, userId=1)
        self.assertEqual(412, res.status_code)
        expr = {"errorCode": -1011, "errorMsg": "user change!"}
        OutputCheck().assert_output(expr, res.json())

    def testCase11(self):
        """查看分组下便签 X - user - key 入参校验:X-user-key为空"""
        step("PRE-STEP：新增一个分组")
        groupIds = CreateGroup().create_group(self.userId1, self.sid1, 1)
        step("PRE-STEP：在分组下新增一个便签")
        group_note_content_info = CreateGroup().create_group_note(groupIds[0], self.userId1, self.sid1, 1)
        step("STEP: 查看分组下便签的接口请求")
        body = {
            'groupId': groupIds[0],
            'startIndex': 0,
            'rows': 10
        }
        res = self.re.post(self.url, body, self.sid1, userId="")
        self.assertEqual(412, res.status_code)
        expr = {"errorCode": -1011, "errorMsg": "user change!"}
        OutputCheck().assert_output(expr, res.json())

    def testCase12(self):
        """查看分组下便签 wps_sid 入参校验:wps_sid失效"""
        step("PRE-STEP：新增一个分组")
        groupIds = CreateGroup().create_group(self.userId1, self.sid1, 1)
        step("PRE-STEP：在分组下新增一个便签")
        group_note_content_info = CreateGroup().create_group_note(groupIds[0], self.userId1, self.sid1, 1)
        step("STEP: 查看分组下便签的接口请求")
        body = {
            'groupId': groupIds[0],
            'startIndex': 0,
            'rows': 10
        }
        res = self.re.post(self.url, body, "111111111", self.userId1)
        self.assertEqual(412, res.status_code)
        expr = {"errorCode": -1011, "errorMsg": "user change!"}
        OutputCheck().assert_output(expr, res.json())

    def testCase13(self):
        """查看分组下便签 wps_sid 入参校验:wps_sid为空"""
        step("PRE-STEP：新增一个分组")
        groupIds = CreateGroup().create_group(self.userId1, self.sid1, 1)
        step("PRE-STEP：在分组下新增一个便签")
        group_note_content_info = CreateGroup().create_group_note(groupIds[0], self.userId1, self.sid1, 1)
        step("STEP: 查看分组下便签的接口请求")
        body = {
            'groupId': groupIds[0],
            'startIndex': 0,
            'rows': 10
        }
        res = self.re.post(self.url, body, "", self.userId1)
        self.assertEqual(412, res.status_code)
        expr = {"errorCode": -1011, "errorMsg": "user change!"}
        OutputCheck().assert_output(expr, res.json())
