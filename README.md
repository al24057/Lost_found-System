# Campus_Lost&Found
> **カスタマイズ済みYOLOを活用した学内落とし物スマート管理システム**

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2.13-092e20?logo=django)](https://www.djangoproject.com/)
[![YOLO](https://img.shields.io/badge/Model-YOLOv26-00FFFF?logo=ultralytics)](https://github.com/ultralytics/ultralytics)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📝 概要
キャンパス内での落とし物管理を自動化し、学生課に赴かなければ忘れ物があるかどうかわからないというユーザの不安や労力をすぐさま軽減するための、掲示板型のWebアプリケーションです。YOLOv26をファインチューニングし、ユーザが写真をアップロードするだけで、AIが写真を解析し、色やアイテムのカテゴリを仮決めします。

## ✨ 主な機能
- 🔐 **学内者限定ログイン**: Google OAuth 2.0を利用し、特定のドメイン（@school.ac.jp）のみアクセス可能。
- 🔍 **AI自動解析**: アップロードされた画像をYOLOv26で解析し、アイテム（財布、スマホなど）や色のカテゴリを自動判定。
- 📁 **スマート検索**: アイテムや色のカテゴリによる絞り込み検索。
- 📱 **レスポンシブ対応**: スマホからもPCからも使いやすいUI。
- 🛡️ **不正抑止**: 全ての投稿詳細閲覧ログおよび「チェックマーク（自分の落とし物です）」申告時のユーザー情報をデータベースに記録。

## 🚀 今後の展望
本プロジェクトは、単なる管理システムを超え、学内コミュニティの善意を最大化するプラットフォームへの進化を目指しています。

- **徳（Toku）ポイントシステム**
    - 落とし物の届け出や持ち主への返却完了時に「徳ポイント」を付与。
    - 蓄積されたポイントに基づく称号授与や学内ランキングの実装。
    - 将来的な学内生協マネーとの連携プロトタイプ設計。
- **デジタルツイン・マップ連携**
    - デジタルハイパーツイン技術を活用し、キャンパスの3D空間上に発見場所をプロット。
    - 視覚的なナビゲーションにより、広いキャンパス内でも正確な発見場所を特定可能にします。
- **異常挙動の自動検知アルゴリズム**
    - ログデータを解析し、短時間での大量閲覧や、不自然な解決申告をシステムが自動でフラグ（警告）を立てる機能の実装。

## 🛠️ セットアップと開発手順

### 📋 前提条件
本システムの実行には **Python 3.11 以上** が必要です。
インストールされていない場合は、[Python公式サイト](https://www.python.org/downloads/)よりダウンロードしてセットアップを完了させてください。

### 1. リポジトリのクローンと環境構築
まずはリポジトリを手元にコピーし、仮想環境を構築します。プロジェクトを行いたいディレクトリに移動し、以下のコマンドを順に実行してください。

```bash
#リポジトリのクローン
git clone https://github.com/al24057/Lost_found-System

#クローンしたリポジトリへ移動
cd Lost_found-System

# 仮想環境の作成
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存ライブラリのインストール
pip install -r requirements.txt
```

### 2. 作業ブランチの作成と開発サイクル（開発メンバー向け）
**重要：** 設定ファイルを作成する前に、必ず作業用のブランチを作成してください。直接 main で作業することは避け、必ず自分のブランチで作業してください。

#### ブランチの作成と反映
```bash
# 最新状態の取得
git checkout main
git pull origin main

#ブランチの作成
git checkout -b your-branch-name    # your-branch-nameには誰の作業ブランチかわかるような名前をつけてください。

#ブランチをGitHub上に初回反映
git push -u origin your-branch-name # your-branch-nameには一つ前のコマンドで設定した名前を入れてください。
```

#### 基本的な開発サイクル（※随時実施）
**※このステップは、環境構築の段階では実行不要です。実際にコードを書き換え、作業を保存したいタイミングで以下のコマンドを順に実行してください。**

```bash
# 1. 変更したファイルをステージングに追加
git add .

# 2. コミット（作業内容を記録）
git commit -m "変更内容の短い説明"

# 3. GitHubへプッシュ（2回目以降は git push だけでOK）
git push
```
作業が完了したら、GitHub上のリポジトリページから **Pull Request (PR)** を作成してください。管理者が内容を確認し、 `main` ブランチへマージします。

#### Pull Request (PR)の作成（※随時実施）
**※このステップは、環境構築の段階では実行不要です。実際に自分のブランチへ変更をプッシュした後、 `main` ブランチへ変更を合流させたいタイミングで以下を順に実行してください。**

1. GitHubのリポジトリページを開くと表示される **[Compare & pull request]** ボタンをクリック。
2. **ブランチの方向を必ず確認：**
   設定が **`base: main` ← `compare: your-branch-name`** になっていることを確認してください（逆方向にならないよう注意）。
3. **レビューの依頼：**
   画面右側の **Reviewers** 欄から、管理者の **al24057** を選択して指名してください。
4. **内容の記述：**
   実施した作業内容を簡潔に記述し、**[Create pull request]** をクリック。

> [!IMPORTANT]
> **マージのルールについて**
> 本プロジェクトでは管理者の承認（Approve）が必須です。あなたが PR を作成した後、管理者が内容を確認して「Approve」を出すことで、初めてマージボタンが有効になります。

### 3. 環境構築の準備
セキュリティとポータビリティを両立するため、本システムは環境変数で設定を管理しています。プロジェクトのルートディレクトリに `.env.example` ファイルを参考にして `.env` ファイルを作成し、以下の内容を設定してください。

```text
# ドメイン設定
ALLOWED_DOMAIN = example.com         # example.comには制限したいドメインを入れてください。

# Django基本設定
SECRET_KEY = your-random-secret-key  # 各自でランダムな文字列を設定してください
DEBUG = True

# Google OAuth設定
GOOGLE_CLIENT_ID = your-google-client-id
GOOGLE_CLIENT_SECRET = your-google-client-secret

# データベース設定
DB_NAME = your_database_name.sqlite3 # your_database_nameにはあなたのデータベース名にしたい名前を入れてください。
```

**重要：.envファイルは絶対にGitHubへプッシュしないでください**

.env にはGoogle認証の鍵などの機密情報が含まれています。万が一公開されると、悪意のある第三者にシステムを操作される恐れがあります。以下のコマンドを実行して一覧に `.env` ファイルが含まれていないことを確認してください。

```bash
#.envファイルがgitの追跡対象に含まれていないかを確認
git ls-files
```

#### Note:
- .envファイルは機密情報を含むため、Git管理から除外しています。
- GOOGLE_CLIENT_ID / SECRET は、開発チームから共有されたもの、もしくは自身で取得したものを設定してください。
- 本番環境への移行時: サーバー上の .env ファイルを本番用に書き換えるだけで、ソースコードを変更することなく即座に切り替えが可能です。

### 4. AIモデル（YOLOv26）の配置
本システムのコアとなる解析モデルを以下のディレクトリに配置してください。
- **配置パス:** Lost_found_Web/ml_models/your_best.pt
- **入手方法:** 開発チーム内の共有ストレージよりダウンロード、または学習済みカスタムウェイトを配置してください。

### 5. データベースの初期化と起動
```bash
#データベースのマイグレーション
python manage.py migrate

#開発サーバの起動
python manage.py runserver
```

起動後、ブラウザで http://127.0.0.1:8000 にアクセスしてください。

## 📂 ディレクトリ構造
```text
Lost_found-System/
 ├── Lost_found_System/        # プロジェクト全体ルート
 │   ├── Lost_found_System/    # プロジェクト設定フォルダ
 │   │   ├── settings.py       # 環境変数(.env)の読み込み・基本設定
 │   │   └── urls.py           # 全体のルートURL定義
 │   ├── Lost_found_Web/       # メインアプリケーション（ロジック担当）
 │   │   ├── ml_models/        # 【重要】YOLOv26学習済みモデル(best.pt)の配置先
 │   │   ├── services/
 │   │   │   └── signals.py    # Googleログイン時のユーザー情報自動保存ロジック
 │   │   ├── adapter.py        # 特定ドメイン(@school.ac.jp)限定の認証フィルター
 │   │   ├── forms.py          # 拾得物投稿フォーム・バリデーション定義
 │   │   ├── views.py          # AI解析結果の処理・画面表示制御
 │   │   └── models.py         # 落とし物・ログ・ユーザー情報のDB定義
 │   ├── media/
 │   │   └── lost_items/       # アップロードされた落とし物写真の保存先
 │   ├── static/               # プロジェクト全体のCSS, JavaScript, 画像資産
 │   ├── templates/            # プロジェクト全体のHTMLテンプレート
 │   └── manage.py             # Django管理コマンド実行ファイル
 ├── .env                      # 環境変数設定ファイル（Git除外）
 └── requirements.txt          # 依存ライブラリ一覧
```

## 🌐 デプロイに関する補足
本システムは学内ネットワークへのデプロイを想定しています。
- **柔軟な認証切り替え:** Google OAuthの設定はすべて .env で管理されているため、デプロイ後に正式なドメインや組織用IDが確定した際も、サーバー上の設定ファイルを更新するだけでダウンタイムなしに正式運用へ移行可能です。
- **デバッグモード:** 本番稼働時は .env 内の DEBUG=False に設定し、セキュリティを確保してください。
- **スケーラビリティへの対応:** 現在は開発効率を優先しSQLiteを使用していますが、学内利用者（約1万人規模）の同時アクセスに耐えうる堅牢なデータ整合性とパフォーマンスを確保するため、本番環境では **PostgreSQL** への移行を前提とした設計を行っています。

## 📜 ライセンス
MIT License に基づき公開されています。

**Author:** al24057
