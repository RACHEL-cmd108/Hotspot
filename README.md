# Hotspot Monitor

Hotspot Monitor（热点内容运营系统）帮助运营人员把外部信号转化为可追溯的 Event 上下文、账号专属内容候选、人工发布回填与复盘记录。

当前仓库包含：Product Brief v1.5、拆分式 PRD v2.10、UX/UI 设计草案、架构参考资料、Phase 0 内容生成 MVP、测试、样例和文档生成工具。项目仍处于产品定义、设计与验证阶段，不代表生产系统已经完成。

## 文档门禁

项目文档遵循根目录 [`GUIDE.md`](GUIDE.md)。当前状态：

| 阶段 | 状态 | 权威入口 |
|---|---|---|
| Product Brief | 草稿 v1.5 | [`docs/product-requirements/product-brief.md`](docs/product-requirements/product-brief.md) |
| PRD | 草稿 v2.10-module-v3-v12 | [`docs/product-requirements/prd/prd-00-index.md`](docs/product-requirements/prd/prd-00-index.md) |
| UX/UI | 草稿 v2.0-module-v3-v13 | [`docs/ux-ui/ux-00-index.md`](docs/ux-ui/ux-00-index.md) |
| Architecture | 草稿 v0.2 | [`docs/architecture/arch-00-index.md`](docs/architecture/arch-00-index.md) |
| Epics & Stories | 尚未建立 | — |
| Implementation Readiness | 尚未执行 | — |

未完成上游验收前，不应将本仓库视为已具备完整开发就绪条件。

## 仓库结构

```text
.
├── GUIDE.md                         # 软件开发文档规范与阶段门禁
├── 新手开发环境准备指南.md          # GUIDE 引用的环境准备说明
├── docs/
│   ├── README.md                    # 文档总入口
│   ├── product-requirements/
│   │   ├── README.md
│   │   ├── product-brief.md         # 当前 Product Brief v1.5
│   │   └── prd/                     # 当前 PRD v2.10，prd-00 至 prd-09
│   ├── ux-ui/                       # 当前 UX/UI 设计文档集
│   ├── architecture/                # 架构入口、现状参考和图示
│   └── research/                    # 研究与可行性实验记录
├── src/content_mvp/                 # Phase 0 内容生成 MVP
├── tests/                           # 单元测试
├── examples/                        # 示例行动包与账号画像
├── scripts/document-build/          # 文档和图示生成脚本
├── config/fonts.conf                # 文档渲染字体配置
├── _bmad/                           # BMad 工作流、模板与配置
├── _bmad-output/                    # BMad 本地输出说明（生成内容不作为权威文档）
└── requirements.txt                 # Python 依赖
```

`workspace/`、`.agents/`、虚拟环境、外部依赖仓库、运行数据库和渲染产物仅用于本机工作，已从版本控制中排除。

各文档阶段目录中的 `archive/` 仅保存本地历史版本，同样不会同步远端。主文件树只保留当前版本；当用户明确确认新版本为最终版时，旧版本移入对应 `archive/`，新版本接替标准路径。

## 环境要求

- Python 3.10 或更高版本
- macOS（现有文档生成脚本使用系统字体）

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

复制环境变量模板，并填写本机密钥：

```bash
cp .env.example .env
```

不要提交 `.env`、API 密钥、数据库或运行输出。

## 运行内容生成 MVP

从仓库根目录执行：

```bash
PYTHONPATH=src .venv/bin/python -m content_mvp.cli \
  --action examples/action_package.json \
  --account examples/account_profile.json \
  --output workspace/output/content_mvp/demo.json
```

热点承接示例：

```bash
PYTHONPATH=src .venv/bin/python -m content_mvp.cli \
  --action examples/trend_capture_action.json \
  --account examples/watcher_guru_profile.json \
  --output workspace/output/content_mvp/trend-capture-demo.json
```

接入 OpenAI-compatible 模型时，通过环境变量提供配置：

```bash
export CONTENT_LLM_BASE_URL="https://your-provider.example/v1"
export CONTENT_LLM_API_KEY="..."
export CONTENT_LLM_MODEL="your-model"

PYTHONPATH=src .venv/bin/python -m content_mvp.cli \
  --provider llm \
  --action examples/action_package.json \
  --account examples/account_profile.json
```

## TrendRadar 本地适配

TrendRadar 是外部依赖，不作为本仓库源码提交。将其克隆到 `workspace/TrendRadar/` 后运行：

```bash
PYTHONPATH=src .venv/bin/python -m content_mvp.trendradar_cli \
  --trendradar-root workspace/TrendRadar \
  --account examples/watcher_guru_profile.json \
  --scan-limit 100 \
  --draft-limit 10 \
  --output workspace/output/content_mvp/trendradar-drafts.json
```

## 文档生成

构建脚本的二进制输出写入被 Git 忽略的 `workspace/generated-docs/`；架构图资产更新到规范文档目录。

```bash
.venv/bin/python scripts/document-build/build_hotspot_plan.py
.venv/bin/python scripts/document-build/build_hotspot_prd.py
```

## 测试

```bash
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v
```

## 当前限制

- PRD 仍为草稿，开放问题和进入 UX/UI 的门禁尚未全部关闭。
- UX/UI、标准架构文档集、Epic/Story 和实施就绪报告尚未完成。
- 内容 MVP 默认不执行自动发布，事实核验、品牌风险和最终发布决定必须由人工负责。
- TrendRadar 与第三方 API 是外部依赖，生产部署、容量和可扩展性方案仍待架构阶段确认。
