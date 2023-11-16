import re
import time
import unittest

from parameterized import parameterized

from businessCommon.getAllNotes import GetAllNotes
from common.caseLog import info, error, step
from common.outputCheck import OutputCheck
from common.yamlRead import YamlRead
from businessCommon.re import Re
from businessCommon.clearNotes import DeleteAllNotes
from businessCommon.createGroup import CreateGroup
from businessCommon.createNotes import SetNoteContentAndNoteInfo


class GetNoteBody(unittest.TestCase):
    re = Re()
    envConfig = YamlRead().env_config()
    dataConfig = YamlRead().data_config()
    sid1 = envConfig["sid1"]
    userId1 = envConfig["userId1"]
    host = envConfig["host"]
    x_user_Key1 = envConfig["x_user_Key1"]
    url = host + dataConfig["interface"]["GetNoteBody"]["path"]
    base = dataConfig["interface"]["GetNoteBody"]["base"]
    input_noteIds_empty_list = dataConfig["interface"]["GetNoteBody"]["input_noteIds_empty_list"]
    assertBase = {
        "responseTime": int,
        "noteBodies": [
            {
                "summary": "R/RUQ/JH1ma9R2FVaaUzAphoLyPYh3RVXs45PBwgMOA=",
                "noteId": "1699187424655_noteId",
                "infoNoteId": "1699187424655_noteId",
                "bodyType": 0,
                "body": "R/RUQ/JH1ma9R2FVaaUzAtwlXImqcX++1wS1GmEpgL8=",
                "contentVersion": int,
                "contentUpdateTime": int,
                "title": None,
                "valid": 1
            }
        ]
    }

    def setUp(self):
        DeleteAllNotes().delete_all_notes(self.x_user_Key1, self.sid1)

    def tearDown(self) -> None:
        pass

    def testCase01(self):
        """获取标签内容的input校验，不传参数"""
        step("STEP: 获取便签内容的接口请求")
        body = {
        }
        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(input_noteIds_empty_list)
    def testCase02(self, input_value, code):
        """获取便签内容noteid值为空"""
        step("STEP: 获取便签内容")
        body = {
            "noteIds": input_value,
        }
        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(code, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase03(self):
        """获取便签内容,input校验noteid不存在"""
        step("STEP: 获取便签内容")
        body = {
            "noteIds": ["111"],
        }
        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(200, res.status_code)
        expr = {
            "responseTime": int,
            "noteBodies": [
            ]
        }
        OutputCheck().assert_output(expr, res.json())

    def testCase04(self):
        """获取便签内容,input校验，noteid不存在"""
        step("STEP: 获取便签内容")
        body = {
            "noteIds": ["111"],
        }
        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(200, res.status_code)
        expr = {
            "responseTime": int,
            "noteBodies": [
            ]
        }
        OutputCheck().assert_output(expr, res.json())

    def testCase12(self):
        """
        获取便签内容X - user - key
        入参校验: X - user - key不存在
        """
        step("STEP: 获取便签内容的接口请求")
        body = self.base
        res = self.re.post(self.url, body, self.sid1, userId=1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase13(self):
        """
        获取便签内容X - user - key
        入参校验: X - user - key为空
        """
        step("STEP: 上传更新便签内容的接口请求")
        body = self.base
        res = self.re.post(self.url, body, self.sid1, userId="")
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase14(self):
        """
        获取便签内容 wps_sid 入参校验:wps_sid失效
        """
        step("STEP: 上传更新便签内容的接口请求")
        body = self.base
        res = self.re.post(self.url, body, "111111111", self.userId1)
        self.assertEqual(412, res.status_code)
        expr = {"errorCode": -1011, "errorMsg": "user change!"}
        OutputCheck().assert_output(expr, res.json())

    def testCase15(self):
        """
        获取便签内容 wps_sid 入参校验:wps_sid为空
        """
        step("STEP: 上传更新便签内容的接口请求")
        body = self.base
        res = self.re.post(self.url, body, "", self.userId1)
        self.assertEqual(412, res.status_code)
        expr = {"errorCode": -1011, "errorMsg": "user change!"}
        OutputCheck().assert_output(expr, res.json())
