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


class NoteDelete(unittest.TestCase):
    re = Re()
    envConfig = YamlRead().env_config()
    dataConfig = YamlRead().data_config()
    sid1 = envConfig["sid1"]
    userId1 = envConfig["userId1"]
    host = envConfig["host"]
    x_user_Key1 = envConfig["x_user_Key1"]
    sid2 = envConfig["sid2"]
    userId2 = envConfig["userId2"]
    x_user_Key2 = envConfig["x_user_Key2"]
    url = host + dataConfig["interface"]["NoteDelete"]["path"]
    base = dataConfig["interface"]["NoteDelete"]["base"]
    assertBase = {
                "responseTime": int,
            }

    def setUp(self):
        DeleteAllNotes().delete_all_notes(self.x_user_Key1, self.sid1)

    def tearDown(self) -> None:
        pass

    def testCase01(self):
        """软删除便签-handles校验-A用户不可删除B用户的便签"""
        step("STEP: 上传更新便签主体、内容")
        note_content_info_list = SetNoteContentAndNoteInfo().set_note_content_and_note_info(self.userId1, self.sid1, 1)
        step("STEP: 软删除便签的接口请求")
        for i in note_content_info_list:
            noteId = i["noteId"]
            body = {
                "noteId": noteId,
            }
            res = self.re.post(self.url, body, self.sid2, self.userId2)
            self.assertEqual(200, res.status_code)
            expr = self.assertBase
            OutputCheck().assert_output(expr, res.json())
            # 数据源精准校验
            noteIds = GetAllNotes().get_all_notes(self.x_user_Key1, self.sid1)
            info(f'noteId和noteIds是：{noteId} {noteIds}')
            self.assertEqual(noteId, noteIds[0], msg=f'校验失败，数据不存在{res.text}')







