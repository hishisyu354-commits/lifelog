# Claude→GPT bridge (`tools/gpt.py`)

ClaudeがプロンプトをつくってOpenAI APIに投げ、結果（テキスト/画像）を受け取る再利用CLI。

## セットアップ（キーはチャットに貼らない）
自分のターミナルで一度だけ:
```bash
mkdir -p ~/.config/openai
printf '%s' "sk-..." > ~/.config/openai/api_key
chmod 600 ~/.config/openai/api_key
```
（または `export OPENAI_API_KEY=sk-...`）

## 使い方
```bash
# テキスト
python3 tools/gpt.py text "プロンプト" [--model gpt-4o]

# 画像を複数枚（バリエーション）
python3 tools/gpt.py image "プロンプト" --n 4 --size 1024x1024 --quality high \
        --out icon-candidates --label ring

# 選んだ画像 → PWAアイコン3種(+manifest)
python3 tools/gpt.py icons --master icon-candidates/ring_1.png --manifest
```

- 既定モデル: text=`gpt-4o`, image=`gpt-image-1`
- `icon-candidates/` と キーファイルは `.gitignore` 済み（公開リポジトリに出ない）
- 課金は OpenAI API 側（ChatGPT Plus とは別）
