# Tsumugi デザインシステム（藍と生成りの「静かな第二の脳」）

多エージェントによるトレンド分析（AI日記 / 目標習慣 / ウェルネス / 2026モバイルUI / 日本市場＋チャットUI の5レンズ→統合）で策定。
このファイルは**残作業 #9（デザイン深掘り）を会話履歴なしで実行するための一次情報**。土台（トークン/ヘッダ/フォーカス/ダーク整合）は適用済み、以下は「基準」と「未適用の深掘り」の両方を含む。

## コンセプト
**藍(indigo)×生成り(washi)の、急がない内省ジャーナル。** AIは評価者(ダッシュボード)でなく非審判の聞き手。温かい紙にインクが落ち着くように、藍のアクセントは「目を向けるべき一点」だけを差す。

## デザイン原則
1. **会話が入口** — 空のテキストエリア＋点滅カーソルで開く画面を作らない。AIが先に、その日の目標とログに根ざした問いを1つ話す or Quick Start/プロンプトカードを出す。**空状態を全部殺す**（＝離脱の最大要因を潰す＝差別化）。
2. **一画面・一動作** — 余白(Ma)が製品。階層は色でなく**重み/サイズ**で。第二の脳の深さは1階層下（漸進的開示）。
3. **静けさが基調、動きは報酬** — 書いている間は何もループ/呼吸させない。動きは完了の報酬。オーロラ/ブルームは振り返り・マイルストーン面だけ。
4. **一色の規律** — 低彩度の藍を**全体の≤5%**（主CTA・現在時刻線・アクティブタブ・AIの気づき）だけに。他は温かいニュートラル。クリムゾンとテーマ乱立は廃止。
5. **非審判の聞き手を視覚化** — 1–10の気分スコア無し、赤い「未達」/ストリーク断絶の羞恥状態無し、既読無し。継続は**蓄積**として表現（「7日中5日 記録」/紡いだ日々）、週次は温かい手紙（「今週のことば」）。
6. **プライバシーは証明** — 「端末内に保存 / あなたの鍵だけ」の静かな常設表示。CDN/Webフォント/リモート画像/解析ゼロ。
7. **日本語組版は機能** — 読み面は行間1.75–1.85、**正の字間**、palt は短い見出しだけ、合成イタリク禁止。

