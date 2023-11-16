import re
import time
import unittest
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
    assertBase = {
        'responseTime': int,
        'infoVersion': int,
        'infoUpdateTime': int,
    }

    def setUp(self):
        DeleteAllNotes().delete_all_notes(self.x_user_Key1, self.sid1)

    def tearDown(self) -> None:
        pass

    def testCase01_v3_notesvr_set_noteinfo(self):
        step("STEP: 上传更新便签主体的接口请求——star为0")
        noteId = str(int(time.time() * 1000)) + "_noteId"
        body = {
            "noteId": noteId,
            "star": 0,
        }
        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(200, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    def testCase02_v3_notesvr_set_noteinfo(self):
        step("STEP: 上传更新便签主体的接口请求——star为1")
        noteId = str(int(time.time() * 1000)) + "_noteId"
        body = {
            "noteId": noteId,
            "star": 1,
        }
        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(200, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    def testCase03_v3_notesvr_set_noteinfo(self):
        step("STEP: 上传更新便签主体的接口请求——remindType为0")
        noteId = str(int(time.time() * 1000)) + "_noteId"
        body = {
            "noteId": noteId,
            "remindTime": 0,
            "remindType": 0,
        }
        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(200, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    def testCase04_v3_notesvr_set_noteinfo(self):
        step("STEP: 上传更新便签主体的接口请求——remindType为1")
        noteId = str(int(time.time() * 1000)) + "_noteId"
        body = {
            "noteId": noteId,
            "remindTime": 170000000000,
            "remindType": 1,
        }
        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(200, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    def testCase05_v3_notesvr_set_noteinfo(self):
        step("STEP: 上传更新便签主体的接口请求——remindType为2")
        noteId = str(int(time.time() * 1000)) + "_noteId"
        body = {
            "noteId": noteId,
            "remindTime": 170000000000,
            "remindType": 2,
        }
        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(200, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    def testCase06(self):
        """上传更新便签主体 handles校验-A用户不可查看B用户的便签"""
        step("STEP: 上传更新便签主体的接口请求")
        noteId = str(int(time.time() * 1000)) + "_noteId"
        body = {
            "noteId": noteId,
            "star": 1,
        }

        res = self.re.post(self.url, body, sid="V02SkXpn9EteCABt3NL8cLlvU-p3y_w00ad2fc70000d111849834", userId="22679353")
        assert group_note_content_info["noteIds"][0] not in res.json()
        assert groupIds[0] not in res.json()