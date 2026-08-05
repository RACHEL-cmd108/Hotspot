from pathlib import Path
from math import atan2, cos, sin, pi
from PIL import Image, ImageDraw, ImageFont
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "docs" / "prd" / "releases"
ASSET = ROOT / "docs" / "prd" / "assets"
DOCX = OUT / "Predx热点运营产品需求文档_PRD_v1.2_完整修复版.docx"
OUT.mkdir(parents=True, exist_ok=True)
ASSET.mkdir(parents=True, exist_ok=True)

FONT = "Arial Unicode MS"
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
NAVY = "0B2545"
BLUE = "2E74B5"
TEAL = "0F8B8D"
ORANGE = "E07A2D"
GREEN = "3A7D44"
GRAY = "5B6573"
LIGHT = "F2F4F7"
PALE_BLUE = "EAF2F8"
PALE_TEAL = "E9F6F5"
PALE_ORANGE = "FFF3E8"
PALE_GREEN = "EDF6EE"
WHITE = "FFFFFF"
BLACK = "111111"


def rgb(value):
    return RGBColor.from_string(value)


def set_run(run, size=11, bold=False, color=BLACK, italic=False):
    run.font.name = FONT
    rfonts = run._element.get_or_add_rPr().rFonts
    rfonts.set(qn("w:ascii"), FONT)
    rfonts.set(qn("w:hAnsi"), FONT)
    rfonts.set(qn("w:eastAsia"), FONT)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = rgb(color)


def shade(cell, fill):
    tcpr = cell._tc.get_or_add_tcPr()
    node = tcpr.find(qn("w:shd"))
    if node is None:
        node = OxmlElement("w:shd")
        tcpr.append(node)
    node.set(qn("w:fill"), fill)


def cell_margins(cell, top=80, bottom=80, start=120, end=120):
    tcpr = cell._tc.get_or_add_tcPr()
    mar = tcpr.first_child_found_in("w:tcMar")
    if mar is None:
        mar = OxmlElement("w:tcMar")
        tcpr.append(mar)
    for name, value in (("top", top), ("bottom", bottom), ("start", start), ("end", end)):
        item = mar.find(qn(f"w:{name}"))
        if item is None:
            item = OxmlElement(f"w:{name}")
            mar.append(item)
        item.set(qn("w:w"), str(value))
        item.set(qn("w:type"), "dxa")


def table_geometry(table, widths):
    table.autofit = False
    tblpr = table._tbl.tblPr
    tblw = tblpr.find(qn("w:tblW"))
    if tblw is None:
        tblw = OxmlElement("w:tblW")
        tblpr.append(tblw)
    tblw.set(qn("w:w"), str(sum(widths)))
    tblw.set(qn("w:type"), "dxa")
    ind = tblpr.find(qn("w:tblInd"))
    if ind is None:
        ind = OxmlElement("w:tblInd")
        tblpr.append(ind)
    ind.set(qn("w:w"), "120")
    ind.set(qn("w:type"), "dxa")
    grid = table._tbl.tblGrid
    for child in list(grid):
        grid.remove(child)
    for width in widths:
        col = OxmlElement("w:gridCol")
        col.set(qn("w:w"), str(width))
        grid.append(col)
    for row in table.rows:
        trpr = row._tr.get_or_add_trPr()
        cant_split = trpr.find(qn("w:cantSplit"))
        if cant_split is None:
            trpr.append(OxmlElement("w:cantSplit"))
        for i, cell in enumerate(row.cells):
            width = widths[min(i, len(widths) - 1)]
            tcpr = cell._tc.get_or_add_tcPr()
            tcw = tcpr.find(qn("w:tcW"))
            if tcw is None:
                tcw = OxmlElement("w:tcW")
                tcpr.append(tcw)
            tcw.set(qn("w:w"), str(width))
            tcw.set(qn("w:type"), "dxa")
            cell_margins(cell)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER


def add_table(doc, headers, rows, widths, font_size=9.2):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    table.rows[0]._tr.get_or_add_trPr().append(OxmlElement("w:tblHeader"))
    for i, text in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = text
        shade(cell, LIGHT)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.05
        for run in p.runs:
            set_run(run, font_size, True, NAVY)
    for row in rows:
        cells = table.add_row().cells
        for i, value in enumerate(row):
            cells[i].text = str(value)
            p = cells[i].paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.08
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i == 0 else WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                set_run(run, font_size, False, BLACK)
    table_geometry(table, widths)
    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(0)
    spacer.paragraph_format.line_spacing = Pt(2)
    set_run(spacer.add_run("\u200b"), 1, False, WHITE)
    return table


def add_p(doc, text, lead=None, size=11, after=6, color=BLACK, italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.line_spacing = 1.10
    if lead and text.startswith(lead):
        set_run(p.add_run(lead), size, True, color)
        set_run(p.add_run(text[len(lead):]), size, False, color, italic)
    else:
        set_run(p.add_run(text), size, False, color, italic)
    return p


def bullets(doc, items, level=0):
    style = "List Bullet" if level == 0 else "List Bullet 2"
    for item in items:
        p = doc.add_paragraph(style=style)
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.line_spacing = 1.167
        set_run(p.add_run(item), 10.7)


def numbers(doc, items):
    for item in items:
        p = doc.add_paragraph(style="List Number")
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.line_spacing = 1.167
        set_run(p.add_run(item), 10.7)


def callout(doc, label, text, fill=PALE_BLUE, accent=BLUE):
    table = doc.add_table(rows=1, cols=1)
    table.style = "Table Grid"
    table_geometry(table, [9360])
    cell = table.cell(0, 0)
    shade(cell, fill)
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    set_run(p.add_run(label + "  "), 10.8, True, accent)
    set_run(p.add_run(text), 10.8, False, NAVY)
    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(2)


def style_document(doc):
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)
    section.header_distance = Inches(0.492)
    section.footer_distance = Inches(0.492)

    normal = doc.styles["Normal"]
    normal.font.name = FONT
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    normal.font.size = Pt(11)
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.10

    for name, size, color, before, after in (
        ("Heading 1", 16, BLUE, 16, 8),
        ("Heading 2", 13, BLUE, 12, 6),
        ("Heading 3", 12, NAVY, 8, 4),
    ):
        style = doc.styles[name]
        style.font.name = FONT
        style._element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = rgb(color)
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.space_after = Pt(after)
        style.paragraph_format.keep_with_next = True

    for name in ("List Bullet", "List Bullet 2", "List Number"):
        style = doc.styles[name]
        style.font.name = FONT
        style._element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
        style.font.size = Pt(10.7)
        style.paragraph_format.left_indent = Inches(0.5 if name != "List Bullet 2" else 0.75)
        style.paragraph_format.first_line_indent = Inches(-0.25)
        style.paragraph_format.space_after = Pt(8)
        style.paragraph_format.line_spacing = 1.167

    header = section.header.paragraphs[0]
    header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    set_run(header.add_run("PREDX GROWTH SYSTEM  |  PRODUCT REQUIREMENTS"), 8.5, False, GRAY)
    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run(footer.add_run("Predx 内部文档  ·  PRD v1.2  ·  完整修复版  ·  2026-08"), 8.5, False, GRAY)


def image_font(size):
    return ImageFont.truetype(FONT_PATH, size=size)


def arrow(draw, start, end, color="#64748B", width=4):
    draw.line((*start, *end), fill=color, width=width)
    angle = atan2(end[1] - start[1], end[0] - start[0])
    length = 18
    spread = pi / 7
    p1 = (end[0] - length * cos(angle - spread), end[1] - length * sin(angle - spread))
    p2 = (end[0] - length * cos(angle + spread), end[1] - length * sin(angle + spread))
    draw.polygon([end, p1, p2], fill=color)


def centered(draw, box, title, lines, fill, outline):
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=24, fill=fill, outline=outline, width=3)
    tf = image_font(31)
    bf = image_font(22)
    tw = draw.textbbox((0, 0), title, font=tf)[2]
    draw.text(((x1 + x2 - tw) / 2, y1 + 34), title, font=tf, fill="#0B2545")
    y = y1 + 92
    for line in lines:
        lw = draw.textbbox((0, 0), line, font=bf)[2]
        draw.text(((x1 + x2 - lw) / 2, y), line, font=bf, fill="#5B6573")
        y += 37


def build_architecture(path):
    w, h = 1900, 980
    im = Image.new("RGB", (w, h), "white")
    draw = ImageDraw.Draw(im)
    title_font = image_font(44)
    sub_font = image_font(24)
    draw.text((70, 55), "热点运营产品四模块架构", font=title_font, fill="#0B2545")
    draw.text((70, 120), "一级架构保持简洁；热点雷达和 Future Event 都归入热点输入中心", font=sub_font, fill="#5B6573")
    draw.line((70, 168, 1830, 168), fill="#D7DEE8", width=3)

    boxes = [
        (70, 240, 445, 630),
        (530, 240, 905, 630),
        (990, 240, 1365, 630),
        (1450, 240, 1825, 630),
    ]
    centered(draw, boxes[0], "01  热点输入中心", ["实时突发", "未来可预见事件", "周期、长期与内部热点"], "#EAF2F8", "#2E74B5")
    centered(draw, boxes[1], "02  事件中心", ["信号去重与事件聚类", "形成 Event Card", "理解热度、受众与窗口"], "#E9F6F5", "#0F8B8D")
    centered(draw, boxes[2], "03  机会与行动中心", ["决定参与、观察或拒绝", "确定目标与承接方式", "生成统一行动任务包"], "#FFF3E8", "#E07A2D")
    centered(draw, boxes[3], "04  执行与复盘中心", ["任务下发、审核和发布", "监控、追踪与归因", "复盘并更新规则"], "#EDF6EE", "#3A7D44")
    for i in range(3):
        arrow(draw, (boxes[i][2] + 12, 435), (boxes[i + 1][0] - 12, 435))

    base = (370, 760, 1530, 900)
    draw.rounded_rectangle(base, radius=22, fill="#F2F4F7", outline="#94A3B8", width=3)
    bf = image_font(28)
    text = "专业执行系统：X 矩阵｜Predx 产品｜其他社媒、KOL、CRM 与活动"
    tw = draw.textbbox((0, 0), text, font=bf)[2]
    draw.text(((w - tw) / 2, 805), text, font=bf, fill="#0B2545")
    arrow(draw, (1635, 630), (1530, 830), "#3A7D44", 4)
    im.save(path, quality=95)


