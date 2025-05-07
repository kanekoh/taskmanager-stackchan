FROM debian

# gitをインストールします。
# ソース[1]で simple-stt-server リポジトリをクローンするために必要です。
RUN apt-get update && \
    apt-get install -y --no-install-recommends npm git wget unzip ca-certificates build-essential && \
    rm -rf /var/lib/apt/lists/*

# simple-stt-server リポジトリをクローンします。
# ソース[1]で示されている手順です。
RUN git clone https://github.com/meganetaaan/simple-stt-server.git /app/simple-stt-server

# 作業ディレクトリを simple-stt-server ディレクトリに変更します。
# ソース[1]で示されている `cd simple-stt-server` に対応します。
WORKDIR /app/simple-stt-server

# 必要なnpmパッケージをインストールします。
RUN npm install

# VOSKモデルファイルをダウンロードし、展開します。
# ソース[1]でモデルファイルをダウンロード・展開し、modelディレクトリに配置する手順が示されています。
# ここではユーザーから指定されたURLを使用し、wgetとunzipコマンド（ソースには明記されていません）を使用して自動化します。
# Note: This step downloads the model file using the URL provided by the user.
# Note: wget and unzip commands are used for this purpose, which are not explicitly in the source.
RUN mkdir model && \
    wget https://alphacephei.com/vosk/models/vosk-model-ja-0.22.zip -O vosk-model-ja-0.22.zip && \
    unzip vosk-model-ja-0.22.zip -d model && \
    rm vosk-model-ja-0.22.zip # ダウンロードしたzipファイルを削除してイメージサイズを削減

# コンテナが起動した際に実行するコマンドを指定します。
# ソース[2]で示されている `npm start` コマンドです。
# ソース[2]では、PCマイク認識のために `--device default` オプションが必要な場合があることも言及されています。
# ご自身の環境に合わせて、必要であれば `CMD ["npm", "start"]` に変更してください。
CMD ["npm", "start", "--", "--device", "default"]

# VOSKサーバーはデフォルトでポート8080で待機します。
# ソース[2]のログに記載されています。
# このポートを外部に公開することで、ｽﾀｯｸﾁｬﾝやブラウザからアクセスできるようになります。
EXPOSE 8080