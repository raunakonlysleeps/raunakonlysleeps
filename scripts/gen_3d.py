"""Generates the animated pseudo-3D SVGs used in the profile README.
GitHub strips JS from READMEs, so the 3D motion is precomputed projections
animated with SMIL/CSS, which GitHub renders inside <img>."""
import math, random
random.seed(7)
F = "Arial,Helvetica,sans-serif"; M = "Consolas,monospace"

def rot(p, ax, ay):
    x, y, z = p
    y, z = y*math.cos(ax)-z*math.sin(ax), y*math.sin(ax)+z*math.cos(ax)
    x, z = x*math.cos(ay)+z*math.sin(ay), -x*math.sin(ay)+z*math.cos(ay)
    return x, y, z

def proj(p, cx, cy, s, d=4.0):
    x, y, z = p; k = s*d/(d+z)
    return cx+x*k, cy+y*k

def spin_paths(verts, edges, cx, cy, s, n=60, tilt=0.45):
    """animated <path d> per edge for a full Y rotation."""
    out = []
    for a, b in edges:
        ds = []
        for i in range(n+1):
            ay = 2*math.pi*i/n
            pa = proj(rot(verts[a], tilt, ay), cx, cy, s)
            pb = proj(rot(verts[b], tilt, ay), cx, cy, s)
            ds.append(f"M{pa[0]:.1f} {pa[1]:.1f}L{pb[0]:.1f} {pb[1]:.1f}")
        out.append(ds)
    return out

