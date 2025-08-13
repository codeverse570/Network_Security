from dataclasses import dataclass

@dataclass
class ArtificatConfig:
    def __init__(self, train_file,test_file):
        self.train_file=train_file
        self.test_file=test_file