"""Draw the sea train as an editable, self-contained animated SVG."""

import base64
import math
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/chihiro-sea-train.svg"
SPEED = 140


def wheel(x, y, radius):
    period = math.tau * radius / SPEED
    return f'''<g transform="translate({x} {y})">
      <circle r="{radius}" fill="#163544" stroke="#9fb1af" stroke-width="3"/>
      <circle r="{radius-5}" fill="#234b59" stroke="#0f2f3c" stroke-width="2"/>
      <g>
        <path d="M0 -{radius-5}V{radius-5}M-{radius-5} 0H{radius-5}M-{(radius-5)*.707:.2f} -{(radius-5)*.707:.2f}L{(radius-5)*.707:.2f} {(radius-5)*.707:.2f}M-{(radius-5)*.707:.2f} {(radius-5)*.707:.2f}L{(radius-5)*.707:.2f} -{(radius-5)*.707:.2f}" stroke="#c1b799" stroke-width="2.4"/>
        <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="{period:.7f}s" repeatCount="indefinite"/>
      </g>
      <circle r="4" fill="#d9b575"/>
    </g>'''


def coach(x, portrait=False):
    bits = [f'''<g transform="translate({x} 0)">
      <path d="M2 326Q3 313 19 313H237Q253 313 254 326Z" fill="#193b48" stroke="#102f3e" stroke-width="2"/>
      <path d="M7 327H248V416Q246 423 238 423H17Q9 423 7 416Z" fill="url(#car-paint)" stroke="#1d3e48" stroke-width="2"/>
      <path d="M10 398H246V409H10Z" fill="#a84f44"/>
      <path d="M12 330H244M12 411H244" stroke="#ffe4ad" stroke-width="2" opacity=".8"/>
      <path d="M18 332V395M72 332V395M129 332V395M186 332V395M243 332V395" stroke="#a97a4e" stroke-width="1" opacity=".45"/>
      <path d="M15 425H241" stroke="#173745" stroke-width="7"/>
      <path d="M82 423V434M178 423V434" stroke="#183845" stroke-width="6"/>
      <path d="M-8 413H7M248 413H264" stroke="#203c46" stroke-width="4"/>
    ''']
    for index, wx in enumerate((21, 78, 135, 192)):
        bits.append(f'<rect x="{wx}" y="339" width="43" height="50" rx="5" fill="#ffe2a3" stroke="#6e634f" stroke-width="2"/>')
        if portrait and index == 1:
            bits.append(f'<image x="{wx+2}" y="341" width="39" height="46" preserveAspectRatio="xMidYMid slice" href="{{AVATAR}}" clip-path="url(#avatar-window)"/>')
            bits.append(f'<path d="M{wx+2} 345H{wx+41}V387H{wx+2}Z" fill="#ffd594" opacity=".12"/>')
        else:
            bits.append(f'<path d="M{wx+3} 346H{wx+40}V385H{wx+3}Z" fill="url(#window-light)"/>')
            bits.append(f'<path d="M{wx+7} 381V365Q{wx+14} 350 {wx+21} 365V381M{wx+26} 381V369Q{wx+32} 357 {wx+37} 369V381" fill="#bc8a62" opacity=".32"/>')
        bits.append(f'<path d="M{wx+5} 344H{wx+38}" stroke="#fff0c9" opacity=".65"/>')
    bits += [wheel(63, 443, 18), wheel(191, 443, 18)]
    bits.append('<path d="M83 414H172" stroke="#f8ce8c" stroke-width="1"/><text x="127" y="419" text-anchor="middle" font-family="serif" font-size="8" fill="#613f3b">海の向こう</text></g>')
    return "".join(bits)


