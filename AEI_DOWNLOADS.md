# AEI 完整交付 · 2026-10-20 真实缺陷图像案例

标题：*Executable Evidence Management for Aircraft Inspection*。
正文 18 页、7 幅图、34 篇参考文献（11 篇 AEI）；补充材料 59 页。

- [正文 PDF](https://github.com/edrisskrah131-lang/A20-AEI-R8/raw/main/manuscript/A20_AEI_Manuscript.pdf)
- [补充材料 PDF](https://github.com/edrisskrah131-lang/A20-AEI-R8/raw/main/manuscript/Supplement.pdf)

本轮使用免费 CC BY 4.0 的 Innovation Hangar v2 实际训练检测器、执行检测、校准并运行报告更新流程。发布版 10,722 张图像包含增强和重复采集；本轮保留 1,339 张代表图像、222 个推断来源组，按整组划分训练/开发/校准/测试。四个生产者共执行 3,524 个图像输出；独立复算预测、评分和 16 个事件的二项上界。

在预先设置的组失败容许值 0.25 下，通过校准的请求为 0/16。结果保留全部漏检和误报，没有为取得正面结果放宽测试标准。报告流程执行 408 步，68 次合法修复提交；完整性修复与质量准入分别判断。正文展示真实输入、标注和实际检测框。

原 CAD 案例的 54/64 支持、35.19% 完整目录证据评估缩减及 128 个有效修复节点保留。全部 1,559 份此前研究文件逐字节不变。旧几何挑战继续保留在补充材料及源数据中。数据出处、许可、实现范围和声明集中在补充材料末尾；统计单位与必要方法条件在正文定义。

## 完整源码和数据

阅读只需两份 PDF。复现时下载以下源码包和全部数据卷（每个 ZIP 小于 90 MiB），放在同一目录：

- [A20_AEI_Complete_Source.zip（44.53 MiB）](https://github.com/edrisskrah131-lang/A20-AEI-R8/raw/main/A20_AEI_Complete_Source.zip)
- [A20_AEI_Data_001.zip（56.32 MiB）](https://github.com/edrisskrah131-lang/A20-AEI-R8/raw/main/A20_AEI_Data_001.zip)
- [A20_AEI_Data_002.zip（81.58 MiB）](https://github.com/edrisskrah131-lang/A20-AEI-R8/raw/main/A20_AEI_Data_002.zip)
- [A20_AEI_Data_003.zip（83.78 MiB）](https://github.com/edrisskrah131-lang/A20-AEI-R8/raw/main/A20_AEI_Data_003.zip)
- [A20_AEI_Data_004.zip（74.81 MiB）](https://github.com/edrisskrah131-lang/A20-AEI-R8/raw/main/A20_AEI_Data_004.zip)
- [A20_AEI_Data_005.zip（35.02 MiB）](https://github.com/edrisskrah131-lang/A20-AEI-R8/raw/main/A20_AEI_Data_005.zip)

解压源码包后进入 `manuscript`，按 README 安装论文和检测器的两个依赖环境，再运行：

```sh
python reporting/restore_data.py --archive-dir ..
A20_PYTHON=/path/to/paper/python A20_DETECTOR_PYTHON=/path/to/detector/python bash reproduce_artifacts.sh
```

交付共 5,883 个有效载荷文件，包含代表图像、原始/转换标注、模型权重、原始预测、评分、协议、代码、图源和历次研究。恢复工具逐文件核对 SHA-256；默认复现使用已归档权重重新推理，不重新选择模型或改动历史实验计时。

## 校验值

| 文件 | SHA-256 |
|---|---|
| `manuscript/A20_AEI_Manuscript.pdf` | `bc6a0b18daf9ed5c9560ff470c7751b971b43fab5ad4e720c0af9d86f0f7eb69` |
| `manuscript/Supplement.pdf` | `0a2f3c7b0dc37e843167e92f741f7825c9090edbedf563b0c0faf0282fc89f68` |
| `A20_AEI_Complete_Source.zip` | `2ed95b4f57f40a77df267bdfecc040bfaa8d469d80cd37e501f7e06274168b8e` |
| `A20_AEI_Data_001.zip` | `a878c889111041e53c4ae56f121220f5c5ba4fccc1ee36341acb9a19340f2c22` |
| `A20_AEI_Data_002.zip` | `e3082ed8d1fdef6fff1ca774aa49228435ab73a783a25e4efa22d04c39c3e0ee` |
| `A20_AEI_Data_003.zip` | `b53dd42faad850c9950b4956cfff49968adf5876486fb48c52efea05fff75bde` |
| `A20_AEI_Data_004.zip` | `4499fea3b0a876d6ca3f7db3a004995de13319d68931e20233af52378d81667f` |
| `A20_AEI_Data_005.zip` | `89daf99dea001e31b0eb6406af258202e9e3cfdb413d16929684af16aa880475` |

当前交付位于 `main`；无需切换分支或账号。
