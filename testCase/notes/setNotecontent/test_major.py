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
    assertBase = {
        "responseTime": int,
        "contentVersion": 1,
        "contentUpdateTime": int
    }

    def setUp(self):
        DeleteAllNotes().delete_all_notes(self.x_user_Key1, self.sid1)

    def tearDown(self) -> None:
        pass

    def testCase01_v3_notesvr_set_notecontent(self):
        """"上传跟新便签内容主流程"""
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

        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(200, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())
        # 数据源精准校验
        noteIds = GetAllNotes().get_all_notes(self.x_user_Key1, self.sid1)
        print(f'noteId和noteIds是：{noteId} {noteIds}')
        self.assertEqual(noteId, noteIds[0], msg=f'校验失败，数据不存在{res.text}')
