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


class SetNoteContent(unittest.TestCase):
    re = Re()
    envConfig = YamlRead().env_config()
    dataConfig = YamlRead().data_config()
    sid1 = envConfig["sid1"]
    userId1 = envConfig["userId1"]
    host = envConfig["host"]
    x_user_Key1 = envConfig["x_user_Key1"]
    url = host + dataConfig["interface"]["SetNoteContent"]["path"]
    base = dataConfig["interface"]["SetNoteContent"]["base"]
    optionKeys = dataConfig["interface"]["SetNoteContent"]["optionKeys"]
    input_noteId_empty_list = dataConfig["interface"]["SetNoteContent"]["input_noteId_empty_list"]
    input_body_empty_list = dataConfig["interface"]["SetNoteContent"]["input_body_empty_list"]
    input_title_list = dataConfig["interface"]["SetNoteContent"]["input_title_list"]
    input_summary_list = dataConfig["interface"]["SetNoteContent"]["input_summary_list"]
    input_localContentVersion_list = dataConfig["interface"]["SetNoteContent"]["input_localContentVersion_list"]
    input_bodyType_list = dataConfig["interface"]["SetNoteContent"]["input_bodyType_list"]
    assertBase = {
        "responseTime": int,
        "contentVersion": 1,
        "contentUpdateTime": int
    }

    def setUp(self):
        DeleteAllNotes().delete_all_notes(self.x_user_Key1, self.sid1)

    def tearDown(self) -> None:
        pass

    def _testCase01(self):
        """上传更新便签主体noteid必填项校验        """
        step("STEP: 上传更新便签主体")
        note_info = SetNoteContentAndNoteInfo().set_note_info(self.x_user_Key1, self.sid1, 1)
        step("STEP: 上传更新便签内容的接口请求")
        noteId = note_info[0]["noteId"]
        infoVersion = note_info[0]["infoVersion"]
        body = {"title": "oZIyHTsF3CyIESOiGvuiEQ==",
                "summary": "R/RUQ/JH1ma9R2FVaaUzAphoLyPYh3RVXs45PBwgMOA=",
                "body": "R/RUQ/JH1ma9R2FVaaUzAtwlXImqcX++1wS1GmEpgL8=",
                "localContentVersion": infoVersion,
                # "noteId": noteId,
                "bodyType": 0}  # "thumbnail": null,

        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(input_noteId_empty_list)
    def _testCase02(self, input_value, code):
        """上传更新便签主体noteid值为空        """
        step("STEP: 上传更新便签主体")
        note_info = SetNoteContentAndNoteInfo().set_note_info(self.x_user_Key1, self.sid1, 1)
        step("STEP: 上传更新便签内容的接口请求")
        noteId = note_info[0]["noteId"]
        infoVersion = note_info[0]["infoVersion"]
        body = {"title": "oZIyHTsF3CyIESOiGvuiEQ==",
                "summary": "R/RUQ/JH1ma9R2FVaaUzAphoLyPYh3RVXs45PBwgMOA=",
                "body": "R/RUQ/JH1ma9R2FVaaUzAtwlXImqcX++1wS1GmEpgL8=",
                "localContentVersion": infoVersion,
                "noteId": input_value,
                "bodyType": 0}  # "thumbnail": null,

        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(code, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def _testCase03(self):
        """上传更新便签主体body必填项校验        """
        step("STEP: 上传更新便签主体")
        note_info = SetNoteContentAndNoteInfo().set_note_info(self.x_user_Key1, self.sid1, 1)
        step("STEP: 上传更新便签内容的接口请求")
        noteId = note_info[0]["noteId"]
        infoVersion = note_info[0]["infoVersion"]
        body = {"title": "oZIyHTsF3CyIESOiGvuiEQ==",
                "summary": "R/RUQ/JH1ma9R2FVaaUzAphoLyPYh3RVXs45PBwgMOA=",
                # "body": "R/RUQ/JH1ma9R2FVaaUzAtwlXImqcX++1wS1GmEpgL8=",
                "localContentVersion": infoVersion,
                "noteId": noteId,
                "bodyType": 0}  # "thumbnail": null,

        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(412, res.status_code)
        expr = {"errorCode": -1012, "errorMsg": "Note body Requested!"}
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(input_body_empty_list)
    def _testCase04(self, input_value, code):
        """上传更新便签主体body必填项校验        """
        step("STEP: 上传更新便签主体")
        note_info = SetNoteContentAndNoteInfo().set_note_info(self.x_user_Key1, self.sid1, 1)
        step("STEP: 上传更新便签内容的接口请求")
        noteId = note_info[0]["noteId"]
        infoVersion = note_info[0]["infoVersion"]
        body = {"title": "oZIyHTsF3CyIESOiGvuiEQ==",
                "summary": "R/RUQ/JH1ma9R2FVaaUzAphoLyPYh3RVXs45PBwgMOA=",
                "body": input_value,
                "localContentVersion": infoVersion,
                "noteId": noteId,
                "bodyType": 0}  # "thumbnail": null,

        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(code, res.status_code)
        expr = {"errorCode": -1012, "errorMsg": "Note body Requested!"}
        OutputCheck().assert_output(expr, res.json())

    @parameterized.expand(optionKeys)
    def testCase05(self, key):
        """上传更新便签主体非必填项校验        """
        step("STEP: 上传更新便签主体")
        note_info = SetNoteContentAndNoteInfo().set_note_info(self.x_user_Key1, self.sid1, 1)
        step("STEP: 上传更新便签内容的接口请求")
        noteId = note_info[0]["noteId"]
        infoVersion = note_info[0]["infoVersion"]
        body = {"title": "oZIyHTsF3CyIESOiGvuiEQ==",
                "summary": "R/RUQ/JH1ma9R2FVaaUzAphoLyPYh3RVXs45PBwgMOA=",
                "body": "R/RUQ/JH1ma9R2FVaaUzAtwlXImqcX++1wS1GmEpgL8=",
                "localContentVersion": infoVersion,
                "noteId": noteId,
                "bodyType": 0}  # "thumbnail": null,
        body.pop(key)

        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(200, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    # todo
    @parameterized.expand(input_title_list)
    def _testCase06(self, input_value, code):
        """上传更新便签主体非必填项title"""
        step("STEP: 上传更新便签主体")
        note_info = SetNoteContentAndNoteInfo().set_note_info(self.x_user_Key1, self.sid1, 1)
        step("STEP: 上传更新便签内容的接口请求")
        noteId = note_info[0]["noteId"]
        infoVersion = note_info[0]["infoVersion"]
        body = {"title": input_value,
                "summary": "R/RUQ/JH1ma9R2FVaaUzAphoLyPYh3RVXs45PBwgMOA=",
                "body": "R/RUQ/JH1ma9R2FVaaUzAtwlXImqcX++1wS1GmEpgL8=",
                "localContentVersion": infoVersion,
                "noteId": noteId,
                "bodyType": 0}  # "thumbnail": null,

        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(code, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())
        # 数据源精准校验
        noteIds = GetAllNotes().get_all_notes(self.x_user_Key1, self.sid1)
        print(f'noteId和noteIds是：{noteId} {noteIds}')
        self.assertEqual(noteId, noteIds[0], msg=f'校验失败，数据不存在{res.text}')

    # todo
    @parameterized.expand(input_summary_list)
    def _testCase07(self, input_value, code):
        """上传更新便签主体非必填项summary"""
        step("STEP: 上传更新便签主体")
        note_info = SetNoteContentAndNoteInfo().set_note_info(self.x_user_Key1, self.sid1, 1)
        step("STEP: 上传更新便签内容的接口请求")
        noteId = note_info[0]["noteId"]
        infoVersion = note_info[0]["infoVersion"]
        body = {"title": "oZIyHTsF3CyIESOiGvuiEQ==",
                "summary": input_value,
                "body": "R/RUQ/JH1ma9R2FVaaUzAtwlXImqcX++1wS1GmEpgL8=",
                "localContentVersion": infoVersion,
                "noteId": noteId,
                "bodyType": 0}  # "thumbnail": null,

        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(code, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())
        # 数据源精准校验
        noteIds = GetAllNotes().get_all_notes(self.x_user_Key1, self.sid1)
        print(f'noteId和noteIds是：{noteId} {noteIds}')
        self.assertEqual(noteId, noteIds[0], msg=f'校验失败，数据不存在{res.text}')

    # todo
    @parameterized.expand(input_localContentVersion_list)
    def _testCase08(self, input_value, code):
        """上传更新便签主体非必填项localContentVersion"""
        step("STEP: 上传更新便签主体")
        note_info = SetNoteContentAndNoteInfo().set_note_info(self.x_user_Key1, self.sid1, 1)
        step("STEP: 上传更新便签内容的接口请求")
        noteId = note_info[0]["noteId"]
        infoVersion = note_info[0]["infoVersion"]
        body = {"title": "oZIyHTsF3CyIESOiGvuiEQ==",
                "summary": "R/RUQ/JH1ma9R2FVaaUzAphoLyPYh3RVXs45PBwgMOA=",
                "body": "R/RUQ/JH1ma9R2FVaaUzAtwlXImqcX++1wS1GmEpgL8=",
                "localContentVersion": input_value,
                "noteId": noteId,
                "bodyType": 0}  # "thumbnail": null,

        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(code, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())
        # 数据源精准校验
        noteIds = GetAllNotes().get_all_notes(self.x_user_Key1, self.sid1)
        print(f'noteId和noteIds是：{noteId} {noteIds}')
        self.assertEqual(noteId, noteIds[0], msg=f'校验失败，数据不存在{res.text}')

    # todo
    @parameterized.expand(input_bodyType_list)
    def _testCase09(self, input_value, code):
        """上传更新便签主体非必填项bodyType"""
        step("STEP: 上传更新便签主体")
        note_info = SetNoteContentAndNoteInfo().set_note_info(self.x_user_Key1, self.sid1, 1)
        step("STEP: 上传更新便签内容的接口请求")
        noteId = note_info[0]["noteId"]
        infoVersion = note_info[0]["infoVersion"]
        body = {"title": "oZIyHTsF3CyIESOiGvuiEQ==",
                "summary": "R/RUQ/JH1ma9R2FVaaUzAphoLyPYh3RVXs45PBwgMOA=",
                "body": "R/RUQ/JH1ma9R2FVaaUzAtwlXImqcX++1wS1GmEpgL8=",
                "localContentVersion": infoVersion,
                "noteId": noteId,
                "bodyType": input_value}  # "thumbnail": null,

        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(code, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())
        # 数据源精准校验
        noteIds = GetAllNotes().get_all_notes(self.x_user_Key1, self.sid1)
        print(f'noteId和noteIds是：{noteId} {noteIds}')
        self.assertEqual(noteId, noteIds[0], msg=f'校验失败，数据不存在{res.text}')

    # todo
    def _testCase10(self):
        """上传更新便签主体非必填项bodyType值为-1"""
        step("STEP: 上传更新便签主体")
        note_info = SetNoteContentAndNoteInfo().set_note_info(self.x_user_Key1, self.sid1, 1)
        step("STEP: 上传更新便签内容的接口请求")
        noteId = note_info[0]["noteId"]
        infoVersion = note_info[0]["infoVersion"]
        body = {"title": "oZIyHTsF3CyIESOiGvuiEQ==",
                "summary": "R/RUQ/JH1ma9R2FVaaUzAphoLyPYh3RVXs45PBwgMOA=",
                "body": "R/RUQ/JH1ma9R2FVaaUzAtwlXImqcX++1wS1GmEpgL8=",
                "localContentVersion": infoVersion,
                "noteId": noteId,
                "bodyType": -1}  # "thumbnail": null,

        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    # todo
    def _testCase11(self):
        """上传更新便签主体非必填项bodyType值为小数"""
        step("STEP: 上传更新便签主体")
        note_info = SetNoteContentAndNoteInfo().set_note_info(self.x_user_Key1, self.sid1, 1)
        step("STEP: 上传更新便签内容的接口请求")
        noteId = note_info[0]["noteId"]
        infoVersion = note_info[0]["infoVersion"]
        body = {"title": "oZIyHTsF3CyIESOiGvuiEQ==",
                "summary": "R/RUQ/JH1ma9R2FVaaUzAphoLyPYh3RVXs45PBwgMOA=",
                "body": "R/RUQ/JH1ma9R2FVaaUzAtwlXImqcX++1wS1GmEpgL8=",
                "localContentVersion": infoVersion,
                "noteId": noteId,
                "bodyType": 2.1}  # "thumbnail": null,

        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def _testCase12(self):
        """
        上传更新便签主体X - user - key
        入参校验: X - user - key不存在
        """
        step("STEP: 上传更新便签内容的接口请求")
        body = self.base
        res = self.re.post(self.url, body, self.sid1, userId=1)
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())

    def _testCase13(self):
        """
        上传更新便签主体X - user - key
        入参校验: X - user - key为空
        """
        step("STEP: 上传更新便签内容的接口请求")
        body = self.base
        res = self.re.post(self.url, body, self.sid1, userId="")
        self.assertEqual(500, res.status_code)
        expr = {"errorCode": -7, "errorMsg": "参数不合法！"}
        OutputCheck().assert_output(expr, res.json())


    def _testCase14(self):
        """
        上传更新便签主体 wps_sid 入参校验:wps_sid失效
        """
        step("STEP: 上传更新便签内容的接口请求")
        body = self.base
        res = self.re.post(self.url, body, "111111111", self.userId1)
        self.assertEqual(412, res.status_code)
        expr = {"errorCode": -1011, "errorMsg": "user change!"}
        OutputCheck().assert_output(expr, res.json())

    def _testCase15(self):
        """
        上传更新便签主体 wps_sid 入参校验:wps_sid为空
        """
        step("STEP: 上传更新便签内容的接口请求")
        body = self.base
        res = self.re.post(self.url, body, "", self.userId1)
        self.assertEqual(412, res.status_code)
        expr = {"errorCode": -1011, "errorMsg": "user change!"}
        OutputCheck().assert_output(expr, res.json())
