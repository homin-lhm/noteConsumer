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

    def testCase01(self):
        """上传更新便签主内容 handles校验-A用户不可查看B用户的便签"""
        step("STEP: 上传更新便签主体")
        note_info = SetNoteContentAndNoteInfo().set_note_info(self.x_user_Key1, self.sid1, 1)
        step("STEP: 上传更新便签内容的接口请求")
        noteId = note_info[0]["noteId"]
        infoVersion = note_info[0]["infoVersion"]
        body = self.base

        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(200, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())
        # 数据源精准校验
        noteIds = GetAllNotes().get_all_notes(sid="V02SkXpn9EteCABt3NL8cLlvU-p3y_w00ad2fc70000d111849834",
                                              userId="22679353")
        print(f'noteId和noteIds是：{noteId} {noteIds}')
        self.assertEqual(noteId, noteIds[0], msg=f'校验失败，A用户可查看B用户的便签！！！{res.text}')
