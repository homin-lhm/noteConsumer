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
        """便签软删除的主流程"""
        step("STEP: 上传更新便签主体、内容")
        note_content_info_list = SetNoteContentAndNoteInfo().set_note_content_and_note_info(self.userId1, self.sid1, 1)
        step("STEP: 软删除便签的接口请求")
        for i in note_content_info_list:
            noteId = i["noteId"]
            body = {
                "noteId": noteId,
            }
            res = self.re.post(self.url, body, self.sid1, self.userId1)
            self.assertEqual(200, res.status_code)
            expr = self.assertBase
            OutputCheck().assert_output(expr, res.json())
            # 数据源精准校验
            noteIds = GetAllNotes().get_all_notes(self.x_user_Key1, self.sid1)
            print(f'noteId和noteIds是：{noteId} {noteIds}')
            self.assertNotIn(noteId, noteIds, msg=f'校验失败，数据不存在{res.text}')

    def testCase02(self):
        """在分组下，便签软删除的主流程"""
        step("STEP: 在分组下，上传更新便签主体、内容")
        note_content_info_list = CreateGroup().create_group_note("11111111_groupId", self.userId1, self.sid1, 1)
        step("STEP: 软删除便签的接口请求")
        for i in note_content_info_list:
            noteId = i["noteId"]
            body = {
                "noteId": noteId,
            }
            res = self.re.post(self.url, body, self.sid1, self.userId1)
            self.assertEqual(200, res.status_code)
            expr = self.assertBase
            OutputCheck().assert_output(expr, res.json())
            # 数据源精准校验
            noteIds = CreateGroup().get_group_note("11111111_groupId", self.x_user_Key1, self.sid1)
            print(f'noteId和noteIds是：{noteId} {noteIds}')
            self.assertNotIn(noteId, noteIds, msg=f'校验失败，数据不存在{res.text}')


