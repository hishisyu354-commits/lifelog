# HANDOFF.md — Claude Code → 次のエージェント（Codex等）引き継ぎ

作成: 2026-07-11 / 対象ブランチ: `tsumugi-mvp` / 直近コミット: `db4d112`（コード）＋本ドキュメント群
恒久ルール→ `AGENTS.md`、デザイン仕様→ `docs/design-system.md`。まず3つとも読むこと。

---

## 0. TL;DR（現在地）
未使用の生活ログPWA `index.html` を、**Tsumugi（紡ぎ）＝「目標→実行→AI対話で振り返る」サイクル＋第二の脳**へピボット中。
本セッションで **(A) 入力摩擦の低減 / (B) 目標階層(月→週→日) / (C) 藍×生成りへのデザイン再スキン土台** を実装・ブラウザ検証・コミット済み。
残りは **(D) 日/週/月レビュー強化 / (E) AI対話をレビューの“振り返りエンジン”に接続 / (F) デザイン深掘り**。

## 1. 目的と完成条件（Definition of Done）
- **目的**: 「Claude+Obsidianの“対話で思考が深まる日記＋第二の脳”体験」を、二重課金/デスクトップ/技術構築なしに、スマホ1つ・ローカル保存・BYOKで再現する製品。MVPで **継続率(D30)** を最優先検証できる状態にする。
- **MVP完成条件**:
  1. 目標(月→週→日)を立て、常時見える。
  2. 予定/行動を**最小摩擦**で記録できる（入力の友人FBを満たす）。【概ね達成】
  3. 日/週/月の振り返りが **AIとの対話** で回り、空状態が無い（AIが先に問う）。【E/F残】
  4. タグ/対話/目標が蓄積し検索・双方向に辿れる（第二の脳）。【一部：タグ検索=振り返りノート実装済、対話はローカル保存＋履歴実装済】
  5. 藍×生成りの一貫したUI、ライト/ダーク、単一HTML・オフライン。【土台済、深掘り残】

## 2. 実装済み（すべて `http://localhost:8765` でブラウザ検証・console error 0）
### (A) 入力摩擦の低減 — 友人FBの最優先
- `getSmartDefaultTimes(date, type)` `index.html:3243` … 既定開始時刻を**その日の“前タスクの終了時刻”**に自動補完（同種type優先→無ければ全ログの最遅end→今日ならnow丸め→他日は9:00）。丸めは**5分**。呼び出しは `showPlanForm`(:3263)/`showActualForm`(:3267) が `"plan"/"actual"` を渡す。
- `formBase(...)` の time入力に `step="300"`（5分刻み） … `index.html` ~3180（`<input id="startTime" type="time" step="300">` を grep）。
- `onWeekDayColClick` `index.html:5558` … 週タイムライン空白タップの丸めを15分→**5分**（`Math.round(totalMin/5)*5`）。
- 頻用予定をカテゴリ紐づけ: `_freqName/_freqCat`（~2446）, `frequentPlanOptions` `index.html:2448`（`data-cat`付きoption）, `applyFrequentPlan` `index.html:3172`（選択で本文＋カテゴリを同時セット）, `addFrequentPlan`/`deleteSelectedFrequentPlan`(~3173-3174)。データは文字列/`{name,categoryId}`混在を許容（後方互換）。
- 未記録空白: `buildGapPrompts` `index.html:3822` … しきい値を反転（`gap>0&&gap<=60` → **`gap>=60`**、表示は `minutesToHourText`、コピーも「1時間以上」に）。**＜1hは出さない／≥1hをまとめて振り返り**。

### (B) 目標階層（月→週→日）
- キー: `MONTH_GOAL_KEY="tsumugiMonthGoalsV1"` `index.html:2092`。**週目標は既存の weeklyIntent（`WEEKLY_INTENT_KEY`）を再利用**（`getWeeklyIntent`/`upsertWeeklyIntent` ~2151、月曜起点 `getMondayOfWeek`）。
- 関数: `loadMonthGoals`:2165 / `getMonthGoal`/`upsertMonthGoal`:2169 / `renderGoalHeader`:2188 / `openGoalEditor`:2204 / `saveGoalEditor`:2227 / `currentWeekStartStr`。CSSは `_goalInjectStyle()` がJSでinject。
- DOM: `<div id="goalHeader">` `index.html:1935`（`todayBar` の直下）。空なら「🎯 今月・今週の目標を決める」、設定済なら 今月/今週 のチップ2つ（タップで編集）。
- 描画フック: 初期化（`updateTodayBar();` の直後に `renderGoalHeader();`）＋ Drive同期後の2ブロック＋ `saveGoalEditor` 内。
- **同期4点セットに反映済**: `SYNC_KEYS`:5923 / `collectAllLocalData`:6015（`monthGoals`）/ `applyAllLocalData`:6030 / `mergeAllData`:6075（`mergeByKeyTs(...,"month")`）。頻用予定の混在配列は `mergeTemplatesByName`（name一意・カテゴリ付き優先）でマージするよう修正（旧 `new Set` はオブジェクト非対応だった）。

