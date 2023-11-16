import re
import time
import unittest

from parameterized import parameterized

from common.caseLog import info, error, step
from common.outputCheck import OutputCheck
from common.yamlRead import YamlRead
from businessCommon.re import Re
from businessCommon.clearNotes import DeleteAllNotes
from businessCommon.createGroup import CreateGroup
from businessCommon.createNotes import SetNoteContentAndNoteInfo


class SetNoteInfo(unittest.TestCase):
    re = Re()
    envConfig = YamlRead().env_config()
    dataConfig = YamlRead().data_config()
    sid1 = envConfig["sid1"]
    userId1 = envConfig["userId1"]
    host = envConfig["host"]
    x_user_Key1 = envConfig["x_user_Key1"]
    url = host + dataConfig["interface"]["SetNoteInfo"]["path"]
    base = dataConfig["interface"]["SetNoteInfo"]["base"]
    mustKey = dataConfig["interface"]["SetNoteInfo"]["mustKey"]
    optionKeys = dataConfig["interface"]["SetNoteInfo"]["optionKeys"]
    input_star_empty_list = dataConfig["interface"]["SetNoteInfo"]["input_star_empty_list"]
    input_remindTime_empty_list = dataConfig["interface"]["SetNoteInfo"]["input_remindTime_empty_list"]
    input_remindType_empty_list = dataConfig["interface"]["SetNoteInfo"]["input_remindType_empty_list"]
    input_groupId_empty_list = dataConfig["interface"]["SetNoteInfo"]["input_groupId_empty_list"]
    input_noteId_list = dataConfig["interface"]["SetNoteInfo"]["input_noteId_list"]
    input_star_list = dataConfig["interface"]["SetNoteInfo"]["input_star_list"]
    input_groupId_list = dataConfig["interface"]["SetNoteInfo"]["input_groupId_list"]
    input_remindTime_list = dataConfig["interface"]["SetNoteInfo"]["input_remindTime_list"]
    input_remindType_list = dataConfig["interface"]["SetNoteInfo"]["input_remindType_list"]
    assertBase = {
        'responseTime': int,
        'infoVersion': int,
        'infoUpdateTime': int,
    }

    def setUp(self):
        DeleteAllNotes().delete_all_notes(self.x_user_Key1, self.sid1)

    def tearDown(self) -> None:
        pass

    @parameterized.expand(optionKeys)
    def testCase01(self, key):
        """上传更新便签主体的必填项校验"""
        step("STEP: 上传更新便签主体的接口请求")
        body = {
            'noteId': '',
            "star": 0
        }
        body.pop(key)
        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase02(self):
        """上传更新便签主体的noteId值为空字符串"""
        step("STEP: 上传更新便签主体的接口请求")
        body = {
            'noteId': '',
            "star": 0
        }
        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def testCase03(self):
        """上传更新便签主体的noteId值为None"""
        step("STEP: 上传更新便签主体的接口请求")
        body = {
            'noteId': None,
            "star": 0
        }
        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(optionKeys)
    def testCase04(self, key):
        """上传更新便签主体的非必填项校验"""
        step("STEP: 上传更新便签主体的接口请求")
        noteId = str(int(time.time() * 1000)) + "_noteId"
        groupId = str(int(time.time() * 1000)) + "_groupId"
        body = {
            "noteId": noteId,
            "star": 0,
            "remindTime": 1699282800000,
            "remindType": 0,
            "groupId": groupId
        }
        body.pop(key)

        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(200, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(input_star_empty_list)
    def testCase05(self, input_value, code):
        """上传更新便签主体的star值为None或空"""
        noteId = str(int(time.time() * 1000)) + "_noteId"
        groupId = str(int(time.time() * 1000)) + "_groupId"
        step("STEP: 上传更新便签主体的接口请求")
        body = {
            "noteId": noteId,
            "star": input_value,
            "remindTime": 1699282800000,
            "remindType": 0,
            "groupId": groupId
        }
        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(code, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(input_remindTime_empty_list)
    def testCase06(self, input_value, code):
        """上传更新便签主体的remindTime值为None或空"""
        noteId = str(int(time.time() * 1000)) + "_noteId"
        groupId = str(int(time.time() * 1000)) + "_groupId"
        step("STEP: 上传更新便签主体的接口请求")
        body = {
            "noteId": noteId,
            "star": 0,
            "remindTime": input_value,
            "remindType": 0,
            "groupId": groupId
        }
        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(code, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(input_remindType_empty_list)
    def testCase07(self, input_value, code):
        """上传更新便签主体的remindType值为None或空"""
        noteId = str(int(time.time() * 1000)) + "_noteId"
        groupId = str(int(time.time() * 1000)) + "_groupId"
        step("STEP: 上传更新便签主体的接口请求")
        body = {
            "noteId": noteId,
            "star": 0,
            "remindTime": 1700000000,
            "remindType": input_value,
            "groupId": groupId
        }
        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(code, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(input_groupId_empty_list)
    def testCase08(self, input_value, code):
        """上传更新便签主体的groupId值为None或空"""
        noteId = str(int(time.time() * 1000)) + "_noteId"
        groupId = str(int(time.time() * 1000)) + "_groupId"
        step("STEP: 上传更新便签主体的接口请求")
        body = {
            "noteId": noteId,
            "star": 0,
            "remindTime": 1700000000,
            "remindType": 0,
            "groupId": input_value
        }
        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(code, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(input_noteId_list)
    def testCase09(self, input_value, code):
        """上传更新便签主体的startIndex 入参校验"""
        noteId = str(int(time.time() * 1000)) + "_noteId"
        groupId = str(int(time.time() * 1000)) + "_groupId"
        step("STEP: 上传更新便签主体的接口请求")
        body = {
            "noteId": input_value,
            "star": 0,
        }
        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(code, res.status_code)

    @parameterized.expand(input_star_list)
    def testCase10(self, input_value, code):
        """上传更新便签主体的star 入参校验"""
        noteId = str(int(time.time() * 1000)) + "_noteId"
        groupId = str(int(time.time() * 1000)) + "_groupId"
        step("STEP: 上传更新便签主体的接口请求")
        body = {
            "noteId": noteId,
            "star": input_value,
        }
        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(code, res.status_code)

    @parameterized.expand(input_remindTime_list)
    def testCase11(self, input_value, code):
        """上传更新便签主体的star 入参校验"""
        noteId = str(int(time.time() * 1000)) + "_noteId"
        step("STEP: 上传更新便签主体的接口请求")
        body = {
            "noteId": noteId,
            "star": 0,
            "remindTime": input_value,
            "remindType": 0,
        }
        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(code, res.status_code)

    @parameterized.expand(input_groupId_list)
    def testCase12(self, input_value, code):
        """上传更新便签主体的startIndex 入参校验"""
        noteId = str(int(time.time() * 1000)) + "_noteId"
        step("STEP: 上传更新便签主体的接口请求")
        body = {
            "noteId": noteId,
            "star": 0,
            'groupId': input_value,
        }
        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(code, res.status_code)

    def testCase13(self):
        """上传更新便签主体 X - user - key 入参校验:X-user-key不存在"""
        step("STEP: 上传更新便签主体的接口请求")
        noteId = str(int(time.time() * 1000)) + "_noteId"
        body = {
            "noteId": noteId,
            "star": 0
        }
        res = self.re.post(self.url, body, self.sid1, userId=1)
        self.assertEqual(412, res.status_code)
        expr = {"errorCode": -1011, "errorMsg": "user change!"}
        OutputCheck().assert_output(expr, res.json())

    def testCase14(self):
        """上传更新便签主体 X - user - key 入参校验:X-user-key为空"""
        step("STEP: 上传更新便签主体的接口请求")
        noteId = str(int(time.time() * 1000)) + "_noteId"
        body = {
            "noteId": noteId,
            "star": 0
        }
        res = self.re.post(self.url, body, self.sid1, userId="")
        self.assertEqual(412, res.status_code)
        expr = {"errorCode": -1011, "errorMsg": "user change!"}
        OutputCheck().assert_output(expr, res.json())

    def testCase15(self):
        """上传更新便签主体 wps_sid 入参校验:wps_sid失效"""
        step("STEP: 上传更新便签主体的接口请求")
        noteId = str(int(time.time() * 1000)) + "_noteId"
        body = {
            "noteId": noteId,
            "star": 0
        }
        res = self.re.post(self.url, body, "111111111", self.userId1)
        self.assertEqual(412, res.status_code)
        expr = {"errorCode": -1011, "errorMsg": "user change!"}
        OutputCheck().assert_output(expr, res.json())

    def testCase16(self):
        """上传更新便签主体 wps_sid 入参校验:wps_sid为空"""
        step("STEP: 上传更新便签主体的接口请求")
        noteId = str(int(time.time() * 1000)) + "_noteId"
        body = {
            "noteId": noteId,
            "star": 0
        }
        res = self.re.post(self.url, body, "", self.userId1)
        self.assertEqual(412, res.status_code)
        expr = {"errorCode": -1011, "errorMsg": "user change!"}
        OutputCheck().assert_output(expr, res.json())
