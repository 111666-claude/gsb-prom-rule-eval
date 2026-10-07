"""按 tick 求值告警规则。"""


class Counter:
    """记录比较次数。"""

    def __init__(self):
        self.scanned = 0


def _compare(value, op, threshold):
    if op == ">":
        return value > threshold
    if op == ">=":
        return value >= threshold
    if op == "<":
        return value < threshold
    return value == threshold


class Evaluator:
    def __init__(self, rules):
        self.rules = rules
        self.history = []

    def observe(self, samples, ts, counter):
        self.history.extend(samples)
        out = []
        for rule in self.rules:
            counter.scanned += 1
            matched = False
            for sample in self.history:
                counter.scanned += 1
                if sample["metric"] == rule["metric"] and _compare(
                        sample["value"], rule["op"], rule["threshold"]):
                    matched = True
            if matched:
                out.append({"rule": rule["name"], "labels": {}})
        return out
