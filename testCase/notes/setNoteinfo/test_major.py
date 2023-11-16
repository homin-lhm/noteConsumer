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
        """
        Test case for v3_notesvr_set_noteinfo
        """
        step("STEP: 上传更新便签主体的接口请求——普通便签")
        noteId = str(int(time.time() * 1000)) + "_noteId"
        body = {"noteId": noteId, "star": 0}
        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(200, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    def testCase02_v3_notesvr_set_noteinfo(self):
        """
        Test case for v3_notesvr_set_noteinfo
        """
        step("STEP: 上传更新便签主体的接口请求——日历便签")
        noteId = str(int(time.time() * 1000)) + "_noteId"
        body = {"noteId": noteId, "star": 0, "remindTime": 1699282800000, "remindType": 0}
        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(200, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())

    def testCase03_v3_notesvr_set_noteinfo(self):
        """
        Test case for v3_notesvr_set_noteinfo
        """
        step("STEP: 上传更新便签主体的接口请求——分组便签")
        noteId = str(int(time.time() * 1000)) + "_noteId"
        groupId = str(int(time.time() * 1000)) + "_groupId"
        body = {"noteId": noteId, "star": 0, "groupId": groupId}
        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(200, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())
