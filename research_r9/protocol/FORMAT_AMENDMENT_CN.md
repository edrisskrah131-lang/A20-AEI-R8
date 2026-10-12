# 冻结格式修正 v1.1（正式数据生成前）

初版冻结文件及其阶段ZIP保留。下载/提交检查发现Windows路径分隔符和Git文本换行转换会影响跨机器校验，因此在正式校准、确认输入均为0时修正格式：清单键统一为正斜线，带哈希的JSON在Git中保留原始字节。

冻结版本改为 R9-prospective-1.1-format-amendment。未改变输入采样、种子域、样本数、阈值、相机配置、策略、校准规则或置信预算。原冻结文件保存在protocol/history_v1，当前freeze.json与protocol.json经Git对象字节校验后才启动正式数据生成。