### (C) デザイン再スキン土台（藍×生成り）— `docs/design-system.md` 準拠
- 既定トークンを差替: `index.html:937-943`（`--bg:#f6f4ef` `--accent:#40608f` ほか＋`--ink-2/--on-accent/--good/--warn/--accent-strong` 追加）。
- クリムゾン全廃: `#8b0026/#9b1230/#c93a52/#b8003c` と `rgba(139,0,38,*)` グローを藍へ置換（`.score-result`グラデ、`.summary-num`等の `color:#8b0026;` → `var(--accent)`、`rgba(139,0,38,` → `rgba(64,96,143,` を sed一括）。フォーカスリング(:271)を `color-mix(in srgb,var(--accent) 22%,transparent)` に。
- ヘッダ/今日バーは既にクリムゾン帯を廃止し静音化済（`header{background:var(--bg)}` ~950）。ヘッダ表記も「Tsumugi」に。
- ダークは "red-dark" テーマに温炭+藍を載せ替え（tokens ~28、accent ~1024）。テーマ選択の表示名/swatchを「藍・ライト/藍・ダーク」に（`THEME_OPTIONS`:4330）。
- `manifest.json` の `theme_color`/`background_color` を `#f6f4ef` に。`<meta name="theme-color">` も。

### 既存で継承した要素（本セッション前から存在）
- 対話ループ: `data-tab="dialogue"`(:2055) → `renderDialogue`:2581 / `startDialogue`:2610 / `sendDialogueTurn`:2680 / `finishDialogue`:2709。reviewScreen に描画、`DIALOGUE_KEY` は端末ローカル（**SYNC_KEYS非対象**）。
- 週=縦タイムライン `renderWeekView`:5425、日ホーム `renderDayHome`:5207（24hリング＋アジェンダ）、日次充実度 `showDailyFulfillment`:4011、週次 `showWeeklyReview`:4464、月次 `showMonthlyReview`:4662、振り返りノート（#タグ検索）`showReflectionNotebook`。
- `callGemini(prompt,schema,opts)`（BYOK, gemini-2.5-flash）。

## 3. 変更ファイルと理由
- `index.html` … 上記(A)(B)(C)全て。単一HTMLに全機能が入るため。
- `manifest.json` … リブランド（Tsumugi）＋テーマ色を生成りに。
- `AGENTS.md`（新規）… 恒久ルール。`docs/design-system.md`（新規）… #9の一次情報（元は一時ファイル `w0aq13i3f.output`＝Codexからは参照不可のため repo に固定）。`HANDOFF.md`（本ファイル）。

## 4. 重要な設計判断
- **方向=統合案**: 友人FBの「目標→反省サイクル」を**継続エンジンの背骨**に、市場戦略の「AI対話＋プライバシー」を**差別化＋堀**に据えて統合（＝どちらか一方でなく合成）。理由: 市場分析の最大リスク=日記のD30低さ(3–8%)を、目標サイクルが構造的に緩和する。
- **週目標は新規キーを作らず weeklyIntent を再利用**（二重管理回避）。月曜起点で統一。
- **色はトークン中心**: `--accent` 1つを差し替えれば全体が変わる構造にした（将来の藍/苔/弁柄 切替のため）。クリムゾンのハードコードを撲滅。
- **クリムゾン→藍は多エージェント分析の推奨**（SaaS警告色→calm/信頼、藍染の文化的含意）。ブランド色変更なのでユーザーが嫌えば `--accent` を戻すだけで可逆。
- **頻用予定を後方互換で objects 化**（既存の文字列配列を壊さない）。

## 5. ユーザー要件（会話で受けた、厳守すべきもの）
- モバイル中心・**追加の有料API無し**・コスト限りなくゼロ。**製品で Gemini 無料枠に依存しない**（学習利用/日本非対象/突然改定）。
- プライバシー＝**データはローカル＋自分のキー**。便利機能がこっそり生データを作り手サーバに通したら即崩壊。
- APIキー/PATをチャットやファイルに貼らない。**コミット/プッシュはユーザーが頼んだ時だけ**。
- アプリ名は **Tsumugi（紡ぎ）** で確定。
- デザインは「流行の類似アプリを徹底分析し傾向を抽出して改良」。友人FBは「必要に応じて取り入れる」（＝取捨は任せられている）。

## 6. 未完了作業（優先順）
1. **(F-優先) デザイン深掘り #9**（`docs/design-system.md` の優先順3–8）: 空状態の撲滅 / AI対話ビューを非IM streamingチャット＋stickyコンポーザ / 日本語組版のグローバル修正 / prefers-color-scheme 自動ダーク＋auto-light-darkトグル / ストリーク廃止＆藍ヒートマップ＆1–10スコア撤去 / bento化＋4項目フローティングナビ(記録/対話/振り返り/蓄積) / 気分チェック行 / 日タイムラインの height=duration。
2. **(D) レビュー強化 #7**: 日次＝達成 **Yes/No**＋充実度＋**できなかった理由**＋≥1h穴埋め。週次＝達成率・**自己認識と実績のズレ**・睡眠・次週目標。月次＝**5段階**評価・月目標。既存 `showDailyFulfillment`/`showWeeklyReview`/`showMonthlyReview` を拡張。
3. **(E) AI対話を各レビューの振り返りエンジンに #8**: 日/週/月レビューから対話ループ（`startDialogue`）を起動し、その期間の集計（`aggregatePeriodData` 等）を**集計のみ**文脈注入して深掘り。差別化の核。

