# 概要
[dephpend](https://github.com/mihaeu/dephpend)で抽出したクラス依存関係の中から特定のクラスに関連したものだけを抽出後、  
mermaid記法でグラフを生成をするスクリプトです。

# 開発環境
Python 3.11.6

# 使用方法（Laravelのappフォルダ以下の例）
## dephpend
- 開発環境にdephpendをインストール  
composer global require dephpend/dephpend:dev-main --dev
- appフォルダ以下の全ての依存関係をテキスト形式で出力する  
./vendor/dephpend/dephpend/bin/dephpend text app > dephpend_result.txt

## スクリプトの実行（例）
- 調査対象となるクラス、出力した依存関係、除外対象となる文言を指定してスクリプトを実行する  
### Windows
python class_dependencies_extractor.py MonthlyBillingTransaction ./dephpend_result.txt --black_list ServiceProvider Request Flow Executor ViewModel
### Mac
python3 .\class_dependencies_extractor.py MonthlyBillingTransaction ./dephpend_result.txt --black_list ServiceProvider Request Flow Executor ViewModel