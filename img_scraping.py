# コマンド引数の一つ目に、欲しい画像の名前
#             二つ目に、欲しい枚数(20おきに読み込むため余分な枚数が出る)


from bs4 import BeautifulSoup
from requests import get
import urllib.request
import urllib.parse
import sys  # sysモジュールとはsystemmoduleのこと
import os
import time

num = 0
query_word = sys.argv[1] 
target_num = -(-(int(sys.argv[2])) // 20)  # 割り算の切り上げで、必要なページ数を表している
# 1ページが20枚分

for num in range(target_num):
    url = f"https://search.yahoo.co.jp/image/search?p={query_word}&ei=UTF-8&b={1 + 20*num}"
    resp = get(url)
    time.sleep(2)
    soup = BeautifulSoup(resp.content, "html.parser")

    imgs = soup.find_all(
        alt=f"「{query_word}」の画像検索結果"
    )  # alt＝～はyahoo側が画像を探し出せなかったときに表示するもの

    for i in range(len(imgs)):
        dir_name = f".\data\{query_word}"
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        filepath = dir_name + f"/{num}-{i}.jpg"
        urllib.request.urlretrieve(imgs[i]["src"], filepath)
