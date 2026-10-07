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
        self._states = {}

    def observe(self, samples, ts, counter):
        out = []
        for rule in self.rules:
            counter.scanned += 1
            seen = set()
            for sample in samples:
                counter.scanned += 1
                if sample["metric"] != rule["metric"]:
                    continue
                labels = sample.get("labels", {})
                key = (rule["name"], tuple(sorted(labels.items())))
                if key in seen:
                    continue
                seen.add(key)
                state = self._states.setdefault(key, [0, False])
                if _compare(sample["value"], rule["op"], rule["threshold"]):
                    state[0] += 1
                    if state[0] > rule["for"] and not state[1]:
                        state[1] = True
                        out.append({"rule": rule["name"], "labels": dict(labels)})
                else:
                    state[0] = 0
                    state[1] = False
            for key, state in self._states.items():
                if key[0] == rule["name"] and key not in seen:
                    state[0] = 0
                    state[1] = False
        return out
