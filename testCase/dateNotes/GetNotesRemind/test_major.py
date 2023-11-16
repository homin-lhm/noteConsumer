import re
import unittest
import time

from common.caseLog import info, error, step
from common.outputCheck import OutputCheck
from common.yamlRead import YamlRead
from businessCommon.re import Re
from businessCommon.clearNotes import DeleteAllNotes
from businessCommon.createGroup import CreateGroup
from businessCommon.createNotes import SetNoteContentAndNoteInfo
from businessCommon.getRemindNotes import GetRemindNotes



class SetGroupNote(unittest.TestCase):
    re = Re()
    envConfig = YamlRead().env_config()
    dataConfig = YamlRead().data_config()
    sid1 = envConfig["sid1"]
    userId1 = envConfig["userId1"]
    host = envConfig["host"]
    x_user_Key1 = envConfig["x_user_Key1"]
    url = host + dataConfig["interface"]["GetNotesRemind"]["path"]
    base = dataConfig["interface"]["GetNotesRemind"]["base"]
    assertBase = {
        "responseTime": 0,
        "webNotes": [
            {
                "noteId": "21cdd0380b6a87287527771fa36ea831",
                "createTime": int,
                "star": 0,
                "remindTime": 1700186400000,
                "remindType": 1,
                "infoVersion": 1,
                "infoUpdateTime": int,
                "groupId": None,
                "title": str,
                "summary": str,
                "thumbnail": None,
                "contentVersion": 1,
                "contentUpdateTime": int
            }
        ]

    }

    def setUp(self):
        DeleteAllNotes().delete_all_notes(self.x_user_Key1, self.sid1)
        noteIds = GetRemindNotes().get_remind_notes(self.x_user_Key1, self.sid1)
        for noteId in noteIds:
            DeleteAllNotes().delete_notes(noteId, self.x_user_Key1, self.sid1)


    def tearDown(self) -> None:
        pass

    def testCase01(self, remindTime=1700186400000):
        """查看日历下便签的主流程"""
        step("STEP: 上传更新便签主体、内容")
        note_content_info_list = SetNoteContentAndNoteInfo().set_note_content_and_note_info(self.userId1, self.sid1, 1,
                                                                                            remindTime=1700186400000)
        step("STEP: 查看日历下便签的主流程的接口请求")
        # remindStartTime = str(int(time.time() * 1000))
        body = self.base
        body["remindStartTime"] = remindTime
        body["remindEndTime"] = remindTime

        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(200, res.status_code)
        expr = self.assertBase
        expr["webNotes"][0]["noteId"] = note_content_info_list[0]["noteId"]
        OutputCheck().assert_output(expr, res.json())
        # step("STEP:获取分组列表")
        # groupIds = CreateGroup().get_group(self.userId1, self.sid1)
        # self.assertNotIn(groupId, groupIds)
