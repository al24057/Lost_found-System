FROM python:3.11-slim

# OpenCVやYOLOの動作に必要なLinuxライブラリをインストール
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

# requirements.txt をコピーしてパッケージをインストール
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 残りのプログラム一式をコピー
COPY . .

# データベースの初期化と静的ファイルの集約
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# ポート7860でDjangoを起動
CMD ["python", "manage.py", "runserver", "0.0.0.0:7860"]