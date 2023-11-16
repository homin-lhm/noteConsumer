# todo
# valid	int	便签是否有效(1:有效，0：回收站，2：从回收站删除)
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
        """获取便签内容 handles校验-A用户不可查看B用户的便签"""
        step("STEP: 上传更新便签主体、内容")
        note_content_info_list = SetNoteContentAndNoteInfo().set_note_content_and_note_info(self.userId1, self.sid1, 1)
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
            # 数据源精准校验
            noteIds = GetAllNotes().get_all_notes(sid="V02SZjpl_yuVlqJhROP2TXX4oEH0YJg00ae3f64d000b74ebde", userid="192211934")
            print(f'noteId和noteIds是：{noteId} {noteIds}')
            self.assertNotIn(noteId, noteIds, msg=f'校验失败，A用户可查看B用户的便签！！！{res.text}')



