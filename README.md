# A20–AEI 最新论文与完整研究资料

最新版本在主分支 **main**，已加入免费真实缺陷图像的实际训练、检测和校准结果。

论文：*Executable Evidence Management for Aircraft Inspection*。

- **[正文 PDF（18 页）](manuscript/A20_AEI_Manuscript.pdf)**：7 幅图，34 篇参考文献，其中 11 篇 AEI。
- **[补充材料（59 页）](manuscript/Supplement.pdf)**。
- **[源码、全部数据卷和下载校验值](AEI_DOWNLOADS.md)**。
- [免费真实数据的来源、分组和执行结果](experiments/real_image_data/README.md)。

两个案例共用同一证据接口：CAD 关联检验空间质量，真实图像案例检验缺陷召回与误报。真实数据保留 1,339 张代表图像、222 个推断来源组，实际执行四个检测生产者的 3,524 个图像输出。当前组失败容许值下通过 0/16 个请求，实际结果和全部失败均已写入正文。报告完整性修复与质量准入分别验证。

阅读只需下载两份 PDF。复现时请下载完整源码 ZIP 与索引列出的每个数据卷；源码内 README 说明两个 Python 环境、离线恢复和完整复现命令。归档恢复、独立重推理、统计、图源、引用和排版检查均已通过。

原 CAD 研究和 1,559 份此前研究文件保留。根目录名称带 R8 的旧文件是早期归档；当前请使用以上 `manuscript/` 链接。原 DET2023 准备工具仍在 [experiments/det2023](experiments/det2023/README.md)。
