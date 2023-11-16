import unittest


class OutputCheck(unittest.TestCase):
    def assert_output(self, expr, actural, sort_type=None):
        """
        Test the output of the program
        """
        self.assertEqual(len(expr.keys()), len(actural.keys()), msg='key长度不一致')
        for k, v in expr.items():
            self.assertIn(k, actural.keys(), msg=f'{k}不存在')  #
            if isinstance(v, type):
                self.assertEqual(v, type(actural[k]), msg=f'{k}的值不一致, 期望值{v}, 实际值{actural[k]}')
            elif isinstance(v, dict):
                self.assert_output(v, actural[k])
            elif isinstance(v, list):
                self.assertEqual(len(v), len(actural[k]), msg='key长度不一致')
                # if sort_type is not None:
                #     v = sorted(v, key=lambda x: x[sort_type])
                #     actural[k] = sorted(actural[k], key=lambda x: x[sort_type])
                # #     todo
                for i in range(len(v)):
                    if isinstance(v[i], dict):
                        for j in range(len(actural[k])):
                            if isinstance(actural[k][j], dict):
                                if v[i].keys() == actural[k][j].keys():
                                    self.assert_output(v[i], actural[k][j])
                                else:
                                    self.assertEqual(v[i], actural[k][j],
                                                     msg=f'{k}的值不一致1, 期望值{v[i]}, 实际值{actural[k][i]}')

                            else:
                                self.assertEqual(v[i], actural[k][j], msg=f'{k}的值不一致1, 期望值{v[i]}, 实际值{actural[k][i]}')

                    else:
                        self.assertEqual(v[i], actural[k][i], msg=f'{k}的值不一致1, 期望值{v[i]}, 实际值{actural[k][i]}')
            else:
                self.assertEqual(v, actural[k], msg=f'{k}的值不一致, 期望值{v}, 实际值{actural[k]}')





# if __name__ == "__main__":
#     expr = {"q": 1, "w": 2}
#     actural = {"q": 2, "w": 2}
#     OutputCheck().assert_output(expr, actural)
