# 每日作业报告

## 1. 本日问题

- 里程碑：day-02
- 学生或小组：LHL
- 使用者：需要初步筛查照片、但必须人工复核的设施维护团队
- 真实输入：Kaggle Concrete Crack Images 中 40,000 张真实混凝土表面照片（Positive/Negative 各 20,000 张）
- 需要的输出：多数类基线与小型 CNN 在同一固定测试子集上的指标对比，以及漏检裂缝的错误图像列表
- 与使用者最相关的错误：漏检裂缝（真实裂缝被预测为无裂缝）——这正是筛查器最不能犯的错误
- 本日产品边界：筛查器只做初筛，输出必须由人工复核，不构成结构安全结论

## 2. 真实数据或真实课程输入

- 所有者/发布者：Kaggle 用户 arunrk7 发布的数据集（源自 SDNET 混凝土表面图像）
- 标题：Surface Crack Detection
- 原始 URL：https://www.kaggle.com/datasets/arunrk7/surface-crack-detection
- 许可标签或使用许可：Kaggle 数据集许可，仅限本课程用途
- 下载/取得日期：2026-08-17
- 预期文件与结构：`data/raw/Positive`（20,000 张有裂缝）、`data/raw/Negative`（20,000 张无裂缝）
- 检查命令：`python train.py --check-data`
- 实际检查结果：`REAL DATA CHECK PASSED`；class_root: data\raw；counts: {'Negative': 20000, 'Positive': 20000}
- 已知缺失、偏差或限制：图像来自固定拍摄环境，同一类内存在相似图像块，指标不能外推到其他拍摄条件

## 3. 可复现运行

```powershell
# 当前目录
ai-camp-2026-deploy\day-02-vision

# 安装
python -m pip install -r requirements.txt

# 数据检查
python train.py --check-data

# 基线
python train.py --model baseline

# 候选（CNN）
python train.py --model cnn --epochs 2

# 测试
python -m unittest discover -s tests -v
```

关键预期输出：数据检查 `REAL DATA CHECK PASSED`（各 20,000 张）；测试 `Ran 3 tests ... OK`；基线写 `runs/baseline.json`，CNN 写 `runs/cnn.json` 和 `runs/cnn-errors.png`。

## 4. 基线与候选

### 简单基线

- 方法：多数类基线，统计训练子集多数类后对所有测试图像给同一预测（本子集为 Positive 裂缝）
- 为什么足够简单：不学习任何像素特征
- 命令：`python train.py --model baseline`
- 结果：accuracy 0.500；crack_precision 0.5；crack_recall 1.0；混淆矩阵 [[0, 150], [0, 150]]——漏检 0 张，但 150 张无裂缝图全部误报为裂缝

### 候选方法

- 学生完成的核心改动：`models.py` 的 `SmallCNN`，两层卷积 + 池化 + 全连接，输出 2 类分数
- 保持不变的条件：同一固定子集划分（每类 600 张、seed 2026、75% 训练 / 25% 测试）、同一评估函数、Adam lr=0.001、2 epochs
- 命令：`python train.py --model cnn --epochs 2`
- 结果：accuracy 0.813；crack_precision 0.892；crack_recall 0.713；混淆矩阵 [[137, 13], [43, 107]]——漏检 43 张真实裂缝

| 项目 | 基线 | 候选 | 含义 |
| --- | ---: | ---: | --- |
| accuracy | 0.500 | 0.813 | 300 张测试图上整体正确率大幅提升 |
| crack_recall | 1.000 | 0.713 | 基线靠"全报裂缝"达到不漏检，代价是 150 张误报 |
| false_negative_cracks | 0 | 43 | CNN 有 43 张漏检裂缝，需人工复核 |

## 5. 一个真实失败案例

- 样本位置/编号：`runs/cnn-errors.png` 错误图像列表（`runs/cnn.json` 的 first_errors 前 12 条）
- 真实结果：该图像属于 Positive（有裂缝）
- 系统输出：SmallCNN 预测 no_crack（无裂缝）——假阴性漏检
- 可以观察到什么：漏检图像多为裂缝细小、对比度低、与背景纹理接近的照片
- 说明的限制：小型 CNN 对低对比度小裂缝的判别能力有限；该模型在固定拍摄环境中训练，不同光线和材料会让漏检更多
- 不能证明什么：不能证明这些图像"实际上没有裂缝"，也不能证明筛查器在任意工地可用
- 下一项最小检查：统计 43 张漏检图像的裂缝面积/对比度特征，看是否集中在某类低可见度图像

## 6. 智能体与学生工作边界

- 智能体提出/生成/修改了什么：智能体实现了 `models.py` 的 `SmallCNN` 网络结构，并生成报告草稿
- 学生怎样核对文件、来源、输出、测试和 diff：运行 `--check-data` 确认图像数量；运行测试确认网络输出形状 (4, 2)；打开 `runs/cnn.json` 对照混淆计数；用 `git diff` 确认只改 `models.py`
- 学生修改或拒绝了什么建议：拒绝增加数据增强或更换预训练模型（超出本日单一改动边界，且会让比较条件变化）；拒绝随机裁剪增强以避免相似图像块泄漏风险
- 每名成员能独立解释的代码或证据：`balanced_split_indices` 的按类平衡划分、`confusion_counts` 的四个计数、CNN 张量从 (N,3,64,64) 到 (N,2) 的形状变化

## 7. 结论与限制

1. CNN 在 300 张固定测试图上 accuracy 0.813，明显高于多数类基线 0.500。2. 基线通过"全部判为裂缝"获得 0 漏检，代价是 150 张误报，因此 1.0 召回不代表"好"。3. CNN 漏检 43 张真实裂缝（crack_recall 0.713），这是维护场景最危险的错误。4. 误报从 150 张降到 13 张，说明 CNN 同时减少了人工复核负担。5. 数据限制：图像来自单一拍摄环境，同类内相似图像块可能导致指标偏乐观。6. 方法限制：2 epochs 的小型网络训练不充分，指标不能代表调参后的最优表现。7. 不能用于真实决策：不能作为结构安全结论，不能替代现场检查与工程师判断。

## 8. 提交复核

- [x] README 从新环境可以开始运行
- [x] 数据检查、测试和主程序重新运行
- [x] 报告数字与保存输出一致
- [x] `presentation.pptx` 在 3 分钟内讲完
- [x] `submission.json` 路径正确
- [x] 无密钥、大数据、私人信息、虚拟环境或缓存
- [ ] GitHub 网页复查并邮件发送 URL（由学生本人完成）
