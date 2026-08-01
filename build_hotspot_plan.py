from pathlib import Path
from math import atan2, cos, sin, pi
from PIL import Image, ImageDraw, ImageFont
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


ROOT = Path("/Users/rachelyuan/Documents/热点监控")
OUT = ROOT / "output"
ASSET = OUT / "assets"
DOCX = OUT / "Predx热点运营系统建设方案_v2.0.docx"
OUT.mkdir(exist_ok=True)
ASSET.mkdir(exist_ok=True)

FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
FONT = "Arial Unicode MS"
NAVY = "0B2545"
BLUE = "2E74B5"
TEAL = "0F8B8D"
ORANGE = "E07A2D"
GREEN = "3A7D44"
PURPLE = "6B5CA5"
RED = "B04444"
GRAY = "5B6573"
LIGHT = "F2F4F7"
PALE_BLUE = "EAF2F8"
PALE_TEAL = "E9F6F5"
PALE_ORANGE = "FFF3E8"
PALE_GREEN = "EDF6EE"
PALE_PURPLE = "F1EFF8"
WHITE = "FFFFFF"
BLACK = "111111"


def font(size, bold=False):
    return ImageFont.truetype(FONT_PATH, size=size)


def wrapped(draw, text, fnt, max_width):
    lines = []
    for raw in text.split("\n"):
        if not raw:
            lines.append("")
            continue
        cur = ""
        for ch in raw:
            trial = cur + ch
            if draw.textbbox((0, 0), trial, font=fnt)[2] <= max_width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = ch
        if cur:
            lines.append(cur)
    return lines


def round_box(draw, box, fill, outline, title, body="", title_size=34, body_size=24, radius=24):
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=3)
    tf = font(title_size, True)
    bf = font(body_size)
    title_lines = wrapped(draw, title, tf, x2 - x1 - 38)
    body_lines = wrapped(draw, body, bf, x2 - x1 - 38) if body else []
    title_h = len(title_lines) * (title_size + 8)
    body_h = len(body_lines) * (body_size + 7)
    total = title_h + (12 if body_lines else 0) + body_h
    y = y1 + (y2 - y1 - total) / 2
    for line in title_lines:
        bb = draw.textbbox((0, 0), line, font=tf)
        draw.text(((x1 + x2 - (bb[2] - bb[0])) / 2, y), line, font=tf, fill="#111111")
        y += title_size + 8
    if body_lines:
        y += 8
        for line in body_lines:
            bb = draw.textbbox((0, 0), line, font=bf)
            draw.text(((x1 + x2 - (bb[2] - bb[0])) / 2, y), line, font=bf, fill="#4B5563")
            y += body_size + 7


def arrow(draw, start, end, color="#64748B", width=5):
    x1, y1 = start
    x2, y2 = end
    draw.line((x1, y1, x2, y2), fill=color, width=width)
    angle = atan2(y2 - y1, x2 - x1)
    length = 20
    spread = pi / 7
    p1 = (x2 - length * cos(angle - spread), y2 - length * sin(angle - spread))
    p2 = (x2 - length * cos(angle + spread), y2 - length * sin(angle + spread))
    draw.polygon([(x2, y2), p1, p2], fill=color)


def diagram_title(draw, title, subtitle, width):
    tf = font(48, True)
    sf = font(26)
    draw.text((70, 52), title, font=tf, fill="#0B2545")
    draw.text((70, 116), subtitle, font=sf, fill="#5B6573")
    draw.line((70, 158, width - 70, 158), fill="#D7DEE8", width=3)


def build_overall_diagram(path):
    W, H = 1800, 2500
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    diagram_title(d, "Predx 热点运营系统整体架构", "从热点进入、事件理解到跨系统执行与学习闭环", W)
    layers = [
        ("1  热点输入", "实时突发｜未来事件｜周期热点｜结构性议题｜内部与自造热点", "#EAF2F8", "#2E74B5"),
        ("2  事件化处理", "标准化 → 去重 → 聚类 → 人工合并/拆分 → 统一 Trend Event", "#EDF6EE", "#3A7D44"),
        ("3  Event Card", "事件身份｜事实证据｜传播热度｜生命周期｜受众｜平台｜窗口风险｜初步信号", "#FFF3E8", "#E07A2D"),
        ("4  Opportunity 判断", "相关性｜业务价值｜平台与受众适配｜产品承接｜参与资格｜资源与风险", "#F1EFF8", "#6B5CA5"),
        ("5  行动设计", "目标架构 → 目标-渠道-动作适配 → 统一行动任务包", "#E9F6F5", "#0F8B8D"),
        ("6  专业执行", "X 矩阵｜Predx 产品｜内容视频｜营销活动｜社区/KOL/PR｜品牌风控", "#EAF2F8", "#2E74B5"),
        ("7  审核与发布", "确认事实、边界与风险 → 各执行系统发布/上线 → 异常处置", "#FFF3E8", "#E07A2D"),
        ("8  追踪与复盘", "曝光互动 → 点击注册 → 激活留存 → 成本 ROI → 规则与策略更新", "#EDF6EE", "#3A7D44"),
    ]
    x1, x2 = 160, 1640
    y = 210
    h = 215
    gap = 72
    centers = []
    for title, body, fill, outline in layers:
        round_box(d, (x1, y, x2, y + h), fill, outline, title, body, 36, 26)
        centers.append((900, y, y + h))
        y += h + gap
    for i in range(len(centers) - 1):
        arrow(d, (900, centers[i][2] + 4), (900, centers[i + 1][1] - 8), "#758195", 6)
    # feedback loop
    d.line((1500, centers[-1][2] - 30, 1700, centers[-1][2] - 30, 1700, centers[0][1] + 55, 1645, centers[0][1] + 55),
           fill="#6B5CA5", width=5)
    arrow(d, (1645, centers[0][1] + 55), (1640, centers[0][1] + 55), "#6B5CA5", 5)
    rf = font(24, True)
    d.text((1515, 1180), "学习反馈", font=rf, fill="#6B5CA5")
    im.save(path, quality=95)


def build_source_relation_diagram(path):
    W, H = 1900, 1740
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    diagram_title(d, "五类热点输入及相互关系", "每类热点有独立入口；周期、长期和内部热点会转化为未来事件或实时热点", W)

    # Top row: long-term / cyclical / internal sources.
    round_box(d, (90, 240, 550, 500), "#F1EFF8", "#6B5CA5",
              "长期结构性议题", "行业母题、社会议题\n用户兴趣、历史内容", 34, 25)
    round_box(d, (720, 240, 1180, 500), "#EDF6EE", "#3A7D44",
              "周期性热点", "赛事、财报、经济数据\n节日、年度事件", 34, 25)
    round_box(d, (1350, 240, 1810, 500), "#E9F6F5", "#0F8B8D",
              "内部与自造热点", "Predx 数据、用户行为\n产品事件、主动策划", 34, 25)

    # Middle row: future events. The cyclical template generates future events.
    round_box(d, (610, 705, 1290, 970), "#EAF2F8", "#2E74B5",
              "可预见未来事件", "公共/行业日历、预测市场、新闻预告\n周期模板、产品日历、人工录入", 39, 27)
    arrow(d, (950, 500), (950, 705), "#3A7D44", 6)
    lf = font(25, True)
    d.text((1010, 580), "周期模板生成下一期", font=lf, fill="#3A7D44")

    # Real-time is the convergence point for activated topics.
    round_box(d, (610, 1145, 1290, 1405), "#FFF3E8", "#E07A2D",
              "实时突发热点", "热榜、新闻、官方账号、社区\n以及被新进展激活的其他四类热点", 39, 27)
    arrow(d, (610, 875), (465, 875), "#6B5CA5", 5)
    d.line((465, 875, 465, 1095, 610, 1230), fill="#6B5CA5", width=5)
    arrow(d, (465, 1095), (610, 1230), "#6B5CA5", 5)
    d.text((105, 850), "新事件激活长期母题", font=lf, fill="#6B5CA5")
    arrow(d, (1290, 875), (1435, 875), "#0F8B8D", 5)
    d.line((1435, 875, 1435, 1095, 1290, 1230), fill="#0F8B8D", width=5)
    arrow(d, (1435, 1095), (1290, 1230), "#0F8B8D", 5)
    d.text((1460, 850), "外部传播形成热点", font=lf, fill="#0F8B8D")
    arrow(d, (950, 970), (950, 1145), "#2E74B5", 6)
    d.text((1015, 1035), "进入发生窗口", font=lf, fill="#2E74B5")

    round_box(d, (610, 1510, 1290, 1685), "#EAF2F8", "#0B2545",
              "统一候选事件池", "五类入口均可直接进入；统一标准化、去重与聚类", 38, 25)
    arrow(d, (950, 1405), (950, 1510), "#758195", 6)
    im.save(path, quality=95)


