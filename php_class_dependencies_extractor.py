import re
import argparse

parser = argparse.ArgumentParser(description=
    "dephpendのtextコマンドで実行したクラスの依存関係の中から特定のクラスに関連するものを抽出してmermaid記法でグラフを生成するスクリプトです。"
    "コマンド例:"
    "python .\class_dependencies_extractor.py XxxModel ./dephpend_result.txt --black_list ServiceProvider Request Flow Executor ViewModel"
)

parser.add_argument("target_class_name", type=str, help="抽出対象となるクラス名")
parser.add_argument("file_path", type=str, help="dephpend実行結果のファイルパス")
parser.add_argument('--black_list', nargs='+', type=str, help='指定した文言が含まれるクラス名は除外（スペース区切りで複数可）')

# コマンドライン引数を取得
args = parser.parse_args()
target_class_name = args.target_class_name
file_path = args.file_path
if args.black_list:
    black_list = args.black_list
    black_list_filter_word = "|".join(black_list)

# dephpendで取得した依存関係を読み込む
f = open(file_path, 'r')

# ハッシュで検索する形にしてパフォーマンスを上げるために、すべての行を辞書に格納する
class_dependencies_dict = {}
for line in f:
    # 指定した文言が含まれる場合は除外する
    if re.findall(black_list_filter_word, line):
        continue 
    # 「参照元 --> 参照先」という形から参照元と参照先を分割する
    dependency_source, dependency_target = line.split(" --> ")
    # クラス名のみ抽出して\nを取り除く
    dependency_source_class_name = dependency_source.split("\\")[-1].replace("\n", "")
    dependency_target_class_name = dependency_target.split("\\")[-1].replace("\n", "")
    # どこから依存されているか？をチェックすることが目的なので、dict[依存先] = [依存元1, 依存元2]という形にする
    if dependency_target_class_name in class_dependencies_dict:
        class_dependencies_dict[dependency_target_class_name].append(dependency_source_class_name)
    else:
        class_dependencies_dict[dependency_target_class_name] = [dependency_source_class_name]
f.close()

# 指定したクラスの依存関係を調べ上げて出力結果に格納する（幅優先探索の要領で進める）
output = []
queue = []
queue.append(target_class_name)

# 相互に参照するクラスがあったら無限ループになるので処理済みのクラスはfinishedで記録する
finished = []

while queue:
    current_node = queue.pop()
    finished.append(current_node)
    # 末端の場合は次に進む
    if not current_node in class_dependencies_dict:
        continue
    for neighbor_node in class_dependencies_dict[current_node]:
        output_row = neighbor_node + " --> " + current_node
        output.append(output_row)
        if not neighbor_node in queue and not neighbor_node in finished:
            queue.append(neighbor_node)

output_file_path = target_class_name + "_output.md"
output_file = open(output_file_path, "w")

# mermaid記法の最初に書く文を追加する
output_file.write("```mermaid" + "\n")
output_file.write("graph LR" + "\n")

# 抽出した内容をmermaid記法でファイルに書き込む
for line in output:
    print(line)
    output_file.write(line + "\n")

print(len(output))

output_file.close()