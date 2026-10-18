# AEI 当前完整交付 · 2026-10-18 连续变更与结构化图像实验

正文：19 页、8 幅图、31 篇参考文献（其中 11 篇 AEI）。补充材料：55 页。标题为 *Executable Evidence Management for CAD-Guided Aircraft Inspection*。

- [正文 PDF（19 页）](https://github.com/edrisskrah131-lang/A20-AEI-R8/raw/aei-complete-20261014/manuscript/A20_AEI_Manuscript.pdf)
- [补充材料（55 页）](https://github.com/edrisskrah131-lang/A20-AEI-R8/raw/aei-complete-20261014/manuscript/Supplement.pdf)

## 本轮完成

- 将正文组织为同一巡检输出经历要求变化、组件更新、旧输出误到、修复与数值回滚的连续案例；实际执行 256 个校准场景和 64 条独立测试轨迹，每条 16 步。
- 完整 64 事件族中，各完整方法支持相同的 54 个配置。证据复用将记录评估从 13,824 降至 8,960（35.19%）；单独的轨迹请求目录从 2,048 降至 1,536（25%）。目录只构建一次，未按场景重复计费。
- 四种完整实现分别恢复全部 128 个有效修复节点。数值计算、证据准备和绑定恢复分别归因；共享依赖缓存的 59.31% 工作流 CPU 缩减未归为复用方法独有收益。
- 新增四类蒙皮结构，每类独立采样场景并施加四种成像工况，共 256 张实际 Cycles 测试图像；两个固定图像处理器产生 512 个评价结果。正文展示原始输入、实际匹配和失败案例。
- 方法选择只使用 8 个开发场景；后两类结构不参与选择。全量成功、失败、遮挡及未相交结果均保留，配对区间以独立场景为重采样单位。
- 核查正文、补充材料、图源、引用和复现入口；保留 419 份此前研究文件的原始字节。声明、图片授权和实现范围统一置于补充材料末尾。

## 源码与全部数据

源码与原始数据采用独立 ZIP 分卷，每个文件小于 90 MiB。重新计算时，请下载源码包与下列全部数据卷，放在同一目录。

- [A20_AEI_Complete_Source.zip（22.52 MiB）](https://github.com/edrisskrah131-lang/A20-AEI-R8/raw/aei-complete-20261014/A20_AEI_Complete_Source.zip)
- [A20_AEI_Data_001.zip（56.32 MiB）](https://github.com/edrisskrah131-lang/A20-AEI-R8/raw/aei-complete-20261014/A20_AEI_Data_001.zip)
- [A20_AEI_Data_002.zip（81.58 MiB）](https://github.com/edrisskrah131-lang/A20-AEI-R8/raw/aei-complete-20261014/A20_AEI_Data_002.zip)
- [A20_AEI_Data_003.zip（83.78 MiB）](https://github.com/edrisskrah131-lang/A20-AEI-R8/raw/aei-complete-20261014/A20_AEI_Data_003.zip)
- [A20_AEI_Data_004.zip（54.43 MiB）](https://github.com/edrisskrah131-lang/A20-AEI-R8/raw/aei-complete-20261014/A20_AEI_Data_004.zip)

解压源码包后，在 `manuscript` 目录运行：

```sh
python reporting/restore_data.py --archive-dir ..
A20_PYTHON=python bash reproduce_artifacts.sh
```

依赖安装见源码内 README。复现入口使用临时副本，验证后复制论文生成物，保留归档实验与计时。源码及数据卷共含 1,786 个有效载荷文件，逐文件 SHA-256 清单与恢复工具均已打包。第三方论文全文不再分发；文献元数据和引用依据保留。

## 文件完整性

| 文件 | SHA-256 |
|---|---|
| `manuscript/A20_AEI_Manuscript.pdf` | `602ff95fe2616092a0ebb490f7334f047f0d8f77a14ab2ddadf87e154957e3ac` |
| `manuscript/Supplement.pdf` | `70193c2f9bacd6931359641e57b64333ddf2a4ae89c9bb779ce81b5e7b8a1626` |
| `A20_AEI_Complete_Source.zip` | `4faa7d400e24642a55fe5947138c91c00b60179531bd144663f27dfd210eb3f1` |
| `A20_AEI_Data_001.zip` | `a878c889111041e53c4ae56f121220f5c5ba4fccc1ee36341acb9a19340f2c22` |
| `A20_AEI_Data_002.zip` | `e3082ed8d1fdef6fff1ca774aa49228435ab73a783a25e4efa22d04c39c3e0ee` |
| `A20_AEI_Data_003.zip` | `b53dd42faad850c9950b4956cfff49968adf5876486fb48c52efea05fff75bde` |
| `A20_AEI_Data_004.zip` | `cb984e40cf1c0d108aa13b36c16d867efefcdeaadd8f0a8429af80d0c2f0ea09` |

仓库主分支未修改。交付分支为 `aei-complete-20261014`；以上公开链接无需切换账号或登录。
