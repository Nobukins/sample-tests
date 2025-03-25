# Browser Automation Script

このプロジェクトは、Playwright を使用した簡単なブラウザ自動化ツールです。定義されたアクションを実行し、ブラウザ操作を自動化することができます。

## インストール

### 前提条件

- Python 3.8+
- pip

### セットアップ

1. 依存関係をインストールします:

```bash
pip install playwright
playwright install chromium
```

## 使用方法

### 基本的な使い方

```bash
python action_runner.py --action <アクション名> [オプション]
```

### 利用可能なオプション

- `--action`: 実行するアクションファイル名（拡張子なし）
- `--query`: 検索クエリ（アクションで使用される）
- `--slowmo`: スロー実行の時間（ミリ秒）
- `--headless`: ヘッドレスモードで実行（画面表示なし）
- `--countdown`: 終了前のカウントダウン時間（秒）
- `--new`: 新しいアクションテンプレートを作成
- `--list`: 利用可能なアクションを一覧表示

### 例

1. 利用可能なアクションを一覧表示:
```bash
python action_runner.py --list
```

2. 特定のアクションを実行:
```bash
python action_runner.py --action nogtips_search --query "Playwright"
```

3. 新しいアクションテンプレートを作成:
```bash
python action_runner.py --new my_custom_action
```

## 独自アクションの作成

1. 新しいアクションテンプレートを作成:
```bash
python action_runner.py --new my_action
```

2. 生成された `actions/my_action.py` ファイルを編集します。

3. Playwright Codegenを使用してブラウザ操作を記録します:
```bash
playwright codegen
```

4. 生成されたコードを `run_actions` 関数内に貼り付けます。

5. 実行:
```bash
python action_runner.py --action my_action
```

## 既存のアクション

### nogtips_search
nogtipsサイトで検索を実行します:
```bash
python action_runner.py --action nogtips_search --query "検索ワード"
```

## 高度な使用例

スロー実行とカウントダウン時間を設定:
```bash
python action_runner.py --action nogtips_search --query "Playwright" --slowmo 100 --countdown 3
```

ヘッドレスモードで実行:
```bash
python action_runner.py --action nogtips_search --query "Playwright" --headless
```
