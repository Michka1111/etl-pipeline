class MetaViewFilter:
    def __init__(self, log):
        self.log = log

    def filter(self, **criteria):
        return [
            entry for entry in self.log
            if all(entry.get(k) == v for k, v in criteria.items())
        ]
