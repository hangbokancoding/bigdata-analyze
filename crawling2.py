import requests
from bs4 import BeautifulSoup
import csv
import sys

# 프로그래밍 파일 확장자 나열
programming_file_extensions = (".py", ".c", ".cpp", ".java", ".cs", ".js", ".go")

# i번째 페이지 불러오고 분석
respose = requests.get(f"https://gist.github.com/starred?page={sys.argv[1]}")
soup = BeautifulSoup(respose.content, "html.parser")

# gist의 파일명 불러오기
gist_names_in_page = soup.select(".css-truncate-target")

names = []
codes = []

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

        names.append(gist_name.text)
        codes.append(code)

        code_respose.close()

res = []
for i in range(len(names)):
    name = names[i]
    code = codes[i]
    res.append(f"{name}\n{code}")
print("\n==<SEPERATOR>==\n".join(res))
respose.close()
