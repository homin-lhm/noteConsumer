import re
import unittest
from common.caseLog import info, error, step
from common.outputCheck import OutputCheck
from common.yamlRead import YamlRead
from businessCommon.re import Re
from copy import deepcopy
from businessCommon.clearNotes import DeleteAllNotes
from businessCommon.createGroup import CreateGroup
from businessCommon.createNotes import SetNoteContentAndNoteInfo


class GetGroupNote(unittest.TestCase):
    re = Re()
    envConfig = YamlRead().env_config()
    dataConfig = YamlRead().data_config()
    sid1 = envConfig["sid1"]
    userId1 = envConfig["userId1"]
    host = envConfig["host"]
    x_user_Key1 = envConfig["x_user_Key1"]
    url = host + dataConfig["interface"]["GetGroupNote"]["path"]
    base = dataConfig["interface"]["GetGroupNote"]["base"]
    assertBase = {
        'responseTime': int,
        'webNotes': [
            {
                'noteId': '',
                'createTime': int,
                'star': 0,
                'remindTime': 0,
                'remindType': 0,
                'infoVersion': int,
                'infoUpdateTime': int,
                'groupId': '',
                'title': 'oZIyHTsF3CyIESOiGvuiEQ==',
                'summary': 'R/RUQ/JH1ma9R2FVaaUzAphoLyPYh3RVXs45PBwgMOA=',
                'thumbnail': None,
                'contentVersion': int,
                'contentUpdateTime': int
            }
        ]
    }

    def setUp(self):
        DeleteAllNotes().delete_all_notes(self.x_user_Key1, self.sid1)

    def tearDown(self) -> None:
        pass

    def testCase01(self):
        """查看分组下便签的主流程"""
        step("PRE-STEP：新增一个分组")
        groupIds = CreateGroup().create_group(self.userId1, self.sid1, 1)
        step("PRE-STEP：在分组下新增一个便签")
        group_note_content_info = CreateGroup().create_group_note(groupIds[0], self.userId1, self.sid1, 1)
        step("STEP: 查看分组下便签的接口请求")
        body = self.base
        body["groupId"] = groupIds[0]

        res = self.re.post(self.url, body, self.sid1, self.userId1)
        self.assertEqual(200, res.status_code)
        expr = deepcopy(self.assertBase)
        expr['webNotes'][0]['noteId'] = group_note_content_info["noteIds"][0]
        expr['webNotes'][0]['groupId'] = groupIds[0]
        OutputCheck().assert_output(expr, res.json())









