import yaml
from main import ENVIRON, Dir


class YamlRead:
    @staticmethod
    def env_config():
        """
        读取环境配置，字典结构
        """
        file = f'{Dir}/envConfig/{ENVIRON}/config.yaml'
        with open(file=file, mode="r", encoding="utf-8")as f:
            return yaml.load(f,  Loader=yaml.FullLoader)

    @staticmethod
    def data_config():
        """"
        读取数据配置，字典结构
        """
        file = f'{Dir}/data/interface_config.yaml'
        with open(file=file, mode="r", encoding="utf-8")as f:
            return yaml.load(f, Loader=yaml.FullLoader)
