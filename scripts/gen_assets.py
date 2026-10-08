# -*- coding: utf-8 -*-
import html, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
os.makedirs(OUT, exist_ok=True)

# Palette (blue / cyan)
BG1, BG2 = "#03100f", "#07201f"
CYAN, BLUE, SKY = "#40e0d0", "#14b8a6", "#99f6e4"
TXT, MUTED, DIM = "#e8fffb", "#8fb8b3", "#4d7a76"
LINE = "#1b4d4a"


def esc(s):
    return html.escape(s, quote=False)


def t(x, y, s, size=12, fill=TXT, cls="sans", weight="400", anchor="start", sp=0, extra=""):
    spacing = f' letter-spacing="{sp}"' if sp else ""
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" class="{cls}" '
            f'font-weight="{weight}" text-anchor="{anchor}"{spacing} {extra}>{esc(s)}</text>')


def defs():
    return f"""<defs>
<style>
.mono{{font-family:'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace}}
.sans{{font-family:'Segoe UI','Helvetica Neue',Arial,sans-serif}}
@keyframes pulse{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}
.pulse{{animation:pulse 2.8s ease-in-out infinite}}
@keyframes glow{{0%,100%{{stroke-opacity:.3}}50%{{stroke-opacity:1}}}}
.glow{{animation:glow 3s ease-in-out infinite}}
@keyframes flow{{to{{stroke-dashoffset:-9}}}}
.flow{{animation:flow .9s linear infinite}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
.spin{{animation:spin 8s linear infinite}}
@keyframes load{{0%{{transform:scaleX(.2)}}100%{{transform:scaleX(1)}}}}
.load{{animation:load 2.4s ease-in-out infinite alternate}}
</style>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG2}"/></linearGradient>
<linearGradient id="card" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b2b2a" stop-opacity=".92"/><stop offset="1" stop-color="#061a19" stop-opacity=".92"/></linearGradient>
<linearGradient id="acc" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{BLUE}"/></linearGradient>
<linearGradient id="accfade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset=".5" stop-color="{CYAN}"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></linearGradient>
<radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{CYAN}" stop-opacity=".28"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
<pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" fill="none" stroke="{CYAN}" stroke-opacity=".05"/></pattern>
</defs>"""


def frame(w, h, title, sub, body, title_y=52):
    c = 18
    brackets = (f'<path d="M10 {10+c}V10H{10+c} M{w-10-c} 10H{w-10}V{10+c} M10 {h-10-c}V{h-10}H{10+c} '
                f'M{w-10-c} {h-10}H{w-10}V{h-10-c}" fill="none" stroke="{CYAN}" stroke-opacity=".55" stroke-width="1.5"/>')
    head = ""
    if title:
        head = (t(w/2, title_y, title, 30, "url(#acc)", "sans", "800", "middle", 1.5) +
                t(w/2, title_y + 22, sub, 9.5, CYAN, "mono", "400", "middle", 3) +
                f'<rect x="{w/2-90}" y="{title_y+32}" width="180" height="1.5" fill="url(#accfade)"/>')
    parts = ""
    for i in range(12):
        px = (61 * i + 47) % (w - 60) + 30
        dur = 8 + (i % 5) * 2
        parts += (f'<circle cx="{px}" r="{1.2 + (i % 3) * .5}" fill="{CYAN}" opacity=".4">'
                  f'<animate attributeName="cy" from="{h}" to="0" dur="{dur}s" begin="-{i * 1.7:.1f}s" repeatCount="indefinite"/></circle>')
    scan = (f'<rect y="12" width="2" height="{h-24}" fill="{CYAN}" opacity=".3">'
            f'<animate attributeName="x" from="14" to="{w-14}" dur="10s" repeatCount="indefinite"/></rect>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">'
            f'{defs()}<rect width="{w}" height="{h}" rx="16" fill="url(#bg)"/>'
            f'<rect width="{w}" height="{h}" rx="16" fill="url(#grid)"/>'
            f'<rect x=".75" y=".75" width="{w-1.5}" height="{h-1.5}" rx="15" fill="none" stroke="{LINE}"/>'
            f'{brackets}{parts}{head}{body}{scan}</svg>')


