import re
import time
import unittest

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
        """获取便签内容主流程"""
        step("STEP: 上传更新便签主体、内容")
        note_content_info_list = SetNoteContentAndNoteInfo().set_note_content_and_note_info(self.userId1, self.sid1, 2)
        step("STEP: 获取便签内容的接口请求")
        for i in note_content_info_list:
            noteId = i["noteId"]
            body = {
                "noteIds": [noteId],
            }
            res = self.re.post(self.url, body, self.sid1, self.userId1)
            self.assertEqual(200, res.status_code)
            expr = self.assertBase
            expr["noteBodies"][0]["summary"] = i["summary"]
            expr["noteBodies"][0]["noteId"] = noteId
            expr["noteBodies"][0]["infoNoteId"] = noteId
            expr["noteBodies"][0]["body"] = i["body"]
            expr["noteBodies"][0]["title"] = i["title"]
            OutputCheck().assert_output(expr, res.json())



