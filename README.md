# fulltext-demo-app
Demo app for fulltext and streamlit.

## fulltext
本家のリポジトリではExcelに対応していなかったため、fork先を利用しています。
- 本家: https://github.com/btimby/fulltext
- fork先: https://github.com/beatrust/fulltext

### 既知の未対応ファイル & 怪しい挙動
- 日本語を含む画像
  - OCRライブラリが日本語に対応していないため
- floatを含むjsonファイル
  - fulltextの実装上の都合
	- 該当箇所: https://github.com/btimby/fulltext/blob/master/fulltext/backends/__json.py
- 対応していないファイル形式に対して、エラー等ではなく空文字列が返される場合がある
  - 文字列がないファイルとの見分けがつかない

## streamlit ( https://streamlit.io/ )
フロントをPythonで手軽に実装できるライブラリ。

### デプロイ
デモアプリとしてはstreamlitのクラウド( https://docs.streamlit.io/streamlit-cloud )を使ってデプロイしています。

→ https://share.streamlit.io/ikokobi/fulltext-demo-app