def add_picture(doc, path, caption):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(str(path), width=Inches(6.25))
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_after = Pt(8)
    set_run(cap.add_run(caption), 9, False, GRAY, True)


def title_page(doc):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(58)
    p.paragraph_format.space_after = Pt(8)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    set_run(p.add_run("PRODUCT REQUIREMENTS DOCUMENT"), 11, True, BLUE)
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(5)
    set_run(p.add_run("Predx 热点运营产品"), 27, True, NAVY)
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(22)
    set_run(p.add_run("产品需求文档（PRD）"), 18, False, GRAY)

    add_table(doc, ["文档项", "内容"], [
        ["版本", "v1.2（完整修复版）"],
        ["状态", "产品立项 / 需求评审稿"],
        ["产品负责人", "待指定"],
        ["目标用户", "热点运营、内容运营、产品运营、增长、品牌风控与数据团队"],
        ["计划范围", "MVP：热点输入 → Event Card → 机会与行动 → X/Predx执行 → 结果回传"],
        ["更新时间", "2026 年 8 月"],
    ], [1900, 7460], 10)
    callout(doc, "产品定义", "以现实世界事件为中心，把热点来源、事件理解、业务判断、跨系统执行和效果学习连接起来的运营决策与协同产品。", PALE_BLUE, BLUE)
    doc.add_page_break()


