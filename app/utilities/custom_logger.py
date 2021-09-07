import logging


class YOLogger(logging.Logger):
    def __init__(self, name: str):
        super().__init__(name)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.addHandler(handler)
