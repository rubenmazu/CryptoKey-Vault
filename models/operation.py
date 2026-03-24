class Operation:
    def __init__(self, id, file_id, key_id, algorithm_id, op_type, framework, time, memory, file_hash, date):
        self.id = id
        self.file_id = file_id
        self.key_id = key_id
        self.algorithm_id = algorithm_id
        self.op_type = op_type
        self.framework = framework
        self.time = time
        self.memory = memory
        self.file_hash = file_hash
        self.date = date
