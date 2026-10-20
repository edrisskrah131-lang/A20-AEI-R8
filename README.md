# A20–AEI 最新论文与完整研究资料

最新完整版本已于 **2026-10-20 同步到主分支 `main`**。打开这个仓库即可查看，无需切换分支。

论文：*Executable Evidence Management for CAD-Guided Aircraft Inspection*。

## 查看与下载

- **[正文 PDF（19 页）](manuscript/A20_AEI_Manuscript.pdf)**：8 幅图、31 篇参考文献，其中 11 篇 AEI。
- **[补充材料（55 页）](manuscript/Supplement.pdf)**。
- **[完整下载索引：源码、四个数据分卷与 SHA-256 校验值](AEI_DOWNLOADS.md)**。

在 PDF 页面可使用右上角下载按钮。仅阅读论文时，下载正文和补充材料即可。

## 完整源码与数据

如需复现，下载 `A20_AEI_Complete_Source.zip` 和 `A20_AEI_Data_001.zip` 至 `A20_AEI_Data_004.zip`，将五个 ZIP 放在同一目录。解压源码包后，在其中的 `manuscript` 目录运行：

```sh
python reporting/restore_data.py --archive-dir ..
A20_PYTHON=python bash reproduce_artifacts.sh
```

依赖安装及运行方式见源码包内 README。完整交付包含 1,786 个源码和数据文件；归档恢复、实验重算、图表生成、引用及 PDF 排版检查已通过。

## 版本说明

本次同步采用论文交付提交 `3979e9b` 的正文、补充材料、源码及数据，文件内容和校验值保持一致。原交付分支 `aei-complete-20261014` 保留。

根目录中名称带 `R8` 的论文、报告、旧来源清单和历史文件属于早期归档。当前版本请使用上面的 `manuscript/` 链接与 `AEI_DOWNLOADS.md`。
