# prom-rule-eval

按 tick 求值告警规则：连续为真满 for 时长才触发，条件转假就复位，分组分别记账，触发只报一次。只用 Python 标准库。

```
python3 -m unittest discover -s tests
python3 -m ruleeval --sample=for
python3 -m ruleeval --sample=reset
python3 -m ruleeval --sample=group
python3 -m ruleeval --sample=once
python3 -m ruleeval --sample=work
```

## 口径

- **判定**：样本指标名与规则一致、且按规则里的比较符号与阈值判真。
- **for**：条件连续为真满 `for` 个时间单位才触发（含起点的那一 tick）。
- **复位**：条件转为假时，该组的已经等待时长清零。
- **分组**：按规则名与样本标签组合分组，各组的等待与触发互不影响。
- **一次**：只在"从未触发"变成"触发"的那一 tick 报一次，持续为真不重复报。
- **只看当前 tick**：求值只读本 tick 的样本，不重扫历史。

## 不变量

- 触发一定发生在连续为真满 `for` 之后。
- 条件转假之后不会在等待期未满时触发。
- `scanned` 不随 tick 数平方级放大：八百个 tick 的 `scanned` 不超过 6000。

## 输出契约

`observe(samples, ts)` 返回本 tick 新触发的告警（每条含规则名与分组标签）。场景打印一行 JSON。
`--sample=work` 打印 `{"ticks": N, "scanned": N}`。
