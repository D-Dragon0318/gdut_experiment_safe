import re
import common
import json

# config
database_id = "409399"
max_page = 200

last_view = common.url_base + "redir.php?catalog_id=6&tikubh=" + database_id + "&cmd=learning"
dataset = {}
for i in range(200):
    print("Fetching Page " + str(i + 1))
    url_page = common.url_base + 'redir.php?catalog_id=6&cmd=learning&tikubh=' + database_id + '&page=' + str(i + 1)
    headers = {'Referer': last_view}
    result = common.http_get(url_page, headers)
    last_view = url_page

    index = re.search(r'<div class="shiti-content">(.*?)<div class="fy">', result, re.I | re.M | re.S).span()
    find_range = result[index[0]:index[1]]
    find_result = re.findall(
        r'<div class="shiti"><h3>[0-9]*、(.*?)</h3>.*?<span style="color:#666666">（标准答案： {4}(.*?)）</span>',
        find_range, re.I | re.M | re.S)
    for (question, answer) in find_result:
        dataset[question.strip()] = str(answer).replace("正确", "1").replace("错误", "0").replace("\r\n", "").strip()
with open("./answer.json", "w", encoding="utf8") as f:
    json.dump(dataset, f, ensure_ascii=False)
