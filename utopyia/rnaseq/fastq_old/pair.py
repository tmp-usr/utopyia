class FastQPair(object):
    def __init__(self, reads_1, reads_2, name= "", compressed= True, ):
        self.name = name
        self.reads_1 = reads_1
        self.reads_2 = reads_2
        self.compressed = compressed

