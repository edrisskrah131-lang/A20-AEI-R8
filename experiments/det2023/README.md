# Aircraft_Fuselage_DET2023 接入

已选定这个数据集作为真实图像缺陷检测案例的来源。本目录当前提供来源核实、COCO 数据审计、分组划分和分组风险计算工具；尚未取得原始数据，也未产生该数据集的训练或实验结果。

## 已核实的官方信息

- [IEEE DataPort 官方数据页](https://doi.org/10.21227/3ref-ex71)，2023 年发布，作者来自中国民航大学。
- 官方 README 明确列出 **389 张有标注图像 + 5,212 张未标注图像 = 5,601 张**，分辨率 1120 × 960。
- COCO、VOC、YOLO 三个目录是同一批 389 张图像的不同标注表示。统计和划分只使用 COCO 一份。
- 官方 ZIP 名称 `Aircraft_Fuselage_DET2023.zip`，页面标示 216.66 MB。
- DataCite 元数据登记 CC BY 4.0；2026-10-20 访问官方下载页时显示需登录并提示订阅要求。许可与文件访问条件分别记录在 [source_metadata.json](source_metadata.json)。
- 官方页面要求配套引用 *A Semi-Supervised Aircraft Fuselage Defect Detection Network with Dynamic Attention and Class-aware Adaptive Pseudo-Label Assignment*，见 [IEEE 文献页](https://ieeexplore.ieee.org/document/10457003)。

四类缺陷的原始类别名、类别数量、飞机/区域/拍摄批次和重复情况，均须读取真实标注后确定。未标注图像不作为无缺陷负样本，也不作为具有真值的测试数据。

## 拿到数据后的入口

将官方 ZIP 下载并解压到仓库外，或本目录被 Git 忽略的 `data/` 中。按实际目录填写下面的标注文件和图像根目录。

```sh
python -m pip install -r requirements.txt
python intake.py audit \
  --annotations /path/to/COCO/annotations.json \
  --images-root /path/to/COCO/images \
  --output outputs/intake
```

多份 COCO 标注可在 `--annotations` 后依次传入。不同文件的 image ID 使用标注文件哈希区分；重复传入同一份标注会报错。图像文件缺失、尺寸不符、无效边框、未知类别及尚无评分规则的 crowd/ignore 标注也会报错，避免静默删除数据。

输出包括：

- `audit.json`：图像/标注哈希、真实类别、每图目标、元数据中已有的分组线索。
- `duplicate_candidates.json`：完全相同像素及 dHash 距离不超过 4 的相似图像候选。
- `groups_template.csv`：逐图填写 `group_id` 与 `group_basis`，说明同一架飞机、物理区域或连续拍摄批次的归组依据。

分组须有采集来源依据；仅把每张图命名为一个“组”不能建立独立性。视觉查重也无法证明飞机或场景独立。工具会合并相似图像连接的组，保证这些候选不会跨越数据划分，相关假设仍需根据采集信息审阅。

```sh
python intake.py split \
  --audit outputs/intake/audit.json \
  --groups outputs/intake/groups_reviewed.csv \
  --output outputs/intake/split.json
```

固定种子为 20261020。完整组按约 55%/15%/15%/15% 分配给 train、development、calibration、test；小样本比例受整数取整影响。输出逐类阳性组数，不按测试表现重分数据。划分前重新核对图像与标注哈希。模型训练仅用 train，模型及阈值选择仅用 development，calibration 和 test 分开保留。5,212 张未标注图像暂不加入训练；若以后做半监督训练，也须先排除与保留组重叠的采集来源。

## 统计口径

检测性能应报告实际标注框上的召回率、精确率及适当的 AP 指标。当前 `risk.py` 提供的是**另一项明确的组事件**：对于含某类缺陷的采集组，全部图像汇总后的召回率是否低于预先指定阈值。CP 的样本量是阳性采集组数，不是图像中标注框的数量。

组事件风险上界不能直接改称“项目检出率”，也不控制误报率。项目指标映射、误报约束、类别映射及最终事件族，需要根据真实标注和明确的任务定义确定。母项目合同及个人、账户信息不放入本目录或公开仓库。

`fixed_family_cards` 要求预先给定事件族、完整的校准单元清单及每幅图的显式结果。推理失败也须留行并计入未检出；工具拒绝遗漏图像、篡改目标计数和混入测试结果。零阳性组的上界为 1，不签发无样本支持的结论。事件族大小包含所有预定事件，不以实验成功与否删减。

例如，95% 家族置信度、四个事件、组失败率上限 10% 时，即使零失败，每个事件也需要至少 42 个独立阳性组；16 个事件则至少需要 55 个。389 张标注图像是否足够，取决于真实分组与类别分布。

## 当前验证与待接入项

```sh
python -m unittest -v test_intake.py
```

13 项检查使用明确的程序生成测试夹具，覆盖图像/标注一致性、分组泄漏、失败记录完整性、CP 边界和测试集隔离；这些检查不是 DET2023 实验结果。

当前云环境没有可用 GPU。数据审计与风险计算可在 CPU 上完成。取得数据和分组依据后，再固定检测模型、训练方案和事件族，接入预测文件、实际模型版本及既有 binding/repair 实现。当前论文 PDF 和七个既有交付文件保持不变。
