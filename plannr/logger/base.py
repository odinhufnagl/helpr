import logging

class Logger():
    def __init__(self) -> None:   
        self.logger = logging.getLogger(__name__)
        
        self.logger.addHandler(logging.StreamHandler())
        
    def info(self, msg):
        if self.logger.level != 'INFO':
          self.logger.setLevel('INFO')
        self.logger.info(msg)
        
    
logger = Logger()