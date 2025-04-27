# Stackchan Task Assistant

スタックチャンがあなたのタスクを管理してくれるアシスタントプロジェクトです！  
人を認識すると、Trelloに登録された今日のタスクを教えてくれます。

---

## ✨ 特徴

- 人を認識して自動で挨拶＆タスクを確認
- Trelloと連携してタスクの状態管理（完了・実施中に移動）
- タスク予定時間が近づくと自動リマインド
- VOICEVOXを使ってスタックチャンが音声で喋る
- これから状態管理型（State Machine）に進化予定

---

## 🛠 システム構成

```plaintext
スタックチャン
  ↓
  Pythonアプリ
    - Trello API
    - VOICEVOX API
  ↓
  Trelloでタスク管理
```

---

## ⚙️ セットアップ

1. Python 3.12 環境を用意
2. 仮想環境を作成してアクティベート

```bash
python -m venv venv
source venv/bin/activate  # Windowsなら venv\Scripts\activate
```

3. ライブラリをインストール

```bash
pip install -r requirements.txt
```

4. `.env`ファイルを作成して、以下を記入

```
TRELLO_API_KEY=あなたのTrello APIキー
TRELLO_API_TOKEN=あなたのTrelloトークン
TRELLO_TODO_LIST_ID=タスク追加用リストID
TRELLO_DOING_LIST_ID=作業中リストID
TRELLO_DONE_LIST_ID=完了リストID
```

5. VOICEVOXエンジンを起動

```bash
# 例
docker run --rm -p 50021:50021 voicevox/voicevox_engine
```
またはローカルで起動しておきます。

---

## 🚀 起動方法

```bash
python -m app.main
```

スタックチャンが起動し、待機状態になります！

- `/detect {名前}` を入力すると認識トリガー
- Trelloからタスクを取得して対話を開始します
- タスクが残っていれば、やったか？いつやるか？を聞いてきます

---

## ⚠️ 注意事項

- `.env`ファイルは必ず`.gitignore`に追加して、GitHubに公開しないようにしてください
- Trelloの各リストIDが正しいことを確認してください
- VOICEVOXエンジンを起動してからアプリを実行してください
- スタックチャンの自由会話モードを使用する場合、ChatAPIクライアント設定も必要です

---

## 🌟 今後の拡張予定

- 状態管理（State Machine）をベースにリファクタリング
- 雑談の中にタスク確認を自然に挟む自然会話モード
- タスク登録やタスク完了報告の自動化
- Slack連携、センサー連動も検討

---

# 📢 ライセンス・免責事項

- 本プロジェクトは個人利用・学習目的に作成されています。
- Trello API、VOICEVOX APIの利用規約に従ってご利用ください。

