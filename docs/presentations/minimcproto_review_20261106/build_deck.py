#!/usr/bin/env python3
"""从冻结资料和结构化讲稿生成可编辑 PPT；不执行工程构建、测试或硬件操作。"""

import hashlib
import json
import shutil
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.xmlchemy import OxmlElement
from pptx.util import Inches, Pt


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
FROZEN = ROOT / "artifacts/ppt_protocol_20261106"
DATA = json.loads((HERE / "deck_content.json").read_text())
MANIFEST = json.loads((FROZEN / "source_manifest.json").read_text())
FONT = "WenQuanYi Zen Hei"
MONO = "WenQuanYi Zen Hei Mono"
C = {"bg": "F4F7FB", "ink": "13263E", "muted": "52667D", "blue": "175CD3",
     "teal": "087F8C", "amber": "B46012", "line": "D9E2EF", "white": "FFFFFF",
     "pale": "EAF0FA", "warn": "FFF3E3", "code": "13263E"}


def color(value: str) -> RGBColor:
    """将 value 六位十六进制颜色转换为 PPT 颜色；返回 RGBColor。"""
    return RGBColor.from_string(C.get(value, value))


def box(slide, rect: tuple, style: dict = None):
    """在 slide 的 rect 英寸矩形绘制背景；style 指定颜色/圆角，返回可编辑形状。"""
    opt = style or {}
    kind = MSO_SHAPE.ROUNDED_RECTANGLE if opt.get("round") else MSO_SHAPE.RECTANGLE
    shape = slide.shapes.add_shape(kind, *[Inches(v) for v in rect])
    shape.fill.solid()
    shape.fill.fore_color.rgb = color(opt.get("fill", "white"))
    shape.line.fill.background()
    shape._element.spPr.append(OxmlElement("a:effectLst"))
    if opt.get("round"):
        shape.adjustments[0] = 0.12
    return shape


def text(slide, rect: tuple, content: str, style: dict = None):
    """在 slide/rect 写入 content；style 控制字号等，返回可编辑文本框。"""
    opt = style or {}
    shape = slide.shapes.add_textbox(*[Inches(v) for v in rect])
    frame = shape.text_frame
    frame.word_wrap = True
    frame.margin_left = frame.margin_right = 0
    frame.margin_top = frame.margin_bottom = 0
    frame.vertical_anchor = MSO_ANCHOR.TOP
    for idx, line in enumerate(content.split("\n")):
        p = frame.paragraphs[0] if idx == 0 else frame.add_paragraph()
        p.text = line
        p.font.name = opt.get("font", FONT)
        p.font.size = Pt(opt.get("size", 18))
        p.font.bold = opt.get("bold", False)
        p.font.color.rgb = color(opt.get("color", "ink"))
        p.space_after = Pt(opt.get("space", 8))
        p.line_spacing = opt.get("line", 1.15)
        p.alignment = opt.get("align", PP_ALIGN.LEFT)
        for run in p.runs:
            rpr = run._r.get_or_add_rPr()
            east = OxmlElement("a:ea")
            east.set("typeface", opt.get("font", FONT))
            rpr.append(east)
    return shape


def arrow(slide, points: tuple, style: dict = None):
    """在 slide 连接 points=(x1,y1,x2,y2)；style 指定颜色/宽度，返回连接线。"""
    opt = style or {}
    line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, *[Inches(v) for v in points])
    line.line.color.rgb = color(opt.get("color", "blue"))
    line.line.width = Pt(opt.get("width", 2))
    tail = OxmlElement("a:tailEnd")
    tail.set("type", "triangle")
    line.line._get_or_add_ln().append(tail)
    return line


def card(slide, rect: tuple, item: dict):
    """在 slide/rect 画标题与正文卡片；item 含文案，返回空值。"""
    x, y, w, h = rect
    compact = h < 1.7
    body_y = 0.65 if compact else 0.96
    box(slide, rect, {"round": True, "fill": item.get("fill", "white")})
    box(slide, (x, y + 0.22, 0.055, 0.42), {"fill": item.get("accent", "blue")})
    text(slide, (x + 0.24, y + 0.17, w - 0.46, 0.5), item["title"],
         {"size": 17 if compact else item.get("title_size", 20), "bold": True, "color": item.get("accent", "blue")})
    text(slide, (x + 0.24, y + body_y, w - 0.46, h - body_y - 0.1), item.get("body", ""),
         {"size": 14 if compact else item.get("size", 18), "space": 3 if compact else 9, "line": 1.06 if compact else 1.15})


