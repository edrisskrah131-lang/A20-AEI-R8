# 轻量阅读与重新实验

阅读包的两份 R9 PDF、报告、交接说明、`RESULT_FACTS.json` 和 `tables/` 足以继续审稿与写作，无需下载多 GB 数组。英文稿的 editable 来源在 `paper/`，主稿用 pdflatex/bibtex，中文报告用 XeLaTeX。

## 恢复档案

新原始数据索引给出恢复前缀，例如 `research_r9/data/A/calibration`。同阶段的 raw ZIP 和 tables ZIP 都是独立完整 ZIP，不需要二进制拼接。核对每归档 SHA256，在相同前缀解压，再核对每个成员的哈希。卡/计划证据包恢复至 `research_r9/data/evidence`。

R8 核心依赖 ZIP 解压为 `A20_release/`；R8 在 `output/A20_AEI_R8`，A19 在 `work/a19/RAS_A19`。环境变量 `A20_R8_ROOT` 可指向 R8 根，但保留上述相对关系。历史沙盒绝对路径不是接手条件。

## 完成的运行与可重建输出

本轮 Windows/Python 3.14.3、归档 Windows BVH DLL、原 R8 预测器环境详见审计。F0 哈希覆盖数值/事件源码及依赖，不能编辑后宣称旧证书仍有效。确认前依赖/公平比较修正保留了历史版本。

原顺序为：F0/试点 → A/B 校准 → `analysis/fair_selection.py` 公开修正和 F1 → `receipt_preflight.py` 观察器冻结 → `confirmation_guard.py` 收集确认/压力 → `stream_requests.py`。**封存后不要再次执行写入 F1 历史的修正器覆盖本轮档案。**

数据齐全可用 `reporting/audit.py` 复查原始哈希和独立二项反演，`analyze.py` 重建图表，`write_si_tables.py` 重建补充表。`benchmark.py` 与 `replay.py` 是已执行的计时/重放诊断；后续验证使用新的目录，保留原计时和审计。

## 网页端边界

Work 可读取保存结果、分析 CSV、编辑论文，不依赖本机空间。新 Linux/native 环境未在本轮全量验证；库、编译器、浮点平台或物理设备改变时，不能仅凭源码匹配继承 Windows 事件证书。新实验放新研究目录/分支，试点后冻结实际生产者、事件和预算，以新的不相交校准/确认种子执行。

证据复用须满足数据依赖、总体与包含条件。截止时间影响曝光或调度时，不只是消费者文字放宽。所有方法继续共享旧卡、数据、缓存、知识、风险和预算；完整程序式/直接续证结果持平或更优时仍保留。不要根据确认结果调阈值。
