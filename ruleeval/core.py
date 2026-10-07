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


def _labels_key(labels):
    return tuple(sorted(labels.items()))


class Evaluator:
    def __init__(self, rules):
        self.rules = rules
        self._states = [{} for _ in rules]

    def observe(self, samples, ts, counter):
        out = []
        for index, rule in enumerate(self.rules):
            counter.scanned += 1
            states = self._states[index]
            current = {}
            for sample in samples:
                counter.scanned += 1
                if sample["metric"] != rule["metric"]:
                    continue
                labels = sample.get("labels", {})
                key = _labels_key(labels)
                if key not in current:
                    current[key] = [labels, False]
                if _compare(sample["value"], rule["op"], rule["threshold"]):
                    current[key][1] = True
            for key in list(states):
                if key not in current:
                    del states[key]
            for key, (labels, matched) in current.items():
                state = states.get(key)
                if state is None:
                    state = {"streak": 0, "firing": False, "labels": labels}
                    states[key] = state
                if matched:
                    state["streak"] += 1
                    if not state["firing"] and state["streak"] >= rule.get("for", 0):
                        state["firing"] = True
                        out.append({"rule": rule["name"], "labels": dict(labels)})
                else:
                    state["streak"] = 0
                    state["firing"] = False
        return out
