#!/usr/bin/env python3
"""
gpt.py — Claude→GPT bridge CLI (OpenAI API)

Claude（私）がプロンプトを生成し、このCLIがOpenAI APIを呼んで結果を返す。
テキスト（chat）と画像（image, 複数枚バリエーション）に対応。

APIキーの読み込み順（チャットに貼らないこと）:
  1) 環境変数 OPENAI_API_KEY
  2) ~/.config/openai/api_key
  3) リポジトリ直下の .openai_key（.gitignore 済み）

使い方:
  python3 tools/gpt.py text  "日本語で一句"                 [--model gpt-4o]
  python3 tools/gpt.py image "a minimal crimson 24h ring app icon, flat" \
          --n 4 --size 1024x1024 --quality high --out icon-candidates --label ring
  python3 tools/gpt.py icons --master icon-candidates/ring_1.png --manifest
"""
import os, sys, json, base64, argparse, urllib.request, urllib.error, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_key():
    k = os.environ.get("OPENAI_API_KEY")
    if k and k.strip():
        return k.strip()
    for p in (os.path.expanduser("~/.config/openai/api_key"),
              os.path.expanduser("~/.openai_key"),
              os.path.join(ROOT, ".openai_key")):
        if os.path.exists(p):
            v = open(p).read().strip()
            if v:
                return v
    sys.exit("ERROR: OpenAI API key not found.\n"
             "  Set it once (in YOUR terminal, not in chat):\n"
             "    mkdir -p ~/.config/openai && printf '%s' \"sk-...\" > ~/.config/openai/api_key && chmod 600 ~/.config/openai/api_key")


def post(url, payload, key, timeout=300):
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:800]
        sys.exit(f"OpenAI API error {e.code}:\n{body}")
    except urllib.error.URLError as e:
        sys.exit(f"Network error: {e}")


def cmd_text(a):
    key = get_key()
    res = post("https://api.openai.com/v1/chat/completions",
               {"model": a.model, "messages": [{"role": "user", "content": a.prompt}]}, key)
    print(res["choices"][0]["message"]["content"])


def cmd_image(a):
    key = get_key()
    payload = {"model": a.model, "prompt": a.prompt, "n": a.n, "size": a.size}
    if a.quality:
        payload["quality"] = a.quality
    res = post("https://api.openai.com/v1/images/generations", payload, key)
    os.makedirs(a.out, exist_ok=True)
    saved = []
    for i, item in enumerate(res.get("data", [])):
        fn = os.path.join(a.out, f"{a.label}_{i+1}.png")
        if item.get("b64_json"):
            open(fn, "wb").write(base64.b64decode(item["b64_json"]))
        elif item.get("url"):
            urllib.request.urlretrieve(item["url"], fn)
        else:
            continue
        saved.append(fn)
        print("saved", fn)
    print(f"DONE: {len(saved)} image(s) -> {a.out}")


def cmd_icons(a):
    """選んだマスター画像から PWA アイコン3種を生成（macОS sips）。--manifest で manifest.json も作成。"""
    master = a.master
    if not os.path.exists(master):
        sys.exit(f"master not found: {master}")
    for size, name in ((192, "icon-192.png"), (512, "icon-512.png"), (180, "apple-touch-icon.png")):
        out = os.path.join(ROOT, name)
        subprocess.run(["sips", "-z", str(size), str(size), master, "--out", out], check=True,
                       stdout=subprocess.DEVNULL)
        print("wrote", name)
    if a.manifest:
        manifest = {
            "name": a.app_name, "short_name": a.app_name,
            "start_url": "./", "scope": "./", "display": "standalone",
            "background_color": "#f3f2ef", "theme_color": "#8b0026",
            "icons": [
                {"src": "./icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
                {"src": "./icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"},
            ],
        }
        open(os.path.join(ROOT, "manifest.json"), "w").write(json.dumps(manifest, ensure_ascii=False, indent=2))
        print("wrote manifest.json")
    print("DONE: icons ready")


def main():
    ap = argparse.ArgumentParser(description="Claude→GPT bridge (OpenAI API)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    t = sub.add_parser("text", help="chat completion")
    t.add_argument("prompt")
    t.add_argument("--model", default="gpt-4o")
    t.set_defaults(func=cmd_text)

    im = sub.add_parser("image", help="image generation (n variations)")
    im.add_argument("prompt")
    im.add_argument("--model", default="gpt-image-1")
    im.add_argument("--n", type=int, default=1)
    im.add_argument("--size", default="1024x1024")
    im.add_argument("--quality", default=None, help="low|medium|high (gpt-image-1)")
    im.add_argument("--out", default="icon-candidates")
    im.add_argument("--label", default="img")
    im.set_defaults(func=cmd_image)

    ic = sub.add_parser("icons", help="master png -> PWA icons (+ optional manifest)")
    ic.add_argument("--master", required=True)
    ic.add_argument("--manifest", action="store_true")
    ic.add_argument("--app-name", default="生活ログ")
    ic.set_defaults(func=cmd_icons)

    a = ap.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