cube = [(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
cedges = [(i, j) for i in range(8) for j in range(i+1, 8)
          if sum(a != b for a, b in zip(cube[i], cube[j])) == 1]
inner = [(x*.5, y*.5, z*.5) for x, y, z in cube]
tv = cube + inner
tedges = cedges + [(a+8, b+8) for a, b in cedges] + [(i, i+8) for i in range(8)]

def anim_edges(verts, edges, cx, cy, s, dur, color, width, tilt=.45, op=1):
    g = []
    for ds in spin_paths(verts, edges, cx, cy, s, tilt=tilt):
        g.append(f'<path d="{ds[0]}" stroke="{color}" stroke-width="{width}" stroke-linecap="round" opacity="{op}">'
                 f'<animate attributeName="d" dur="{dur}s" repeatCount="indefinite" values="{";".join(ds)}"/></path>')
    return "".join(g)

# ---------------- banner ----------------
W, H = 1200, 420
stars = "".join(
    f'<circle cx="{random.randint(0,W)}" cy="{random.randint(0,H)}" r="{random.choice([.8,1.2,1.6])}" fill="#fff">'
    f'<animate attributeName="opacity" values=".1;.9;.1" dur="{random.uniform(2,6):.1f}s" begin="{random.uniform(0,4):.1f}s" repeatCount="indefinite"/></circle>'
    for _ in range(70))
# perspective floor grid
floor = []
hz, vx = 300, 600
for i in range(-14, 15):
    floor.append(f'<line x1="{vx}" y1="{hz}" x2="{vx+i*120}" y2="{H}" />')
floor_h = "".join(f'<line x1="0" y1="{hz+o}" x2="{W}" y2="{hz+o}"><animate attributeName="y1" values="{hz+o};{hz+o2}" dur="2s" repeatCount="indefinite"/><animate attributeName="y2" values="{hz+o};{hz+o2}" dur="2s" repeatCount="indefinite"/></line>'
                  for o, o2 in [(2,6),(6,14),(14,28),(28,52),(52,90),(90,130)])
tags = ["PYTHON", "LUA / LUAU", "JAVA", "FIVEM", "ROBLOX", "MINECRAFT MODS", "WEB", "C++"]
ticker = "   ◆   ".join(tags*2)
banner = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img"><title>Raunak 3D banner</title>
<defs><linearGradient id="bg" x2="0" y2="1"><stop stop-color="#070a18"/><stop offset=".7" stop-color="#160d2c"/><stop offset="1" stop-color="#2a0f3a"/></linearGradient>
<radialGradient id="sun" cx=".5" cy=".5"><stop stop-color="#afffd1" stop-opacity=".5"/><stop offset="1" stop-color="#8855ff" stop-opacity="0"/></radialGradient>
<linearGradient id="fl" x2="0" y2="1"><stop stop-color="#c58bff" stop-opacity="0"/><stop offset="1" stop-color="#c58bff" stop-opacity=".55"/></linearGradient>
<linearGradient id="txt" x2="1"><stop stop-color="#faf8ff"/><stop offset=".5" stop-color="#afffd1"/><stop offset="1" stop-color="#c3a0ff"/>
<animate attributeName="x1" values="0;1;0" dur="6s" repeatCount="indefinite"/></linearGradient>
<clipPath id="r"><rect width="{W}" height="{H}" rx="24"/></clipPath>
<filter id="gl"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<g clip-path="url(#r)"><rect width="{W}" height="{H}" fill="url(#bg)"/>{stars}
<circle cx="930" cy="190" r="230" fill="url(#sun)"/>
<g stroke="url(#fl)" stroke-width="1">{''.join(floor)}</g><g stroke="#c58bff" stroke-opacity=".35">{floor_h}</g>
<g fill="none" filter="url(#gl)">{anim_edges(tv, tedges, 930, 185, 70, 12, "#afffd1", 2.2)}</g>
<g fill="none" opacity=".55">{anim_edges(cube, cedges, 1110, 90, 18, 5, "#c3a0ff", 1.5, tilt=.8)}{anim_edges(cube, cedges, 770, 70, 13, 7, "#ff9ecf", 1.3, tilt=-.6)}</g>
<text x="48" y="40" font-family="{M}" font-size="12" fill="#9b9fba" letter-spacing="2">RAUNAK // CREATIVE DEVELOPER // GAME BUILDER</text>
<text x="54" y="100" font-family="{F}" font-size="15" fill="#afffd1" font-weight="700" letter-spacing="4">THE IDEAS DON’T SLEEP.</text>
<text x="45" y="205" font-family="{F}" font-size="112" fill="url(#txt)" font-weight="800" letter-spacing="-7">RAUNAK</text>
<text x="54" y="248" font-family="{F}" font-size="24" fill="#cfc4ee">Web, servers &amp; game worlds — Roblox, Minecraft, FiveM.</text>
<text x="56" y="285" font-family="{M}" font-size="17" fill="#afffd1">&gt; building<tspan>_<animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite" calcMode="discrete"/></tspan></text>
<rect x="0" y="378" width="{W}" height="42" fill="#0b0716" opacity=".85"/>
<text y="405" font-family="{M}" font-size="15" fill="#c3a0ff" letter-spacing="3">{ticker}   ◆   {ticker}<animate attributeName="x" from="20" to="-1490" dur="22s" repeatCount="indefinite"/></text>
</g><rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="24" fill="none" stroke="#3a2f5c"/></svg>'''
open("assets/raunak-banner-3d.svg", "w").write(banner)

# ---------------- game worlds ----------------
def iso(x, y, z, ox, oy, s):
    return ox+(x-y)*s*0.866, oy+(x+y)*s*0.5-z*s

def poly(pts, fill, extra=""):
    return f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a,b in pts)}" fill="{fill}" {extra}/>'

def block(ox, oy, s, top, left, right, px=4, tex=None):
    """isometric voxel block with pixel-texture faces."""
    out = []
    n = px
    for i in range(n):
        for j in range(n):
            c = top[(i*7+j*3) % len(top)] if tex is None else tex("t", i, j)
            out.append(poly([iso(i/n, j/n, 1, ox, oy, s), iso((i+1)/n, j/n, 1, ox, oy, s),
                             iso((i+1)/n, (j+1)/n, 1, ox, oy, s), iso(i/n, (j+1)/n, 1, ox, oy, s)], c))
            cl = tex("l", i, j) if tex else left[(i+j*5) % len(left)]
            out.append(poly([iso(i/n, 1, 1-j/n, ox, oy, s), iso((i+1)/n, 1, 1-j/n, ox, oy, s),
                             iso((i+1)/n, 1, 1-(j+1)/n, ox, oy, s), iso(i/n, 1, 1-(j+1)/n, ox, oy, s)], cl))
            cr = tex("r", i, j) if tex else right[(i*3+j) % len(right)]
            out.append(poly([iso(1, i/n, 1-j/n, ox, oy, s), iso(1, (i+1)/n, 1-j/n, ox, oy, s),
                             iso(1, (i+1)/n, 1-(j+1)/n, ox, oy, s), iso(1, i/n, 1-(j+1)/n, ox, oy, s)], cr))
    return "".join(out)

grassT = ["#6fbf3f", "#5aa832", "#7ccc4a", "#4f9a2c"]
def grass(face, i, j):
    if face == "t": return grassT[(i*7+j*3) % 4]
    dirt = ["#8a5a33", "#7a4e2c", "#9b6a3d", "#6d4426"]
    if j == 0 or (j == 1 and (i*5) % 3 == 0): return ["#5aa832","#4f9a2c"][i % 2] if face == "l" else ["#4c8f2a","#437f25"][i % 2]
    c = dirt[(i*3+j*5) % 4]
    return c if face == "l" else c.replace("#", "#") and dirt[(i+j) % 4]
def shade(face, cols):
    return lambda f, i, j: cols[f][(i*5+j*3) % len(cols[f])]
stone = shade(None, {"t": ["#9a9a9a","#8a8a8a","#a8a8a8","#7d7d7d"], "l": ["#7f7f7f","#707070","#8c8c8c"], "r": ["#636363","#585858","#6e6e6e"]})
diamond = shade(None, {"t": ["#8a8a8a","#5ff0e8","#8a8a8a","#9a9a9a","#2fd4cc"], "l": ["#707070","#3fc8c0","#7f7f7f"], "r": ["#5a5a5a","#2aa8a0","#636363"]})

def bob(content, dur, amp, begin=0):
    return f'<g>{content}<animateTransform attributeName="transform" type="translate" values="0 0;0 -{amp};0 0" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></g>'

# blocky avatar (generic, own design) built from iso cuboids
def cuboid(x, y, z, w, d, h, ox, oy, s, ct, cl, cr):
    P = lambda a, b, c: iso(a, b, c, ox, oy, s)
    return (poly([P(x,y,z+h),P(x+w,y,z+h),P(x+w,y+d,z+h),P(x,y+d,z+h)], ct) +
            poly([P(x,y+d,z+h),P(x+w,y+d,z+h),P(x+w,y+d,z),P(x,y+d,z)], cl) +
            poly([P(x+w,y,z+h),P(x+w,y+d,z+h),P(x+w,y+d,z),P(x+w,y,z)], cr))
def avatar(ox, oy, s):
    parts = [  # back-to-front draw order
        (-.45,.25,1.0,.42,.5,1.0, "#f4c99b","#e0b383","#c79a6c"),   # back arm
        (0,.25,0,.45,.5,1.0, "#3b4bd6","#2f3db0","#25318e"),       # legs
        (.5,.25,0,.45,.5,1.0, "#3b4bd6","#2f3db0","#25318e"),
        (0,.25,1.0,.95,.5,1.0, "#ff5c8a","#e04a75","#b83a5f"),      # torso
        (.2,.2,2.0,.6,.6,.6, "#f4c99b","#e0b383","#c79a6c"),        # head
        (.98,.25,1.0,.42,.5,1.0, "#f4c99b","#e0b383","#c79a6c"),    # front arm
    ]
    g = "".join(cuboid(*p[:6], ox, oy, s, *p[6:]) for p in parts)
    # face on head right-side
    fx, fy = iso(.8, .38, 2.42, ox, oy, s); fx2, fy2 = iso(.8, .62, 2.42, ox, oy, s)
    g += f'<circle cx="{fx:.1f}" cy="{fy:.1f}" r="3" fill="#1b1b2b"/><circle cx="{fx2:.1f}" cy="{fy2:.1f}" r="3" fill="#1b1b2b"/>'
    mx, my = iso(.8, .5, 2.25, ox, oy, s)
    g += f'<path d="M{mx-8:.1f} {my-2:.1f}q8 7 16 0" stroke="#1b1b2b" stroke-width="2.4" fill="none"/>'
    return g

W2, H2 = 1200, 460
particles = "".join(
    f'<rect x="{random.randint(40,1160)}" y="{H2}" width="{s}" height="{s}" fill="{c}" opacity=".7">'
    f'<animate attributeName="y" values="{H2};-10" dur="{random.uniform(6,12):.1f}s" begin="{random.uniform(0,8):.1f}s" repeatCount="indefinite"/></rect>'
    for s, c in [(random.choice([4,6,8]), random.choice(["#afffd1","#c3a0ff","#5ff0e8","#7ccc4a","#ff9ecf"])) for _ in range(28)])

mc = (bob(block(300, 250, 92, None, None, None, px=8, tex=grass), 3, 12) +
      bob(block(150, 300, 56, None, None, None, px=6, tex=stone), 3.6, 8, .6) +
      bob(block(430, 310, 50, None, None, None, px=6, tex=diamond), 2.6, 10, 1.1))
# little pickaxe orbiting
pick = ('<g><g transform="translate(480 175) rotate(-35)"><rect x="-3" y="0" width="6" height="58" fill="#8a5a33"/>'
        '<path d="M-28 4 Q0 -14 28 4 L24 10 Q0 -4 -24 10Z" fill="#5ff0e8" stroke="#2aa8a0" stroke-width="2"/></g>'
        '<animateTransform attributeName="transform" type="rotate" values="-8 480 215;10 480 215;-8 480 215" dur="1.4s" repeatCount="indefinite"/></g>')

rb_plat = cuboid(0, 0, 0, 3.2, 2.4, .35, 870, 215, 46, "#7ccc4a", "#5aa832", "#4f9a2c")
rb_plat2 = cuboid(0, 0, 0, 1.2, 1.2, .35, 1060, 165, 44, "#c3a0ff", "#9d7ae0", "#7d5eb0")
coin = '<g><ellipse cx="1095" cy="130" rx="14" ry="14" fill="#ffd34d" stroke="#e0a800" stroke-width="3"><animate attributeName="rx" values="14;2;14" dur="1.6s" repeatCount="indefinite"/></ellipse></g>'
rb = (rb_plat + bob(rb_plat2 + coin, 2.8, 14, .4) +
      f'<g>{avatar(880, 300, 40)}<animateTransform attributeName="transform" type="translate" values="0 0;0 -38;0 0;0 0" keyTimes="0;.25;.5;1" dur="2.2s" repeatCount="indefinite"/></g>')

def card(x, title, sub, lines, accent):
    l = "".join(f'<text x="{x+26}" y="{392+i*22}" font-family="{M}" font-size="14" fill="#cfc4ee">{t}</text>' for i, t in enumerate(lines))
    return (f'<text x="{x+26}" y="58" font-family="{F}" font-size="30" font-weight="800" fill="#faf8ff">{title}</text>'
            f'<text x="{x+26}" y="84" font-family="{M}" font-size="13" fill="{accent}" letter-spacing="2">{sub}</text>{l}')

games = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W2}" height="{H2}" viewBox="0 0 {W2} {H2}" role="img"><title>Game worlds</title>
<defs><linearGradient id="g1" x2="1" y2="1"><stop stop-color="#0b1020"/><stop offset="1" stop-color="#17102b"/></linearGradient>
<clipPath id="r"><rect width="{W2}" height="{H2}" rx="24"/></clipPath></defs>
<g clip-path="url(#r)"><rect width="{W2}" height="{H2}" fill="url(#g1)"/>{particles}
<rect x="600" y="0" width="600" height="{H2}" fill="#1a0f30" opacity=".6"/>
<line x1="600" y1="30" x2="600" y2="{H2-30}" stroke="#3a2f5c" stroke-dasharray="4 8"/>
{card(0, "Minecraft Mods", "JAVA // MODDING // CUSTOM BLOCKS &amp; ITEMS", ["▸ new blocks, items &amp; mechanics", "▸ gameplay tweaks that feel vanilla+"], "#7ccc4a")}
{mc}{pick}
{card(600, "Roblox Games", "LUAU // ROBLOX STUDIO // GAME DESIGN", ["▸ obbies, systems &amp; game loops", "▸ scripting UI, data &amp; multiplayer"], "#ff9ecf")}
{rb}
</g><rect x=".5" y=".5" width="{W2-1}" height="{H2-1}" rx="24" fill="none" stroke="#3a2f5c"/></svg>'''
open("assets/game-worlds.svg", "w").write(games)
print("ok")