## カラートークン（`:root` を差し替え／`index.html` の既定テーマに適用済み）
### Light（生成り × 藍）
```
--bg: #F6F4EF;            /* 生成り washi。#FFF は使わない（表計算に見える） */
--surface: #FDFCFA;       /* 上げ面/AI対話面。bg より一段明るく暖かい（現行 --card 相当） */
--surface-2: #F1EEE7;     /* 沈み面/soft-bg（現行 --soft-bg 相当） */
--ink: #22201D;           /* 主テキスト（墨）。純黒は使わない（現行 --text 相当） */
--ink-2: #55514B;         /* 副読テキスト（本文でAA） */
--muted: #7C766C;         /* 三次メタ。12px semibold以上のみ */
--border: #E7E3DB;        /* 1pxヘアライン。箱でなく線で */
--accent: #40608F;        /* 藍。唯一のアクセント。主CTA/now-line/activeタブ/insight */
--accent-strong: #35527D; /* 押下/ホバー、より強い藍テキスト */
--accent-soft: #E9EDF4;   /* ユーザー発話カード/insightの淡い地 */
--accent-line: #D3DBE8;   /* 藍のヘアライン（AI発話の左3px 等） */
--on-accent: #FDFCFA;     /* 藍塗り面の上のテキスト */
--good: #5A8F6F;          /* くすんだ抹茶。穏やかな肯定（鮮緑にしない） */
--warn: #B0803F;          /* くすんだ琥珀。最弱の注意。ほぼ使わない */
--mood-1:#8FA9C4; --mood-2:#A7B79E; --mood-3:#D6CBB0; --mood-4:#D3B49A; --mood-5:#C79FA0; /* 気分チェック専用 */
--shadow-card: 0 1px 2px rgba(34,32,29,.04), 0 6px 20px rgba(34,32,29,.05); /* 低く柔らかい影 */
```
### Dark（温炭 × 藍。夜こそ最高の内省タイミング＝一級市民）
```
--bg: #151412;            /* 温かい準黒。#000/青黒にしない（真黒はOLED opt-inのみ） */
--surface: #1D1B17;       /* 温チャコール。影でなくrim-lightで分離 */
--surface-2: #23201B;
--ink: #E8E4DC;           /* 約85%のoff-white。#FFFにしない（夜のハレーション） */
--ink-2: #B4AEA3;  --muted: #8B857A;
--border: #302C25;
--accent: #8AA4D6;        /* チャコール上でやや明るく低彩度に */
--accent-strong: #A6BCE4; --accent-soft: #23262F; --accent-line: #3A4256;
--on-accent: #14161C;     /* 明るい藍CTAの上は暗テキスト（lightと反転、トークン構造は同一） */
--good:#6FA083; --warn:#C79A5C;
--mood-1:#6E8AAA; --mood-2:#7E9078; --mood-3:#A99B7C; --mood-4:#A98A72; --mood-5:#A67C7D;
--shadow-card: 0 1px 0 rgba(255,255,255,.04) inset, 0 0 0 1px var(--border); /* rim-light＋ヘアライン */
```
**根拠**: クリムゾン(#8b0026/#9b1230/#c93a52)は“ニュース/SaaS警告色”で calm/trustworthy と衝突。藍=知性・信頼・落ち着き＋藍染の日本文化的含意で muji/washi に最適。周囲のニュートラルをクリーム側に寄せることで“陰鬱な青灰の海”を回避。全ペアで WCAG AA（本文≥4.5:1、大/UI≥3:1）を両モードで満たす。曲線的に**3色の厳選アクセント切替（藍 既定 / 苔 #5A8F6F / 弁柄 #A96A52）**を提供可（`--accent` 1トークンだけ差し替え、`color-mix()` で全tintを導出）。

## タイポグラフィ
- スタック（CSP安全、`@import`禁止）: `-apple-system, BlinkMacSystemFont, 'Hiragino Sans','Hiragino Kaku Gothic ProN','Yu Gothic', YuGothic, 'Noto Sans JP', system-ui, sans-serif`。
- 階層は**サイズ＋ウェイト**のみ。ウェイト: 本文400 / 小見出し・UI 600 / ディスプレイ 700（**800は使わない**＝現行の見出し800は喧しい）。`font-optical-sizing:auto` をグローバル。
- スケール(px): display26 / title20 / subhead17 / body16 / body-reading17（AI発話・日記）/ label13 / meta12 / micro11。
- **日本語必須**: 読み面 line-height 1.8、UI 1.45、日本語を含む要素は**負の字間を剥がして +0.02em**（現行の -.02/-.035em はかなを潰す。負トラッキングは大きなラテン数字のみ）。`palt` は短い見出し/ラベルのみ。stats/時刻/ログは `tabular-nums`。見出し・プロンプトに `text-wrap:balance`、日本語折返しは `line-break:strict; overflow-wrap:anywhere`。読み幅は1行≒15–35文字に上限。週/月レビューの“手紙”見出しだけ任意で明朝（`'Hiragino Mincho ProN','Yu Mincho', serif`）。**日本語に CSS italic 禁止**。

## スペーシング / 角丸
4pxグリッド、トークン化して**たっぷり使う**（余白＝最安の高級感）: `--s1:4 … --s4:16(既定カード内側) --s6:24(カード間) --s8:48`。カード内側18–20px、カード間20–24px、画面横16px＋safe-area、一枚一アイデア。角丸: `--r-chip:999px` / `--r-sm:10px`(入力・タイムラインブロック) / `--r-md:16px`(既定カード) / `--r-lg:22px`(シート・AI対話面) / `--r-sheet:26px`。タップ標的 ≥44×44。段差は**トーン差＋`--shadow-card`**（積んだ影でなく）、ダークは rim-light＋ヘアライン。

## コンポーネント仕様（#9で作り込む対象）
- **目標ヘッダ（月→週→日カスケード）**: クリムゾンの帯は廃止済み→ on-bg の静かなヘッダ（時間帯挨拶＋scope切替）。目標は**最大3階層の入れ子展開**。月目標カード（slimなロールアップ進捗を藍で~14%）→タップで週目標→日タスク。**重要な連結**: 各目標エリアが1つのくすんだカテゴリ色を持ち、**同じ色を日タイムラインのブロックにも反映**して「目標と実行が一つのシステム」に見せる。展開はspring ~280ms。OKR密度にしない。
- **日タイムライン（実行）**: 単一の縦スクロール列（上=朝→下=夜）。タスクは**高さ=所要時間**の角丸ブロック（絶対配置）で“1日の形”を前意識的に感じさせる。塗り=目標エリア色の15–22%＋左3pxはフル彩度。幅いっぱいの1px藍 now-line（唯一JSが位置を駆動）。主導線は**タップで追加/長押しで割当**、ドラッグ再配置（15分スナップ）は副次。カテゴリチップ行＝タイムラインのフィルタ兼用。下部に常設のquick-add（自然文1フィールド「明日9時 英語30分」→時刻/所要/#エリアの確認チップに、まずは最小パーサ）。※現状は既に週=縦タイムライン（`renderWeekView`）＋空白タップ追加（`onWeekDayColClick`）がある。日ビューも height=duration 化する。
- **レビュー・ダッシュボード（週/月）**: calmなbento（`display:grid` 2→1列、gap16、`--r-md`、余白多め、**タイル2–4＋ヒーロー1**）。順=(1)ヒーロー＝AIの“手紙”insight（「今週のことば」、明朝見出し任意、accent-soft地）(2)3–4の小stat（時間/エリア・継続・目標達成、tabular-nums）(3)1–3のAIアクション（次期の目標に流す）。継続=**単色藍のヒートマップ（5段階の不透明度）**で（炎/ストリークでなく）。5分と30分で重みを変え、寛容かつ正直に。棒グラフ密度/赤い未達/1–10気分スコアは禁止。レビュー完了時だけ稀な色ブルーム＋（Android）ソフトhaptic。
- **AIチャットの吹き出し＋コンポーザ（対話で振り返る）**: 非IM化。AI発話=地に近い枠なし、`--ink-2→--ink`、行間1.8、**吹き出しでなく左3pxの藍ヘアライン**、トークンstream（BYOKのSSE、追記トークンのopacityを動かす）。ユーザー発話=`--accent-soft`の淡いカード（右寄せだが完全右端でない）、既読/配信チェック/時刻chrome無し。思考中=AIスタイルの三点、送信<300msで出す。**楽観的UI**（送信で即ユーザーカード追記＋コンポーザ消去＋思考中→その後リクエスト、失敗時はその発話にinline retry）。**各レビューは必ずAI作の、ログ根拠の問い1つで開く**（空フィールドで開かない）。二段モード（まず低摩擦の自由記述→「もっと深掘りする」チップで多往復へ）。AIの構え2–3種（問いだけ/壁打ち/共感、既定=優しめ）。コンポーザ最重要: `position:sticky` 下部、`dvh`でサイズ（iOSキーボードで隠れない）、`padding-bottom:env(safe-area-inset-bottom)`、自動伸長textarea、≥44pxの送信ボタンを親指圏、Send↔停止クロスフェード、スクロール時「最新へ↓」ピル。
- **タグチップ（#集中 #反省 #学び）**: 低彩度ピル、`--r-chip`、タップでフィルタ。非選択=`--surface-2`地/`--ink-2`/1px`--border`。選択=`--accent-soft`地/`--accent`/`--accent-line`（“淡い紙”、塗り潰しは主CTAだけに温存）。既存の #集中/#反省/#学び を再利用。
- **気分チェック（触覚的な瞬間）**: 5つのくすんだswatch（`--mood-1..5`、笑顔だけでなく疲れ/重い/平坦も、😌🙂😐😔😮‍💨 か素のswatch、マスコット禁止）。選択=springのscale settle＋任意Android haptic。任意で「なぜ？」1行＋ログ紐づけ。D30維持の低摩擦タッチポイント。
- **下部ナビ**: 親指圏のフローティング4項目 **記録 / 対話 / 振り返り / 蓄積(第二の脳)**、インラインSVG＋日本語ラベル11px。**磨りガラスはここだけ**（`-webkit-backdrop-filter:blur(12px) saturate(1.2)`＋`background:color-mix(in srgb, var(--surface) 82%, transparent)` の**不透明フォールバック必須**、`prefers-reduced-transparency`尊重）。active=`--accent`＋小ドット、inactive=`--muted`。

## モーション
「紙にインクが落ち着く」：急がず ease-out 主体、低オーバーシュート。120–160ms タップ / 180–260ms UI・メッセージ入場 / 280–360ms シート・カスケード展開。springは1トークンだけ `--ease-spring: linear(0, 0.5 7%, 0.92, 1.04 30%, 1.0)`（低オーバーシュート、transform/opacityのみ、log確定・シート・トグル・気分選択）。標準は `--ease:cubic-bezier(.2,.6,.2,1)`。メッセージ入場=fade＋6–8px上へ~180ms（scale-popしない）。AIテキストは追記opacityでstream、下端アンカー維持。**オーロラ/mesh呼吸背景は振り返り面だけ**（12s ease-in-out、pulseでなくbreathe）。色ブルーム/“紡いだ”演出は達成マイルストーンだけ。`transform/opacity`のみ60fps（`backdrop-filter`/レイアウトはアニメしない）。`prefers-reduced-motion:reduce` で~150msのopacityのみに縮退。haptic=Android限定の進歩的強化（iOS無視、load-bearingにしない）。

## アイコン
インラインSVG＋絵文字のみ（アイコンフォント/CDN/リモート画像禁止）。小さな一貫セット（ナビ:記録/対話/振り返り/蓄積＋send/back/chevron/plus/calendar/tag）。24×24 viewBox、`stroke:currentColor; stroke-width:1.75; fill:none; stroke-linecap:round; stroke-linejoin:round`（`currentColor`で `--ink/--accent` 継承）。絵文字は感情面（気分行/温かい空状態）だけ。マスコット禁止（コンサル/VC層に幼稚）。

## 実装ノート（`index.html`への落とし込み）
1. `:root`/既定テーマのトークンを上記Lightに差し替え（**適用済み** ~L937–943）。旧`body[data-theme=*]`バリアントは将来的に1アイデンティティへ collapse（**未**：現状は8テーマ残存、既定"red-light"に藍トークンを載せ替えた形）。
2. Darkは `@media (prefers-color-scheme:dark){ :root{...} }` ＋ `:root[data-theme='dark']`/`['light']` 手動トグルで（**未**：現状は "red-dark" テーマに温炭+藍を載せ替え済みだが、prefers-color-scheme 自動切替は未実装。ユーザー期待に沿い auto/light/dark トグル＋localStorage永続を入れる）。任意でOLED真黒トグル。
3. 状態色は `color-mix(in srgb, var(--accent) N%, var(--surface))` で `--accent` から導出し、3色アクセント切替（藍/苔/弁柄）を公開。
4. フォーカスリングは `color-mix(in srgb, var(--accent) 22%, transparent)`（**適用済み**）。
5. レイアウト mobile-first `max-width:480px`、コンポーザ/シートは `dvh`、固定要素は `env(safe-area-inset-*)`。
6. 磨りガラスは `-webkit-backdrop-filter` プレフィックス＋不透明フォールバック、`prefers-reduced-transparency` 尊重。
7. 広い内容（タイムライン/ヒートマップ/表）は自前の `overflow-x:auto` に閉じ、body は横スクロールさせない。
8. 任意：≤3–4%の washi グレイン（inline base64 SVG turbulence、`fixed; pointer-events:none`）。
9. `sw.js`/`manifest.json` はそのまま。`theme_color`/`background_color` は `--bg`（#F6F4EF）に一致（**適用済み**）。
10. BYOK呼び出しは fetch+SSE で楽観的UI＋inline retry、round-trip中もコンポーザをブロックしない。

## 優先順（高レバレッジ順）
1. **クリムゾン全廃→藍/生成り**（トークン差替・テーマバリアント整理・ヘッダ静音・フォーカスリング）＝1変更でアプリ全体を“SaaS警告”から“calm/信頼”へ。**【済】**
2. **温かいダークを一級で**（prefers-color-scheme＋手動auto/light/darkトグル、温炭#151412/85%off-white/rim-light）。**【一部：トークンは用意、自動切替UIは未】**
3. **空状態を全部殺す**（レビュー/日面はAI作のログ根拠の問い or Quick Start＋プロンプトカードで開く）。離脱最大要因＝核の差別化＝D30直結。**【未】**
4. **AI振り返りビューを非IMのstreamingチャット＋stickyコンポーザに**（枠なしAIの“手紙”＋藍ヘアライン、淡い紙のユーザーカード、楽観的UI、トークンstream、三点、Send↔停止、dvh）。**【未】**
5. **日本語組版をグローバル修正**（負の字間を剥がす→+0.02em、読み面1.8、tabular-nums、palt短見出しのみ、font-optical-sizing:auto）。**【未】**
6. **ストリークをやめ寛容な単色藍ヒートマップ＋穏やかな継続コピー**（「7日中5日 記録」）、赤い未達/1–10気分スコアを除去。**【一部：スコア系は旧UIに残存、要撤去】**
7. **ホーム/レビューを calm 2タイルbento＋余白多め**、主ナビをフローティング4項目（記録/対話/振り返り/蓄積）磨りガラス（不透明フォールバック）に。**【未：現状ナビは calendar/対話/today/trend/record/menu の6タブ】**
8. **気分チェック行**＋**日タイムラインの height=duration ブロック（目標エリア色連動）**。**【未】**

## 全文一次資料
本ファイルは 2026-07-11 の多エージェントワークフロー `w0aq13i3f` の統合結果を再構成したもの。5レンズ（ai-journaling / goal-habit-productivity / wellness-calm / mobile-ui-2026 / jp-market-and-chat-ui）の詳細所見は当該runの journal に残る。