def card(x, y, w, h, top=True):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="url(#card)" stroke="{LINE}"/>'
    if top:
        s += f'<rect x="{x+10}" y="{y}" width="{w-20}" height="3" rx="1.5" fill="url(#acc)"/>'
        d = ((int(x) * 7 + int(y) * 3) % 17) / 5
        s += (f'<rect x="{x+10}" y="{y}" width="46" height="3" rx="1.5" fill="{SKY}" opacity=".85">'
              f'<animate attributeName="x" from="{x+10}" to="{x+w-56}" dur="3.4s" begin="{d:.1f}s" repeatCount="indefinite"/></rect>')
    return s


def chip(x, y, label, w=38, h=30):
    d = ((int(x) * 5 + int(y) * 3) % 20) / 8
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#0a2423" stroke="{CYAN}" class="glow" style="animation-delay:{d:.2f}s"/>'
            + t(x + w/2, y + h/2 + 3.5, label, 9.5, CYAN, "mono", "700", "middle"))


def write(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)


# ---------------------------------------------------------------- HEADER
def header():
    w, h = 900, 250
    b = f'<ellipse cx="450" cy="110" rx="330" ry="90" fill="url(#glow)"/>'
    b += t(450, 62, "// BACKEND ENGINEER PROFILE", 10, CYAN, "mono", "400", "middle", 4)
    b += t(450, 120, "EXAR VÍQUEZ MASÍS", 44, "url(#acc)", "sans", "800", "middle", 2)
    b += t(450, 154, "Backend Developer  ·  AI-Driven Development  ·  SDD & TDD", 15, TXT, "sans", "500", "middle")
    b += f'<rect x="300" y="168" width="300" height="1.5" fill="url(#accfade)"/>'
    labels = ["JAVA", "SPRING BOOT", "MICROSERVICES", "HEXAGONAL"]
    widths = [70, 120, 130, 110]
    total = sum(widths) + 14 * (len(widths) - 1)
    x = 450 - total / 2
    for lab, wd in zip(labels, widths):
        b += (f'<rect x="{x}" y="184" width="{wd}" height="26" rx="13" fill="#0a2423" stroke="{CYAN}" stroke-opacity=".5"/>'
              + t(x + wd/2, 201, lab, 10, SKY, "mono", "700", "middle", 1.5))
        x += wd + 14
    b += t(450, 232, "ALAJUELA, COSTA RICA   //   ES: NATIVE   ·   EN: B2   //   UNIVERSIDAD NACIONAL", 8.5, DIM, "mono", "400", "middle", 2)
    scan = (f'<rect y="14" width="2" height="222" fill="{CYAN}" opacity=".35">'
            f'<animate attributeName="x" from="20" to="880" dur="7s" repeatCount="indefinite"/></rect>')
    return frame(w, h, "", "", b)