def build_document():
    arch = ASSET / "product_architecture.png"
    build_architecture(arch)
    doc = Document()
    style_document(doc)
    title_page(doc)

    doc.add_heading("0. 文档摘要", level=1)
    add_p(doc, "本PRD把前期的热点运营业务方案转化为产品需求。产品一级架构由四个模块组成：热点输入中心、事件中心、机会与行动中心、执行与复盘中心。热点雷达、未来事件中心等不再作为一级模块，而是热点输入中心内部的不同视图和能力。")
    callout(doc, "MVP结论", "第一版不追求接入所有平台或自动发布，而是跑通一条可追溯闭环：发现一个热点 → 形成Event Card → 判断机会 → 生成行动包 → X矩阵和Predx产品执行 → 回传效果并复盘。", PALE_TEAL, TEAL)
    add_table(doc, ["章节", "回答的问题"], [
        ["产品定义", "为什么做、服务谁、解决什么问题"],
        ["产品架构", "有哪些一级模块，边界如何划分"],
        ["功能需求", "每个模块包含哪些页面和能力"],
        ["数据与状态", "核心对象如何关联和流转"],
        ["MVP", "第一版做什么、不做什么、如何验收"],
        ["指标", "如何衡量产品与热点行动是否有效"],
    ], [2100, 7260])

    doc.add_heading("1. 背景与问题", level=1)
    doc.add_heading("1.1 业务背景", level=2)
    add_p(doc, "Predx希望建立一套与产品深度连接的热点运营能力：不仅监控当下正在发生的热点，也提前管理未来可预见事件、周期事件、长期议题和内部可制造事件；事件出现后，系统还需要判断是否参与、如何承接，以及内容和产品分别做什么。")
    doc.add_heading("1.2 当前痛点", level=2)
    bullets(doc, [
        "热点信息分散在热榜、媒体、预测市场、日历、社媒账号和内部数据中，发现依赖个人经验。",
        "单条帖子、新闻与现实事件混在一起，重复信息多，难以形成统一事件理解。",
        "“热点很热”和“值得Predx参与”没有被分开，容易追逐声量却无法承接业务价值。",
        "内容、产品、营销和X矩阵各自执行，但缺少统一目标、事实、边界和追踪ID。",
        "发布后通常只看平台互动，无法定位曝光、点击、注册、首次预测和留存在哪一步流失。",
    ])
    doc.add_heading("1.3 产品机会", level=2)
    add_p(doc, "将热点运营从一次性人工协作升级为事件驱动的产品系统：所有来源围绕同一事件聚合，所有行动围绕同一机会和目标编排，所有效果回到同一事件与规则体系中。")

    doc.add_heading("2. 产品目标与边界", level=1)
    doc.add_heading("2.1 产品目标", level=2)
    add_table(doc, ["目标", "产品结果"], [
        ["更早发现", "覆盖实时、未来、周期、长期和内部五类输入，并对高价值信号及时提醒"],
        ["更准理解", "把多条信号去重聚类为统一事件，形成可核验Event Card"],
        ["更好决策", "区分事件热度与业务机会，明确参与、观察或拒绝"],
        ["更快协同", "用统一行动任务包连接X矩阵、Predx产品与其他渠道系统"],
        ["更强承接", "按产品适配度和准备度选择内容先行、轻联动、直连或产品造热点"],
        ["持续学习", "把执行与漏斗结果回流来源、机会判断、平台适配和行动模板"],
    ], [1900, 7460])
    doc.add_heading("2.2 非目标", level=2)
    bullets(doc, [
        "MVP不建设覆盖所有国家、语言和社媒平台的通用舆情系统。",
        "MVP不替代X矩阵已有的账号定位、文案改编和账号风控逻辑。",
        "MVP不承诺完全自动判断机会或完全自动发布高风险内容。",
        "MVP不将所有自然传播结果包装成精确因果归因。",
    ])

    doc.add_heading("3. 用户与角色", level=1)
    add_table(doc, ["角色", "核心任务", "主要使用模块"], [
        ["热点运营", "监控热点、确认事件、发起机会、协调行动与复盘", "全部模块"],
        ["研究/值班运营", "巡检来源、核验事实、修正聚类、补充Event Card", "热点输入、事件中心"],
        ["内容/渠道运营", "接收任务包、完成渠道改编、审核与发布", "机会与行动、执行与复盘"],
        ["X矩阵Owner", "按账号规则完成路由、内容编排、发布互动和回传", "外部X子系统＋执行任务"],
        ["产品运营", "确认产品准备、建立市场/专题/Push并回传产品结果", "机会与行动、执行与复盘"],
        ["品牌/风控", "审核高风险事件，决定暂停、撤回或更正", "事件中心、执行与复盘"],
        ["数据/产品/研发", "维护指标、数据对象、接口、权限和系统可靠性", "配置与数据层"],
    ], [1700, 4400, 3260])

    doc.add_heading("4. 产品架构与信息架构", level=1)
    add_picture(doc, arch, "图1  热点运营产品一级架构")
    add_p(doc, "四个模块是一级产品导航；模块内部通过同一个事件、机会和行动任务包关联。业务操作可以从工作台、搜索、提醒或关联对象直接进入，不要求用户机械地逐步点击。")
    doc.add_heading("4.1 一级导航", level=2)
    add_table(doc, ["一级模块", "核心对象", "核心页面"], [
        ["热点输入中心", "Source Signal / Future Event", "实时雷达、未来事件、周期模板、主题监控、内部信号"],
        ["事件中心", "Trend Event / Event Card", "事件列表、事件详情、合并拆分、证据与传播分析"],
        ["机会与行动中心", "Opportunity / Action Package", "待判断机会、行动设计器、目标适配、行动包"],
        ["执行与复盘中心", "Task / Publication / Performance", "执行任务、审核发布、实时监控、漏斗与复盘"],
    ], [1850, 2450, 5060])
    doc.add_heading("4.2 全局能力", level=2)
    bullets(doc, [
        "统一搜索：按事件、人物、组织、主题、平台、时间、状态和负责人搜索。",
        "统一工作台：展示今日重点、未来准备节点、待判断机会、待审核任务和异常提醒。",
        "全局快捷创建：手动创建未来事件、现实事件、机会或行动任务包。",
        "关联跳转：从事件查看机会和任务，从发布结果回看事件、目标和产品漏斗。",
    ])

    doc.add_heading("5. 模块一：热点输入中心", level=1)
    doc.add_heading("5.1 模块目标", level=2)
    add_p(doc, "统一承接五类热点输入。实时雷达与未来事件不是两个孤立产品，而是同一输入中心的不同视图：一个面向正在发生，一个面向即将发生；周期、长期和内部热点可生成未来事件或被激活为实时事件。")
    doc.add_heading("5.2 页面结构", level=2)
    add_table(doc, ["页面", "主要内容", "主要操作"], [
        ["实时雷达", "热榜、新闻、种子账号、社区、跨平台异常信号", "筛选、订阅、标记无关/重复、创建或并入事件"],
        ["未来事件", "公共/行业日历、预测市场、新闻预告、产品日历", "创建、确认、延期、取消、设置准备节点、转实时"],
        ["周期模板", "赛事、财报、经济数据、节日和年度事件模板", "生成下一期、维护提前量、历史基线和准备资产"],
        ["长期议题", "母题、子议题、实体、立场、触发器和常青资产", "维护知识树、设置激活规则、关联事件"],
        ["内部信号", "概率、交易、站内搜索、浏览和产品运营节点", "设置阈值、发起自造热点、创建产品动作"],
        ["来源与监控配置", "API、来源库、关键词、实体、种子账号、刷新频率", "启停、分级、黑白名单、异常查看"],
    ], [1850, 4270, 3240])
    doc.add_heading("5.3 核心功能需求", level=2)
    add_table(doc, ["ID", "需求", "优先级", "验收要点"], [
        ["IN-01", "接入首批实时信号源，并保存原文、时间、作者、平台、URL、语言和互动数据", "P0", "采集失败可见；每条信号可追溯原始来源"],
        ["IN-02", "支持按主题、平台、地区、语言、时间和热度筛选实时信号", "P0", "组合筛选结果正确，可保存常用视图"],
        ["IN-03", "支持人工将信号标记为有效、无关、重复或高风险", "P0", "状态即时生效，并记录操作者与时间"],
        ["IN-04", "支持创建Future Event，包含时间类型、确认状态、证据和下一次核验时间", "P0", "日期不确定时可使用时间窗口或条件触发"],
        ["IN-05", "Future Event支持T-30/T-7/T-1提醒和进入发生窗口后转实时", "P0", "提醒按配置触发；转实时后保留原关联"],
        ["IN-06", "支持周期模板自动生成下一期Future Event", "P1", "生成时间、来源、准备节点和负责人正确"],
        ["IN-07", "支持内部指标异常创建候选信号", "P1", "触发阈值、证据和对应产品对象可追溯"],
        ["IN-08", "支持来源优先级、白名单、黑名单与健康状态", "P1", "停用来源不再采集；失败能提醒维护人"],
    ], [1100, 4570, 950, 2740], 8.8)
    doc.add_heading("5.4 Future Event字段", level=2)
    bullets(doc, [
        "事件身份：标题、主题、主体、地区、语言和关联周期模板。",
        "时间：准确日期、时间窗口、条件触发或持续进程。",
        "确认状态：传闻、报道、预期、官方确认、进行中、完成、延期或取消。",
        "证据与结果：主来源、辅助来源、可能结果分支和关键触发条件。",
        "准备计划：内容、产品、活动和风险动作的提前节点。",
    ])

    doc.add_heading("6. 模块二：事件中心", level=1)
    doc.add_heading("6.1 模块目标", level=2)
    add_p(doc, "把分散的Source Signal转化为统一的现实事件，并通过Event Card完成结构化理解。Event Card只回答“发生了什么”，不直接代替“Predx是否参与”的业务判断。")
    doc.add_heading("6.2 事件化处理", level=2)
    numbers(doc, [
        "标准化信号：统一时间、语言、链接、作者、实体和平台指标。",
        "内容去重：识别相同URL、转发、转载、同源新闻和搬运。",
        "事件聚类：结合主体、动作、时间、地点和语义形成事件候选。",
        "人工治理：支持合并、拆分、设置主事件/子事件和指定权威来源。",
        "生成Canonical Trend Event，并持续接收新信号和事实更新。",
    ])
    doc.add_heading("6.3 Event Card八大模块", level=2)
    add_table(doc, ["模块", "核心字段", "指导作用"], [
        ["事件身份", "标题、类型、主题、实体、地区、语言、主/子事件", "明确事件边界与所属业务主题"],
        ["事实与证据", "事实清单、未确认点、来源等级、独立来源数、核验时间", "判断能说什么、是否需要等待"],
        ["传播热度", "声量、增速、加速度、独立作者、互动和跨平台数", "判断传播势能而非只看绝对热度"],
        ["生命周期", "萌芽、上升、爆发、峰值、回落、长尾、再激活", "选择快讯、解释、深度或结果内容"],
        ["受众结构", "观察受众、潜在受众、目标受众、地区、语言和动机", "决定角度、难度、渠道和CTA"],
        ["平台传播", "首发、发酵、目标受众、执行和产品承接平台", "避免把最热平台误当最佳转化平台"],
        ["窗口与风险", "注意力/内容/产品/长尾窗口及事实、品牌、法律风险", "决定做什么、最晚何时做、是否放弃"],
        ["系统初步信号", "信息完整度、异常项、建议观察方向和置信度", "判断是否可以进入Opportunity"],
    ], [1550, 5000, 2810], 8.8)
    doc.add_heading("6.4 生命周期与窗口规则", level=2)
    add_p(doc, "MVP每15-30分钟计算主题内标准化声量、增速和加速度，并结合跨平台数、新信息率与人工确认输出生命周期及置信度。可用行动窗口按“预计窗口－制作耗时－审核耗时－分发准备”计算。")
    doc.add_heading("6.5 核心功能需求", level=2)
    add_table(doc, ["ID", "需求", "优先级", "验收要点"], [
        ["EV-01", "硬去重与模型辅助软去重", "P0", "重复传播不重复计作独立事实来源"],
        ["EV-02", "模型辅助事件聚类，并展示置信度", "P0", "低置信聚类进入人工队列"],
        ["EV-03", "支持合并、拆分、锁定、主子事件和操作记录", "P0", "修正后关联信号、机会和任务不丢失"],
        ["EV-04", "提供Event Card八大模块并支持人工确认", "P0", "每个关键判断可查看证据和更新时间"],
        ["EV-05", "提供事件传播曲线、来源列表和平台时间线", "P0", "可定位首发、发酵和当前主要平台"],
        ["EV-06", "支持事件状态：候选、观察、活跃、回落、结束、归档、再激活", "P0", "状态变化有记录且可触发提醒"],
        ["EV-07", "支持历史相似事件和长期议题关联", "P1", "用户可查看历史表现与复盘结论"],
    ], [1100, 4700, 950, 2610], 8.9)

    doc.add_heading("7. 模块三：机会与行动中心", level=1)
    doc.add_heading("7.1 模块目标", level=2)
    add_p(doc, "读取完整Event Card，再结合Predx业务目标、产品准备、平台受众和风险条件，决定参与、观察或拒绝；若参与，则生成统一行动任务包。")
    doc.add_heading("7.2 Opportunity判断", level=2)
    add_table(doc, ["维度", "判断问题"], [
        ["Predx相关性", "与产品、用户、品牌和长期叙事是否相关"],
        ["增长价值", "能否带来有效触达、拉新、激活、留存或合作价值"],
        ["参与资格", "是否拥有数据、产品、专家或独特观点"],
        ["平台与受众", "讨论在哪里、目标用户在哪里、在哪执行最有效"],
        ["产品承接", "是否已有预测市场、专题页、推荐位、Push或活动能力"],
        ["时间与资源", "剩余窗口是否覆盖生产、审核和上线时间"],
        ["风险", "事实、品牌、法律、地区和平台风险是否可控"],
    ], [2200, 7160])
    add_p(doc, "MVP使用红/黄/绿或1-5级辅助比较，不使用黑盒总分直接决策。任何高风险、无事实基础或产品不可用条件都可以成为否决项。")
    doc.add_heading("7.3 目标与适配逻辑", level=2)
    bullets(doc, [
        "目标支持曝光、拉新、激活和留存；每次机会设置主目标、次目标、权重和护栏。",
        "系统按目标 → 受众 → 平台 → 动作 → 产品路径完成适配，不要求每个渠道承担所有目标。",
        "同一平台同时承担曝光和转化时，可编排为主帖曝光、回复/Thread转化、结果帖留存。",
        "平台角色必须区分首发平台、发酵平台、目标受众平台、执行平台和产品承接终点。",
    ])
    doc.add_heading("7.4 参与与产品承接方式", level=2)
    add_table(doc, ["类别", "可选方式"], [
        ["内容参与", "信息翻译、事实核验、观点、预测、数据、互动、Meme、视频或观察不参与"],
        ["产品承接", "内容先行、轻产品联动、产品直连、战略级专题/活动、产品反向造热点"],
        ["业务组合", "内容、产品、营销、社区/KOL、PR和风险动作组合"],
    ], [2100, 7260])
    doc.add_heading("7.5 统一行动任务包", level=2)
    add_table(doc, ["模块", "内容"], [
        ["目标架构", "主目标、次目标、权重、目标受众、目标行为、KPI和护栏"],
        ["统一事实", "确认事实、证据、未确认点和最后更新时间"],
        ["统一叙事", "核心判断、可选角度、必说、禁说、语气和品牌边界"],
        ["行动组合", "渠道、产品、营销、社区、风控和数据任务"],
        ["产品承接", "目标市场/页面、CTA、用户路径、追踪参数和备用方案"],
        ["节奏依赖", "优先级、截止时间、先后顺序、依赖和停止条件"],
        ["审核回传", "风险等级、审核人、最终内容、链接、成本和效果字段"],
    ], [2250, 7110])
    callout(doc, "定义", "统一行动任务包既规定统一对外口径，也规定内容、产品、营销、社区和风控分别如何响应；它统一共同目标和边界，但不替代专业执行系统。", PALE_ORANGE, ORANGE)
    doc.add_heading("7.6 核心功能需求", level=2)
    add_table(doc, ["ID", "需求", "优先级", "验收要点"], [
        ["OP-01", "从Event Card创建Opportunity并选择参与、观察或拒绝", "P0", "记录理由、负责人、判断时间和有效期"],
        ["OP-02", "展示七个判断维度及证据，不以单一总分替代人工结论", "P0", "每项可编辑、可追溯、可标记否决"],
        ["OP-03", "支持多目标、主次权重、目标受众和护栏", "P0", "行动设计能读取并继承目标配置"],
        ["OP-04", "根据平台、受众和产品准备推荐参与与承接方式", "P1", "推荐可修改，并保存采纳/拒绝结果"],
        ["AP-01", "从Opportunity生成统一行动任务包", "P0", "目标、事实、边界、任务和回传要求完整"],
        ["AP-02", "支持将行动包拆成X、产品和其他渠道任务", "P0", "任务共享event_id、opportunity_id和package_id"],
        ["AP-03", "支持行动模板和最小有效动作", "P1", "资源或窗口不足时可快速缩减方案"],
    ], [1100, 4700, 950, 2610], 8.8)

    doc.add_heading("8. 模块四：执行与复盘中心", level=1)
    doc.add_heading("8.1 模块目标", level=2)
    add_p(doc, "把行动包交给专业执行系统，确认最终执行符合目标、事实和边界；发布后完成基础监控、结果回传、归因和复盘。该模块保持轻量，不重复建设复杂内容工作流。")
    doc.add_heading("8.2 任务状态", level=2)
    add_p(doc, "主状态：待接受 → 生产中 → 待审核 → 已批准 → 已执行 → 已回传。异常状态：已拒绝、失败、取消、暂停和撤回。")
    doc.add_heading("8.3 X矩阵接入边界", level=2)
    add_table(doc, ["热点产品提供", "X矩阵负责", "X矩阵回传"], [
        ["事件、目标、受众、核心事实、角度、必说禁说、产品链接和窗口", "账号选择、X原生改编、发布顺序、时间、互动和账号风险", "接受/拒绝、账号方案、最终文案、发布链接、曝光互动点击和异常"],
    ], [3120, 3120, 3120], 8.8)
    add_p(doc, "接入流程：热点产品生成X任务 → X系统推荐账号和行动方案 → 人工确认 → X系统执行 → 结果回传。热点产品决定为什么做和边界，X系统决定在X上怎么做。")
    doc.add_heading("8.4 Predx产品接入", level=2)
    bullets(doc, [
        "查询现有预测市场、专题页、推荐位、Push、Watchlist和活动能力。",
        "提交关联市场、新建市场、专题/推荐、Push或结果提醒任务。",
        "回传页面访问、注册、首次预测、再次预测及产品异常。",
        "机会判断同时使用Product Fit与Product Readiness，相关但未准备好时不得强行直连。",
    ])
    doc.add_heading("8.5 发布后监控", level=2)
    bullets(doc, [
        "记录最终内容/素材、平台、账号、发布时间、链接和追踪参数。",
        "监控事实变化、舆情异常、账号状态、产品链接和市场可用性。",
        "发生事实变化或风险升级时，由人工选择更新、暂停、撤回或更正。",
        "把平台表现、产品漏斗和成本关联回同一事件、机会和行动包。",
    ])
    doc.add_heading("8.6 复盘诊断", level=2)
    add_table(doc, ["现象", "优先诊断"], [
        ["曝光高、点击低", "受众、角度、CTA或产品连接"],
        ["曝光低、转化率高", "分发、账号选择和发布时间"],
        ["点击高、注册低", "落地页与注册流程"],
        ["注册高、首次预测低", "首次体验、市场解释和激活路径"],
        ["激活高、留存低", "结果提醒、Watchlist和相关事件推荐"],
    ], [2800, 6560])
    doc.add_heading("8.7 核心功能需求", level=2)
    add_table(doc, ["ID", "需求", "优先级", "验收要点"], [
        ["EX-01", "按标准接口向X矩阵和Predx产品下发任务", "P0", "接收方可接受/拒绝并返回原因"],
        ["EX-02", "保存最终执行记录和统一追踪ID", "P0", "从事件可追到账号、内容、页面和产品行为"],
        ["EX-03", "提供事实、舆情、账号和产品异常提醒", "P0", "提醒包含对象、原因、时间和处理入口"],
        ["EX-04", "支持更新、暂停、撤回和更正", "P0", "操作有权限控制和审计记录"],
        ["EX-05", "回传平台、产品和成本指标", "P0", "字段口径一致，失败和延迟可见"],
        ["RV-01", "每个已执行机会生成复盘卡", "P0", "输出继续、停止、实验和规则更新四项"],
        ["RV-02", "按事件类型、平台、账号、目标和承接模式查看历史效果", "P1", "筛选维度可组合，结果可下钻"],
    ], [1100, 4700, 950, 2610], 8.8)

    doc.add_heading("9. 核心数据对象与关系", level=1)
    add_table(doc, ["对象", "定义", "关键关系"], [
        ["Source Signal", "帖子、新闻、视频、日历项、预测问题或内部异常", "多条信号聚合为一个事件"],
        ["Future Event", "尚未发生但可结构化准备的现实事件", "发生时转为Trend Event；可提前产生机会和任务"],
        ["Trend Event", "统一的现实世界事件", "可有主/子事件；可关联多个机会"],
        ["Event Card", "对事件的客观结构化理解", "一张卡读取全部来源、证据和分析"],
        ["Opportunity", "Predx对事件的业务参与判断", "可关联多个事件，可生成多个行动包"],
        ["Action Package", "跨系统统一目标、事实、边界和任务协议", "拆分为多个Execution Task"],
        ["Execution Task", "交给具体渠道或产品系统的行动请求", "形成Publication或Product Action"],
        ["Performance/Learning", "平台、产品、成本结果与复盘结论", "回流来源、判断、渠道和模板规则"],
    ], [1800, 4050, 3510], 8.9)
    callout(doc, "关系原则", "真正的产品网状结构来自对象关系，而不是把流程图画得复杂：事件、机会、行动包和执行结果可以被多对多关联、搜索、复用和重新激活。", PALE_TEAL, TEAL)

    doc.add_heading("10. 状态、权限与通知", level=1)
    doc.add_heading("10.1 核心状态", level=2)
    add_table(doc, ["对象", "状态"], [
        ["Future Event", "候选、待确认、已确认、临近、进行中、完成、延期、取消"],
        ["Trend Event", "候选、观察、活跃、回落、结束、归档、再激活"],
        ["Opportunity", "待判断、参与、观察、拒绝、待复查、关闭"],
        ["Action Package", "草稿、待确认、已批准、执行中、完成、暂停、取消"],
        ["Execution Task", "待接受、生产中、待审核、已批准、已执行、已回传及异常状态"],
    ], [2250, 7110])
    doc.add_heading("10.2 权限", level=2)
    bullets(doc, [
        "来源和信号：研究/值班运营可标注；来源配置仅管理员可修改。",
        "事件：热点运营可合并拆分；关键事实锁定需高级权限。",
        "机会和行动包：热点负责人可创建；高风险机会必须品牌/法务审批。",
        "执行：渠道Owner确认最终内容；暂停、撤回和更正按风险等级授权。",
        "所有关键状态、事实、判断、审核和撤回操作保留审计记录。",
    ])
    doc.add_heading("10.3 通知与SLA", level=2)
    add_table(doc, ["触发器", "通知对象", "默认动作"], [
        ["实时信号异常增长", "值班运营", "进入待确认队列"],
        ["Future Event到达准备节点", "事件负责人、产品/内容Owner", "检查准备状态"],
        ["Opportunity接近窗口截止", "热点负责人", "缩减动作或放弃"],
        ["任务超时或被拒绝", "行动包负责人", "调整渠道、资源或时间"],
        ["事实变化/风险升级", "热点负责人、品牌风控、执行Owner", "更新、暂停、撤回或更正"],
        ["结果回传失败", "数据/系统Owner", "重试并标记数据不完整"],
    ], [2950, 3100, 3310])

    doc.add_heading("11. 指标体系", level=1)
    doc.add_heading("11.1 产品使用指标", level=2)
    add_table(doc, ["阶段", "核心指标"], [
        ["发现", "有效信号数、发现领先时间、来源稳定性、有效机会召回"],
        ["事件理解", "去重率、聚类人工修正率、Event Card完整率与确认时长"],
        ["机会判断", "参与/观察/拒绝分布、人工采纳率、机会命中率"],
        ["行动协同", "立项到下发时间、任务接受率、窗口内完成率、审核耗时"],
        ["数据闭环", "追踪ID完整率、结果回传率、复盘完成率、规则更新率"],
    ], [2250, 7110])
    doc.add_heading("11.2 热点行动结果指标", level=2)
    bullets(doc, [
        "曝光：有效触达、目标受众覆盖、分享和讨论质量。",
        "拉新：产品点击、注册、注册转化率和单位注册成本。",
        "激活：首次预测人数、激活率和单位激活成本。",
        "留存：再次访问、再次预测、结果提醒打开率和相关事件参与。",
        "经济性与风险：总成本、机会级ROI、事实错误、投诉、撤回和账号处罚。",
    ])
    add_p(doc, "归因原则：优先使用直接追踪参数和产品路径；自然传播使用时间窗口贡献判断；在条件允许时使用对照实验，不虚构精确因果。")

    doc.add_heading("12. MVP范围", level=1)
    callout(doc, "MVP原则", "架构完整、主题有限、来源有限、执行系统有限，优先证明一条真实热点能被发现、理解、利用、承接和复盘。", PALE_BLUE, BLUE)
    doc.add_heading("12.1 MVP必须包含", level=2)
    add_table(doc, ["模块", "MVP范围"], [
        ["热点输入", "X/新闻或热榜/预测市场/1个垂直日历＋人工录入；Future Event基础提醒"],
        ["事件中心", "硬去重、模型辅助软去重与聚类、人工合并拆分、Event Card八模块"],
        ["机会与行动", "七维判断、参与/观察/拒绝、多目标、产品模式、统一行动任务包"],
        ["执行与复盘", "X任务下发与结果回传、Predx产品链接、基础监控、漏斗和复盘卡"],
        ["基础能力", "统一ID、搜索、权限、审计、提醒和基本配置"],
    ], [2250, 7110])
    doc.add_heading("12.2 MVP暂不包含", level=2)
    bullets(doc, [
        "一次接入所有社媒、地区、行业和语言。",
        "全自动机会决策与高风险自动发布。",
        "复制X矩阵内部账号画像、内容生成和排期系统。",
        "复杂BPM、版本树、资源排班和全量营销自动化。",
        "复杂机器学习峰值预测和自然传播精确归因。",
    ])
    doc.add_heading("12.3 推荐试点", level=2)
    add_p(doc, "优先选择结果明确、频率稳定、产品天然相关且风险相对可控的体育赛事。试点链路：赛程生成Future Event → T-7准备 → 实时信号形成Event Card → Opportunity判断 → X账号路由与概率内容 → Predx市场承接 → 结果提醒 → 漏斗复盘。")

    doc.add_heading("13. 迭代计划", level=1)
    add_table(doc, ["阶段", "建议周期", "范围", "关键交付"], [
        ["Phase 0 需求与数据对齐", "2周", "主题、来源、对象、接口、指标与历史样本", "PRD、数据字典、原型、接口清单、样本集"],
        ["Phase 1 输入与事件", "4-6周", "首批来源、Future Event、去重聚类、Event Card", "热点池、事件列表、详情页、提醒与人工治理"],
        ["Phase 2 机会与X闭环", "4-6周", "Opportunity、目标适配、行动包、X任务与回传", "机会工作台、行动设计器、X接口和执行记录"],
        ["Phase 3 产品与复盘", "4周", "产品承接、注册/首次预测、成本和复盘", "产品接口、漏斗看板、复盘卡和规则更新"],
        ["Phase 4 扩展", "持续", "更多平台、自动化和低风险半自动执行", "模板库、规则引擎、多渠道协同"],
    ], [1600, 1350, 3600, 2810], 8.8)

    doc.add_heading("14. MVP验收标准", level=1)
    bullets(doc, [
        "首批来源稳定采集；采集失败、延迟和来源健康状态可见。",
        "同一热点的重复信号可去重聚类，人工能够合并、拆分并保留完整关联。",
        "Event Card八大模块可以支持人工完成参与、观察或拒绝判断。",
        "Opportunity能够设置多目标并生成包含事实、边界、产品路径和回传要求的行动包。",
        "X矩阵任务可完成接受/拒绝、账号方案、最终文案、发布链接和效果回传。",
        "内容点击可关联到Predx访问、注册和首次预测，数据缺失和失败状态可见。",
        "每个已执行机会形成复盘，至少更新一条来源、判断、渠道、模板或产品规则。",
        "高风险事件未经批准不能发布；事实变化时支持暂停、撤回和更正。",
    ])

    doc.add_heading("15. 前置依赖与待决策项", level=1)
    add_table(doc, ["事项", "建议默认方案", "需要确认"], [
        ["首批主题", "3-5个Predx高相关主题；优先体育试点", "具体清单与排除项"],
        ["首批数据源", "X、新闻/热榜、预测市场、1个垂直日历", "API、供应商、成本与合规"],
        ["目标市场和语言", "团队可直接审校的1-2种语言", "地区、时区和本地化Owner"],
        ["X矩阵接口", "任务下发、接受/拒绝、账号方案、发布与效果回传", "现有系统字段和接口成熟度"],
        ["Predx产品接口", "市场查询、链接、页面事件、注册和首次预测", "埋点口径和责任人"],
        ["风险审批", "高风险与重大品牌议题强制审批", "审批人、值班机制和SLA"],
        ["北极星指标", "有效增长价值＋热点行动ROI", "核心产品行为和价值权重"],
    ], [1900, 3950, 3510], 8.9)
    callout(doc, "下一步", "基于本PRD进入信息架构和低保真原型设计，优先画出工作台、热点输入、事件详情、Opportunity判断、行动设计器和执行任务六个核心页面。", PALE_GREEN, GREEN)

    doc.add_page_break()
    doc.add_heading("16. 核心对象数据字典", level=1)
    add_p(doc, "本章补充字段级产品需求。字段标记规则：P0表示MVP必须落库或可计算；P1表示MVP可预留、后续补充。必填字段在对象进入下一状态前必须完整；系统计算字段允许人工修正，但必须保留原值、修正人、修正时间和修正理由。")
    callout(doc, "字段治理原则", "所有核心对象必须包含唯一ID、创建/更新时间、来源、负责人、状态和审计记录；所有模型结论必须同时保存结果、置信度、依据和人工修正。", PALE_BLUE, BLUE)

    doc.add_heading("16.1 Source Signal字段", level=2)
    add_table(doc, ["字段", "类型", "必填/MVP", "来源或生成方式", "业务用途"], [
        ["signal_id", "string", "必填/P0", "系统生成", "信号唯一标识"],
        ["source_type", "enum", "必填/P0", "采集配置", "热榜、新闻、社媒、日历、预测市场、内部数据或人工"],
        ["source_name", "string", "必填/P0", "来源库", "识别具体媒体、平台、日历或数据系统"],
        ["platform", "enum", "必填/P0", "采集器", "平台筛选和平台内指标归一化"],
        ["source_url", "url", "条件必填/P0", "原始数据", "事实追溯与去重"],
        ["external_id", "string", "条件必填/P0", "平台原始ID", "防重复采集和回查"],
        ["author_id / author_name", "string", "条件必填/P0", "平台原始数据", "识别首发、传播者和种子账号"],
        ["author_type", "enum", "可选/P1", "账号库或模型", "官方、媒体、记者、KOL、普通用户、机器人嫌疑"],
        ["published_at", "datetime", "必填/P0", "原始数据", "首发判断和传播时间线"],
        ["collected_at", "datetime", "必填/P0", "系统生成", "计算发现延迟和采集健康"],
        ["title", "text", "条件必填/P0", "原始数据", "摘要、检索和聚类"],
        ["body_text", "text", "条件必填/P0", "原始数据/转写", "实体抽取、语义聚类和事实分析"],
        ["media_type", "enum", "必填/P0", "原始数据", "文本、图片、视频、音频、直播或数据记录"],
        ["media_urls", "array", "可选/P1", "原始数据", "内容审查和素材复用"],
        ["language / region", "enum", "必填/P0", "原始数据＋识别模型", "地区语言筛选和受众判断"],
        ["engagement_metrics", "object", "条件必填/P0", "平台数据", "点赞、评论、分享、播放、浏览等平台原始指标"],
        ["normalized_heat", "number", "系统/P0", "平台内归一化", "跨平台热度比较"],
        ["growth_rate / acceleration", "number", "系统/P0", "时间序列计算", "异常检测和生命周期判断"],
        ["entities", "array", "系统＋人工/P0", "实体抽取", "事件聚类和知识关联"],
        ["keywords / topics", "array", "系统＋人工/P0", "主题模型/词典", "主题监控与检索"],
        ["originality_type", "enum", "系统/P0", "转发链、URL与文本相似", "原创、转发、引用、转载或搬运"],
        ["duplicate_of", "signal_id", "条件/P0", "去重引擎", "避免重复计量"],
        ["cluster_id / event_id", "string", "条件/P0", "聚类引擎＋人工", "关联叙事簇和统一事件"],
        ["source_reliability", "enum", "系统＋人工/P0", "来源等级规则", "事实核验和风险控制"],
        ["risk_labels", "array", "可选/P0", "规则＋人工", "政治、法律、品牌、敏感内容等风险"],
        ["review_status", "enum", "必填/P0", "人工操作", "未处理、有效、无关、重复、高风险"],
    ], [1750, 1050, 1300, 2750, 2510], 8.2)

    doc.add_heading("16.2 Future Event字段", level=2)
    add_table(doc, ["字段", "类型", "必填/MVP", "来源或生成方式", "业务用途"], [
        ["future_event_id", "string", "必填/P0", "系统生成", "未来事件唯一标识"],
        ["title / normalized_title", "text", "必填/P0", "来源＋人工", "展示与跨来源归并"],
        ["event_type / topic", "enum", "必填/P0", "主题词典", "分类、路由和历史基线"],
        ["entities", "array", "必填/P0", "抽取＋人工", "主体、组织、人物、赛事或产品关联"],
        ["region / language / timezone", "enum", "必填/P0", "来源＋人工", "本地化、提醒和时间换算"],
        ["time_type", "enum", "必填/P0", "人工/抽取", "准确日期、时间窗口、条件触发或持续进程"],
        ["start_at / end_at", "datetime", "条件必填/P0", "来源＋人工", "发生窗口和倒计时"],
        ["time_precision", "enum", "必填/P0", "系统＋人工", "分钟、小时、日期、周、月或未知"],
        ["trigger_condition", "text", "条件必填/P0", "人工/模型", "无确定日期事件的触发描述"],
        ["result_time", "datetime", "可选/P0", "来源＋人工", "结果内容、市场结算和留存提醒"],
        ["confirmation_status", "enum", "必填/P0", "人工＋来源规则", "传闻、报道、预期、官方确认、进行中、完成、延期、取消"],
        ["primary_evidence", "signal/url", "必填/P0", "人工指定", "确定事件是否可信"],
        ["supporting_evidence", "array", "可选/P0", "系统聚合＋人工", "补充交叉核验"],
        ["next_verification_at", "datetime", "必填/P0", "人工/规则", "不确定事件定期复查"],
        ["outcome_branches", "array", "可选/P0", "预测市场/人工", "预设可能结果与内容、产品动作"],
        ["branch_probability", "object", "可选/P1", "预测市场/模型", "展示当前概率及变化"],
        ["prediction_market_ids", "array", "可选/P0", "预测市场映射", "现实事件与预测问题分离关联"],
        ["recurrence_template_id", "string", "可选/P0", "周期模板", "自动生成下一期"],
        ["prep_T30 / T7 / T1", "object", "可选/P0", "规则＋任务状态", "内容、产品、营销、风险准备"],
        ["content_readiness", "enum", "可选/P0", "内容任务", "未准备、准备中、就绪、不可用"],
        ["product_readiness", "enum", "可选/P0", "产品能力中心", "判断能否直接承接"],
        ["owner / watchers", "user/array", "必填/P0", "人工", "责任与提醒"],
        ["conversion_status", "enum", "系统/P0", "状态机", "未转实时、已转Trend Event或已关闭"],
        ["delay_cancel_reason", "text", "条件/P0", "人工/来源", "变更解释和审计"],
    ], [1750, 1050, 1300, 2750, 2510], 8.2)

    doc.add_heading("16.3 Trend Event基础字段", level=2)
    add_table(doc, ["字段", "类型", "必填/MVP", "来源或生成方式", "业务用途"], [
        ["event_id", "string", "必填/P0", "系统生成", "统一现实事件ID"],
        ["canonical_title", "text", "必填/P0", "模型建议＋人工", "统一对外展示标题"],
        ["summary", "text", "必填/P0", "模型＋人工", "快速理解事件"],
        ["hotspot_type", "enum", "必填/P0", "规则＋人工", "实时、未来、周期、长期或内部"],
        ["topic / subtopic", "enum", "必填/P0", "主题体系", "业务路由和统计"],
        ["entities / location", "array", "必填/P0", "信号聚合＋人工", "事件边界和检索"],
        ["event_start_at / detected_at", "datetime", "必填/P0", "信号时间线", "计算发现领先时间"],
        ["parent_event_id", "string", "可选/P0", "人工/模型", "主事件与子事件"],
        ["related_event_ids", "array", "可选/P1", "相似度＋人工", "相关事件和历史事件"],
        ["future_event_id", "string", "可选/P0", "状态转换", "保留未来准备历史"],
        ["long_term_topic_id", "string", "可选/P1", "母题关联", "结构性议题激活"],
        ["signal_count / independent_sources", "number", "系统/P0", "聚合统计", "规模和证据独立性"],
        ["event_status", "enum", "必填/P0", "状态机", "候选、观察、活跃、回落、结束、归档、再激活"],
        ["owner / risk_level", "user/enum", "必填/P0", "人工＋规则", "责任、权限与审批路由"],
        ["merge_split_history", "array", "系统/P0", "操作日志", "事件边界审计"],
    ], [1750, 1050, 1300, 2750, 2510], 8.2)

    doc.add_heading("17. Event Card八大模块字段字典", level=1)
    doc.add_heading("17.1 事件身份与事实证据", level=2)
    add_table(doc, ["模块", "字段", "类型", "来源/计算", "业务用途"], [
        ["事件身份", "event_id / canonical_title", "string/text", "Trend Event", "唯一识别与展示"],
        ["事件身份", "hotspot_type / topic / subtopic", "enum", "规则＋人工", "分类、路由和历史比较"],
        ["事件身份", "entities / location / language", "array", "信号聚合＋人工", "定义谁、在哪、以何种语言讨论"],
        ["事件身份", "parent / child / related events", "array", "事件图谱", "展示上下文和进展层级"],
        ["事件身份", "future / periodic / long-topic links", "array", "对象关联", "串联未来、周期和长期母题"],
        ["事实证据", "confirmed_facts", "array", "人工确认", "可直接使用的事实清单"],
        ["事实证据", "unconfirmed_claims", "array", "模型＋人工", "禁止当成事实传播"],
        ["事实证据", "disputed_points", "array", "冲突检测", "标记来源冲突和观点争议"],
        ["事实证据", "primary_source", "signal/url", "人工指定", "权威依据"],
        ["事实证据", "supporting_sources", "array", "系统聚合", "交叉验证"],
        ["事实证据", "source_independence_count", "number", "传播关系去重", "避免把转载当多个证据"],
        ["事实证据", "evidence_grade", "enum", "来源等级规则", "事实可靠度"],
        ["事实证据", "last_verified_at / verifier", "datetime/user", "人工操作", "确定事实新鲜度与责任"],
        ["事实证据", "fact_change_log", "array", "系统记录", "事实更新、更正与撤回依据"],
    ], [1300, 2350, 1400, 2050, 2260], 8.2)

    doc.add_heading("17.2 传播热度与生命周期", level=2)
    add_table(doc, ["模块", "字段", "类型", "来源/计算", "业务用途"], [
        ["传播热度", "signal_volume", "number", "去重后信号数", "当前传播规模"],
        ["传播热度", "independent_authors / sources", "number", "传播图谱", "真实扩散广度"],
        ["传播热度", "engagement_total", "number", "平台指标归一化", "综合互动规模"],
        ["传播热度", "growth_rate / acceleration", "number", "时间序列", "判断上升和爆发速度"],
        ["传播热度", "cross_platform_count", "number", "平台聚合", "跨圈层扩散程度"],
        ["传播热度", "search_interest", "number", "搜索趋势", "主动信息需求"],
        ["传播热度", "baseline_deviation", "number", "同主题历史基线", "识别异常而非只看绝对值"],
        ["传播热度", "bot_suspicion_ratio", "number", "账号异常规则", "避免虚假热度"],
        ["生命周期", "lifecycle_stage", "enum", "规则/模型＋人工", "萌芽、上升、爆发、峰值、回落、长尾、再激活"],
        ["生命周期", "stage_entered_at", "datetime", "状态计算", "计算阶段持续时间"],
        ["生命周期", "new_information_rate", "number", "新事实/内容占比", "区分新进展与重复讨论"],
        ["生命周期", "content_saturation", "number", "相似内容占比", "判断同质化程度"],
        ["生命周期", "predicted_peak_at", "datetime", "历史基线/模型", "安排内容和产品节奏"],
        ["生命周期", "reactivation_probability", "number", "日程与触发器", "决定是否保留长期观察"],
        ["生命周期", "stage_confidence / evidence", "number/text", "模型输出", "支持人工判断与修正"],
    ], [1300, 2350, 1400, 2050, 2260], 8.2)

    doc.add_heading("17.3 受众与平台传播", level=2)
    add_table(doc, ["模块", "字段", "类型", "来源/计算", "业务用途"], [
        ["受众", "observed_audiences", "array", "作者/互动者分析", "当前实际讨论人群"],
        ["受众", "potential_audiences", "array", "兴趣相似模型", "可能被事件吸引的人群"],
        ["受众", "predx_target_audiences", "array", "目标人群库", "公司希望触达的人群"],
        ["受众", "region / language distribution", "object", "账号与内容数据", "地区和语言适配"],
        ["受众", "interest_tags / communities", "array", "共现主题与社区", "内容角度和渠道选择"],
        ["受众", "attention_motivation", "enum/array", "内容语义＋抽样", "求知、娱乐、立场、交易、身份认同等"],
        ["受众", "knowledge_level", "enum", "内容与互动分析", "决定解释深度"],
        ["受众", "product_intent", "enum/number", "行为与站内相似人群", "预测转化意图"],
        ["受众", "predx_overlap", "number", "站内/外人群匹配", "判断业务相关性"],
        ["受众", "audience_confidence / evidence", "number/text", "模型＋人工", "避免无依据画像"],
        ["平台", "origin_platform", "enum", "最早有效信号", "识别首发平台"],
        ["平台", "amplification_platforms", "array", "跨平台时间线", "识别发酵平台"],
        ["平台", "target_audience_platforms", "array", "受众平台画像", "找到目标用户所在平台"],
        ["平台", "recommended_execution_platforms", "array", "适配引擎", "选择实际行动平台"],
        ["平台", "product_destination", "url/object", "产品能力中心", "最终承接终点"],
        ["平台", "platform_heat / growth / saturation", "object", "平台内归一化", "比较传播势能和内容拥挤度"],
        ["平台", "format_fit / link_ability", "object", "平台能力库", "适配内容形式和外链能力"],
    ], [1300, 2350, 1400, 2050, 2260], 8.1)

    doc.add_heading("17.4 窗口风险与系统初步信号", level=2)
    add_table(doc, ["模块", "字段", "类型", "来源/计算", "业务用途"], [
        ["窗口", "attention_window_end", "datetime", "热度曲线/日程", "公众注意力预计结束"],
        ["窗口", "content_window_end", "datetime", "生命周期＋饱和度", "内容仍有新增价值的截止时间"],
        ["窗口", "product_window_end", "datetime", "事件结果和市场状态", "用户仍可执行产品行为的时间"],
        ["窗口", "long_tail_window", "range", "搜索与历史事件", "结果、解释和复盘需求"],
        ["窗口", "production_sla / approval_sla", "duration", "模板与审核规则", "计算实际可用窗口"],
        ["窗口", "remaining_action_window", "duration", "窗口减去SLA", "决定完整版、最小动作或放弃"],
        ["风险", "fact_risk", "enum", "证据完整度", "误报和事实变化风险"],
        ["风险", "brand / legal / region risk", "enum/array", "规则库＋人工", "审批与禁区"],
        ["风险", "platform / account risk", "enum", "平台和账号规则", "账号处罚和限流风险"],
        ["风险", "risk_triggers / mitigations", "array", "规则＋人工", "触发暂停、撤回和备选方案"],
        ["风险", "risk_owner / approver", "user", "权限规则", "明确审批责任"],
        ["系统信号", "card_completeness", "number", "字段完整度", "判断是否可进入Opportunity"],
        ["系统信号", "blocking_gaps", "array", "规则", "列出缺失事实、受众、窗口或产品信息"],
        ["系统信号", "suggested_watchpoints", "array", "模型/规则", "提示需要继续观察的变量"],
        ["系统信号", "overall_confidence", "number", "各模块置信度", "辅助人工判断，不替代决策"],
        ["系统信号", "human_override", "object", "人工操作", "保存修正值、理由和审计"],
    ], [1300, 2350, 1400, 2050, 2260], 8.1)

    doc.add_heading("18. 决策与行动对象字段字典", level=1)
    doc.add_heading("18.1 Opportunity Card字段", level=2)
    add_table(doc, ["字段", "类型", "必填/MVP", "来源或生成方式", "业务用途"], [
        ["opportunity_id / event_ids", "string/array", "必填/P0", "系统＋人工", "机会唯一标识及关联事件"],
        ["decision", "enum", "必填/P0", "人工", "参与、观察或拒绝"],
        ["decision_reason", "text", "必填/P0", "人工＋系统建议", "可解释业务判断"],
        ["decision_at / owner", "datetime/user", "必填/P0", "系统记录", "责任与审计"],
        ["valid_until / review_at", "datetime", "条件/P0", "人工/窗口", "结论过期和复查"],
        ["review_triggers", "array", "可选/P0", "人工/规则", "新事实、热度、产品或风险变化时重判"],
        ["predx_relevance", "score+evidence", "必填/P0", "系统＋人工", "产品、用户、品牌和长期叙事相关性"],
        ["growth_value", "score+evidence", "必填/P0", "目标与历史效果", "曝光、拉新、激活、留存或合作价值"],
        ["participation_qualification", "score+evidence", "必填/P0", "数据/产品/专家资产", "判断是否具备独特参与资格"],
        ["platform_audience_fit", "score+evidence", "必填/P0", "Event Card＋平台库", "目标用户与执行平台适配"],
        ["product_fit", "score+evidence", "必填/P0", "产品能力库", "事件与产品的天然关联"],
        ["product_readiness", "score+evidence", "必填/P0", "产品状态", "市场、页面、推荐和提醒是否就绪"],
        ["time_resource_fit", "score+evidence", "必填/P0", "窗口与SLA", "能否在窗口内完成"],
        ["risk_result / veto", "object", "必填/P0", "风险规则＋审批", "风险等级、否决条件和控制措施"],
        ["primary_goal", "enum", "必填/P0", "人工", "曝光、拉新、激活或留存"],
        ["secondary_goals / weights", "object", "可选/P0", "人工", "多目标组合与权重"],
        ["target_audiences", "array", "必填/P0", "Event Card＋人工", "明确行动服务人群"],
        ["desired_user_actions", "array", "必填/P0", "目标配置", "关注、点击、注册、首次预测或再次参与"],
        ["goal_guardrails", "array", "可选/P0", "人工/风险规则", "不得为曝光牺牲的品牌、成本或质量底线"],
        ["recommended_modes", "array", "可选/P0", "适配引擎", "参与方式和产品承接模式"],
        ["recommended_platforms", "array", "可选/P0", "平台适配", "建议执行平台及理由"],
        ["resource_budget", "object", "可选/P1", "人工", "人力、制作、KOL和活动预算"],
        ["success_conditions", "array", "必填/P0", "目标与指标", "进入执行和复盘的判断依据"],
    ], [1750, 1050, 1300, 2750, 2510], 8.1)

    doc.add_heading("18.2 Action Package字段", level=2)
    add_table(doc, ["字段", "类型", "必填/MVP", "来源或生成方式", "业务用途"], [
        ["action_package_id", "string", "必填/P0", "系统生成", "统一行动任务包ID"],
        ["opportunity_id / event_ids", "string/array", "必填/P0", "对象关联", "继承事件与机会上下文"],
        ["version / status / valid_until", "object", "必填/P0", "系统＋人工", "草稿、批准、执行、暂停和过期控制"],
        ["owner / participants", "user/array", "必填/P0", "人工", "跨团队责任"],
        ["primary_goal / secondary_goals", "object", "必填/P0", "Opportunity继承", "统一业务目标"],
        ["goal_weights / KPIs / guardrails", "object", "必填/P0", "目标配置", "适配、执行和复盘标准"],
        ["target_audiences", "array", "必填/P0", "Opportunity继承", "统一受众"],
        ["confirmed_facts", "array", "必填/P0", "Event Card快照", "所有系统共同事实基础"],
        ["unconfirmed_points", "array", "可选/P0", "Event Card快照", "不可当事实传播"],
        ["evidence_snapshot / updated_at", "object", "必填/P0", "系统快照", "防止执行期事实漂移"],
        ["core_narrative", "text", "必填/P0", "内容策略＋人工", "统一核心判断"],
        ["optional_angles", "array", "可选/P0", "系统建议＋人工", "允许渠道差异化表达"],
        ["must_say / must_not_say", "array", "必填/P0", "品牌/事实/风险", "规定表达边界"],
        ["tone / brand_guidance", "object", "可选/P0", "品牌规则", "语气、人格和敏感表达"],
        ["participation_modes", "array", "必填/P0", "Opportunity", "信息、观点、预测、互动、产品或风险动作"],
        ["channel_actions", "array", "必填/P0", "行动设计器", "各渠道任务及目标分工"],
        ["product_actions", "array", "条件必填/P0", "产品适配", "市场、专题、推荐、Push或提醒任务"],
        ["product_destination / CTA", "object", "条件必填/P0", "产品能力中心", "最终承接入口和用户行为"],
        ["tracking_parameters", "object", "必填/P0", "系统生成", "UTM、campaign和统一追踪ID"],
        ["priority / deadline / sequence", "object", "必填/P0", "窗口与人工", "执行优先级、最晚时间和顺序"],
        ["dependencies", "array", "可选/P0", "任务编排", "事实、素材、产品和审核前置条件"],
        ["approval_route / risk_level", "object", "必填/P0", "风险规则", "审核人和SLA"],
        ["stop_conditions", "array", "必填/P0", "风险与事实规则", "何时暂停、撤回或放弃"],
        ["fallback_plan", "object", "可选/P0", "人工", "产品不可用、窗口缩短或风险升级的备选动作"],
        ["return_schema", "object", "必填/P0", "接口规范", "要求执行系统回传哪些字段"],
    ], [1750, 1050, 1300, 2750, 2510], 8.0)

    doc.add_heading("19. 执行、发布与效果字段字典", level=1)
    doc.add_heading("19.1 Execution Task字段", level=2)
    add_table(doc, ["字段", "类型", "必填/MVP", "来源或生成方式", "业务用途"], [
        ["task_id / task_type", "string/enum", "必填/P0", "系统生成/模板", "任务唯一标识和内容、产品、活动、风控、数据分类"],
        ["package_id / event_id / opportunity_id", "string", "必填/P0", "对象继承", "全链路追踪"],
        ["target_system / platform", "enum", "必填/P0", "行动包", "X矩阵、Predx产品或其他系统"],
        ["account_constraints", "object", "可选/P0", "行动包/账号库", "账号目标、受众、风险和排除条件"],
        ["task_goal / audience", "object", "必填/P0", "行动包继承", "执行系统理解任务目的"],
        ["input_brief / assets", "object", "必填/P0", "行动包＋素材", "事实、角度、CTA和素材输入"],
        ["assignee / owner", "user/system", "必填/P0", "路由＋人工", "执行责任"],
        ["priority / deadline / SLA", "object", "必填/P0", "行动包", "窗口内执行"],
        ["dependencies", "array", "可选/P0", "任务编排", "前置事实、产品、素材或审批"],
        ["status", "enum", "必填/P0", "状态机", "待接受、生产、审核、批准、执行、回传及异常"],
        ["acceptance / rejection_reason", "object", "条件/P0", "接收系统", "判断执行能力与重新路由"],
        ["draft_versions", "array", "可选/P1", "执行系统", "保留主要版本和反馈"],
        ["approver / approval_at", "user/datetime", "条件/P0", "审核流程", "发布权限与审计"],
        ["executed_at", "datetime", "条件/P0", "执行系统", "实际发布时间/上线时间"],
        ["final_output / publication_ids", "object", "条件/P0", "执行系统回传", "最终文案、素材、链接和发布对象"],
        ["failure / pause / cancel reason", "object", "条件/P0", "人工/系统", "异常诊断和复盘"],
        ["cost", "object", "可选/P0", "人工/系统", "人力、制作、KOL、活动和工具成本"],
    ], [1750, 1050, 1300, 2750, 2510], 8.1)

    doc.add_heading("19.2 Publication与Product Action字段", level=2)
    add_table(doc, ["对象", "字段", "类型", "来源/生成", "用途"], [
        ["Publication", "publication_id / task_id", "string", "系统/渠道回传", "唯一发布记录与任务关联"],
        ["Publication", "platform / account_id", "enum/string", "渠道回传", "平台与账号贡献分析"],
        ["Publication", "content_type / final_text / media", "object", "渠道回传", "保留最终实际执行内容"],
        ["Publication", "published_at / url", "datetime/url", "渠道回传", "监控、点击和事实更新"],
        ["Publication", "tracking_ids / UTM", "object", "系统生成", "连接平台点击与产品行为"],
        ["Publication", "edit / correction / withdrawal history", "array", "渠道回传＋人工", "事实变化与风险审计"],
        ["Product Action", "product_action_id / task_id", "string", "系统/产品回传", "产品动作唯一记录"],
        ["Product Action", "action_type", "enum", "任务模板", "关联市场、新建市场、专题、推荐、Push、提醒或活动"],
        ["Product Action", "market/page/campaign_id", "string", "产品系统", "实际承接对象"],
        ["Product Action", "availability / region limits", "object", "产品系统", "判断用户是否可用"],
        ["Product Action", "online_at / offline_at", "datetime", "产品系统", "承接窗口和归因"],
        ["Product Action", "destination_url / CTA", "object", "产品系统", "用户路径"],
        ["Product Action", "status / failure_reason", "object", "产品系统", "上线状态与异常处理"],
    ], [1450, 2350, 1400, 2000, 2160], 8.2)

    doc.add_heading("19.3 Performance与Review字段", level=2)
    add_table(doc, ["类别", "字段", "类型", "来源/计算", "用途"], [
        ["平台效果", "impressions / reach / views", "number", "平台回传", "曝光与有效触达"],
        ["平台效果", "likes / comments / shares / saves", "number", "平台回传", "互动结构与传播质量"],
        ["平台效果", "link_clicks / CTR", "number", "平台＋追踪", "从内容到产品的兴趣"],
        ["平台效果", "target_audience_reach", "number", "平台画像/估算", "目标人群覆盖"],
        ["平台效果", "sentiment / discussion_quality", "object", "舆情分析＋抽样", "公众反馈和观点质量"],
        ["产品漏斗", "landing_visits", "number", "产品埋点", "产品入口访问"],
        ["产品漏斗", "registrations / registration_rate", "number", "产品埋点", "拉新效果"],
        ["产品漏斗", "first_prediction / activation_rate", "number", "产品埋点", "首次激活"],
        ["产品漏斗", "repeat_visit / repeat_prediction", "number", "产品埋点", "留存和持续参与"],
        ["产品漏斗", "reminder_open / related_market_action", "number", "Push/产品", "结果与相关事件承接"],
        ["成本", "labor / content / KOL / activity / tool cost", "object", "人工＋系统", "总成本和单位经济性"],
        ["归因", "attribution_type", "enum", "规则", "直接、时间窗口贡献或实验"],
        ["归因", "attribution_window / touchpoints", "object", "规则＋事件流", "记录归因时间与触点"],
        ["归因", "baseline / control_group", "object", "历史/实验", "估算增量而非只看总量"],
        ["结果", "goal_result / ROI", "object", "目标权重＋成本", "评价主目标和经济性"],
        ["风险", "errors / complaints / penalties / withdrawals", "object", "监控＋人工", "风险护栏"],
        ["复盘", "discovery / understanding / decision findings", "text", "人工复盘", "定位发现、事件和机会问题"],
        ["复盘", "action / execution / funnel findings", "text", "人工＋漏斗诊断", "定位动作、渠道和产品问题"],
        ["复盘", "continue / stop / experiment", "array", "人工", "形成明确下一步"],
        ["复盘", "rule_updates", "array", "人工确认", "更新来源、判断、渠道、模板、产品和风险规则"],
        ["复盘", "review_owner / completed_at", "user/datetime", "系统记录", "复盘责任和完成度"],
    ], [1450, 2350, 1400, 2000, 2160], 8.0)

    doc.add_heading("20. 配置对象字段", level=1)
    add_table(doc, ["配置对象", "关键字段", "维护者", "被哪些模块使用"], [
        ["数据源档案", "source_id、类型、平台、地区、语言、可信等级、刷新频率、认证、成本、健康状态、白名单/黑名单", "数据/运营管理员", "热点输入、事实证据、异常提醒"],
        ["主题与实体库", "topic_id、层级、关键词、别名、实体关系、排除词、负责人、风险标签", "热点运营/研究", "采集、聚类、检索、路由"],
        ["长期议题库", "母题、子议题、实体、立场、触发器、历史基线、常青资产", "研究/内容策略", "热点输入、事件关联、内容准备"],
        ["周期模板", "周期规则、提前量、来源、结果分支、准备动作、历史表现", "热点运营", "Future Event自动生成"],
        ["平台能力档案", "用户画像、内容形式、传播机制、热点寿命、外链、转化、地区语言、风险", "渠道Owner", "平台判断和行动适配"],
        ["受众标签库", "受众ID、地区语言、兴趣、社区、动机、知识水平、产品阶段、敏感属性限制", "增长/数据", "Event Card和目标适配"],
        ["账号能力摘要", "账号ID、目标、受众、人格、内容能力、风险、状态、历史表现", "X矩阵系统", "X任务约束和路由建议"],
        ["产品能力档案", "市场/页面/推荐/Push/Watchlist/活动能力、地区限制、负责人、最短准备时间、状态", "产品运营", "Product Fit与Readiness、行动设计"],
        ["行动模板", "适用事件、生命周期、目标、受众、渠道动作、产品动作、SLA、KPI和停止条件", "热点/增长运营", "行动设计器和最小有效动作"],
        ["风险与审核规则", "风险类型、等级、触发条件、审核人、SLA、禁区、暂停/撤回/更正规则", "品牌/法务/风控", "Opportunity、行动包、执行监控"],
        ["通知规则", "触发器、阈值、对象、渠道、频率、升级路径、静默时间", "产品管理员", "未来准备、异常、超时和风险提醒"],
    ], [1800, 4600, 1450, 1510], 8.1)

    doc.add_heading("21. 字段来源、权限与页面映射", level=1)
    doc.add_heading("21.1 字段生成与修改规则", level=2)
    add_table(doc, ["字段类型", "默认生成方式", "修改规则", "必须保留"], [
        ["原始字段", "外部API、采集器或内部系统", "不可覆盖原值；可补充规范化值", "原文、原始时间、来源、采集时间"],
        ["系统计算字段", "规则、统计或模型", "允许重新计算；显示算法版本", "当前值、历史值、计算时间、算法版本"],
        ["模型判断字段", "分类、摘要、聚类、受众或生命周期模型", "人工可修正", "模型原值、置信度、依据、修正值和理由"],
        ["人工判断字段", "运营、品牌、产品或渠道负责人", "按权限修改", "操作者、时间、理由和审批记录"],
        ["外部执行回传", "X矩阵、Predx产品或其他渠道", "来源系统负责；本系统不可静默改写", "来源系统、回传时间、失败与重试记录"],
    ], [1650, 2700, 2400, 2610], 8.4)

    doc.add_heading("21.2 核心页面字段映射", level=2)
    add_table(doc, ["页面", "主要读取对象", "必须展示/编辑字段"], [
        ["实时雷达", "Source Signal", "来源、平台、发布时间、正文摘要、互动、增速、实体、去重/聚类、风险和处理状态"],
        ["未来事件", "Future Event", "时间类型、确认状态、证据、结果分支、市场映射、准备节点、Owner和下一次核验"],
        ["事件详情", "Trend Event＋Event Card", "八大模块、来源时间线、主子事件、关联机会和行动记录"],
        ["合并拆分工作台", "Signal＋Cluster＋Event", "相似信号、实体动作时间、置信度、目标事件和操作影响"],
        ["Opportunity判断", "Event Card＋Opportunity", "七维判断、证据、否决项、目标、受众、平台、产品、窗口、风险和结论"],
        ["行动设计器", "Opportunity＋Action Package", "目标权重、事实、叙事、渠道/产品动作、依赖、SLA、审核、CTA、追踪和回传"],
        ["执行任务", "Execution Task＋Publication/Product Action", "接收状态、负责人、截止、输入、审核、最终输出、链接、异常和成本"],
        ["效果复盘", "Performance＋Review", "平台指标、产品漏斗、成本、归因、风险、诊断和四项复盘结论"],
    ], [1800, 2400, 5160], 8.3)

    doc.add_heading("21.3 对象进入下一阶段的字段门槛", level=2)
    add_table(doc, ["阶段转换", "最低字段条件"], [
        ["Signal → Event候选", "至少包含来源、原文/内容、发布时间、实体或主题；去重完成；聚类有结果或人工指定"],
        ["Future Event → 准备中", "时间类型、确认状态、主证据、Owner、下一核验时间和至少一个准备节点完整"],
        ["Event → Opportunity", "事件身份、确认事实、当前热度、生命周期、受众/平台初判、剩余窗口和风险完整；阻塞项已处理"],
        ["Opportunity → Action Package", "参与结论、理由、主目标、目标受众、产品模式、风险结果、负责人和有效期完整"],
        ["Action Package → 执行", "统一事实、必说禁说、渠道/产品任务、截止时间、审核路径、停止条件和追踪参数完整"],
        ["Task → 发布/上线", "最终内容/产品对象、批准记录、目标链接、追踪ID和风险检查完成"],
        ["执行完成 → 复盘", "最终链接/对象、平台指标、产品漏斗、成本和异常至少达到数据完整度阈值"],
    ], [2700, 6660], 8.5)

    callout(doc, "更新后的交付边界", "PRD v1.2已覆盖模块、功能、字段、规则、状态、权限和页面映射，并已修复全部列表内容。下一步原型设计应直接使用本字段字典确定列表列项、详情页区块、表单字段和校验门槛。", PALE_GREEN, GREEN)

    doc.save(DOCX)
    return DOCX


if __name__ == "__main__":
    print(build_document())
