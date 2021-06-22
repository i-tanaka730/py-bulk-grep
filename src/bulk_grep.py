# -*- coding: utf-8 -*-

import os
import re

from chardet.universaldetector import UniversalDetector

# 検索対象のディレクトリ
search_dir = r"C:\Git\SvnLib"

# 検索対象の文字列
search_patterns = (
  "using System.Linq",
  "using System.Diagnostics"
)

# 検索対象の拡張子
ext_patterns = (
    ".cs"
)

# 指定したディレクトリ＋ファイルを検索し、
# 「ファイルパス」「行数」「行の文字列」のファイル情報リストを作成する
def search_files(dir_path, file_name_list, search_pattern):
    matched_list = []
    for file_name in file_name_list:
        # ファイル名から拡張子を取得
        _, ext = os.path.splitext(file_name)

        # 拡張子が取得できない場合はスキップ
        if not ext:
            continue

        # 検索対象の拡張子に一致しない場合はスキップ
        if not ext in ext_patterns:
            continue

        # ファイルのフルパスを作成
        file_path = os.path.join(dir_path, file_name)
        # ファイルをオープン
        with open(file_path, encoding="utf-8") as f:
            line_number = 1
            # 行毎に検索し、検索対象文字列に一致する場合は
            # ファイル情報を作成しリストに追加する
            for line in f:
                m = re.search(search_pattern, line)
                if m:
                    file_info = {
                        "path": file_path,
                        "line_number": line_number,
                        "line": line.strip()
                    }
                    matched_list.append(file_info)
                line_number = line_number + 1
    return matched_list

# ヒットした「ファイルパス」「行数」「行の文字列」を出力する
def print_matched_list(matched_list):
    for file_info in matched_list:
        print("%s,%d : %s" % (file_info["path"], file_info["line_number"], file_info["line"]))

matched_list = []

# 指定したディレクトリを走査する(サブディレクトリも対象となる)
#  - root : 現在のディレクトリ
#  - dirs : 内包するディレクトリ(未使用)
#  - files : 内包するファイル
for root, dirs, files in os.walk(search_dir):
    for search_pattern in search_patterns:
        sub_matched_list = search_files(root, files, search_pattern)
        matched_list.extend(sub_matched_list)

# 出力
print_matched_list(matched_list)