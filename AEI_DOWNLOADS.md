# AEI 当前完整交付 · 2026-10-18 综合修订

正文：14页、8幅图。补充材料：46页。当前标题为 *Executable Evidence Management for CAD-Guided Aircraft Inspection*。

- [正文 PDF（14页）](https://github.com/edrisskrah131-lang/A20-AEI-R8/raw/aei-complete-20261014/manuscript/A20_AEI_Manuscript.pdf)
- [补充材料（46页）](https://github.com/edrisskrah131-lang/A20-AEI-R8/raw/aei-complete-20261014/manuscript/Supplement.pdf)
- [完整编辑源码与原始实验图像（89.10 MiB）](https://github.com/edrisskrah131-lang/A20-AEI-R8/raw/aei-complete-20261014/A20_AEI_Complete_Source.zip)

## 本轮完成内容

- 用完整数值案例串起要求变化、证据更新、错误绑定和验证恢复；具体服务阈值进入正文。
- 重新表述校准后选定服务的风险保证，补充独立测试族核验：41项准入服务的同时测试风险上界均不超过0.074568224。
- 将不可逆历史锁改为绑定隔离与验证修复。新模型、权威快照和事件日志实现一致，恢复1536个不同的源/请求组合；保留错配来源检查和审计历史。
- 新增24个独立几何场景、72张Blender Cycles实际渲染图，继续使用原检测器和位姿估计器。全部成功与失败结果都保留，新增渲染总体与原校准总体分开。
- 完成13组恢复机制检查、72图像重新处理、6图像从头重渲染，以及两份PDF和6幅新图的独立重建。

## 文件完整性

**正文 PDF（14页）**
`b4c78fe3a8afcad52d676be605ddd92b6cd1983dcfe64438e88e1ab77112a61f`

**补充材料（46页）**
`f48ec2eb0e803015bc01d28764bb1ef5ddb0d1d03970a40bd242d4848e59bd5a`

**完整编辑源码与原始实验图像（89.10 MiB）**
`08a617d1001945adbbc0f6eccba0f87159312907758e6fa94f738ad1db9b6845`

源码ZIP含611个有效载荷文件及逐文件SHA-256清单。所有原始实验图像、数据、几何与渲染脚本保留。成稿PDF单独下载；源码包省略重复编译PDF和可重生成的展示PNG/SVG，保留出版PDF图件及编辑脚本。

仓库主分支未修改；当前交付分支为 `aei-complete-20261014`。无需切换账号或登录即可使用上述公开下载链接。
