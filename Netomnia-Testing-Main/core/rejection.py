class RejectionCollector:

    def __init__(self):
        self.items = []

    def add(self, feature_id, code, reason):
        self.items.append({
            "feature_id": feature_id,
            "code": code,
            "reason": reason
        })

    def to_list(self):
        return self.items

    def print_all(self):
        if not self.items:
            print("\nNo rejected features")
            return

        print("\nRejected Features")
        print("=" * 50)
        for r in self.items:
            print(
                f"Feature ID: {r['feature_id']} | "
                f"Code: {r['code']} | "
                f"Reason: {r['reason']}"
            )