## 7. 現在のエラー / 懸念点
- **console エラーは 0**（ライト既定・目標ヘッダ・入力フォーム・同期マージを検証済）。機能的な既知バグは無し。
- **視覚未確認**: Playwright MCP の `browser_take_screenshot` が本環境で 5000ms タイムアウトし、スクショが撮れていない。**実ブラウザで `http://localhost:8765/index.html` を開いて目視**すること（配色は computed style で `--bg=#f6f4ef`/`--accent=#40608f`/ヘッダ生成り色を確認済）。
- **テーマ系はまだ collapse していない**: 8テーマが残存し、既定 "red-light" に藍トークンを載せ替えた形。design-system の理想（1アイデンティティ＋3アクセント＋prefers-color-scheme自動）へは #9 で整理が必要。旧の上書き済みクリムゾン定義が `index.html:20-22` に**不活性のまま**残る（後発の :937-943 が同セレクタで勝つ）。気になれば削除可。
- **旧UIに残る非design要素**: 1–10 の充実度スコアバー（`renderScoreBar`/`.score-cell`）やストリーク的表現は design-system 方針では撤去対象（#9-6）。まだ残っている。
- ルートに無関係な未追跡ファイル `__home.html` `__preview.html` `__rev.html` がある（本作業とは無関係、コミットに含めていない）。

## 8. 実行したテストと結果（ブラウザ `browser_evaluate`）
- 既定開始=前タスク終了: plan→`12:00`、actual→`14:20`、記録なし他日→`09:00`。**PASS**
- time入力 `step=300` / 頻用セレクト存在 / 対話タブ描画。**PASS**
- 空白しきい値: 90分ギャップ表示・30分ギャップ非表示。**PASS**
- 目標: 空状態→`openGoalEditor`→`saveGoalEditor`→ヘッダに月/週表示。**PASS**
- 同期マージ: 頻用予定を name一意・カテゴリ付き優先で統合 / 月目標を updatedAt 新しい方採用。**PASS**
- 配色適用: `--bg=#f6f4ef` `--accent=#40608f` `--text=#22201d`、header bg=生成り、縦向きガードOFF。**PASS**

## 9. 次に実行すべき具体手順
1. 環境: `cd <repo> && python3 -m http.server 8765 --directory .` → 実ブラウザで目視（`file://` は不可）。
2. まず `AGENTS.md` / `docs/design-system.md` / `git log`・`git show db4d112` を読む。**最初はコードを変えず**、現状理解・矛盾点・次の変更計画を報告してから着手。
3. #9 の「空状態撲滅」と「AI対話ビューのstreamingチャット化」から入るのが最高レバレッジ（`docs/design-system.md` のコンポーネント「AIチャット…」節が実装仕様）。`renderDialogue`/`sendDialogueTurn`(2581/2680) を土台に、楽観的UI＋SSE streaming＋sticky `dvh` コンポーザへ。
4. 続けて #7（レビューにYes/No達成・できなかった理由・ズレ・5段階を追加）、#8（各レビューから対話起動＋集計注入）。
5. 新しい永続キーを足す時は必ず **SYNC_KEYS / collect / apply / merge の4点**に反映（(B)を踏襲）。
6. 変更後は毎回ブラウザで console error 0 と主要フロー（記録→目標→振り返り）を確認。ユーザーが頼んだらコミット（Co-Authored-By トレーラ付き）。

## 10. 壊してはいけない既存仕様
- **単一HTML・外部リクエストゼロ**（CDN/フォント/画像/解析を足さない。アイコンはinline SVG/絵文字、CSSのみ）。
- **localStorage スキーマ互換**（`dailyLifeLogsV6` ほか。破壊的変更はマイグレーション必須）。
- **BYOK＆プライバシー**: AIへ送るのは最小限、期間系は**集計のみ**。対話全文(`DIALOGUE_KEY`)は端末ローカル＝SYNC_KEYS非対象を維持。
- **AIは断定しない**（“問い”を返す。答え/助言を述べない）。
- **Google Calendar / Drive 同期を壊さない**（`collect/apply/mergeAllData`、Gcal push）。
- モバイルファースト `max-width:480px`、body横スクロール禁止、safe-area 尊重。
- `.env`/キー/秘密情報をコード・ドキュメント・コミットに含めない。

## 11. 参照
- コード: `index.html`（全機能）, `manifest.json`, `sw.js`。行番号は上記（本コミット時点。ズレたら関数名で grep）。
- ドキュメント: `AGENTS.md`（恒久ルール）, `docs/design-system.md`（デザイン一次情報）。
- 記憶（Claude Code側メモリ、Codexは読めないので要点は本ファイルに転記済）: `tsumugi-app` に方向・デザイン・進捗を保存済み。
