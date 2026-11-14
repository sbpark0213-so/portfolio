"""portfolio.json 에서 img 가 비어 있는 칸의 url 을 찍어 img/w{주}.png 로 넣는다.

    python3 shot.py          # img 가 빈 칸만
    python3 shot.py 3        # 3주 칸을 다시 찍기 (이미 있어도)
"""
import json, subprocess, sys
from pathlib import Path

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
HERE = Path(__file__).parent
P = HERE / "portfolio.json"

data = json.loads(P.read_text(encoding="utf-8"))
redo = {int(a) for a in sys.argv[1:]}

for c in data["cards"]:
    if not c.get("url") or (c.get("img") and c["week"] not in redo):
        continue
    rel = f"img/w{c['week']}.png"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=2", "--window-size=900,490",
                    "--virtual-time-budget=5000", f"--screenshot={HERE / rel}", c["url"]],
                   check=True, capture_output=True)
    c["img"] = rel
    print(f"{c['week']}주  {c['url']}  ->  {rel}")

P.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