# ---------------------------------------------------------------- TECH UNIVERSE
def tech():
    w, h = 900, 500
    cols = [
        ("01 / LOGIC", "BACKEND", "APIs · Services · Security",
         ["JV", "SB", "SEC", "PY", "FA", "REST"],
         ["Java", "Spring Boot", "Spring Security", "Hibernate / JPA", "Python", "FastAPI", "REST APIs", "Role-based Auth"],
         "REQUEST FLOW", "SERVICES SYNCED"),
        ("02 / KNOWLEDGE", "DATA", "Persistence · Modeling · Migrations",
         ["SQL", "MDB", "JPA", "FLY", "ERD", "TXN"],
         ["MySQL", "MongoDB", "JPA / Hibernate", "Flyway", "Data Modeling", "Query Design", "Entities", "Migrations"],
         "DATA PIPELINE", "PERSISTENCE ONLINE"),
        ("03 / DESIGN", "ARCHITECTURE", "Patterns · Services · Events",
         ["HEX", "DDD", "EUR", "KFK", "SLD", "CLN"],
         ["Hexagonal", "Domain-Driven", "Microservices", "Eureka", "Kafka Events", "Clean Code", "SOLID", "Clean Arch."],
         "DESIGN MODE", "CLEAN BOUNDARIES"),
        ("04 / WORKFLOW", "TOOLING", "Testing · Versioning · Delivery",
         ["GIT", "PM", "DOC", "LNX", "IJ", "TDD"],
         ["Git / GitHub", "Postman", "Docker", "Linux", "IntelliJ IDEA", "TDD", "SDD", "Contract Tests"],
         "DELIVERY", "SHIPPING CONTINUOUSLY"),
    ]
    b = ""
    cw, gap, x0, y0, ch = 198, 16, 30, 100, 360
    for i, (lab, name, sub, chips, items, flabel, fval) in enumerate(cols):
        x = x0 + i * (cw + gap)
        b += card(x, y0, cw, ch)
        b += t(x + 14, y0 + 30, lab, 9, CYAN, "mono", "400", "start", 2)
        b += t(x + 14, y0 + 56, name, 19, TXT, "sans", "800")
        b += t(x + 14, y0 + 74, sub, 8.5, MUTED)
        for j, c in enumerate(chips):
            cx = x + 14 + (j % 4) * 44
            cy = y0 + 92 + (j // 4) * 38
            b += chip(cx, cy, c, 38, 30)
        b += f'<rect x="{x+14}" y="{y0+178}" width="{cw-28}" height="1" fill="{LINE}"/>'
        b += t(x + 14, y0 + 198, "CORE TOOLCHAIN", 8.5, CYAN, "mono", "400", "start", 2)
        for k, it in enumerate(items):
            ix = x + 14 + (k % 2) * 92
            iy = y0 + 220 + (k // 2) * 22
            b += t(ix, iy, it, 9.5, MUTED)
        b += f'<rect x="{x+14}" y="{y0+ch-62}" width="{cw-28}" height="1" fill="{LINE}"/>'
        b += t(x + 14, y0 + ch - 44, flabel, 8.5, CYAN, "mono", "400", "start", 2)
        b += t(x + 14, y0 + ch - 26, fval, 11, TXT, "sans", "700")
        b += f'<rect x="{x+14}" y="{y0+ch-14}" width="{cw-28}" height="3" rx="1.5" fill="{LINE}"/>'
        b += f'<rect x="{x+14}" y="{y0+ch-14}" width="{(cw-28)*0.7:.0f}" height="3" rx="1.5" fill="url(#acc)" class="load" style="transform-origin:{x+14}px {y0+ch-14}px;animation-delay:{i*0.35}s"/>'
    b += t(450, 482, "SYSTEMS CONNECTED  //  4 DOMAINS  //  SPEC-DRIVEN  //  TEST-FIRST  //  BUILD · TEST · SHIP",
           8, DIM, "mono", "400", "middle", 2)
    return frame(w, h, "TECHNOLOGY UNIVERSE", "BACKEND STACK / DATA / ARCHITECTURE / TOOLING", b)


# ---------------------------------------------------------------- ARCHITECTURE
def arch():
    w, h = 900, 540
    b = f'<ellipse cx="450" cy="215" rx="260" ry="120" fill="url(#glow)"/>'
    pills = [("CLIENT / API CONSUMER", 0), ("REST API  ·  SPRING SECURITY", 1), ("APPLICATION  +  DOMAIN CORE", 2), ("PORTS  →  ADAPTERS", 3)]
    py = 100
    for label, i in pills:
        y = py + i * 46
        b += (f'<rect x="320" y="{y}" width="260" height="34" rx="9" fill="#0a2423" stroke="{CYAN}" stroke-opacity="{.9 if i==2 else .5}"/>'
              f'<rect x="320" y="{y}" width="4" height="34" rx="2" fill="url(#acc)"/>'
              + t(450, y + 21, label, 10.5, TXT, "mono", "700", "middle", 1.5))
        if i < 3:
            b += f'<circle cx="450" cy="{y+40}" r="2.6" fill="{CYAN}" class="pulse"/>'
    b += f'<line x1="40" y1="300" x2="860" y2="300" stroke="{CYAN}" stroke-opacity=".6" stroke-dasharray="3 6" class="flow"/>'
    b += f'<circle cx="450" cy="300" r="5" fill="{CYAN}" class="pulse"/>'
    for k, path in enumerate(["M450 104 V 262", "M450 104 V 262"]):
        b += (f'<circle r="3.5" fill="{SKY}"><animateMotion dur="2.6s" begin="-{k*1.3}s" repeatCount="indefinite" path="{path}"/></circle>')
    for k, path in enumerate(["M450 300 H 40", "M450 300 H 860", "M40 300 H 450", "M860 300 H 450"]):
        b += (f'<circle r="3" fill="{SKY}" opacity=".9"><animateMotion dur="3.2s" begin="-{k*0.8}s" repeatCount="indefinite" path="{path}"/></circle>')
    cards = [
        ("01 / ENTRY", "API", "CONTROLLERS / SECURITY", ["REST Controllers", "JWT Authentication", "Role-based Access"]),
        ("02 / USE CASES", "APPLICATION", "ORCHESTRATION / PORTS", ["Use Cases", "Input / Output Ports", "Transactions"]),
        ("03 / CORE", "DOMAIN", "RULES / MODEL", ["Entities & Aggregates", "Value Objects", "Business Rules"]),
        ("04 / EDGE", "ADAPTERS", "INTEGRATIONS", ["JPA Repositories", "Kafka Events", "Service Discovery"]),
        ("05 / STORAGE", "PERSISTENCE", "DATA / MIGRATIONS", ["MySQL", "Flyway Migrations", "MongoDB"]),
    ]
    cw, gap, x0, y0, ch = 160, 10, 30, 322, 190
    for i, (lab, name, sub, lines) in enumerate(cards):
        x = x0 + i * (cw + gap)
        b += card(x, y0, cw, ch)
        b += t(x + 12, y0 + 26, lab, 8.5, CYAN, "mono", "400", "start", 1.5)
        b += (f'<circle cx="{x+cw-24}" cy="{y0+46}" r="14" fill="none" stroke="{CYAN}" stroke-opacity=".7" stroke-dasharray="5 4" '
              f'class="spin" style="transform-origin:{x+cw-24}px {y0+46}px"/>')
        b += f'<circle cx="{x+cw-24}" cy="{y0+46}" r="4" fill="{CYAN}" class="pulse"/>'
        b += t(x + 12, y0 + 62, name, 15, TXT, "sans", "800")
        b += t(x + 12, y0 + 80, sub, 7.5, MUTED, "mono", "400", "start", 1)
        b += f'<rect x="{x+12}" y="{y0+94}" width="{cw-24}" height="1" fill="{LINE}"/>'
        for k, ln in enumerate(lines):
            b += f'<rect x="{x+12}" y="{y0+114+k*22}" width="5" height="5" rx="1" fill="{CYAN}"/>'
            b += t(x + 24, y0 + 120 + k * 22, ln, 10, MUTED)
    b += t(450, 528, "CLIENT → API → APPLICATION → DOMAIN → ADAPTERS → PERSISTENCE", 8, DIM, "mono", "400", "middle", 2)
    return frame(w, h, "SYSTEM ARCHITECTURE", "HEXAGONAL / DDD / EVENT-DRIVEN / MICROSERVICES", b)


# ---------------------------------------------------------------- AI ENGINEERING
def ai():
    w, h = 900, 424
    b = f'<ellipse cx="450" cy="210" rx="120" ry="150" fill="url(#glow)"/>'
    left = ("01 / METHOD", "SPEC-DRIVEN DEV", "SPECS · TESTS · REFACTOR",
            ["Specs before code (SDD)", "Red → Green → Refactor (TDD)", "Contract testing with Postman", "Clean Code & SOLID"])
    right = ("02 / AUTOMATION", "AI-ASSISTED WORKFLOW", "MODELS · AGENTS · CONTEXT",
             ["Multi-agent orchestration", "Prompt engineering", "MCP integrations", "Human in the loop for key decisions"])
    for i, (lab, name, sub, lines) in enumerate([left, right]):
        x = 30 + i * 440
        b += card(x, 100, 410, 224)
        b += t(x + 20, 130, lab, 9, CYAN, "mono", "400", "start", 2)
        b += t(x + 20, 162, name, 21, TXT, "sans", "800")
        b += t(x + 20, 182, sub, 8.5, MUTED, "mono", "400", "start", 1.5)
        b += f'<rect x="{x+20}" y="196" width="370" height="1" fill="{LINE}"/>'
        for k, ln in enumerate(lines):
            b += f'<circle cx="{x+26}" cy="{222+k*22}" r="3" fill="{CYAN}" class="pulse" style="animation-delay:{k*0.45+i*0.2:.2f}s"/>'
            b += t(x + 40, 226 + k * 22, ln, 11.5, MUTED)
    b += f'<line x1="30" y1="334" x2="870" y2="334" stroke="{CYAN}" stroke-opacity=".5" stroke-dasharray="3 6" class="flow"/>'
    for k in range(2):
        b += (f'<circle r="3.5" fill="{SKY}"><animateMotion dur="4s" begin="-{k*2}s" repeatCount="indefinite" path="M30 334 H 870"/></circle>')
    labs = ["SDD", "TDD", "MCP", "AGENTS"]
    x = 450 - (4 * 110 + 3 * 14) / 2
    for lab in labs:
        b += (f'<rect x="{x}" y="344" width="110" height="34" rx="9" fill="#0a2423" stroke="{CYAN}" stroke-opacity=".5"/>'
              + t(x + 55, 366, lab, 11, SKY, "mono", "700", "middle", 2))
        x += 124
    b += t(450, 408, "SPEC → TEST → CODE → REVIEW  //  HUMAN-IN-THE-LOOP", 8, DIM, "mono", "400", "middle", 2)
    return frame(w, h, "AI-DRIVEN ENGINEERING", "SPECS / TESTS / AGENTS / CONTEXT", b)


# ---------------------------------------------------------------- PROJECTS
def projects():
    w, h = 900, 330
    items = [
        ("01 / FEATURED", "AegisNotify", "Resilient & Smart Notification Orchestrator",
         ["JAVA", "MICROSERVICE", "FAULT-TOLERANT"],
         ["Mission-critical notification microservice", "Centralized notification delivery", "Fault tolerance as a core requirement"]),
        ("02 / FEATURED", "Bank-project", "Banking backend · Java 24 · Spring Boot 4",
         ["HEXAGONAL", "DDD", "KAFKA", "JWT"],
         ["Accounts, cards, envelopes, transactions", "JWT authentication & Kafka events", "MySQL persistence with Flyway"]),
    ]
    b = ""
    for i, (lab, name, sub, tags, lines) in enumerate(items):
        x = 30 + i * 440
        b += card(x, 100, 410, 200)
        b += t(x + 20, 128, lab, 9, CYAN, "mono", "400", "start", 2)
        b += f'<circle cx="{x+390}" cy="124" r="4" fill="{CYAN}" class="pulse" style="animation-delay:{i*0.6}s"/>'
        b += t(x + 20, 160, name, 24, TXT, "sans", "800")
        b += t(x + 20, 180, sub, 10, MUTED)
        tx = x + 20
        for tg in tags:
            wd = 14 + len(tg) * 7.2
            b += (f'<rect x="{tx}" y="194" width="{wd:.0f}" height="22" rx="11" fill="#0a2423" stroke="{CYAN}" class="glow" style="animation-delay:{(len(tg)%5)*0.5:.1f}s"/>'
                  + t(tx + wd/2, 209, tg, 8.5, SKY, "mono", "700", "middle", 1))
            tx += wd + 8
        for k, ln in enumerate(lines):
            b += f'<circle cx="{x+26}" cy="{238+k*20}" r="2.5" fill="{CYAN}" class="pulse" style="animation-delay:{k*0.4+i*0.2:.1f}s"/>'
            b += t(x + 38, 242 + k * 20, ln, 10.5, MUTED)
    return frame(w, h, "FEATURED PROJECTS", "BACKEND SYSTEMS / OPEN SOURCE", b)


# ---------------------------------------------------------------- PRINCIPLES
def principles():
    w, h = 900, 240
    items = [("01", "SPEC FIRST", "Define behavior before code."),
             ("02", "TEST FIRST", "Red, green, refactor. Always."),
             ("03", "CLEAN DESIGN", "Hexagonal boundaries, SOLID code."),
             ("04", "SECURE BY DEFAULT", "Auth and roles in every layer."),
             ("05", "HUMAN IN LOOP", "AI accelerates. I decide.")]
    b = ""
    cw, gap, x0 = 160, 10, 30
    for i, (n, name, desc) in enumerate(items):
        x = x0 + i * (cw + gap)
        b += card(x, 96, cw, 120)
        b += f'<g class="pulse" style="animation-delay:{i*0.5}s">' + t(x + 14, 124, n, 18, CYAN, "mono", "700") + '</g>'
        b += f'<circle cx="{x+cw-18}" cy="118" r="4" fill="{CYAN}" class="pulse" style="animation-delay:{i*0.5}s"/>'
        b += t(x + cw/2, 158, name, 11.5, TXT, "sans", "800", "middle", 1)
        b += f'<rect x="{x+14}" y="170" width="{cw-28}" height="1" fill="{LINE}"/>'
        b += t(x + cw/2, 194, desc, 8.8, MUTED, "sans", "400", "middle")
    return frame(w, h, "ENGINEERING PHILOSOPHY", "PRINCIPLES FOR SYSTEMS THAT LAST", b)


if __name__ == "__main__":
    write("header.svg", header())
    write("tech-universe.svg", tech())
    write("architecture.svg", arch())
    write("ai-engineering.svg", ai())
    write("projects.svg", projects())
    write("principles.svg", principles())
    print("ok")
