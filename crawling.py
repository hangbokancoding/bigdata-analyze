import requests
from bs4 import BeautifulSoup
import csv

print()

max_page = 50

# 프로그래밍 파일 확장자 나열
programming_file_extensions = (".py", ".c", ".cpp", ".java", ".cs", ".js", ".go")

# csv 파일 생성
csv_file = open("output.csv", "w", encoding="utf-8")
writer = csv.writer(csv_file)
writer.writerow(["name", "code"])

# 1~max_page까지의 페이지 내 코드 가져오기
for i in range(1, max_page + 1):
    # i번째 페이지 불러오고 분석
    respose = requests.get(f"https://gist.github.com/starred?page={i}")
    soup = BeautifulSoup(respose.content, "html.parser")

    # gist의 파일명 불러오기
    gist_names_in_page = soup.select(".css-truncate-target")

    for j, gist_name in enumerate(gist_names_in_page):
        # 확장자 검사
        if gist_name.text.endswith(programming_file_extensions):
            # gist starred 페이지에서는 전체코드가 안 나오기 때문에 href속성을 이용해 전체 코드 열람
            gist_code = soup.select_one(f".gist-snippet:nth-child({j+1}) .link-overlay")
            code_url = gist_code.get_attribute_list("href")[0]

            code_respose = requests.get(code_url)
            code_soup = BeautifulSoup(code_respose.content, "html.parser")
            lines = code_soup.select(".blob-code-inner")
            code = "\n".join([line.text for line in lines])

            # csv 파일명, 코드 쓰기
            writer.writerow([gist_name.text, code])

            code_respose.close()

    respose.close()
    print(f"\r[{i}/{max_page}] done!", end="")

csv_file.close()
print("\rall done!", " " * 10)
