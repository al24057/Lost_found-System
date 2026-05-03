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
- 📁 **スマート検索**: カテゴリ、日時、場所による絞り込み検索。
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

## 🛠️ クイックスタート

### 📋 前提条件
本システムの実行には **Python 3.11 以上** が必要です。
インストールされていない場合は、[Python公式サイト](https://www.python.org/downloads/)よりダウンロードしてセットアップを完了させてください。

### 1. 環境構築
```bash
# 仮想環境の作成
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存ライブラリのインストール
pip install -r requirements.txt
```

### 2. 環境構築の準備
セキュリティとポータビリティを両立するため、本システムは環境変数で設定を管理しています。プロジェクトのルートディレクトリに `.env` ファイルを作成し、以下の内容を設定してください。

```text
# ドメイン設定
ALLOWED_DOMAIN = example.com

# Django基本設定
SECRET_KEY = your-random-secret-key  # 各自でランダムな文字列を設定してください
DEBUG = True

# Google OAuth設定
GOOGLE_CLIENT_ID = your-google-client-id
GOOGLE_CLIENT_SECRET = your-google-client-secret

# データベース設定
DB_NAME = your_database_name.sqlite3
```

#### Note:
- .envファイルは機密情報を含むため、Git管理から除外しています。
- GOOGLE_CLIENT_ID / SECRET は、開発チームから共有されたもの、もしくは自身で取得したものを設定してください。
- 本番環境への移行時: サーバー上の .env ファイルを本番用に書き換えるだけで、ソースコードを変更することなく即座に切り替えが可能です。

### 3. AIモデル（YOLOv26）の配置
本システムのコアとなる解析モデルを以下のディレクトリに配置してください。
