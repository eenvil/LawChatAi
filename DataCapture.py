import json 
import webbrowser
import os
import time
import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
import multiprocess as mp
import requests
from bs4 import BeautifulSoup
import json

def fetch_and_parse_content(url):
    # 發送請求
    response = requests.get(url)
    # 檢查響應狀態碼
    if response.status_code != 200:
        return "Error: Unable to fetch the webpage"
    
    # 解析HTML內容
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 找到目標div
    target_div = soup.find('div', {'id': 'sandbox', 'class': 'draw-focus'})
    
    if not target_div:
        return "Error: Target div not found"
    
    # 獲取<pre>標籤內的文本
    pre_text = target_div.find('pre').get_text(strip=True)
    # 尋找關鍵詞並分割文字
    question_start = pre_text.find('法律問題') + len('法律問題')
    question_end = pre_text.find('討論意見')
    answer_start = pre_text.find('理由') + len('理由')
    if answer_start == -1:
        answer_start = pre_text.find('意見') + len('意見')
    if answer_start == -1:
        amswer_start = pre_text.find('解釋') + len('解釋')
    if answer_start == -1:
        answer_start = pre_text.find('說明') + len('說明')
    if answer_start == -1:
        answer_start = pre_text.find('結果') + len('結果')
    print(pre_text[answer_start:])
    #find the next ':' after '理由'
    answer_end = pre_text.find('：', answer_start+5)
    #fint the next '。' between '理由' and answer_end that is as close to answer_end as possible
    answer_end = pre_text.rfind('。', answer_start, answer_end) + 1
    print(question_start, question_end, answer_start, answer_end)
    
    if question_start == -1 or answer_start == -1 or question_end == -1 or answer_end == -1:
        return "Error: Required text markers not found"
    
    question_text = pre_text[question_start:question_end].strip().replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')
    answer_text = pre_text[answer_start:answer_end].strip().replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')
    
    # 創建JSON輸出
    result = {
        "question": question_text,
        "answer": answer_text
    }
    result["url"] = url
    return result
# 使用函式的範例
url = input("Enter URL: ")
result = fetch_and_parse_content(url)
with open("result.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=4)
