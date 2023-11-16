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


class SetGroupNote(unittest.TestCase):
    re = Re()
    envConfig = YamlRead().env_config()
    dataConfig = YamlRead().data_config()
    sid1 = envConfig["sid1"]
    userId1 = envConfig["userId1"]
    host = envConfig["host"]
    x_user_Key1 = envConfig["x_user_Key1"]
    url = host + dataConfig["interface"]["SetNoteGroup"]["path"]
    base = dataConfig["interface"]["SetNoteGroup"]["base"]
    assertBase = {"responseTime": int, "updateTime": int}

    def setUp(self):
        DeleteAllNotes().delete_all_notes(self.x_user_Key1, self.sid1)
        info("PRE_STEP：获得所有分组")
        groupIds = CreateGroup().get_group(self.x_user_Key1, self.sid1)
        step("PRE_STEP：获得分组下便签")
        for groupId in groupIds:
            noteIds = CreateGroup().get_group_note(groupId, self.x_user_Key1, self.sid1)
            for noteId in noteIds:
                step("PRE_STEP：删除分组下便签")
                DeleteAllNotes().delete_notes(noteId, self.x_user_Key1, self.sid1)
            step("PRE_STEP：删除分组")
            if groupId == "226793524":
                continue
            CreateGroup().delete_group(self.x_user_Key1, self.sid1, groupId)

    def tearDown(self) -> None:
        pass

    def testCase01_v3_notesvr_set_notegroup(self):
        """新增分组的主流程"""
        step("STEP: 新增分组的接口请求")
        groupName = str(int(time.time() * 1000)) + "_groupName"
        groupId = str(int(time.time() * 1000)) + "_groupId"
        body = {
          "groupName": groupName,
          "groupId": groupId,
          "order": 0
        }
        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(200, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json())
        step("STEP:获取分组列表")
        groupIds = CreateGroup().get_group(self.userId1, self.sid1)
        self.assertIn(groupId, groupIds)

