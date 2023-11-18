package main

// 모듈/라이브러리 가져오기
import (
	"bufio"
	"encoding/csv"
	"fmt"
	"os"
	"os/exec"
	"strconv"
	"strings"
)

// 진입점
func main() {
	// 채널 생성 (비동기 사용시 데이터 처리에 사용)
	resultCodes := make(chan string)
	count := 100

	for i := 1; i <= count; i++ {
		// 비동기 사용
		go func(page int) {
			// crawling.py 실행
			cmd := exec.Command("py", "crawling2.py", strconv.Itoa(page))
			cmd.Dir = "C:\\Users\\cdh88\\Documents\\programming\\python\\bigdata\\project2"

			// 결과 가져오기
			output, err := cmd.Output()

			if err != nil {
				fmt.Println(err)
			}

			// 채널에 값 넣기
			resultCodes <- string(output)
		}(i)
	}

	result := [][]string{}
	for i := 1; i <= count; i++ {
		codes := <-resultCodes
		// "\n==<SEPERATOR>==\n"로 데이터 나누기
		_code := strings.Split(codes, "\n==<SEPERATOR>==\n")
		for _, c := range _code {
			nameAndCode := strings.Split(c, "\n")
			name := nameAndCode[0]
			code := strings.Join(nameAndCode[1:], "\n")
			if len(strings.TrimSpace(name)) != 0 && len(strings.TrimSpace(code)) != 0 {
				// 문제 없을 경우 데이터 주입
				result = append(result, []string{name, code})
			}
		}
	}

	// csv 생성
	file, err := os.Create("./output2.csv")
	if err != nil {
		panic(err)
	}

	wr := csv.NewWriter(bufio.NewWriter(file))

	// csv 작성
	wr.Write([]string{"name", "code"})
	wr.WriteAll(result)
	wr.Flush()
}
