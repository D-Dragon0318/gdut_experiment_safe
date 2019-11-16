import re
import common
import json

# config
# test_id 每年都会发生变化 请注意更改
test_id = "459227"
# 手动提交模式
# False: 未找到所有答案的情况下，自动提交并重试
# True: 未找到所有答案的情况下，需要手动打开考试页面，自行修改未作答的题目并提交试卷
manual_mode = False

# define urls
url_home = common.url_base + "index.php"
url_login = common.url_base + 'exam_login.php'
url_entering = common.url_base + 'redir.php?catalog_id=6'
url_exam = common.url_base + "redir.php?catalog_id=6&cmd=kaoshi_chushih&kaoshih=" + test_id
url_answer = common.url_base + 'redir.php?catalog_id=6&cmd=dati'

if __name__ == "__main__":
    with open("./answer.json", "r", encoding="utf8") as f:
        database = json.load(f)
    student_no = input('请输入你的学号：')
    student_password = input('请输入你的密码 默认为123456：')

    # init
    common.http_get(url_home, {})
    login_data = {'xuehao': student_no, 'password': student_password, 'postflag': '1',
                  'cmd': 'login', 'role': '0', '%CC%E1%BD%BB': '%B5%C7%C2%BC'}
    common.http_post(url_login, login_data, {'Referer': url_home, 'Origin': 'http://222.200.98.165:8090'})
    common.http_get(url_home, {'Referer': url_login})
    common.http_get(url_entering, {'Referer': url_home})

    score = 0
    while score < 100:
        found = 0
        question_sheet = common.http_get(url_exam, {'Referer': url_entering})
        extra_headers = {
            'Origin': 'http://222.200.98.165:8090',
            'Referer': url_answer
        }
        for page_id in range(10):
            post_data = {
                'runpage': '0',
                'page': '',
                'direction': '1',
                'tijiao': '0',
                'postflag': '1',
                'autosubmit': '0'
            }
            index = re.search(r'<form method="post" id="dati">(.*?)<div class="nav">', question_sheet,
                              re.I | re.M | re.S).span()
            find_range = question_sheet[index[0]:index[1]]
            question_list = (
                re.findall(r'<div class="shiti"><h3>[0-9]*、(.*?)</h3><ul class=', find_range, re.I | re.M | re.S))

            for question_id in range(10):
                question = question_list[question_id].strip()
                if question in database:
                    post_data['ti_' + str(question_id + page_id * 10 + 1)] = database[question]
                    found += 1
                    print("[成功] " + str(question) + ' \033[7m' + database[question] + "\033[0m")
                else:
                    print("\033[7m" + "[失败] " + str(question) + "\033[0m")

            post_data['page'] = str(page_id)
            if page_id == 9:
                if not manual_mode or found == 100:
                    post_data["tijiao"] = "1"
            question_sheet = common.http_post(url_answer, post_data, extra_headers)
        score = int(re.search(r'本次考试你的得分为<span style="color:#990000">([0-9]{1,3})</span>分', question_sheet,
                              re.I | re.M | re.S).group(1))
        print('得分：' + str(score))
        if manual_mode:
            print("\033[7m" + "[提示] 请手动打开考试页面，自行修改未作答的题目并提交试卷" + "\033[0m")
            break