def build():
    avatar_path = ROOT / "assets/chihiro-avatar.png"
    avatar_format = Image.open(avatar_path).format.lower().replace("jpg", "jpeg")
    avatar = f"data:image/{avatar_format};base64," + base64.b64encode(avatar_path.read_bytes()).decode()
    cars = coach(0) + coach(267, portrait=True) + coach(534)
    engine_wheels = "".join(wheel(x, 434, 27) for x in (886, 952, 1018)) + wheel(1100, 443, 18)
    rod_period = math.tau * 27 / SPEED
    steam = "".join(f'''<g opacity="0">
      <ellipse cx="1040" cy="291" rx="15" ry="8" fill="#f9e6c5"/>
      <ellipse cx="1054" cy="286" rx="13" ry="12" fill="#f9e6c5"/>
      <animateTransform attributeName="transform" type="translate" values="0 0;-336 -112" dur="2.4s" begin="-{i*.6}s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0;.65;.35;0" keyTimes="0;.1;.6;1" dur="2.4s" begin="-{i*.6}s" repeatCount="indefinite"/>
    </g>''' for i in range(4))
    ripples = []
    for row in range(8):
        y = 492 + row*14
        width = 70 + row*9
        pieces = "".join(f'<path d="M{x} {y}h{width}"/>' for x in range(-300, 1900, 240))
        duration = (10, 5, 4)[row % 3]
        ripples.append(f'<g fill="none" stroke="#e3b892" stroke-width="{1+row*.12}" opacity="{.11+row*.012}">{pieces}<animateTransform attributeName="transform" type="translate" from="0 0" to="-240 0" dur="{duration}s" repeatCount="indefinite"/></g>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1600" height="640" viewBox="0 0 1600 640" role="img" aria-labelledby="title desc">
  <title id="title">千尋 — a sea train for wangshen233</title>
  <desc id="desc">An original vector sea railway at sunset. A golden train travels across the frame, with rotating wheels, mechanically linked coupling rods, drifting steam and moving water. The profile avatar rides in a passenger window.</desc>
  <defs>
    <linearGradient id="sky" x2="0" y2="1"><stop stop-color="#24495f"/><stop offset=".54" stop-color="#73808a"/><stop offset="1" stop-color="#edb798"/></linearGradient>
    <linearGradient id="sea" x2="0" y2="1"><stop stop-color="#789392"/><stop offset=".26" stop-color="#3f747e"/><stop offset="1" stop-color="#153f55"/></linearGradient>
    <linearGradient id="car-paint" x2="0" y2="1"><stop stop-color="#f3ce88"/><stop offset="1" stop-color="#d6a15c"/></linearGradient>
    <linearGradient id="window-light" x2="0" y2="1"><stop stop-color="#ffe9b8"/><stop offset="1" stop-color="#dbab74"/></linearGradient>
    <linearGradient id="boiler" x2="0" y2="1"><stop stop-color="#476b71"/><stop offset=".4" stop-color="#234b57"/><stop offset="1" stop-color="#173744"/></linearGradient>
    <radialGradient id="sun-halo"><stop stop-color="#f8d6ac" stop-opacity=".24"/><stop offset="1" stop-color="#f8d6ac" stop-opacity="0"/></radialGradient>
    <filter id="paper" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".78" numOctaves="3" stitchTiles="stitch" seed="12"/><feColorMatrix type="saturate" values="0"/><feColorMatrix type="matrix" values="1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 .045 0"/></filter>
    <clipPath id="frame"><rect width="1600" height="640" rx="12"/></clipPath>
    <clipPath id="avatar-window"><rect x="80" y="341" width="39" height="46" rx="3"/></clipPath>
    <clipPath id="water"><rect y="464" width="1600" height="176"/></clipPath>
    <pattern id="sleepers" width="30" height="10" patternUnits="userSpaceOnUse"><path d="M8 0V10" stroke="#a8ab9b" stroke-width="6"/></pattern>
    <g id="cloud" fill="#e4d7c6"><path d="M0 24Q14 16 37 19Q49 0 75 7Q91 -7 112 9Q132 4 151 19Q177 13 194 24Z"/></g>
    <g id="crane" fill="none" stroke="#f8e8c9" stroke-width="1.3" stroke-linejoin="round"><path d="M0 0L-22 -20L-7 5L2 2L9 10L18 -26L3 -4L0 0L-7 5M2 2L18 -26M-7 5L-22 -20"/></g>
  </defs>
  <g clip-path="url(#frame)">
    <rect width="1600" height="640" fill="url(#sky)"/>
    <circle cx="1240" cy="237" r="181" fill="url(#sun-halo)"/>
    <circle cx="1240" cy="237" r="62" fill="#f5c79e"/>
    <path d="M1183 260H1297M1181 269H1300M1189 280H1290" stroke="#d6a28c" stroke-width="4"/>
    <g opacity=".22"><use href="#cloud" transform="translate(478 105) scale(1.55 .64)"/><use href="#cloud" transform="translate(1045 110) scale(1.3 .55)"/></g>
    <g opacity=".28"><use href="#cloud" transform="translate(757 179) scale(1.1 .5)"/><use href="#cloud" transform="translate(1347 176) scale(1.4 .7)"/></g>
    <path d="M0 350Q110 333 193 348Q253 317 304 348Q383 341 440 356H0M1075 356Q1139 337 1192 348Q1230 325 1271 347Q1343 331 1435 350Q1518 331 1600 342V365H1075" fill="#4e7179" opacity=".5"/>
    <rect y="357" width="1600" height="283" fill="url(#sea)"/>
    <path d="M0 360H1600" stroke="#dfc4a6" opacity=".55"/>
    <g stroke="#f4c698" stroke-width="3" opacity=".25"><path d="M1219 370h43M1200 381h79M1190 394h97M1171 408h133M1160 423h155"/></g>
    <g opacity=".8">
      <use href="#crane" transform="translate(1030 136) rotate(-13) scale(1.2)"/>
      <use href="#crane" transform="translate(1120 96) rotate(8) scale(.64)"/>
      <use href="#crane" transform="translate(950 187) rotate(14) scale(.74)"/>
      <use href="#crane" transform="translate(1174 137) rotate(9) scale(.42)"/>
    </g>
    <g font-family="'Yu Mincho','Noto Serif JP','STKaiti',serif" fill="#f7e8ce">
      <text x="78" y="147" font-size="83" font-weight="400">千尋</text>
      <text x="83" y="190" font-size="21">好奇心の、その先へ。</text>
    </g>
    <path d="M84 220H125" stroke="#e9b487" stroke-width="2"/>
    <text x="84" y="249" font-family="Georgia,serif" font-size="21" fill="#f1dfc4">wangshen233</text>
    <g fill="#294e5d" opacity=".5">
      <path d="M0 391l25-13 30 10 5 13H0M1504 386l34-11 62 12v14h-96"/>
      <path d="M23 382l1-64M22 320l12-11" fill="none" stroke="#294e5d" stroke-width="2"/>
    </g>
    <g clip-path="url(#water)">{''.join(ripples)}</g>
    <use href="#train" transform="translate(0 622.35) scale(1 -.35)" opacity=".13"/>
    <g fill="#1c4658" opacity=".7">
      {''.join(f'<path d="M{x} 469h10l5 79h-20Z"/>' for x in range(20,1650,160))}
    </g>
    <path d="M0 458H1600" stroke="#d1b28c" stroke-width="5"/>
    <rect y="460" width="1600" height="11" fill="url(#sleepers)"/>
    <path d="M0 471H1600" stroke="#173c4e" stroke-width="5"/>
    <g stroke="#263f48" fill="none">
      <path d="M1431 458V290M1424 458H1438" stroke-width="4"/>
      <path d="M1431 291Q1431 276 1416 276H1403" stroke-width="3"/>
      <path d="M1395 277H1414L1411 291H1398Z" fill="#f6d8a3" stroke-width="2"/>
      <path d="M1393 276Q1396 269 1405 269Q1413 269 1417 276Z" fill="#263f48"/>
    </g>
    <g id="train">
      <animateTransform attributeName="transform" type="translate" from="-1200 0" to="1600 0" dur="20s" begin="-8.5s" repeatCount="indefinite"/>
      <path d="M7 458H1148" stroke="#163644" stroke-width="4" opacity=".35"/>
      {cars}
      <g id="engine">
        <path d="M794 418H1138V429H794Z" fill="#143544"/>
        <path d="M806 307H871V413H806Z" fill="#d6a160" stroke="#173b49" stroke-width="2"/>
        <path d="M795 309Q799 299 814 297H868Q877 298 882 309Z" fill="#163847" stroke="#102e3c" stroke-width="2"/>
        <rect x="818" y="318" width="39" height="46" rx="4" fill="#ffd99b" stroke="#625e4d" stroke-width="3"/>
        <path d="M825 359V342Q836 325 847 342V359" fill="#73594a" opacity=".7"/>
        <path d="M871 339H1060Q1084 339 1084 377Q1084 411 1060 411H871Z" fill="url(#boiler)" stroke="#163745" stroke-width="2"/>
        <path d="M893 341V408M948 340V410M1004 340V409" stroke="#d6ab69" stroke-width="4"/>
        <path d="M881 349H1057" stroke="#7e9490" stroke-width="2" opacity=".6"/>
        <path d="M1029 339V304H1052V339" fill="#193b47" stroke="#132f3d" stroke-width="2"/>
        <path d="M1023 303V296H1058V303Z" fill="#c3a16f" stroke="#183847" stroke-width="2"/>
        <path d="M921 338V325Q933 306 945 325V338" fill="#e1b974" stroke="#25434b" stroke-width="2"/>
        <ellipse cx="1085" cy="374" rx="13" ry="35" fill="#193845" stroke="#ac905e" stroke-width="3"/>
        <circle cx="1096" cy="354" r="10" fill="#f8dc97" stroke="#c39c64" stroke-width="3"/>
        <circle cx="1099" cy="354" r="22" fill="url(#sun-halo)"/>
        <path d="M1102 415L1148 450H1095Z" fill="#b35b4a" stroke="#183947" stroke-width="2"/>
        <path d="M1103 422L1136 447M1100 432L1115 447" stroke="#dea977" stroke-width="2"/>
        {engine_wheels}
        <g>
          <path d="M886 434H1018" stroke="#102b37" stroke-width="8" stroke-linecap="round"/>
          <path d="M886 434H1018" stroke="#d1c4a8" stroke-width="4" stroke-linecap="round"/>
          <circle cx="886" cy="434" r="4" fill="#e6cf9f"/><circle cx="952" cy="434" r="4" fill="#e6cf9f"/><circle cx="1018" cy="434" r="4" fill="#e6cf9f"/>
          <animateMotion path="M0 -14A14 14 0 0 1 0 14A14 14 0 0 1 0 -14" dur="{rod_period:.7f}s" repeatCount="indefinite"/>
        </g>
        <path d="M858 405H1074" stroke="#cc9a68" stroke-width="3"/>
        {steam}
      </g>
    </g>
    <g opacity=".42" stroke="#d2c6ad" stroke-width="1.2" fill="none"><path d="M89 583h123m-78 10h47M489 548h88m-43 10h27M1056 598h114m-74 10h35M1374 543h74"/></g>
    <text x="1518" y="607" text-anchor="end" font-family="'Yu Mincho','STKaiti',serif" font-size="15" fill="#d9d4c1" opacity=".7">旅は、つづく。</text>
    <rect width="1600" height="640" fill="#ffffff" filter="url(#paper)" pointer-events="none"/>
  </g>
</svg>'''
    OUT.write_text(svg.replace("{AVATAR}", avatar), encoding="utf-8")
    print(f"Saved {OUT.name}: {OUT.stat().st_size:,} bytes")


if __name__ == "__main__":
    build()