def header(slide, data: dict, number: int):
    """为 slide 设置 data 的标题和 number 页码；返回空值。"""
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color("bg")
    text(slide, (0.55, 0.22, 8, 0.24), "MINIMCPROTO 2.0  /  " + data["section"],
         {"size": 10, "color": "teal", "bold": True})
    text(slide, (0.55, 0.68, 12.25, 0.66), data["title"], {"size": 28, "bold": True})
    text(slide, (0.57, 1.41, 12.15, 0.42), data["lead"],
         {"size": 15, "color": "amber" if data.get("warn") else "muted"})
    box(slide, (0.55, 6.99, 12.2, 0.012), {"fill": "line"})
    refs = " · ".join(data.get("refs", []))
    text(slide, (0.56, 7.1, 10.9, 0.2), "来源 " + refs + "  |  逐页备注含源码定位与讲解边界", {"size": 9, "color": "muted"})
    text(slide, (11.75, 7.08, 1, 0.22), f"{number:02d} / 30", {"size": 10, "color": "muted", "align": PP_ALIGN.RIGHT})


def bottom(slide, content: str):
    """在 slide 底部写 content 提示；返回空值。"""
    box(slide, (0.56, 6.48, 12.2, 0.37), {"fill": "pale"})
    text(slide, (0.7, 6.55, 11.9, 0.25), content, {"size": 11, "color": "muted"})


