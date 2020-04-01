import sys
import requests
from bs4 import BeautifulSoup
import urllib.request
import os
import time
from tqdm import tqdm

def input_request():
    if len(sys.argv) == 3:
        query_word = sys.argv[1]
        all_num = int(sys.argv[2])
        pages_num = -(-(all_num) // 20)
    else:
        while True:
            query_word = input("query_word: ")
            if not " " in query_word:
                break
            else:
                print("空白文字は使えません")
                continue        
        all_num = int(input("How many: "))
        pages_num = -(-(all_num) // 20)

    return query_word, all_num, pages_num   

def mkdirs(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def imgs_scraping(query_word, all_num, pages_num):
    print("\nRunning")
    dir_name = f".\data\{query_word}"
    mkdirs(dir_name)
    print("Downloading")
    for num in range(pages_num):
        print(f"{num + 1}/{pages_num}")
        url = f"https://search.yahoo.co.jp/image/search?p={query_word}&ei=UTF-8&b={1 + 20 * num}"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser") 
        imgs = soup.find_all(alt=f"「{query_word}」の画像検索結果")      

        if num == (pages_num - 1):
            nlast = all_num % 20
            if nlast == 0:
                nlast = 20     
            for i in range(nlast):
                file_name = dir_name + f"\{num}-{i}.jpg"
                urllib.request.urlretrieve(imgs[i]["src"], file_name)
                             
        else:
            for i in range(20):
                file_name = dir_name + f"\{num}-{i}.jpg"
                try:
                    urllib.request.urlretrieve(imgs[i]["src"], file_name)     
                except Exception as e:
                    print(f"{e} 何らかの理由で画像が検索できません\n{url}")
                    sys.exit()
def main():
    while True:
        data = input_request()
        mkdirs("\data")
        imgs_scraping(data[0], data[1], data[2])
        print("\nSuccessfully\n\n")
main()    
