import argparse
import json
import re

from logzero import logger

"""Wikipedia の 全データから、テレビアニメの記事の部分のみを取ってくるスクリプトです。
Wikiextractor で抽出したテキストデータを使います。
https://qiita.com/hoppiece_/items/72753b7ac08f0bd4993f
"""

# ファイルはWikipediaのダンプファイルを WikiExtractor.py で抽出したもの. 3GBの巨大テキスト
EXTRACTED_WIKIPEDIA_PATH = "/Users/JP26788/Documents/data/wikipedia/extracted_text.txt"


def create_title_set(filename="animeinfo.json"):
    try:
        with open("animeinfo.json") as fp:
            anime_info_list = json.loads(fp.read())
    except FileNotFoundError:
        logger.error("create 'animeinfo.json' by running animeinfocrawl.py")

    titles = set()
    for info in anime_info_list:
        titles.add(info["title"])
    return titles


def main():
    parser = argparse.ArgumentParser()
    help_msg = """
    path to the corpus extracted by WikiExtractor.py.\
    More detail: https://qiita.com/hoppiece_/items/72753b7ac08f0bd4993f"
    """
    parser.add_argument("path", help=help_msg)
    args = parser.parse_args()

    titles = create_title_set()
    start_pat = re.compile(r'<doc id="(\d+)" url="(.+?)" title="(.+?)">')
    end_pat = re.compile(r"</doc>")
    is_in_wanted_article = False
    count = 0
    with open(args.path) as fp:
        for line in fp:
            if start_pat.match(line):
                doc_id = start_pat.sub(r"\1", line.strip())
                url = start_pat.sub(r"\2", line.strip())
                title = start_pat.sub(r"\3", line.strip())

                if title in titles:
                    count += 1
                    is_in_wanted_article = True
                    article = ""
                    animeinfo = dict()
                    animeinfo["title"] = title
                    animeinfo["doc_id"] = doc_id
                    animeinfo["url"] = url
                    logger.info(f"{count}/{len(titles)}\t{title}")

                continue

            if end_pat.match(line):
                if is_in_wanted_article:
                    animeinfo["article"] = article
                    print(json.dumps(animeinfo, ensure_ascii=False))

                is_in_wanted_article = False

                continue

            if is_in_wanted_article:
                article += line


if __name__ == "__main__":
    main()
