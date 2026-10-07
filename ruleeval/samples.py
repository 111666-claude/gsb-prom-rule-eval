"""固定场景，用来复现题面里的锚点。"""

import json

from . import core


def _line(obj):
    print(json.dumps(obj, ensure_ascii=False))


def sample(metric, value, **labels):
    return {"metric": metric, "value": value, "labels": labels}


def run(name):
    if name == "for":
        rules = [{"name": "high", "metric": "m", "op": ">", "threshold": 5, "for": 10}]
        ev = core.Evaluator(rules)
        total = 0
        for ts in range(12):
            total += len(ev.observe([sample("m", 9)], ts, core.Counter()))
        _line({"fires": total})
        return 0
    if name == "reset":
        rules = [{"name": "high", "metric": "m", "op": ">", "threshold": 5, "for": 10}]
        ev = core.Evaluator(rules)
        total = 0
        for ts in range(21):
            total += len(ev.observe([sample("m", 9 if ts <= 5 else 1)], ts, core.Counter()))
        _line({"fires": total})
        return 0
    if name == "group":
        rules = [{"name": "high", "metric": "m", "op": ">", "threshold": 5, "for": 0}]
        ev = core.Evaluator(rules)
        fires = ev.observe([sample("m", 9, a="1"), sample("m", 9, a="2")], 0, core.Counter())
        _line({"fires": len(fires)})
        return 0
    if name == "once":
        rules = [{"name": "high", "metric": "m", "op": ">", "threshold": 5, "for": 0}]
        ev = core.Evaluator(rules)
        total = 0
        for ts in range(4):
            total += len(ev.observe([sample("m", 9)], ts, core.Counter()))
        _line({"fires": total})
        return 0
    if name == "work":
        rules = [{"name": "high", "metric": "m", "op": ">", "threshold": 5, "for": 0}]
        ev = core.Evaluator(rules)
        counter = core.Counter()
        for ts in range(800):
            ev.observe([sample("m", 9)], ts, counter)
        _line({"ticks": 800, "scanned": counter.scanned})
        return 0
    raise SystemExit("未知场景：" + name)