def render_cards(slide, data: dict):
    """按 data 卡片数量排列 slide；返回空值。"""
    items = data["cards"]
    if len(items) == 4:
        for idx, item in enumerate(items):
            card(slide, (0.58 + (idx % 2) * 6.17, 1.98 + (idx // 2) * 2.18, 5.99, 2.0), item)
    else:
        width = 12.1 / len(items)
        for idx, item in enumerate(items):
            card(slide, (0.58 + idx * width, 2.35, width - 0.16, 3.05), item)
    if data.get("bottom"):
        bottom(slide, data["bottom"])


def render_table(slide, data: dict):
    """按 data 列宽和数据在 slide 绘制可编辑表格；返回空值。"""
    rows = [data["columns"]] + data["rows"]
    table = slide.shapes.add_table(len(rows), len(rows[0]), Inches(0.61), Inches(2.03),
                                   Inches(12.05), Inches(4.2)).table
    scale = 12.05 / sum(data["widths"])
    for col, width in zip(table.columns, data["widths"]):
        col.width = Inches(width * scale)
    for row_idx, row in enumerate(rows):
        table.rows[row_idx].height = Inches(0.5 if row_idx == 0 else 3.7 / len(data["rows"]))
        for col_idx, value in enumerate(row):
            cell = table.cell(row_idx, col_idx)
            cell.text = value
            cell.margin_left = cell.margin_right = Inches(0.13)
            cell.margin_top = cell.margin_bottom = Inches(0.07)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            cell.fill.fore_color.rgb = color("ink" if row_idx == 0 else ("white" if row_idx % 2 else "pale"))
            for p in cell.text_frame.paragraphs:
                p.font.name = FONT
                p.font.size = Pt(14 if len(rows) > 6 else 15)
                p.font.bold = row_idx == 0
                p.font.color.rgb = color("white" if row_idx == 0 else "ink")
    if data.get("bottom"):
        bottom(slide, data["bottom"])


def render_code(slide, data: dict):
    """在 slide 显示 data 的教学伪代码及侧栏；返回空值。"""
    box(slide, (0.58, 2.04, 7.5, 4.55), {"fill": "code", "round": True})
    text(slide, (0.85, 2.28, 6.95, 0.4), data["code_title"], {"size": 14, "color": "9EC7FF", "bold": True})
    code = "\n".join(f"{idx + 1:02d}  {line}" for idx, line in enumerate(data["code"]))
    text(slide, (0.85, 2.94, 6.98, 3.48), code, {"size": 15, "color": "white", "font": MONO, "space": 4, "line": 1.06})
    items = data["cards"]
    height = (4.55 - 0.15 * (len(items) - 1)) / len(items)
    for idx, item in enumerate(items):
        opts = dict(item, size=16, title_size=18)
        card(slide, (8.27, 2.04 + idx * (height + 0.15), 4.45, height), opts)


def render_flow(slide, data: dict):
    """在 slide 按 data 顺序绘制流程；返回空值。"""
    steps = data["steps"]
    span = 12.18 / len(steps)
    for idx, item in enumerate(steps):
        opts = dict(item, title_size=17, size=16)
        card(slide, (0.57 + idx * span, 2.63, span - 0.18, 2.6), opts)
        if idx < len(steps) - 1:
            x = 0.57 + idx * span + span - 0.16
            arrow(slide, (x, 3.95, x + 0.17, 3.95))
    if data.get("bottom"):
        bottom(slide, data["bottom"])


def render_topology(slide, data: dict):
    """在 slide 绘制 data 的三节点物理拓扑；返回空值。"""
    for idx, item in enumerate(data["cards"]):
        card(slide, (0.72 + idx * 4.19, 2.45, 3.57, 2.72), dict(item, size=20))
        if idx < 2:
            arrow(slide, (4.36 + idx * 4.19, 3.6, 4.86 + idx * 4.19, 3.6))
    text(slide, (0.83, 5.5, 11.8, 0.48), "逻辑寻址与物理串口解耦：AP 构造 DST=0x03，即可请求 TH。", {"size": 20, "color": "teal"})
    bottom(slide, data["bottom"])


def render_wire(slide, data: dict):
    """在 slide 绘制 data 帧头字段宽度图；返回空值。"""
    x = 0.64
    for idx, (offset, name, width) in enumerate(data["fields"]):
        w = width * 0.995
        box(slide, (x, 2.35, w - 0.03, 1.0), {"fill": "blue" if idx % 2 == 0 else "teal"})
        text(slide, (x + 0.02, 2.48, w - 0.07, 0.3), name, {"size": 16, "bold": True, "color": "white", "align": PP_ALIGN.CENTER})
        text(slide, (x + 0.02, 2.94, w - 0.07, 0.25), offset, {"size": 12, "color": "white", "align": PP_ALIGN.CENTER})
        x += w
    box(slide, (0.64, 3.58, 9.4, 0.5), {"fill": "pale"})
    text(slide, (0.85, 3.69, 8.9, 0.3), "Payload：从 Offset 12 开始，长度由 Len 指定", {"size": 16})
    box(slide, (10.08, 3.58, 2.49, 0.5), {"fill": "teal"})
    text(slide, (10.15, 3.69, 2.3, 0.3), "CRC16 · 2B", {"size": 16, "color": "white", "align": PP_ALIGN.CENTER})
    for idx, item in enumerate(data["cards"]):
        card(slide, (0.64 + idx * 4.04, 4.45, 3.87, 1.93), dict(item, title_size=18, size=15))


def crc16(data: bytes) -> int:
    """按 CCITT-FALSE 对 data 计算 CRC；返回16位整数，仅供教学报文生成。"""
    value = 0xFFFF
    # 逐位复算教学向量，避免把字节串误写成现场采集记录。
    for byte in data:
        value ^= byte << 8
        for _ in range(8):
            value = ((value << 1) ^ 0x1021) & 0xFFFF if value & 0x8000 else (value << 1) & 0xFFFF
    return value


def example_frame(hop: int, route: int) -> bytes:
    """按 hop/route 构造 Seq=1 的TH版本请求；返回含CRC的教学帧字节。"""
    frame = bytes([0x55, 0xAA, 1, 3, 5, 1, hop, route, 1, 0, 0, 0])
    return frame + crc16(frame).to_bytes(2, "little")


def render_hex(slide, data: dict):
    """在 slide 展示 data 对应的两条独立计算教学帧；返回空值。"""
    for idx, frame in enumerate([example_frame(4, 0), example_frame(3, 4)]):
        y = 2.1 + idx * 1.8
        box(slide, (0.63, y, 12.02, 1.5), {"round": True})
        item = data["cards"][idx]
        text(slide, (0.9, y + 0.15, 11.4, 0.38), item["title"] + "  ·  " + item["body"], {"size": 19, "color": "blue", "bold": True})
        text(slide, (0.9, y + 0.79, 11.3, 0.42), frame.hex(" ").upper(), {"size": 23, "font": MONO})
    text(slide, (0.78, 5.93, 11.9, 0.32), "教学计算向量 · 非本轮实机抓包", {"size": 14, "color": "amber"})
    bottom(slide, data["bottom"])


def render_sequence(slide, data: dict):
    """在 slide 根据 data 泳道和消息绘制教学时序；返回空值。"""
    xs = [1.5 + idx * 2.54 for idx in range(len(data["lanes"]))]
    for x, label in zip(xs, data["lanes"]):
        box(slide, (x - 1.03, 2.0, 2.06, 0.43), {"fill": "ink", "round": True})
        text(slide, (x - 0.99, 2.1, 1.98, 0.23), label, {"size": 13, "color": "white", "align": PP_ALIGN.CENTER})
        arrow(slide, (x, 2.48, x, 6.64), {"color": "line", "width": 1})
    for idx, (start, end, label) in enumerate(data["messages"]):
        y = 2.89 + idx * 0.49
        arrow(slide, (xs[start], y, xs[end], y), {"color": "blue" if idx < 6 else "teal"})
        left = min(xs[start], xs[end])
        text(slide, (left + 0.08, y - 0.29, abs(xs[end] - xs[start]) - 0.12, 0.28), label,
             {"size": 11, "color": "ink", "align": PP_ALIGN.CENTER})


def render_architecture(slide, data: dict):
    """按冻结源码在 slide 绘制当前AP服务架构；data为本页内容，返回空值。"""
    nodes = [(0.65, "Browser / Web HMI", "HTTP + SSE", "teal"),
             (3.8, "UI Gateway", "HTTP / D-Bus客户端", "blue"),
             (6.95, "DeviceManager", "准入 / 快照 / 新鲜度", "blue"),
             (10.1, "Forward", "串口事务 / 原始采样", "blue")]
    for x, title, body, accent in nodes:
        card(slide, (x, 2.15, 2.6, 2.0), {"title": title, "body": body, "accent": accent, "title_size": 16, "size": 15})
    for start, end, label in [(3.28, 3.76, "HTTP"), (6.43, 6.91, "D-Bus"), (9.58, 10.06, "D-Bus")]:
        arrow(slide, (start, 3.06, end, 3.06))
        text(slide, (start - 0.12, 2.61, 0.8, 0.23), label, {"size": 10, "color": "muted"})
    box(slide, (3.8, 4.73, 8.9, 0.76), {"fill": "pale", "round": True})
    text(slide, (4.04, 4.91, 8.38, 0.4), "DDS：Forward 发布 raw_temp → DeviceManager 订阅并发布 snapshot", {"size": 15, "color": "teal"})
    arrow(slide, (11.39, 4.16, 11.39, 4.7), {"color": "teal"})
    arrow(slide, (8.24, 4.7, 8.24, 4.16), {"color": "teal"})
    text(slide, (10.28, 5.97, 2.35, 0.4), "UART ↔ MC ↔ TH", {"size": 15, "color": "blue", "bold": True})
    arrow(slide, (12.82, 3.3, 12.82, 6.12))
    bottom(slide, "D-Bus SDK / Fast DDS SDK 是通信基础模块；UI 当前通过 D-Bus 获取权威快照。")


def render_cover(slide, data: dict):
    """按 data 生成 slide 深色封面；返回空值。"""
    box(slide, (0, 0, 13.333, 7.5), {"fill": "ink"})
    box(slide, (0.69, 0.72, 0.1, 0.56), {"fill": "teal"})
    text(slide, (0.98, 0.79, 11.3, 0.42), "跨团队技术交流与评审  /  2026.11.06", {"size": 17, "color": "9EC7FF"})
    text(slide, (0.94, 1.67, 11.8, 0.85), data["title"], {"size": 48, "color": "white", "bold": True})
    text(slide, (0.98, 2.76, 11.4, 0.7), data["lead"], {"size": 30, "color": "white"})
    for idx, item in enumerate(data["cards"]):
        x = 1.0 + idx * 4.1
        text(slide, (x, 4.67, 3.4, 0.63), item["title"], {"size": 34, "color": "9EC7FF", "bold": True})
        text(slide, (x, 5.48, 3.55, 0.46), item["body"], {"size": 19, "color": "white"})
        if idx < 2:
            arrow(slide, (x + 2.0, 5.03, x + 3.6, 5.03), {"color": "teal"})
    text(slide, (0.98, 6.83, 11.5, 0.3), "主规范 Rev 2.0.3  ·  已提交代码基线  ·  机制 / 接入 / 架构 / 评审", {"size": 12, "color": "9EC7FF"})


def render_baselines(slide, data: dict):
    """在 slide 展示冻结仓库基线和定位；data提供本页信息，返回空值。"""
    rows = []
    for repo, facts in MANIFEST["repositories"].items():
        rows.append([repo, facts["commit"][:12], facts["branch"]])
    render_table(slide, {"columns": ["仓库", "冻结提交", "分支"], "rows": rows,
                          "widths": [4.6, 3.4, 3.5]})
    bottom(slide, "源码：forward/ · device_manager/ · ui_gateway/ · 两端 minimc_proto.c；完整来源见 SOURCE_INDEX.md。")


def source_record(source_id: str) -> dict:
    """按 source_id 解析冻结来源及定位行；返回包含版本/哈希/路径的字典。"""
    repo, path, anchor = DATA["sources"][source_id]
    frozen_path = FROZEN / "sources" / repo / path
    source = next(item for item in MANIFEST["files"] if item["repository"] == repo and item["path"] == path)
    raw = frozen_path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != source["sha256"]:
        raise ValueError(f"冻结来源校验失败：{source_id}")
    lines = raw.decode().splitlines()
    line = next((idx + 1 for idx, value in enumerate(lines) if anchor in value), 1)
    return dict(source, id=source_id, line=line, anchor=anchor)


def notes(slide, data: dict, number: int):
    """为 slide 写入 data 讲稿和 number 页的来源；返回空值。"""
    entries = [f"第{number}页｜建议{data['minutes']}分钟", data["notes"], "", "资料定位（冻结已提交版本）："]
    for source_id in data.get("refs", []):
        item = source_record(source_id)
        entries.extend([f"[{source_id}] {item['repository']}/{item['path']}:{item['line']}",
                        f"commit={item['commit']}；sha256={item['sha256']}"])
    slide.notes_slide.notes_text_frame.text = "\n".join(entries)


def write_companions():
    """输出来源索引、完整讲稿及冻结清单副本；无参数，返回空值。"""
    index = ["# MiniMCProto PPT 来源索引", "", "生成日期：2026-11-06。讲解稿不构成协议修订、软件或HIL接受。", ""]
    for source_id in DATA["sources"]:
        item = source_record(source_id)
        index.extend([f"- **{source_id}**：`{item['repository']}/{item['path']}:{item['line']}`",
                      f"  - commit `{item['commit']}`；SHA256 `{item['sha256']}`"])
    (HERE / "SOURCE_INDEX.md").write_text("\n".join(index) + "\n")
    script = ["# MiniMCProto v2.0 讲者稿", "", "PPT逐页备注包含相同讲稿及准确来源。", ""]
    for idx, item in enumerate(DATA["slides"], 1):
        script.extend([f"## {idx:02d} {item['title']}（{item['minutes']}分钟）", "", item["lead"], "", item["notes"], "",
                       "来源：" + "、".join(item.get("refs", [])), ""])
    (HERE / "讲者稿.md").write_text("\n".join(script))
    shutil.copyfile(FROZEN / "source_manifest.json", HERE / "source_manifest.json")


def main():
    """生成全部演示文档并保存到本目录；无参数，成功返回空值。"""
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333333), Inches(7.5)
    prs.core_properties.title = DATA["title"]
    prs.core_properties.subject = "AP↔MC↔TH应用协议与D-Bus/Fast DDS通信架构"
    prs.core_properties.author = "sushaohua / 项目助理 AI (Codex)"
    renderers = {"cover": render_cover, "cards": render_cards, "table": render_table,
                 "wire": render_wire, "topology": render_topology, "flow": render_flow,
                 "code": render_code, "hex": render_hex, "sequence": render_sequence,
                 "architecture": render_architecture, "baselines": render_baselines}
    for idx, item in enumerate(DATA["slides"], 1):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        header(slide, item, idx)
        renderers[item["layout"]](slide, item)
        notes(slide, item, idx)
    target = HERE / "MiniMCProto_v2_通信协议与多端接入评审_20261106.pptx"
    prs.save(target)
    write_companions()
    print(f"已生成 {len(prs.slides)} 页：{target}")
    print(f"建议讲解与讨论合计 {sum(item['minutes'] for item in DATA['slides'])} 分钟")


if __name__ == "__main__":
    main()