def build_future_event_diagram(path):
    W, H = 1900, 1220
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    diagram_title(d, "Future Event Center：来源、事件与承接", "保持事件对象产品中立，再按不同业务需要生成预测问题和行动", W)
    sources = [
        (90, 240, 570, 470, "#EAF2F8", "#2E74B5", "通用公共事件源", "官方日历、新闻预告、搜索需求\n节假日与重大公共事件"),
        (710, 240, 1190, 470, "#EDF6EE", "#3A7D44", "行业垂直事件源", "政治、金融、体育、科技\n娱乐、医疗等专业日历"),
        (1330, 240, 1810, 470, "#E9F6F5", "#0F8B8D", "产品专属事件源", "预测市场、内部数据\n产品路线图与业务日历"),
    ]
    for x1, y1, x2, y2, fill, out, title, body in sources:
        round_box(d, (x1, y1, x2, y2), fill, out, title, body, 33, 23)
        arrow(d, ((x1+x2)//2, y2), (950, 585), out, 5)
    round_box(d, (610, 585, 1290, 805), "#FFF3E8", "#E07A2D", "Future Event", "时间、确认状态、结果分支、证据与准备倒计时", 42, 27)
    actions = [
        (55, 950, 350, 1145, "Prediction\nQuestion"),
        (420, 950, 715, 1145, "Content\nAction"),
        (785, 950, 1080, 1145, "Product\nAction"),
        (1150, 950, 1445, 1145, "Campaign\nAction"),
        (1515, 950, 1810, 1145, "Risk\nAction"),
    ]
    for i, (x1, y1, x2, y2, text) in enumerate(actions):
        fills = ["#F1EFF8", "#EAF2F8", "#E9F6F5", "#EDF6EE", "#FFF0F0"]
        outlines = ["#6B5CA5", "#2E74B5", "#0F8B8D", "#3A7D44", "#B04444"]
        round_box(d, (x1, y1, x2, y2), fills[i], outlines[i], text, "", 30, 22)
        arrow(d, (950, 805), ((x1+x2)//2, y1), outlines[i], 4)
    im.save(path, quality=95)


def hexrgb(s):
    return RGBColor.from_string(s)


def set_run(run, size=10.5, bold=False, color=BLACK, italic=False, font_name=FONT):
    run.font.name = font_name
    run._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), font_name)
    run._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), font_name)
    run._element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), font_name)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = hexrgb(color)


