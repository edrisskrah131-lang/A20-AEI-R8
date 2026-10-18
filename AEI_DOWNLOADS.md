# AEI 当前完整交付 · 2026-10-18 文献与贡献论证修订

正文：16页、8幅图、31篇参考文献（其中11篇AEI）。补充材料：46页。标题为 *Executable Evidence Management for CAD-Guided Aircraft Inspection*。

- [正文 PDF（16页）](https://github.com/edrisskrah131-lang/A20-AEI-R8/raw/aei-complete-20261014/manuscript/A20_AEI_Manuscript.pdf)
- [补充材料（46页）](https://github.com/edrisskrah131-lang/A20-AEI-R8/raw/aei-complete-20261014/manuscript/Supplement.pdf)
- [完整编辑源码与原始实验图像（89.13 MiB）](https://github.com/edrisskrah131-lang/A20-AEI-R8/raw/aei-complete-20261014/A20_AEI_Complete_Source.zip)

## 本轮修订

- 重写引言、相关工作和讨论，增加直接近邻比较表；明确承接生命周期知识图谱、动态安全论证、工作流溯源与选择性重算。
- 正文实际引用从18篇调整为31篇，覆盖引言、相关工作、方法、统计机制、实验与讨论；均为正文实际使用的来源。
- 移除已不适用的ICP与协方差引文，改用实际透视投影、矩形赋值、Huber损失及SciPy实现来源。
- 区分Learn then Test的高概率保证与Conformal Risk Control的期望损失保证；核对最新AEI近邻及用户提供的传感器校准论文。
- 逐条核验作者、题名、正式卷期与DOI/官方来源，修复专有名大小写及作者缩写。独立重建两份PDF，文本一致；6幅图重新生成一致。
- 419份原实验与数据文件保持逐字节一致。

## 文件完整性

正文 PDF：`73e041ac1aca11d139cbd97779bd02d4a8c699e7e7a0497b4862c676e8b07eda`

补充材料：`52a0c402eda64ab56d7ffd415f951c214984e6c09f6d3d9828cac1e501d47602`

源码ZIP：`1fe388a118c9ac457715ab7c78dcbe72a1b56d9aa563a9a6272b7894209284f8`

源码ZIP含616个有效载荷文件及逐文件SHA-256清单，CRC和全部文件哈希核验通过。所有原始实验图像、数据、几何与渲染脚本保留。文献元数据与阅读范围保存在机器可读的citation_evidence.json；第三方论文全文不打包。成稿PDF单独下载；源码包保留出版PDF图件及编辑脚本，省略重复编译PDF和可重生成的展示PNG/SVG。

仓库主分支未修改；当前交付分支为 `aei-complete-20261014`。上述公开链接无需切换账号或登录。
