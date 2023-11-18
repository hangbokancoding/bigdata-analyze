from collections import Counter
import csv
import sys
from matplotlib import pyplot as plt
from wordcloud import WordCloud
import pandas as pd

# csv 최대 행 개수 오류 해결용
maxInt = sys.maxsize
while True:
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt / 10)

# csv 파일 읽기
df = pd.read_csv("./output.csv")
all_words = []

max_len = len(df["code"])
for i in range(0, max_len):
    line = df.iloc[i, 1]  # 코드 가져오기

    if len(line) > 0:
        # 문자열을 공백과 개행 문자로 분리하여 단어 list 생성
        words = line.replace("\n", " ").replace("\r", " ").split(" ")
        words = [word for word in words if len(word) != 0]
        all_words.append(words)
    print(f"[{i+1}/{max_len}] done!\r", end="")

# 2차원 배열을 1차원 배열로 평탄화
# list가 커서 numpy로는 에러 발생함. 따라서 이 방법 사용하여 오류 해결
flatten_all_words = [data for inner_list in all_words for data in inner_list]

# 빈도수 분석
c = Counter(flatten_all_words)

# result.csv 쓰기
f = open("result/result.csv", "w", encoding="utf-8")
wr = csv.writer(f)
# 빈도수가 가장 많은 순서로 위부터 채움
wr.writerows(
    [[x, c[x]] for x in dict(sorted(c.items(), key=lambda x: x[1], reverse=True))]
)
f.close()

# 워드 클라우드 생성
wc = WordCloud(
    font_path="malgun",
    width=400,
    height=400,
    background_color="white",
)
gen = wc.generate_from_frequencies(c)

plt.figure()
plt.imshow(gen)
wc.to_file(f"result/result.png")

f.close()
print("\nall done!", " " * 10)
