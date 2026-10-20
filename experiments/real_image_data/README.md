# 免费真实图像数据来源（2026-10-20）

本轮已使用 **Innovation Hangar v2** 完成真实图像缺陷检测案例。完整数据已通过公开论文配套仓库下载，过程无需登录或付费。检测训练、开发集选择、四个生产者的实际推理、来源组校准和报告更新流程均已执行，并已写入新版论文。

## 来源与许可

- [原项目与许可](https://universe.roboflow.com/innovation-hangar/innovation-hangar-v2)：CC BY 4.0。
- [v1 数据版本](https://universe.roboflow.com/innovation-hangar/innovation-hangar-v2/dataset/1)：扩增设置及各划分数量。
- [论文配套 GitHub 中的完整数据](https://github.com/cparyoto/Aircraft-Skin-Defect-Detection-YOLOv9-Vs.-RT-DETR/tree/main/datasets_2)。可直接查看图像和标签，无需 IEEE DataPort 订阅。
- [整个公开仓库 ZIP](https://codeload.github.com/cparyoto/Aircraft-Skin-Defect-Detection-YOLOv9-Vs.-RT-DETR/zip/refs/heads/main)：本次下载约 408 MiB，包含两套数据及代码。
- [使用该数据的 Aerospace 2025 论文](https://doi.org/10.3390/aerospace12040356)：*Advances in Aircraft Skin Defect Detection Using Computer Vision: A Survey and Comparison of YOLOv9 and RT-DETR Performance*。

数据集维护者为 Innovation Hangar；上述 GitHub 是论文配套镜像。数据的 CC BY 4.0 在原项目页和镜像 `datasets_2/data.yaml` 中一致，镜像根目录的 GPL-3.0 为其代码许可。

## 实际核验

| 项目 | 数量 |
|---|---:|
| 原项目列出的来源图像 | 4,288 |
| v1 训练图像（含扩增） | 9,651 |
| v1 验证图像 | 642 |
| v1 测试图像 | 429 |
| 下载版本图像合计 | 10,722 |
| 对应标签文件 | 10,722 |
| 标注实例 | 22,030 |

五类为 `crack`、`dent`、`missing-head`、`paint-off`、`scratch`。20,001 个实例使用 YOLO 检测框，2,029 个使用多边形分割；多边形可转换为轴对齐外接框。640×640 图像、标签类别和归一化坐标已读取检查，所有 21,445 个文件与公开 Git tree 的大小和 blob 哈希一致。

文件下载记录、类别数量和原始包 SHA-256 见 [source_metadata.json](source_metadata.json)。原始图像保留在当前云环境 `/workspace/a20-data/innovation_hangar_v2/`，原 ZIP 在 `/workspace/a20-data/aircraft-skin-defect-author-repository.zip`。

## 接入实验的依据

五类缺陷与航空表面检验任务相关，可用于需求改变、模型/数字图像处理版本改变，以及输出版本绑定的案例。曝光或增益变换应描述为对既有实拍图像的数字变换。

原始版本每个训练来源生成三个输出，不能把 10,722 张当成独立采集样本。来源文件名前缀中有 36 个跨越原有划分的候选，需结合图像与采集来源审查并重分组；仅有相同文件名前缀不能证明重复，名字不同也不能证明独立。本轮按文件来源族、完整拍摄日和视觉相似性重分组，保留 1,339 张代表图像、222 个推断来源组。飞机身份仍未提供，不能把这些组称为已确认独立的飞机。校准与统计单位见下面的实际执行结果。

同一仓库还含 983 张 SUTD Aircraft AI Dataset 图像（缺失铆钉、锈蚀、划痕），也已下载。其当前公开项目列出 CC BY 4.0，但历史导出 YAML 的许可字段写有 Private，相关差异已在元数据中保留；本轮优先选取许可记录一致的 Innovation Hangar v2。

AGDD 航空玻璃数据可从 GitHub 免费获取，但许可包含非商业和相同方式共享要求；AIRSD 的论文公开云盘链接本次返回 404；另一套 Drones 2025 数据的 Zenodo 下载本次受网络访问限制。它们未列为当前首选。

## 实际执行结果

- 按整组划分：训练 122 组/458 图，开发 33 组/34 图，校准 33 组/368 图，测试 34 组/479 图。所选原图、原始标注和转换框均已归档。
- 实际训练 COCO 预训练 YOLO11n；模型和置信阈值只使用训练/开发数据选择。早期/更新模型及数字增益 0.5/1.5 共四个生产者，实际生成 3,524 个图像输出。
- 固定 16 个来源组事件，容许失败概率 0.25，通过 0/16 项；全部漏检、误报和拒绝结果保留。帧数和标注框数不替代来源组样本数。
- 34 个测试组执行 408 个报告操作，68 次合法修复提交，错误绑定签发 0 次。修复完整性和质量准入分别统计。
- 缺铆钉头、掉漆、划痕各只有一个校准和一个测试来源组，逐类结果作为描述性指标，未扩写为项目逐类检出率保证。

[新版正文](../../manuscript/A20_AEI_Manuscript.pdf)、[补充材料](../../manuscript/Supplement.pdf)及[源码和完整数据下载](../../AEI_DOWNLOADS.md)。模型权重、逐图预测、全部评分和复现脚本位于源码/数据 ZIP 的 `manuscript/studies/real_defects_20261020/`。无需访问付费数据平台即可离线复现。
