# D2 混凝土裂缝图像筛查：基线与小型 CNN（student-work 副本）

本仓库是 Day 2 学生工作副本：比较多数类基线与小型 CNN，在真实裂缝照片上筛查"可能有裂缝/未发现裂缝"，重点检查漏检裂缝。

## 数据契约

- 数据所有者/发布者：Kaggle（arunrk7）
- 标题：Surface Crack Detection
- 原始 URL：https://www.kaggle.com/datasets/arunrk7/surface-crack-detection
- 许可：Kaggle 数据集许可，仅限课程用途
- 预期结构：`data/raw/Positive`（20,000 张，有裂缝）与 `data/raw/Negative`（20,000 张，无裂缝）
- 使用边界：筛查结果必须由人工复核，不替代现场检查、工程师判断或安全决策

## 环境与安装

```powershell
python --version
python -m pip install -r requirements.txt
```

## 运行路线（按顺序）

```powershell
# 1. 数据检查（必须先通过，失败就停止）
python train.py --check-data
# 预期：REAL DATA CHECK PASSED
# counts: {'Negative': 20000, 'Positive': 20000}

# 2. 测试
python -m unittest discover -s tests -v
# 预期：Ran 3 tests ... OK

# 3. 基线（多数类，全部判为裂缝）
python train.py --model baseline

# 4. 候选（SmallCNN，固定子集每类 600 张、2 epochs）
python train.py --model cnn --epochs 2
```

## 结果文件

- `runs/baseline.json`：多数类基线指标与 12 个错误样本
- `runs/cnn.json`：CNN 指标、混淆计数、12 个错误样本与训练损失
- `runs/cnn-errors.png`：前 6 个错误样本图像（真标签 vs 预测标签）

## 基线

多数类（训练子集中 600 张 Positive、600 张 Negative，基线预测全部为 Positive 裂缝）：accuracy 0.500，crack_recall 1.0（没有漏检，但 300 张无裂缝图全部误报）。

## 候选

`SmallCNN`：Conv2d(3,8,3,padding=1)→ReLU→MaxPool→Conv2d(8,16,3,padding=1)→ReLU→MaxPool→Flatten→Linear(4096,2)。固定真实子集划分（每类 600、seed 2026）、Adam lr=0.001、CrossEntropyLoss、2 epochs。

## 限制

- 固定子集与相似图像块分割方式决定指标只能代表该子集；
- 不能把筛查器当作结构安全结论，不能替代现场检查；
- 报告和 PPT 中的数字都可以由上述命令重新产生。
