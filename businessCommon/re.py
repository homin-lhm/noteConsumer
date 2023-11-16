import requests
import json
from common import caseLog
from common.caseLog import info, error, step


class Re:
    @staticmethod
    def post(url, body, sid, userId, headers=None):
        if headers is None:
            headers = {
                'Content-Type': 'application/json',
                'Cookie': f'wps_sid={sid}',
                'X-user-key': str(userId)
            }
        # 打印header、body、url
        info(f'res url:{url}')
        info(f'res body:{body}')
        info(f'res headers:{headers}')
        try:
            res = requests.post(url, headers=headers, json=body, timeout=3)
        except TimeoutError:
            error(f'{url} requests timeout')
            return "TimeOut!!!"
        info(f'res code:{res.status_code}')
        info(f'res res:{res.text}')
        return res

    @staticmethod
    def get(url, body, sid, userId, header=None):
        pass
