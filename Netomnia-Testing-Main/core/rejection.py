class RejectionCollector:

    def __init__(self):
        self.items = []
        self.seen = set()  

    def add(self, feature_id, code, reason):

        key = (feature_id, code, reason)

        # Skip if already added
        if key in self.seen:
            return

        self.seen.add(key)

        self.items.append({"feature_id": feature_id,"code": code,"reason": reason})

    def to_list(self):
        return self.items