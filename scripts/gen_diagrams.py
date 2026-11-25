#!/usr/bin/env python3
"""Generate bilingual SVG diagrams for Risk Management Learning.

Run from the project root:
    python -I scripts/gen_diagrams.py

Outputs:
    src/zh/svg/*.svg
    src/en/svg/*.svg
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FONT = "Segoe UI, Microsoft YaHei, Noto Sans SC, sans-serif"
MONO = "Cascadia Mono, Consolas, Menlo, monospace"

BLUE = "#2563eb"
BLUE_SOFT = "#eff6ff"
AMBER = "#b45309"
AMBER_SOFT = "#fffbeb"
GREEN = "#047857"
GREEN_SOFT = "#ecfdf5"
RED = "#b91c1c"
RED_SOFT = "#fef2f2"
INK = "#0f172a"
MUTED = "#475569"
LINE = "#cbd5e1"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def text(x, y, s, size=14, fill=INK, weight=400, anchor="start", mono=False):
    family = MONO if mono else FONT
    return (
        f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
        f'fill="{fill}" font-weight="{weight}" text-anchor="{anchor}">{esc(s)}</text>'
    )


def rect(x, y, w, h, fill="none", stroke=LINE, rx=10, sw=1.5, dash=None, opacity=None):
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    if opacity is not None:
        extra += f' fill-opacity="{opacity}"'
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{extra}/>'
    )


def line(x1, y1, x2, y2, stroke=BLUE, sw=2, marker="arr", dash=None):
    m = f' marker-end="url(#{marker})"' if marker else ""
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" '
        f'stroke-width="{sw}"{m}{d}/>'
    )


def chip(x, y, w, h, label, fill="#ffffff", stroke=LINE, color=INK, size=11.5, mono=False):
    return rect(x, y, w, h, fill, stroke, 8, 1.2) + text(
        x + w / 2, y + h / 2 + size * 0.36, label, size, color, 600, "middle", mono
    )


def svg(w, h, title, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="diagram-title">
<title id="diagram-title">{esc(title)}</title>
<defs>
  <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="{BLUE}"/>
  </marker>
  <marker id="arrAmber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="{AMBER}"/>
  </marker>
  <marker id="arrGreen" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="{GREEN}"/>
  </marker>
  <marker id="arrGray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/>
  </marker>
</defs>
<rect width="100%" height="100%" fill="#ffffff"/>
{body}
</svg>
'''


T = {
    "zh": {
        "d1_title": "三层递进风控模型",
        "d1_sub": "任一层不通过，请求就会被降级处理；最常见的失败不是算法算错，而是状态不自洽。",
        "d1_layers": [
            ("设备层", "这台设备是否真实、身份是否可信", ["设备指纹", "SDI token", "TicketGuard"], BLUE),
            ("网络层", "这条链路是否像真实客户端", ["TLS 指纹", "HTTP/2", "cronet 版本"], GREEN),
            ("行为层", "这组请求的时序与状态是否自洽", ["签名头", "时钟一致性", "会话状态机"], AMBER),
        ],
        "d1_result": "判定与降级",
        "d1_result_items": ["空页 empty", "验证码 blocked", "限流 blocked", "直接拒绝 error/blocked"],
        "d1_note": "三层是“与”的关系：设备真实 + 链路真实 + 行为自洽，缺一不可。",
        "d2_title": "设备身份的交换关系",
        "d2_sub": "注册的本质：用本地声明 + 完整指纹，换取服务端签发的身份与凭证。",
        "d2_left": "本地声明（客户端生成）",
        "d2_left_items": [("openudid", "设备级 · 首次注册上报"), ("cdid", "安装级 · UUID 大写")],
        "d2_right": "服务端签发（对声明的信任）",
        "d2_right_items": [("device_id", "设备级 · 长期"), ("iid", "安装级"), ("sec_device_token", "设备级签名凭证")],
        "d2_req": "注册请求：四件套 + 完整指纹",
        "d2_resp": "注册响应：身份 + token",
        "d2_note": "单向信任：device_id / iid 不可本地伪造；换 App 版本后 token 体系需要重建。",
        "d3_title": "冷启动注册链路",
        "d3_sub": "完整冷注册必须按顺序推进；顺序本身就是服务端建模的一部分。",
        "d3_steps": [
            ("1", "device_register", "获取 device_id / iid（klink.amemv.com）", "身份"),
            ("2", "device_report", "Perseus 设备报告", "报告"),
            ("3", "app_log", "首启埋点（Sword 编码）", "埋点"),
            ("4", "get_token", "SDI token 下发", "token"),
            ("5", "activate / activate_record", "激活状态上报", "激活"),
            ("6", "birth()", "养号链路（app_log / stats / alert）", "养号"),
        ],
        "d3_note": "顺序即契约：乱序不必然失败，但会进入长期画像，后续请求权重会降低。",
        "d4_title": "Medusa field13：两代摘要链路",
        "d4_sub": "输入固定 52 字节；旧版由内容选分支，41.1/41.2 改由 khronos 选分支。",
        "d4_inputs": ["query_sm3 (32B)", "body_md5 (16B)", "khronos_le (4B)"],
        "d4_msg": "msg52 (52B)",
        "d4_old": "旧版 ≤40.x · 内容驱动",
        "d4_old_steps": ["52B 混合函数", "slot 0–15", "slot % 3 → 3 族", "20B 直接输出"],
        "d4_old_sub": "SHA-256 / Whirlpool / MD5；每分支独立常数与轮次",
        "d4_new": "新版 41.1 / 41.2 · khronos 驱动",
        "d4_new_steps": ["slot = (khronos ^ 52) & 15", "slot & 3 → 4 族", "32B → 16B core + 4B 尾", "20B field13"],
        "d4_new_sub": "SHA-256 / Whirlpool / BLAKE2b / MD5；常数由 khronos 旋转派生",
        "d4_warn": "两版不可混用：请求版本号与 field13 派生必须匹配，否则服务端重算必然不一致。",
    },
    "en": {
        "d1_title": "Three-layer risk-control model",
        "d1_sub": "If any layer fails, the request is downgraded. The common failure is inconsistent state, not a broken algorithm.",
        "d1_layers": [
            ("Device", "Is the device real, and is its identity trustworthy?", ["fingerprint", "SDI token", "TicketGuard"], BLUE),
            ("Network", "Does the connection look like a genuine client?", ["TLS profile", "HTTP/2", "cronet version"], GREEN),
            ("Behavior", "Are timing and state self-consistent?", ["signature headers", "clock consistency", "session state"], AMBER),
        ],
        "d1_result": "Decision & downgrade",
        "d1_result_items": ["empty page", "captcha", "rate limit", "hard reject"],
        "d1_note": "All three layers are ANDed: real device + real link + consistent behavior.",
        "d2_title": "How device identity is exchanged",
        "d2_sub": "Registration trades local declarations plus a full fingerprint for server-issued identity and credentials.",
        "d2_left": "Local declarations (client-generated)",
        "d2_left_items": [("openudid", "device-level · first report"), ("cdid", "install-level · uppercase UUID")],
        "d2_right": "Server-issued (trust in the declaration)",
        "d2_right_items": [("device_id", "device-level · long-lived"), ("iid", "install-level"), ("sec_device_token", "device-level credential")],
        "d2_req": "register: IDs + fingerprint",
        "d2_resp": "response: identity + token",
        "d2_note": "One-way trust: device_id / iid cannot be forged locally; changing the app version rebuilds the token system.",
        "d3_title": "Cold-start registration chain",
        "d3_sub": "A full cold registration follows a strict order; the ordering itself is modeled by the server.",
        "d3_steps": [
            ("1", "device_register", "obtain device_id / iid (klink.amemv.com)", "identity"),
            ("2", "device_report", "Perseus device report", "report"),
            ("3", "app_log", "first-launch events (Sword encoding)", "events"),
            ("4", "get_token", "SDI token issuance", "token"),
            ("5", "activate / activate_record", "activation status report", "activate"),
            ("6", "birth()", "nurture chain (app_log / stats / alert)", "nurture"),
        ],
        "d3_note": "Order is a contract: out-of-order calls may not fail, but they enter the long-term profile and lower later request weight.",
        "d4_title": "Medusa field13: two generations",
        "d4_sub": "The input is a fixed 52-byte message; old builds pick the branch from content, 41.1/41.2 pick it from khronos.",
        "d4_inputs": ["query_sm3 (32B)", "body_md5 (16B)", "khronos_le (4B)"],
        "d4_msg": "msg52 (52B)",
        "d4_old": "Old ≤40.x · content-driven",
        "d4_old_steps": ["52B mix function", "slot 0–15", "slot % 3 → 3 families", "20B output"],
        "d4_old_sub": "SHA-256 / Whirlpool / MD5; per-branch constants and rounds",
        "d4_new": "New 41.1 / 41.2 · khronos-driven",
        "d4_new_steps": ["slot = (khronos ^ 52) & 15", "slot & 3 → 4 families", "32B → 16B core + 4B tail", "20B field13"],
        "d4_new_sub": "SHA-256 / Whirlpool / BLAKE2b / MD5; constants derived by khronos rotation",
        "d4_warn": "Never mix generations: the request version and the field13 derivation must match, or the server recomputation will disagree.",
    },
}


def diagram_layers(t):
    w, h = 980, 470
    b = [text(40, 44, t["d1_title"], 24, INK, 700), text(40, 72, t["d1_sub"], 13, MUTED)]
    for i, (name, desc, chips, color) in enumerate(t["d1_layers"]):
        y = 100 + i * 92
        b.append(rect(44, y, 640, 76, "#f8fafc", color, 12))
        b.append(rect(44, y, 7, 76, color, color, 3))
        b.append(text(68, y + 31, name, 16, INK, 700))
        b.append(text(68, y + 55, desc, 12.5, MUTED))
        for j, c in enumerate(chips):
            b.append(chip(350 + j * 106, y + 22, 98, 32, c, "#ffffff", color, INK, 11.5))
        b.append(line(684, y + 38, 736, y + 38, color, 1.6, "arrGray", "4 3"))
    b.append(line(736, 138, 736, 322, BLUE, 2))
    b.append(text(752, 240, "AND", 15, BLUE, 800))
    b.append(rect(788, 100, 150, 260, BLUE_SOFT, BLUE, 12))
    result_label = t["d1_result"]
    result_size = 15 if len(result_label) <= 10 else 12.5
    b.append(text(863, 128, result_label, result_size, BLUE, 700, "middle"))
    for i, item in enumerate(t["d1_result_items"]):
        b.append(chip(802, 148 + i * 48, 122, 34, item, "#ffffff", "#93c5fd", INK, 11))
    b.append(rect(44, 394, 894, 48, "#fff7ed", "#fdba74", 10))
    b.append(text(64, 424, t["d1_note"], 13.5, "#7c2d12", 600))
    return svg(w, h, t["d1_title"], "\n".join(b))


def diagram_identity(t):
    w, h = 980, 430
    b = [text(40, 44, t["d2_title"], 24, INK, 700), text(40, 72, t["d2_sub"], 13, MUTED)]
    b.append(rect(50, 108, 340, 210, "#f8fafc", BLUE, 14))
    b.append(text(70, 140, t["d2_left"], 15, BLUE, 700))
    for i, (name, desc) in enumerate(t["d2_left_items"]):
        y = 162 + i * 70
        b.append(rect(70, y, 300, 54, "#ffffff", "#93c5fd", 8, 1.2))
        b.append(text(220, y + 23, name, 13, INK, 600, "middle", True))
        b.append(text(220, y + 42, desc, 10.5, MUTED, 400, "middle"))
    b.append(rect(590, 108, 340, 210, "#ecfdf5", GREEN, 14))
    b.append(text(610, 140, t["d2_right"], 15, GREEN, 700))
    for i, (name, desc) in enumerate(t["d2_right_items"]):
        y = 158 + i * 52
        b.append(rect(610, y, 300, 42, "#ffffff", "#86efac", 8, 1.2))
        b.append(text(760, y + 18, name, 12.5, INK, 600, "middle", True))
        b.append(text(760, y + 33, desc, 10, MUTED, 400, "middle"))
    b.append(line(390, 175, 590, 175, BLUE, 2))
    b.append(text(490, 163, t["d2_req"], 11.5, BLUE, 600, "middle"))
    b.append(line(590, 265, 390, 265, GREEN, 2, "arrGreen"))
    b.append(text(490, 253, t["d2_resp"], 11.5, GREEN, 600, "middle"))
    b.append(rect(50, 348, 880, 48, "#eff6ff", "#93c5fd", 10))
    b.append(text(70, 378, t["d2_note"], 13.5, "#1e3a8a", 600))
    return svg(w, h, t["d2_title"], "\n".join(b))


def diagram_registration(t):
    w, h = 980, 600
    b = [text(40, 44, t["d3_title"], 24, INK, 700), text(40, 72, t["d3_sub"], 13, MUTED)]
    b.append(line(92, 106, 92, 512, "#93c5fd", 2, None))
    for i, (num, name, detail, tag) in enumerate(t["d3_steps"]):
        y = 112 + i * 66
        b.append(f'<circle cx="92" cy="{y + 24}" r="15" fill="{BLUE}" />')
        b.append(text(92, y + 29, num, 13, "#ffffff", 700, "middle"))
        b.append(rect(126, y, 520, 50, "#f8fafc", "#cbd5e1", 9))
        b.append(text(146, y + 22, name, 13, INK, 700, mono=True))
        b.append(text(146, y + 40, detail, 11, MUTED, mono=False))
        b.append(chip(674, y + 9, 92, 30, tag, BLUE_SOFT, "#93c5fd", BLUE, 10.5))
    b.append(rect(40, 528, 900, 50, "#fff7ed", "#fdba74", 10))
    b.append(text(60, 559, t["d3_note"], 13, "#7c2d12", 600))
    return svg(w, h, t["d3_title"], "\n".join(b))


def diagram_field13(t):
    w, h = 1040, 620
    b = [text(40, 44, t["d4_title"], 24, INK, 700), text(40, 72, t["d4_sub"], 13, MUTED)]
    b.append(rect(726, 88, 220, 64, BLUE_SOFT, BLUE, 10))
    b.append(text(836, 127, t["d4_msg"], 14, BLUE, 700, "middle", True))

    xs = [40, 270, 500]
    for i, label in enumerate(t["d4_inputs"]):
        b.append(chip(xs[i], 92, 200, 54, label, "#f8fafc", "#93c5fd", INK, 12, True))
        b.append(line(xs[i] + 100, 146, xs[i] + 100, 168, "#93c5fd", 1.5, None))
    b.append(line(140, 168, 836, 168, "#93c5fd", 1.5, None))
    b.append(line(836, 168, 836, 155, BLUE, 1.8, "arr"))

    b.append(rect(40, 190, 960, 130, AMBER_SOFT, "#fcd34d", 12))
    b.append(text(60, 220, t["d4_old"], 15, AMBER, 700))
    old_w = [170, 120, 170, 160]
    old_x = [60, 260, 410, 600]
    for i, label in enumerate(t["d4_old_steps"]):
        b.append(chip(old_x[i], 238, old_w[i], 42, label, "#ffffff", "#fbbf24", INK, 11, i in (0, 1, 2)))
        if i < 3:
            b.append(line(old_x[i] + old_w[i], 259, old_x[i + 1] - 6, 259, AMBER, 1.6, "arrAmber"))
    b.append(text(60, 306, t["d4_old_sub"], 11.5, "#92400e"))

    b.append(rect(40, 344, 960, 142, GREEN_SOFT, "#6ee7b7", 12))
    b.append(text(60, 374, t["d4_new"], 15, GREEN, 700))
    new_w = [210, 140, 210, 140]
    new_x = [60, 300, 470, 710]
    for i, label in enumerate(t["d4_new_steps"]):
        b.append(chip(new_x[i], 392, new_w[i], 42, label, "#ffffff", "#34d399", INK, 11, i in (0, 1, 2)))
        if i < 3:
            b.append(line(new_x[i] + new_w[i], 413, new_x[i + 1] - 6, 413, GREEN, 1.6, "arrGreen"))
    b.append(text(60, 470, t["d4_new_sub"], 11.5, "#065f46"))

    b.append(rect(40, 506, 960, 46, RED_SOFT, "#fca5a5", 10))
    b.append(text(60, 535, t["d4_warn"], 12.5, "#7f1d1d", 600))
    return svg(w, h, t["d4_title"], "\n".join(b))


def main():
    builders = {
        "risk_layers.svg": diagram_layers,
        "identity_exchange.svg": diagram_identity,
        "registration_sequence.svg": diagram_registration,
        "medusa_field13.svg": diagram_field13,
    }
    for lang in ("zh", "en"):
        out = ROOT / "src" / lang / "svg"
        out.mkdir(parents=True, exist_ok=True)
        for name, build in builders.items():
            (out / name).write_text(build(T[lang]), encoding="utf-8")
            print(f"wrote src/{lang}/svg/{name}")


if __name__ == "__main__":
    main()
