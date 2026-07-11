# AGENTS.md — Tsumugi（紡ぎ）プロジェクト恒久ルール

このリポジトリで作業するコーディングエージェント（Claude Code / Codex 等）向けの**恒久的な**指示。
今回限りの作業状況は `HANDOFF.md`、デザイン仕様は `docs/design-system.md` を参照。

## プロダクト概要
- **Tsumugi（紡ぎ）**: 未使用だった生活ログPWA「lifelog」をピボットした、プライバシー最優先・低コストのAI内省アプリ。
- 核（統合案）＝「**目標を立て(月→週→日)、実行し、AIと対話で振り返る**サイクル＋蓄積が第二の脳になる」。
- ターゲット＝日本語ネイティブの知的探究層（コンサル/VC志望など）。ゴールはVC exitでなく**ブートストラップ黒字**。

## アーキテクチャ（動かす前に理解すること）
- **単一の自己完結 `index.html`（約6,400行）** にHTML/CSS/JSを全てインライン。ほかに `manifest.json`, `sw.js`, アイコンPNG。
- 永続化は **localStorage のみ**（`STORAGE_KEY="dailyLifeLogsV6"` ほか、`index.html` 冒頭のキー定義参照）。サーバDBなし。
- AIは **BYOK（各自のGemini APIキー）** で `callGemini()` から直接叩く。キーは localStorage、URLクエリに載る。
- Google Calendar / Google Drive 同期あり（`SYNC_KEYS` の localStorage を Drive にJSONで同期・マージ）。

## 絶対に守る制約（違反＝プロダクトの前提崩壊）
1. **外部リクエスト禁止**: 外部CDN・Webフォント・リモート画像・解析ビーコンを追加しない。CSP/オフライン動作が売り。アイコンは**インラインSVGか絵文字**、CSSのみ、アセットは data: URI。
2. **プライバシーは実装で証明する**: 生データ（本文・詳細メモ・対話全文）を作り手のサーバへ通さない。AIへ送るのは最小限（カテゴリ提案は本文のみ、期間レポートは**集計値のみ**）。対話ログ `DIALOGUE_KEY="tsumugiDialoguesV1"` は **`SYNC_KEYS` に入れない＝端末ローカル限定**。この方針を勝手に変えない。
3. **AIは断定しない**: 内省を促す“問い”を返す設計（答え・解釈・助言を述べない）。既存プロンプトのこの制約を保つ。
4. **プロダクトで Gemini 無料枠に依存しない**: 無料枠は規約で学習利用され得る/日本は非対象/突然改定のため、**製品の本番前提にしない**（個人の検証利用は可）。
5. **単一HTML・モバイルファースト**を維持。`max-width:480px` センタリング。固定/スティッキー要素は `env(safe-area-inset-*)`。横スクロールはコンテナ内 `overflow-x:auto` に閉じ、body は横スクロールさせない。
6. **既存の同期・カレンダー機能を壊さない**（`collectAllLocalData`/`applyAllLocalData`/`mergeAllData`、Gcal連携）。新しい永続キーを足したら **3箇所（SYNC_KEYS / collect / apply / merge）**に必ず反映。
7. `.env`・APIキー・秘密鍵・個人データを**コード/ドキュメント/コミットに含めない**。

## コマンド / 検証
- ビルド不要（素のHTML）。ローカル確認は **HTTPサーバ経由**（`file://` は Playwright 等が弾く）:
  ```bash
  python3 -m http.server 8765 --directory .
  # → http://localhost:8765/index.html
  ```
- 自動テストフレームワークは未導入。検証はブラウザでの手動確認＋DevTools/コンソールにエラーが出ないこと。関数単位はブラウザコンソールで直接呼んで確認できる（多くがグローバル関数宣言）。
- 変更後は必ず **実機/ブラウザで挙動確認**し、`console` にエラー0を確認する。

## コード規約
- 周囲のコードに合わせる：関数は素の `function`宣言（巻き上げ前提でファイル内どこからでも呼べる）、命名は英語関数名＋日本語UI文字列、コメントは日本語。
- 色は**CSSトークン（`--accent` 等）経由**。ハードコードのクリムゾン(#8b0026系)は全廃済み。新色を足すなら `color-mix(in srgb, var(--accent) N%, ...)` で `--accent` から導出（テーマ追随のため）。
- localStorage 読み書きは `loadJSON/saveJSON`（`saveJSON` は `SYNC_KEYS` のキーで自動的に Drive 同期をトリガ）。

## Git
- 既定ブランチではなく作業ブランチで進める（現在 `tsumugi-mvp`）。
- **コミット/プッシュはユーザーに頼まれた時だけ**。コミットメッセージ末尾に:
  `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`
