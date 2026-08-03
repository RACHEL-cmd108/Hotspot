# 热点监控（Hotspot Monitor）

这个仓库保存 Predx 热点运营系统建设方案的生成脚本、正式配图和最终 Word 文档。

当前脚本的主要作用是：

- 生成热点运营系统的三张架构图；
- 将方案正文、表格和配图排版为 Word 文档；
- 输出《Predx 热点运营系统建设方案 v2.0》。

## 仓库结构

```text
.
├── build_hotspot_plan.py   # 生成架构图和 Word 文档的主程序
├── fonts.conf              # 本地字体缓存配置
├── requirements.txt        # Python 依赖
└── output/
    ├── assets/             # 方案使用的正式配图
    ├── Predx热点运营系统建设方案_v1.0.docx
    └── Predx热点运营系统建设方案_v2.0.docx
```

临时文件、排版预览图和重复生成的 PDF 已通过 `.gitignore` 排除，不会进入仓库。

## 环境要求

- Python 3.10 或更高版本
- macOS（当前版本使用 macOS 系统字体路径）

## 安装依赖

建议在虚拟环境中安装：

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## 生成文档

```bash
python3 build_hotspot_plan.py
```

程序会生成或更新：

- `output/assets/overall_architecture.png`
- `output/assets/hotspot_source_relationship.png`
- `output/assets/future_event_center.png`
- `output/Predx热点运营系统建设方案_v2.0.docx`

## 当前限制

主程序目前包含作者电脑上的绝对项目路径，并依赖 macOS 的 Arial Unicode 字体。因此，代码当前可在原开发环境运行，但其他人克隆仓库后还不能直接运行。后续需要把项目目录和字体改为可自动识别的相对或跨平台配置。

## 使用说明

这个仓库目前用于方案文档的维护与生成，不是已经上线运行的热点采集或自动发布系统。Word 文档描述的是产品规划、系统架构、MVP 范围和运营流程。
