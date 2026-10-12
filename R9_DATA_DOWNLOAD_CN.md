# R9 数据完整下载索引

**六个正式阶段全部已上传并核验**：12,800个独立输入，38,400个原始数组/元数据文件；176个规范发布文件（ZIP、逐成员清单和阶段索引）。压缩数据共8,084,697,189字节。逐包状态、大小和SHA256见 `R9_DATA_CATALOG.json` 与 `research_r9/audits/GITHUB_FINAL_RAW.json`。

论文状态：17页压缩稿已被用户否定。当前恢复稿45页、补充53页，恢复了原R8主线，仍待编辑与独立审查。数据完整备份不代表论文已获认可或达到9分。

## 原始数据

- **A_calibration_complete**：4,096个独立输入；[下载阶段索引](https://github.com/edrisskrah131-lang/A20-AEI-R8/releases/download/r9-checkpoints-20261012/A20_R9_A_calibration_complete_20261012T112234Z_INDEX.json)。解压相对根：`research_r9/data/A/calibration`。
- **A_confirmation_complete**：2,048个独立输入；[下载阶段索引](https://github.com/edrisskrah131-lang/A20-AEI-R8/releases/download/r9-checkpoints-20261012/A20_R9_A_confirmation_complete_20261012T125135Z_INDEX.json)。解压相对根：`research_r9/data/A/confirmation`。
- **A_stress_complete**：256个独立输入；[下载阶段索引](https://github.com/edrisskrah131-lang/A20-AEI-R8/releases/download/r9-checkpoints-20261012/A20_R9_A_stress_complete_20261012T125208Z_INDEX.json)。解压相对根：`research_r9/data/A/stress`。
- **B_stress_complete**：256个独立输入；[下载阶段索引](https://github.com/edrisskrah131-lang/A20-AEI-R8/releases/download/r9-checkpoints-20261012/A20_R9_B_stress_complete_20261012T125249Z_INDEX.json)。解压相对根：`research_r9/data/B/stress`。
- **B_calibration_complete**：4,096个独立输入；[下载阶段索引](https://github.com/edrisskrah131-lang/A20-AEI-R8/releases/download/r9-checkpoints-20261012/A20_R9_B_calibration_complete_20261012T115213Z_SMALL_INDEX.json)。解压相对根：`research_r9/data/B/calibration`。
- **B_confirmation_complete**：2,048个独立输入；[下载阶段索引](https://github.com/edrisskrah131-lang/A20-AEI-R8/releases/download/r9-checkpoints-20261012/A20_R9_B_confirmation_complete_20261012T125211Z_SMALL_INDEX.json)。解压相对根：`research_r9/data/B/confirmation`。

只需要评审/写作时读取小交接包。需要复现时，下载相应索引列出的ZIP；同阶段各包直接解压到其restore_prefix，文件不重叠。B校准、B确认必须使用上述SMALL_INDEX，勿同时解压旧替代大包。逐成员哈希位于ZIP同名JSON清单。所有试点、冻结版本与中间方案保留在检查点发布，R8及A19/A20历史数据保留在历史发布。两批研究使用各自的种子、事件及置信族，不混算样本。

- [R9检查点发布](https://github.com/edrisskrah131-lang/A20-AEI-R8/releases/tag/r9-checkpoints-20261012)
- [R8及更早完整历史发布](https://github.com/edrisskrah131-lang/A20-AEI-R8/releases/tag/r8-handoff-2026-10-12)
- [当前R9分支](https://github.com/edrisskrah131-lang/A20-AEI-R8/tree/r9-rebuild-20261012)