def set_cell_shading(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = tcPr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tcPr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_margins(cell, top=90, start=120, bottom=90, end=120):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = tcPr.first_child_found_in("w:tcMar")
    if tcMar is None:
        tcMar = OxmlElement("w:tcMar")
        tcPr.append(tcMar)
    for m, val in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tcMar.find(qn(f"w:{m}"))
        if node is None:
            node = OxmlElement(f"w:{m}")
            tcMar.append(node)
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")


def set_table_widths(table, widths):
    table.autofit = False
    tblPr = table._tbl.tblPr
    tblW = tblPr.find(qn("w:tblW"))
    if tblW is None:
        tblW = OxmlElement("w:tblW")
        tblPr.append(tblW)
    total = sum(widths)
    tblW.set(qn("w:w"), str(total))
    tblW.set(qn("w:type"), "dxa")
    tblInd = tblPr.find(qn("w:tblInd"))
    if tblInd is None:
        tblInd = OxmlElement("w:tblInd")
        tblPr.append(tblInd)
    tblInd.set(qn("w:w"), "120")
    tblInd.set(qn("w:type"), "dxa")
    grid = table._tbl.tblGrid
    for child in list(grid):
        grid.remove(child)
    for w in widths:
        gc = OxmlElement("w:gridCol")
        gc.set(qn("w:w"), str(w))
        grid.append(gc)
    for row in table.rows:
        for i, cell in enumerate(row.cells):
            tcPr = cell._tc.get_or_add_tcPr()
            tcW = tcPr.find(qn("w:tcW"))
            if tcW is None:
                tcW = OxmlElement("w:tcW")
                tcPr.append(tcW)
            tcW.set(qn("w:w"), str(widths[min(i, len(widths)-1)]))
            tcW.set(qn("w:type"), "dxa")
            set_cell_margins(cell)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER


def add_table(doc, headers, rows, widths):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    hdr = table.rows[0].cells
    for i, text in enumerate(headers):
        hdr[i].text = text
        set_cell_shading(hdr[i], LIGHT)
        p = hdr[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        for r in p.runs:
            set_run(r, 9.2, True, NAVY)
    for row in rows:
        cells = table.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = str(val)
            p = cells[i].paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.05
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if i > 0 else WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                set_run(r, 9.0, False, BLACK)
    set_table_widths(table, widths)
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = Pt(1)
    r = p.add_run("\u200b")
    set_run(r, 1, False, WHITE)
    return table


def add_p(doc, text="", bold_lead=None, after=6, size=10.5, color=BLACK, italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.line_spacing = 1.1
    if bold_lead and text.startswith(bold_lead):
        r1 = p.add_run(bold_lead)
        set_run(r1, size, True, color)
        r2 = p.add_run(text[len(bold_lead):])
        set_run(r2, size, False, color, italic)
    else:
        r = p.add_run(text)
        set_run(r, size, False, color, italic)
    return p


def add_bullets(doc, items, level=0):
    for item in items:
        p = doc.add_paragraph(style="List Bullet" if level == 0 else "List Bullet 2")
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.08
        for r in p.runs:
            set_run(r, 10.2, False, BLACK)


def add_numbers(doc, items):
    for item in items:
        p = doc.add_paragraph(style="List Number")
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.08
        for r in p.runs:
            set_run(r, 10.2, False, BLACK)


def add_callout(doc, label, text, fill=PALE_BLUE, accent=BLUE):
    t = doc.add_table(rows=1, cols=1)
    t.style = "Table Grid"
    set_table_widths(t, [9360])
    c = t.cell(0, 0)
    set_cell_shading(c, fill)
    p = c.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(f"{label}  ")
    set_run(r, 10.5, True, accent)
    r = p.add_run(text)
    set_run(r, 10.5, False, NAVY)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def add_picture(doc, path, caption, width=6.35):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(str(path), width=Inches(width))
    cp = doc.add_paragraph()
    cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cp.paragraph_format.space_before = Pt(2)
    cp.paragraph_format.space_after = Pt(8)
    r = cp.add_run(caption)
    set_run(r, 9, False, GRAY, italic=True)


def style_doc(doc):
    sec = doc.sections[0]
    sec.top_margin = Inches(0.8)
    sec.bottom_margin = Inches(0.75)
    sec.left_margin = Inches(0.85)
    sec.right_margin = Inches(0.85)
    sec.header_distance = Inches(0.35)
    sec.footer_distance = Inches(0.35)

    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = FONT
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    normal.font.size = Pt(10.5)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.1

    for name, size, color, before, after in [
        ("Heading 1", 16, BLUE, 14, 7),
        ("Heading 2", 13, BLUE, 11, 5),
        ("Heading 3", 11.5, NAVY, 8, 4),
    ]:
        s = styles[name]
        s.font.name = FONT
        s._element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
        s.font.size = Pt(size)
        s.font.bold = True
        s.font.color.rgb = hexrgb(color)
        s.paragraph_format.space_before = Pt(before)
        s.paragraph_format.space_after = Pt(after)
        s.paragraph_format.keep_with_next = True

    for name in ["List Bullet", "List Bullet 2", "List Number"]:
        s = styles[name]
        s.font.name = FONT
        s._element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
        s.font.size = Pt(10.2)

    header = sec.header
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = hp.add_run("Predx Growth System  |  热点运营系统建设方案")
    set_run(r, 8.5, False, GRAY)
    footer = sec.footer
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = fp.add_run("Predx 内部方案  ·  v2.0  ·  2026-07")
    set_run(r, 8.5, False, GRAY)


def add_title_page(doc):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(96)
    p.paragraph_format.space_after = Pt(10)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("PREDX GROWTH SYSTEM")
    set_run(r, 12, True, BLUE)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(8)
    r = p.add_run("热点运营系统建设方案")
    set_run(r, 27, True, NAVY)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(28)
    r = p.add_run("从热点感知、事件理解到跨系统执行与增长复盘")
    set_run(r, 14, False, GRAY)
    add_callout(doc, "核心定位", "以热点事件为基础、以热点机会为决策对象、以统一行动任务包连接内容与产品，并通过执行结果回流持续优化的增长基础系统。", PALE_BLUE, BLUE)
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(38)
    p.paragraph_format.space_after = Pt(4)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("版本 v2.0  |  完整讨论汇总版｜供管理层汇报、MVP 拆解与跨系统对齐")
    set_run(r, 10, False, GRAY)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("2026 年 7 月")
    set_run(r, 10, False, GRAY)
    doc.add_page_break()


def build_document():
    overall = ASSET / "overall_architecture.png"
    relation = ASSET / "hotspot_source_relationship.png"
    future = ASSET / "future_event_center.png"
    build_overall_diagram(overall)
    build_source_relation_diagram(relation)
    build_future_event_diagram(future)

    doc = Document()
    style_doc(doc)
    add_title_page(doc)

    doc.add_heading("执行摘要", level=1)
    add_callout(doc, "一句话结论", "系统不是一个热榜或自动发稿工具，而是一套覆盖热点发现、机会判断、内容与产品承接、跨系统执行、监控归因和复盘学习的注意力经营系统。", PALE_TEAL, TEAL)
    add_p(doc, "终局方案保持大而全，但建设上采用“完整架构、有限主题、有限渠道、单条闭环先验证”的原则。MVP 首先打通热点发现—Event Card—Opportunity—X 矩阵响应—Predx 产品承接—数据回流。")
    add_table(doc, ["设计问题", "方案结论"], [
        ["系统围绕什么组织", "围绕现实世界的热点事件和可执行机会，而非单条帖子。"],
        ["热点从哪里来", "覆盖实时突发、未来事件、周期热点、结构性议题、内部与自造热点。"],
        ["如何决定是否参与", "基于 Event Card，对相关性、价值、平台、受众、产品、窗口和风险进行判断。"],
        ["如何跨系统协同", "使用统一行动任务包定义目标、事实、边界和任务，各专业子系统保留执行主权。"],
        ["如何与产品连接", "根据产品适配度选择内容先行、轻产品联动、产品直连或产品反向造热点。"],
        ["如何形成复利", "统一追踪事件、任务、发布和产品结果，通过复盘更新来源、评分和行动规则。"],
    ], [2200, 7160])
    doc.add_page_break()

    doc.add_heading("1. 建设目标与原则", level=1)
    doc.add_heading("1.1 建设目标", level=2)
    add_bullets(doc, [
        "更早发现：在主流爆发前捕捉萌芽、日历和内部信号。",
        "更准判断：区分“很热”与“值得 Predx 参与”。",
        "更快行动：把机会转化为内容、产品、营销和社区任务。",
        "更强承接：让热点流量进入可观测的产品路径。",
        "更稳治理：在速度之外保留事实、品牌、平台和合规边界。",
        "持续学习：用执行结果更新来源、平台、模板和产品策略。",
    ])
    doc.add_heading("1.2 关键原则", level=2)
    add_table(doc, ["原则", "落地含义"], [
        ["机会优先于内容", "先判断为什么参与，再决定发什么。"],
        ["事件统一、叙事分层", "同一现实事件统一聚合，同时保留不同观点和子事件。"],
        ["母版集中、改编分布", "统一事实与核心叙事，渠道系统完成专业改编。"],
        ["多目标分工", "曝光、拉新、激活、留存由不同渠道按能力承担。"],
        ["人机分层", "机器负责采集、聚类、分析和建议；人负责责任性判断。"],
        ["结果可追溯", "最终结果必须关联事件、机会、任务、平台和产品行为。"],
    ], [2500, 6860])

    doc.add_page_break()
    doc.add_heading("2. 整体架构", level=1)
    add_p(doc, "整体链路按照严格的纵向关系设计：先完成 Event Card，再由下一层读取整张事件卡进行 Opportunity 判断。Event Card 描述客观事件，Opportunity Card 表达 Predx 的业务选择。")
    add_picture(doc, overall, "图 1  Predx 热点运营系统整体架构（调整版）", 5.35)
    add_callout(doc, "对象边界", "Event Card 回答“发生了什么”；Opportunity Card 回答“Predx 为什么以及是否参与”；统一行动任务包回答“各系统分别做什么”。", PALE_ORANGE, ORANGE)

    doc.add_heading("3. 热点输入层", level=1)
    add_p(doc, "热点输入层覆盖五类热点，并为每类热点建立不同的来源与准备机制。五类热点可以相互转化，最终全部汇入统一候选事件池。")
    add_picture(doc, relation, "图 2  五类热点来源及相互关系", 6.25)
    add_table(doc, ["热点类型", "主要来源", "基础建设", "进阶能力"], [
        ["实时突发", "热榜、新闻、官方账号、社区、种子账号", "热榜/RSS 接口、账号库、关键词、事实核验", "跨平台异常检测、传播路径和早期预警"],
        ["未来事件", "公共/行业日历、预测市场、新闻预告、产品日历", "Future Event Center、人工录入、确认状态", "未来时间抽取、结果分支和自动倒计时"],
        ["周期热点", "赛事、财报、经济数据、节日、年度事件", "周期模板和历史案例", "自动生成下一期事件和历史基线"],
        ["结构性议题", "行业研究、社会议题、用户兴趣、历史内容", "母题树、关键词、实体和观点库", "新事件激活、叙事变化和常青资产"],
        ["内部与自造", "概率、交易量、站内搜索、用户行为、主动策划", "内部信号和人工立项入口", "异常检测、预测指数和产品反向造热点"],
    ], [1500, 2350, 2750, 2760])

    doc.add_heading("4. Future Event Center", level=1)
    add_p(doc, "未来事件中心不是普通日历，而是提前结构化未来事件、持续确认状态、生成准备任务，并在临近发生时转入实时雷达的运营中心。预测市场是重要种子来源，但底层 Future Event 保持产品中立。")
    add_picture(doc, future, "图 3  Future Event Center 的来源与承接", 6.25)
    doc.add_heading("4.1 Future Event 的核心信息", level=2)
    add_bullets(doc, [
        "事件身份：标题、主题、主体、地区和语言。",
        "时间：准确日期、时间窗口、条件触发或持续进程。",
        "确认状态：传闻、报道、预期、官方确认、进行中、完成、延期或取消。",
        "证据：主来源、辅助来源、最后核验时间。",
        "结果分支：可能结果、当前概率和关键触发条件。",
        "准备计划：T-30、T-7、T-1、发生时和结果后的动作。",
        "产品准备：是否已有预测市场、专题页、Push 或活动能力。",
    ])
    doc.add_heading("4.2 第一版怎么做", level=2)
    add_numbers(doc, [
        "从 Predx 现有市场反向聚合现实事件，形成 Future Event 种子库。",
        "接入少量官方和行业日历，自动数据进入候选队列，人工确认后入库。",
        "建立 10-20 个周期模板，自动生成下一期事件。",
        "保留人工录入，用于战略、地区、内部和暂定事件。",
        "事件进入发生窗口后自动转入实时热点雷达。",
    ])

    doc.add_heading("5. 事件化处理与 Event Card", level=1)
    doc.add_heading("5.1 从信号到统一事件", level=2)
    add_p(doc, "帖子、新闻、视频、市场和日历记录只是 Source Signal。系统先标准化时间、平台、作者、语言、正文、实体和互动数据，再完成内容去重和事件聚类。")
    add_table(doc, ["步骤", "具体动作", "主要产物"], [
        ["标准化", "统一时间、语言、链接、作者、实体和平台指标", "标准 Source Signal"],
        ["内容去重", "识别相同 URL、转发、转载、同源新闻和搬运", "传播关系与独立来源数"],
        ["事件聚类", "结合主体、动作、时间、地点和语义判断同一事件", "事件候选与叙事簇"],
        ["人工治理", "合并、拆分、设置主事件/子事件、指定权威来源", "Canonical Trend Event"],
    ], [1500, 5200, 2660])
    doc.add_heading("5.2 Event Card 八大模块", level=2)
    add_table(doc, ["模块", "需要回答的问题"], [
        ["1. 事件身份", "谁在何时发生了什么，属于哪类热点，与哪些事件相关。"],
        ["2. 事实与证据", "哪些已确认、哪些未确认，来源是否独立可靠。"],
        ["3. 传播热度", "当前规模、增速、加速度和跨平台扩散情况。"],
        ["4. 生命周期", "处于萌芽、上升、爆发、峰值、回落还是长尾。"],
        ["5. 受众结构", "谁在关注、为什么关注、知识水平和产品意图如何。"],
        ["6. 平台传播", "首发、发酵、目标受众、执行和承接平台分别是什么。"],
        ["7. 窗口与风险", "注意力、内容、产品窗口还剩多久，风险是否可控。"],
        ["8. 系统初步信号", "信息是否足够进入机会判断，需要观察哪些方向。"],
    ], [2350, 7010])
    doc.add_heading("5.3 分析方法", level=2)
    add_bullets(doc, [
        "生命周期：结合规模、增速、加速度、跨平台扩散和内容饱和度判断，并显示置信度。",
        "受众：区分已观察受众、潜在兴趣受众和 Predx 目标受众，重点分析兴趣、社区、语言、地区和参与动机。",
        "窗口：分别估算注意力窗口、内容窗口、产品窗口和长尾窗口；剩余窗口需扣除生产、审批和发布耗时。",
        "平台：先做平台内标准化，再比较传播势能、受众重合、内容形式、产品意图和饱和度。",
    ])
    add_callout(doc, "MVP", "自动采集来源和互动；模型生成摘要、聚类、生命周期和受众建议；人工确认事件边界、事实、风险和是否进入机会判断。", PALE_TEAL, TEAL)

    doc.add_heading("6. Opportunity 判断与承接策略", level=1)
    add_p(doc, "Opportunity 判断位于完整 Event Card 之后。它读取事件卡全部信息，再结合 Predx 的产品、品牌和资源条件，决定参与、观察或拒绝。")
    add_table(doc, ["判断维度", "核心问题"], [
        ["Predx 相关性", "与产品、用户、品牌、市场和长期叙事是否相关。"],
        ["增长价值", "能否带来有效触达、拉新、激活、留存或合作价值。"],
        ["参与资格", "是否拥有数据、产品、专家或独特观点。"],
        ["平台与受众", "讨论在哪里、目标用户在哪里、在哪执行最有效。"],
        ["产品承接", "是否已有市场、专题页、Push 或活动能力。"],
        ["时间与资源", "剩余窗口是否足以完成关键动作。"],
        ["风险", "事实、品牌、法律、平台和地区风险是否可控。"],
    ], [2200, 7160])
    doc.add_heading("6.1 平台角色", level=2)
    add_p(doc, "必须区分首发平台、发酵平台、目标受众平台、执行平台和产品承接终点。哪里最热，不一定就是最适合转化的平台。")
    doc.add_heading("6.2 参与方式", level=2)
    add_bullets(doc, [
        "信息：摘要、时间线、FAQ、事实核验和多方观点。",
        "观点：支持、反对、补充、条件性或反常识角度。",
        "预测与数据：概率、情景、关键变量、舆论与市场分歧。",
        "互动与娱乐：投票、竞猜、AMA、Meme 和视频。",
        "产品与活动：预测市场、专题页、Push、挑战赛、KOL 和社区活动。",
        "风险动作：观察、内部准备、澄清、暂停、拒绝或撤回。",
    ])
    doc.add_heading("6.3 产品承接路径", level=2)
    add_table(doc, ["适配程度", "推荐路径"], [
        ["低相关或产品未准备", "只做品牌/内容，或继续观察。"],
        ["中等相关", "内容先行，通过专题页筛选意向用户。"],
        ["高度相关且有现成市场", "内容直接连接 Predx 市场或产品页面。"],
        ["战略级、高价值", "新建市场、专题、活动和多渠道战役。"],
        ["自有数据形成新闻点", "由产品信号反向生成内容和热点。"],
    ], [2600, 6760])

    doc.add_heading("7. 目标架构与统一行动任务包", level=1)
    add_p(doc, "一个热点可以同时服务曝光、拉新、激活和留存，但不同渠道不必承担全部目标。系统先定义主目标、次目标、权重和护栏，再进行目标—受众—渠道—动作适配。")
    add_table(doc, ["目标", "主要承担渠道/系统", "示例动作"], [
        ["曝光", "X、TikTok、媒体、KOL", "快评、概率卡、短视频和品牌观点"],
        ["兴趣与信任", "Reddit、YouTube、社区", "情景分析、讨论和深度解释"],
        ["拉新", "社媒＋专题页", "热点内容、产品入口和低门槛解释"],
        ["激活", "Predx 产品", "对应市场、首页推荐和首次参与路径"],
        ["留存", "Push、邮件、Watchlist", "概率变化、结果和相关事件提醒"],
    ], [1600, 2800, 4960])
    doc.add_heading("7.1 统一行动任务包包含什么", level=2)
    add_bullets(doc, [
        "目标：主目标、次目标、权重、目标受众和成功指标。",
        "统一内核：确认事实、核心叙事、必说、禁说和风险边界。",
        "行动组合：内容、产品、渠道、营销、社区、风控和数据任务。",
        "产品承接：目标市场、页面、CTA、追踪参数和用户路径。",
        "执行要求：负责人、优先级、截止时间、审核和备用方案。",
    ])
    add_callout(doc, "核心含义", "统一不等于所有渠道发布同一内容，而是所有系统基于同一目标、事实和边界完成不同形式的专业响应。", PALE_ORANGE, ORANGE)

    doc.add_heading("8. 执行、审核与发布", level=1)
    doc.add_heading("8.1 标准行动模板", level=2)
    add_p(doc, "系统使用少量标准模板把任务包转成具体任务。MVP 先覆盖高频场景，不建设复杂工作流。")
    add_table(doc, ["模板类别", "MVP 示例"], [
        ["内容", "X 实时短帖、概率变化帖、Thread、Reddit 讨论、结果快讯和复盘。"],
        ["产品", "关联现有市场、新建市场请求、首页推荐、Push 和结果提醒。"],
        ["营销/社区", "热点竞猜、社区讨论和 KOL 预测邀请。"],
        ["风控/数据", "事实核验、高风险审批、追踪参数和效果回流。"],
    ], [2200, 7160])
    doc.add_heading("8.2 执行确认", level=2)
    add_p(doc, "各渠道在统一行动任务包范围内完成专业改编。发布前只确认事实、必说禁说、产品链接和风险；发布后保存实际内容、平台、账号、时间和链接。")
    doc.add_heading("8.3 审核与异常", level=2)
    add_bullets(doc, [
        "低风险由渠道负责人确认，中风险由内容/热点负责人审核，高风险进入品牌、法务或风控审批。",
        "事实变化、产品不可用或风险升级时，支持继续、更新、暂停、撤回或更正。",
        "任务状态保持简洁：待接受、生产中、待审核、已批准、已执行、已回传；另设拒绝、失败、取消和撤回。",
    ])

    doc.add_heading("9. X 矩阵运营子系统接入（简化版）", level=1)
    add_p(doc, "X 矩阵系统是热点系统在 X 平台的专业执行终端。热点系统不复制账号规则，也不直接控制具体账号；X 系统基于既有账号目标、受众、人格和状态完成路由与执行。")
    add_table(doc, ["热点系统提供", "X 子系统负责", "X 子系统回传"], [
        ["事件、目标、受众、核心事实、角度/母版、必说禁说、产品链接和窗口", "选择账号、内容改编、发布顺序、时间、互动和账号风险", "接受/拒绝、账号方案、最终文案、链接、曝光互动点击和异常"],
    ], [3120, 3120, 3120])
    add_callout(doc, "接入流程", "热点系统生成 X 任务 → X 系统推荐账号和行动方案 → 人工确认 → X 系统执行 → 结果回传。", PALE_BLUE, BLUE)
    add_p(doc, "双方共享 event_id、opportunity_id、action_package_id、x_task_id 和 publication_id，以便把 X 表现与产品注册、激活和留存结果关联。")

    doc.add_heading("10. 监控、追踪与归因", level=1)
    add_table(doc, ["环节", "基础动作", "进阶动作"], [
        ["实时监控", "检查事实、舆情、账号、链接和产品状态", "异常阈值、自动提醒和跨系统暂停"],
        ["平台追踪", "曝光、互动、分享、点击和最终发布链接", "目标受众覆盖、讨论质量和账号贡献"],
        ["产品追踪", "访问、注册、首次预测和再次预测", "用户分群、长期价值和增量实验"],
        ["成本追踪", "人工、内容、活动、KOL 和工具成本", "单位增长成本和机会级 ROI"],
        ["归因", "统一追踪参数和直接路径", "时间窗口贡献与对照实验"],
    ], [1800, 3800, 3760])
    add_p(doc, "所有动作至少关联 event_id、opportunity_id、action_package_id、task_id 和 publication_id。直接归因优先；自然传播采用贡献判断，不伪装成精确因果。")

    doc.add_heading("11. 复盘与学习", level=1)
    add_p(doc, "复盘不以一个总分替代诊断，而是判断问题发生在发现、判断、生产、平台、内容、产品还是留存环节。")
    add_table(doc, ["阶段", "核心指标", "结果不好时优先优化"], [
        ["发现", "发现领先时间、有效机会召回", "来源、关键词、种子账号和异常阈值"],
        ["判断", "机会命中率、人工采纳率", "相关性、平台、产品和窗口权重"],
        ["生产", "立项到发布耗时、窗口内完成率", "模板、任务组合和审批速度"],
        ["平台/内容", "有效触达、互动质量、产品点击", "平台选择、受众、角度、CTA 和发布时间"],
        ["产品", "注册、首次预测、激活率", "落地页、注册和首次参与路径"],
        ["留存", "再次访问、再次预测", "结果提醒、相关市场和个性化推荐"],
        ["经济性", "单位激活成本、ROI", "渠道组合、资源投入和自动化"],
        ["风险", "错误、投诉、撤回、账号处罚", "证据、品牌和审批规则"],
    ], [1500, 2650, 5210])
    doc.add_heading("11.1 典型漏斗诊断", level=2)
    add_bullets(doc, [
        "曝光高、点击低：受众或产品连接有问题。",
        "曝光低、转化率高：内容有效，但分发不足。",
        "点击高、注册低：落地页或注册流程有问题。",
        "注册高、激活低：首次产品体验没有承接热点意图。",
        "激活高、留存低：缺少结果提醒和相关事件推荐。",
    ])
    add_p(doc, "每次复盘必须形成可执行结论：继续什么、停止什么、实验什么，以及需要更新哪条来源、评分、渠道、模板或产品规则。")

    doc.add_heading("12. 核心对象与组织责任", level=1)
    add_table(doc, ["核心对象", "作用"], [
        ["Source Signal", "来自平台、日历、市场或内部数据的最小信号。"],
        ["Trend / Future Event", "统一现实事件及其时间、证据、生命周期和结果分支。"],
        ["Event Card", "对事件进行客观结构化理解。"],
        ["Opportunity Card", "Predx 是否以及为什么参与的业务判断。"],
        ["Action Package", "跨系统目标、事实、边界和任务协议。"],
        ["Execution Task", "交给具体执行系统的一次行动请求。"],
        ["Publication", "实际发布、上线或活动记录。"],
        ["Performance / Learning", "执行结果和复盘结论。"],
    ], [2500, 6860])
    add_table(doc, ["角色", "核心责任"], [
        ["热点运营负责人", "主题策略、机会立项、目标和资源协调、周期复盘。"],
        ["研究/值班运营", "雷达巡检、聚类修正、证据核验和机会初判。"],
        ["内容策略", "核心叙事、母版、事实和品牌表达。"],
        ["渠道/子系统 Owner", "专业改编、排期、发布、互动和数据回传。"],
        ["产品运营", "市场、专题、推荐、Push 和产品承接。"],
        ["品牌/法务/风控", "高风险审批、暂停、撤回和事故处置。"],
        ["数据/产品/工程", "对象、接口、指标、归因、可靠性和权限。"],
    ], [2500, 6860])

    doc.add_heading("13. MVP 路线图", level=1)
    add_callout(doc, "MVP 原则", "终局设计大而全，但第一阶段只验证一条高相关、可执行、可追踪、可复盘的真实闭环。", PALE_TEAL, TEAL)
    add_table(doc, ["阶段", "建议周期", "建设范围", "关键产物"], [
        ["Phase 0 对齐", "2 周", "主题边界、来源、规则、历史样本、X 接口和产品漏斗", "词典、样本集、账号能力摘要、指标口径"],
        ["Phase 1 雷达与事件卡", "4-6 周", "3-4 个来源、去重聚类、Event Card、人工研判", "热点池、事件卡、预警和审核台"],
        ["Phase 2 机会与 X 闭环", "4-6 周", "Opportunity、目标适配、行动包、X 任务与回传", "X 执行任务、账号方案、发布链接"],
        ["Phase 3 产品与复盘", "4 周", "产品点击、注册、首次预测、成本和复盘", "漏斗看板、归因和策略更新"],
        ["Phase 4 扩展", "持续", "更多平台、Future Event 自动化和低风险半自动", "模板库、规则引擎和多渠道协同"],
    ], [1400, 1400, 3760, 2800])
    doc.add_heading("13.1 推荐第一条支线", level=2)
    add_p(doc, "建议优先选择高频、结果明确、产品天然相关且风险相对可控的主题，例如体育赛事；如果业务优先政治新闻，则提高证据和审批要求。")
    add_p(doc, "推荐链路：赛事日历/实时信号 → Event Card → Opportunity → X 账号路由 → 概率内容 → Predx 市场 → 注册/首次预测 → 结果提醒 → 复盘。")
    doc.add_heading("13.2 MVP 验收", level=2)
    add_bullets(doc, [
        "优先来源稳定采集，事件证据可追溯。",
        "相对纯人工监控获得可测量的发现领先时间。",
        "Event Card 能支持人工完成参与/观察/拒绝判断。",
        "X 任务状态、账号、文案和发布链接可以完整回传。",
        "内容点击可以关联到注册和首次预测。",
        "每个已执行机会形成一次简洁复盘并更新至少一条规则。",
    ])

    doc.add_heading("14. 下一轮需要确认的业务决策", level=1)
    add_table(doc, ["决策项", "建议默认方案", "需要确认"], [
        ["首批主题", "3-5 个 Predx 高相关主题", "具体清单与排除项"],
        ["首批输入", "X、Reddit、YouTube、预测市场＋1 个本地源", "API、供应商和合规可用性"],
        ["Future Event", "预测市场种子库＋官方/行业日历＋人工录入", "首批日历和维护 Owner"],
        ["执行系统", "X 矩阵＋Predx 产品运营", "接口成熟度和责任人"],
        ["目标市场/语言", "团队可直接审校的 1-2 种语言", "地区和本地化责任"],
        ["北极星结果", "有效增长价值＋热点行动 ROI", "核心产品行为和价值权重"],
        ["风险审批", "高风险和重大品牌议题强制审批", "审批人、值班和 SLA"],
    ], [1900, 3600, 3860])
    add_callout(doc, "最终建议", "先用有限主题和 X 矩阵跑通一条“发现—判断—内容—产品—归因”闭环，再扩展 Future Event 自动化、更多平台与低风险半自动执行。", PALE_BLUE, BLUE)

    doc.add_page_break()
    doc.add_heading("15. 五类热点输入：具体建设方法", level=1)
    add_p(doc, "本章把“热点从哪里来”展开到可直接配置来源、刷新频率和运营准备的粒度。五类入口不是五套孤立系统，而是共享实体词典、来源库、事件模型和统一候选池。")

    doc.add_heading("15.1 实时突发热点", level=2)
    add_table(doc, ["来源层级", "建议接入", "采集方式", "判断用途"], [
        ["综合热榜", "Google Trends、X Trends、YouTube Trending、本地搜索/资讯热榜", "API、合规数据供应商或定时抓取；5-15 分钟刷新", "发现已开始扩散的事件，观察关键词、地区和速度"],
        ["权威事实源", "政府、监管机构、赛事组织、公司 IR、项目官方账号", "RSS、网页变更、官方账号列表；按主题设置优先级", "核实事实、时间和原始声明，避免把转载当首发"],
        ["新闻与垂直媒体", "通讯社、财经、政治、体育、科技和娱乐媒体", "RSS/API/站点订阅；保留来源等级和发布时间", "补充背景、不同叙事和跨区域传播"],
        ["社媒种子网络", "记者、研究员、KOL、社区管理员、项目方与高质量用户", "维护账号库；监听发帖、转发和共同提及", "在热榜前捕捉弱信号，识别传播起点"],
        ["社区与异常信号", "Reddit、Discord/Telegram 社区、论坛、站内搜索和用户反馈", "关键词/实体监听、量级和增速阈值", "发现尚未进入主流媒体的圈层事件"],
    ], [1550, 2820, 2780, 2210])
    add_p(doc, "基础准备：主题词典、实体别名、来源白名单/黑名单、种子账号库、地区语言和事实核验规则。进阶能力：同一指标在短时间内异常增长、多个独立来源同时出现、或信号从圈层平台跨到大众平台时自动预警。")

    doc.add_heading("15.2 可预见未来事件", level=2)
    add_table(doc, ["来源", "典型内容", "如何进入 Future Event Center"], [
        ["预测市场", "选举、政策、赛事、商业、科技、文化事件及揭晓时间", "从多个问题归并现实事件；保留市场概率，但不把问题等同于事件"],
        ["官方公共日历", "选举、会议、听证、政策生效、发布会、外交访问", "结构化日期、主办方、地区和确认状态；官方变更优先覆盖"],
        ["行业垂直日历", "财报、经济数据、体育赛程、影视上线、颁奖、科研会议", "按行业适配字段；对结果型事件预设结果分支"],
        ["新闻与社媒预告", "“将于”“计划”“预计”“下周发布”等信息", "抽取未来时间、主体、动作和证据；人工确认后入库"],
        ["产品与内部日历", "Predx 市场结算、版本发布、活动、合作和运营节点", "由产品/运营系统同步；可直接生成准备任务"],
        ["人工策划", "尚无标准数据源的战略事件、地区事件和暂定事项", "表单录入；必须标记负责人、证据和复查日期"],
    ], [2100, 3520, 3740])
    add_callout(doc, "关键规则", "未来事件必须有“时间类型＋确认状态＋下一次核验时间”。日期不确定并不等于不能入库，但必须以时间窗口或条件触发方式表达。", PALE_ORANGE, ORANGE)

    doc.add_heading("15.3 周期性热点", level=2)
    add_p(doc, "周期热点不是每次重新发现，而是建立模板：周期规则、提前量、权威来源、往期热度、常见受众、内容资产、产品需求和风险点。系统据此自动生成下一期 Future Event。")
    add_table(doc, ["模板示例", "生成规则", "提前准备"], [
        ["赛事", "按赛程或阶段生成；遇延期同步更新", "球队/选手实体、概率内容模板、赛前/赛中/赛后动作"],
        ["财报与经济数据", "按财报日历或统计机构日历生成", "历史基线、市场预期、结果分支、合规表达"],
        ["节日/纪念日", "年度重复；地区和语言分别维护", "品牌适配、文化禁忌、常青内容和活动机制"],
        ["颁奖/发布季", "按官方日程与提名流程生成", "候选对象、社区受众、预测题和结果快讯模板"],
    ], [1950, 3000, 4410])

    doc.add_heading("15.4 长期结构性议题", level=2)
    add_p(doc, "长期议题本身未必有爆发时间，例如 AI 治理、气候变化、宏观衰退、社会公平或加密监管。应建立“母题—子议题—实体—立场—触发器”知识树，并持续记录长期兴趣基线。")
    add_bullets(doc, [
        "输入：行业报告、政策文件、用户访谈、历史高表现内容、搜索常青需求、社区长期争议。",
        "触发器：新政策、新人物表态、新数据、突发事故、司法进展、产品突破或纪念节点。",
        "激活判断：新信号与母题实体/观点匹配，且热度或独立来源数显著高于日常基线。",
        "准备资产：背景卡、时间线、核心数据、观点谱系、Predx 长期叙事和禁区。",
    ])

    doc.add_heading("15.5 内部与自造热点", level=2)
    add_table(doc, ["内部信号", "触发示例", "可形成的外部动作"], [
        ["市场概率", "短时间大幅变化或与公众叙事明显背离", "概率异动内容、解释、相关市场推荐"],
        ["交易/参与", "交易量、参与人数、地区或人群异常增长", "Predx 数据洞察、榜单、社区讨论"],
        ["搜索与浏览", "站内搜索上升但市场供给不足", "新建市场、专题页、解释内容"],
        ["产品节点", "新功能、合作、结算或里程碑", "发布活动、用户故事、产品教育"],
        ["主动策划", "品牌议题、竞猜、挑战赛、KOL 联动", "预热—引爆—参与—结果的完整活动"],
    ], [1900, 3260, 4200])
    add_p(doc, "自造热点必须标注为内部发起，并设置“能否被外部事实支持、能否形成真实参与、品牌风险和失败退出条件”，避免只制造表面声量。")

    doc.add_heading("16. 从 Source Signal 到 Event Card：操作细则", level=1)
    doc.add_heading("16.1 去重、聚类与事件层级", level=2)
    add_table(doc, ["对象", "定义", "处理规则"], [
        ["Source Signal", "一条帖子、新闻、视频、日历项、预测问题或内部异常", "保留原文、作者、时间、平台、互动、语言、URL 和采集时间"],
        ["传播副本", "转发、转载、搬运、引用或同一稿件", "不重复计作事实来源；保留传播贡献和路径"],
        ["Narrative Cluster", "围绕同一事件的某个叙事、观点或争议", "允许多个叙事共存，避免把反对观点误判为不同事件"],
        ["Trend Event", "可被一致描述的现实世界事件", "以主体＋动作＋时间＋地点＋结果为主键语义"],
        ["主/子事件", "长期进程与其中的阶段性进展", "主事件聚合背景，子事件拥有独立窗口和行动"],
    ], [1900, 3500, 3960])
    add_p(doc, "硬去重先处理相同 URL、平台原生转发和完全相同文本；软去重再用标题/正文相似度、实体、时间和来源关系识别转载。事件聚类同时使用主体、动作、时间、地点和语义，不只依赖关键词。低置信聚类进入人工合并/拆分队列。")

    doc.add_heading("16.2 Event Card 八大模块：字段、数据与判断", level=2)
    add_table(doc, ["模块", "核心字段", "数据/分析方法", "对下一步的指导"], [
        ["事件身份", "event_id、标题、类型、主题、实体、地区、语言、主/子事件", "实体抽取＋人工规范名；连接 Future Event/周期模板", "确定事件边界及适用业务线"],
        ["事实与证据", "事实清单、未确认点、来源等级、独立来源数、最后核验", "官方源优先；区分原始声明、报道和评论；冲突检测", "决定能说什么、是否需要等待"],
        ["传播热度", "声量、增速、加速度、独立作者、互动、跨平台数", "平台内归一化；与主题历史基线比较；剔除重复和疑似机器人", "判断事件势能，而非只看绝对热度"],
        ["生命周期", "阶段、峰值预测、饱和度、置信度", "声量曲线＋增速/加速度＋跨平台扩散＋新信息率", "决定快讯、解释、深度或复盘"],
        ["受众结构", "已观察/潜在/目标受众，地区、语言、兴趣、动机、意图", "作者画像、社区、话题共现、互动者抽样、站内相似人群", "选择受众、角度、表达难度和 CTA"],
        ["平台传播", "首发、发酵、目标受众、执行和承接平台", "跨平台时间线、受众重合、形式适配、意图和饱和度", "避免把“最热平台”误当“最佳转化平台”"],
        ["窗口与风险", "注意力/内容/产品/长尾窗口，事实/品牌/法律/平台风险", "历史同类曲线、事件日程、生产 SLA、风险规则", "判断现在做什么、最晚何时做、是否参与"],
        ["系统初步信号", "信息完整度、异常项、建议观察方向、置信度", "规则＋模型提示；不直接替代 Opportunity 决策", "决定是否具备进入机会判断的条件"],
    ], [1350, 2300, 3440, 2270])

    doc.add_heading("16.3 生命周期怎么判断", level=2)
    add_table(doc, ["阶段", "常见信号", "适合动作"], [
        ["萌芽", "量级低但增速高；少数高质量源出现；信息仍不完整", "核验、观察、准备事实卡和产品能力"],
        ["上升", "多个独立来源加入；跨平台扩散；新信息率高", "快讯、解释、观点、产品预备或轻联动"],
        ["爆发/峰值", "绝对声量高、互动集中、主流媒体/KOL 进入", "高辨识度内容、互动、产品直连；避免同质化"],
        ["回落", "增速转负、重复内容增加、新信息减少", "结果、影响、复盘、长尾搜索内容"],
        ["再激活", "新证据或新节点使增速再次上升", "作为子事件重开窗口，更新原 Event Card"],
    ], [1450, 4300, 3610])
    add_p(doc, "MVP 不追求复杂预测模型：每 15-30 分钟计算主题内标准化声量、增速和加速度，再结合跨平台数、新信息率和人工确认给出阶段与置信度。积累历史样本后，再按主题建立峰值和窗口模型。")

    doc.add_heading("16.4 受众和行动窗口怎么判断", level=2)
    add_bullets(doc, [
        "受众分三层：实际在讨论的人、可能对事件感兴趣的人、Predx 真正希望触达的人。三者可能重合，也可能完全不同。",
        "受众证据来自作者自述、关注关系、常发主题、所在社区、语言地区、互动内容和站内历史行为；敏感属性不得无依据推断。",
        "注意力窗口看公众讨论何时衰减；内容窗口看某种内容形态何时仍有新增价值；产品窗口看用户何时仍可行动；长尾窗口看结果和知识需求持续多久。",
        "实际可用窗口＝预计窗口－制作耗时－审核耗时－分发准备。若可用窗口小于最短执行 SLA，则转为观察、简化动作或放弃。",
    ])

    doc.add_heading("17. 从 Opportunity 到统一行动任务包", level=1)
    doc.add_heading("17.1 Opportunity Card 最小模板", level=2)
    add_table(doc, ["字段组", "必须记录"], [
        ["结论", "参与 / 观察 / 拒绝；判断时间；负责人；有效期"],
        ["理由", "Predx 相关性、增长价值、参与资格、平台受众、产品准备、窗口与风险"],
        ["目标", "主目标、次目标、权重、目标受众、目标行为和护栏"],
        ["承接策略", "参与方式、平台角色、产品路径和成功条件"],
        ["约束", "不可确认事实、不可用平台/地区、资源上限、复查触发器"],
    ], [2400, 6960])
    add_p(doc, "机会判断不建议一开始使用单一总分自动决策。MVP 用红黄绿或 1-5 级辅助比较，但保留维度明细和人工结论：任何高风险、无事实基础或产品不可用都可以直接否决。")

    doc.add_heading("17.2 多目标适配逻辑", level=2)
    add_table(doc, ["输入", "系统判断", "输出"], [
        ["曝光＋拉新＋留存均为目标", "按主次、权重、受众阶段、渠道能力和事件窗口分配", "不同渠道承担不同目标，形成组合动作"],
        ["同一平台既要曝光又要转化", "把目标拆成内容序列或同帖不同入口", "主帖负责传播，回复/Thread/置顶链接负责转化，后续结果帖负责留存"],
        ["目标冲突", "例如最大化曝光会增加品牌风险或降低转化质量", "以主目标和护栏优先，记录被牺牲指标"],
        ["资源不足", "比较机会价值、最小有效动作和剩余窗口", "缩小平台/内容范围，或改为观察"],
    ], [2200, 3900, 3260])

    doc.add_heading("17.3 统一行动任务包完整字段", level=2)
    add_table(doc, ["模块", "内容", "谁使用"], [
        ["任务包身份", "action_package_id、事件、机会、版本、有效期和负责人", "全部执行系统"],
        ["目标架构", "主/次目标、权重、目标受众、目标行为、KPI 和护栏", "渠道、产品、数据"],
        ["统一事实", "已确认事实、证据、待确认点、更新时间", "内容、产品、品牌"],
        ["统一叙事", "核心判断、可选角度、必说、禁说、语气和品牌边界", "内容、社媒、PR、KOL"],
        ["行动组合", "渠道任务、产品任务、活动任务、社区任务、风控和数据任务", "各子系统"],
        ["产品承接", "市场/页面、CTA、用户路径、追踪参数、不可用时备选方案", "产品、增长、渠道"],
        ["节奏与依赖", "优先级、最晚完成时间、先后顺序、依赖和停止条件", "项目协调与执行系统"],
        ["审核与风险", "风险等级、审核人、事实变化和舆情异常时怎么做", "品牌、法务、负责人"],
        ["回传要求", "最终内容、账号、发布时间、链接、成本、平台和产品结果", "数据与复盘"],
    ], [1800, 4800, 2760])
    add_callout(doc, "边界再确认", "行动任务包既是统一对外口径，也是内容、产品、营销、社区和风控分别如何响应的跨系统协议。它规定共同目标与边界，不替代各专业系统的具体执行规则。", PALE_TEAL, TEAL)

    doc.add_heading("18. X 矩阵与产品系统的接口", level=1)
    doc.add_heading("18.1 X 矩阵适配", level=2)
    add_table(doc, ["步骤", "热点系统", "X 矩阵子系统"], [
        ["任务下发", "给出事件、目标、受众、核心事实、可选角度、边界、产品链接和窗口", "校验任务完整性，返回接受/拒绝及原因"],
        ["路由建议", "不指定具体账号或只给约束", "按账号既有目标、受众、人格、内容类型、状态和风险选择账号"],
        ["内容执行", "提供统一内核和截止时间", "完成 X 原生改编、主帖/回复/Thread 组合、排期和互动"],
        ["人工确认", "热点负责人确认事实与目标未偏离", "账号负责人确认账号适配和最终文案"],
        ["结果回传", "接收并关联产品结果", "回传账号、版本、发布时间、链接、曝光、互动、点击和异常"],
    ], [1450, 3910, 4000])
    add_p(doc, "如果一个事件同时追求曝光与转化，X 子系统可将其编排为：高覆盖账号主帖扩大曝光 → 专业账号补充概率和证据 → 回复/Thread 放产品入口 → 结果揭晓后由留存型账号跟进。账号角色仍由 X 系统自己的成熟规则决定。")

    doc.add_heading("18.2 产品承接的四种模式", level=2)
    add_table(doc, ["模式", "适用条件", "典型路径", "重点指标"], [
        ["内容先行", "产品相关性尚不确定或用户意图偏低", "内容 → 解释/专题页 → 再筛选产品兴趣", "有效阅读、专题点击、兴趣信号"],
        ["轻产品联动", "相关但产品准备一般", "内容 → 相关市场集合/Watchlist/提醒", "点击、收藏、提醒订阅"],
        ["产品直连", "高度相关、市场已上线且窗口明确", "内容/活动 → 对应市场 → 注册 → 首次预测", "注册、首次预测、激活成本"],
        ["产品反向造热点", "内部概率或行为数据有外部新闻价值", "产品异动 → 数据内容 → 外部讨论 → 回流产品", "外部引用、品牌认知、增量参与"],
    ], [1650, 2720, 3120, 1870])
    add_p(doc, "选择模式时同时看 Product Fit 与 Product Readiness。高度相关但产品未准备好，不应强行直连；可以先做内容、准备页面或直接放弃窗口。")

    doc.add_heading("19. 发布后监控、归因与复盘模板", level=1)
    doc.add_heading("19.1 发布后只做三件事", level=2)
    add_numbers(doc, [
        "确认实际执行没有偏离行动任务包：记录最终文案/素材、平台、账号、发布时间和链接。",
        "监控事实、舆情、账号和产品链接；事实改变或风险升级时人工选择更新、暂停、撤回或更正。",
        "把平台表现、产品漏斗和成本回传到同一事件与机会下，为复盘提供完整证据。",
    ])
    doc.add_heading("19.2 单次热点行动复盘卡", level=2)
    add_table(doc, ["复盘模块", "要回答的问题", "可采取的优化"], [
        ["发现", "是否足够早？来源是真正的首发还是二次传播？漏掉了什么？", "新增/降权来源，更新关键词、账号和阈值"],
        ["事件理解", "是否正确聚类？事实、生命周期、受众和窗口判断哪里偏差？", "调整事件边界、基线、人工规则和样本"],
        ["机会判断", "参与/拒绝是否正确？目标、平台、产品和风险判断是否成立？", "更新维度权重、否决条件和业务策略"],
        ["行动设计", "目标是否清晰？各渠道分工是否合理？动作是否过多或不足？", "优化任务组合、内容序列、CTA 和产品模式"],
        ["生产发布", "是否赶上窗口？瓶颈在制作、审核还是产品准备？", "增加模板、明确 SLA、减少不必要环节"],
        ["平台内容", "谁看到了、为什么互动/不互动、是否带来有效点击？", "调整账号、受众、角度、形式、时间和分发"],
        ["产品漏斗", "访问→注册→首次预测→再次预测在哪一步流失？", "优化落地页、注册、首次体验、提醒和推荐"],
        ["成本风险", "投入是否值得？是否出现错误、投诉、撤回或账号处罚？", "调整资源上限、证据要求、审批和平台规则"],
    ], [1650, 4360, 3350])
    add_p(doc, "复盘结论固定输出四项：继续什么、停止什么、下次实验什么、更新哪条系统规则。管理层看业务结果与重大风险；执行团队看具体漏斗与规则更新。")

    doc.add_heading("20. MVP 功能清单与验收口径", level=1)
    add_table(doc, ["模块", "MVP 必做", "暂不做", "验收口径"], [
        ["热点输入", "X/新闻或热榜/预测市场/1 个垂直日历＋人工录入", "一次接全平台和全部行业", "稳定采集、来源可追溯、失败可见"],
        ["Future Event", "事件库、确认状态、时间窗口、T-7/T-1 提醒、转实时", "自动发现所有未来事件", "可提前准备且变更可更新"],
        ["事件化", "硬去重、模型辅助软去重/聚类、人工合并拆分", "完全自动聚类", "同一事件不被大量重复；边界可修正"],
        ["Event Card", "八大模块、证据链接、人工确认和置信度", "高精度生命周期预测", "支持参与/观察/拒绝判断"],
        ["Opportunity", "维度卡、红黄绿、人工结论、多目标和产品模式", "黑盒自动决策", "结论有证据、有负责人、有有效期"],
        ["行动任务包", "目标、事实、边界、X 任务、产品任务和回传要求", "复杂 BPM/版本树", "X 与产品团队无需二次猜测需求"],
        ["X 接入", "任务下发、账号方案、人工确认、发布结果回传", "自动发所有账号", "从事件可追到账号和最终链接"],
        ["产品与归因", "统一参数、访问、注册、首次预测和基础成本", "精确计算所有自然传播因果", "至少跑通直接链路并可解释"],
        ["复盘", "单次复盘卡和规则更新记录", "复杂机器学习自优化", "每次行动产生明确改进项"],
    ], [1350, 3230, 2250, 2530])
    # Keep last block together and save.
    for p in doc.paragraphs:
        for r in p.runs:
            if not r.font.name:
                set_run(r)
    doc.save(DOCX)
    return DOCX


if __name__ == "__main__":
    print(build_document())
