# Hotspot Monitor 文档入口

本目录按 [`GUIDE.md`](../GUIDE.md) 的阶段门禁组织。Markdown 文件是权威来源；Word、PDF、渲染图片和 BMad 原始输出不作为需求基线。

每个阶段的主目录只保留当前版本。旧稿与旧图移入该阶段的本地 `archive/`；所有 `archive/` 均由 Git 忽略，不同步远端。

## 产品定义

- [Product Brief](product-requirements/product-brief.md)：草稿，版本 v1.5。
- [PRD 总入口](product-requirements/prd/prd-00-index.md)：草稿，版本 v2.10-module-v3-v12。
- [业务可扩展性需求](product-requirements/business-extensibility-requirements.md)：扩展性总清单、优先级、设计图与验收方向。
- [产品需求目录说明](product-requirements/README.md)。

## 产品设计

- [UX/UI 总入口](ux-ui/ux-00-index.md)：当前远端设计基线为 v2.0-module-v3-v13 草稿。

## 方案设计

- [Architecture 入口](architecture/arch-00-index.md)：当前技术架构草案 v0.2，已对齐 PRD 与 UX/UI 主链。
- `architecture/assets/`：现有系统设计图示。
- `architecture/references/`：历史系统方案的唯一保留参考版本。

## 研究与验证

- `research/experiments/`：Phase 0 可行性实验。
- `research/benchmark-account-distillation/`：账号运营研究。

## 尚未建立

当前尚未形成 `development/` 文档集。PRD、UX/UI 与架构完成门禁检查后，再严格按 GUIDE 建立 Epic、Story、实施就绪和 Sprint 状态文件。
