import re
import unittest
from common.caseLog import info, error, step
from common.outputCheck import OutputCheck
from common.yamlRead import YamlRead
from businessCommon.re import Re
from businessCommon.clearNotes import DeleteAllNotes
from businessCommon.createGroup import CreateGroup
from businessCommon.createNotes import SetNoteContentAndNoteInfo


class GetNoteGroup(unittest.TestCase):
    re = Re()
    envConfig = YamlRead().env_config()
    dataConfig = YamlRead().data_config()
    sid1 = envConfig["sid1"]
    userId1 = envConfig["userId1"]
    host = envConfig["host"]
    x_user_Key1 = envConfig["x_user_Key1"]
    url = host + dataConfig["interface"]["GetNoteGroup"]["path"]
    base = dataConfig["interface"]["GetNoteGroup"]["base"]
    assertBase = {
        "noteGroups": [
            {
                "userId": "226793524",
                "groupId": str,
                "groupName": str,
                "order": 0,
                "valid": 1,
                "updateTime": int
            },
            {
                "userId": "226793524",
                "groupId": str,
                "groupName": str,
                "order": 0,
                "valid": 1,
                "updateTime": int
            }
        ],
        "requestTime": int
    }

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

    def testCase01(self):
        """获取分组列表的主流程"""
        step("PRE-STEP：新增一个分组")
        groupIds = CreateGroup().create_group(self.userId1, self.sid1, 1)  #原先有一个自己账号的分组，后来创建了一个
        step("STEP: 获取分组列表的接口请求")
        body = self.base
        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(200, res.status_code)
        expr = self.assertBase
        OutputCheck().assert_output(expr, res.json(), sort_type="groupId")
        expr['noteGroups'][0]['groupId'] = self.userId1
        expr['noteGroups'][1]['groupId'] = groupIds[0]
        expr['noteGroups'][0]['userId'] = self.userId1
        expr['noteGroups'][1]['userId'] = self.userId1
        expr_groupIds = []
        actural_groupIds = []
        for i in expr['noteGroups']:
            expr_groupIds.append(i['groupId'])
        for i in res.json()['noteGroups']:
            actural_groupIds.append(i['groupId'])
        assert expr_groupIds.sort() == actural_groupIds.sort()
