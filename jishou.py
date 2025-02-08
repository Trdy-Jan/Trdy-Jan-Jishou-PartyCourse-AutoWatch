# 导入
import os
from datetime import datetime
import requests
from DrissionPage import Chromium, ChromiumOptions
import time

from test import browser


def welcome_message():
    print("===============================================")
    print("        欢迎使用 棘手大学智慧党建自动学习脚本！        ")
    print("===============================================")
    print("感谢你选择本脚本，它将帮助你更高效地学习并管理党建相关内容。")
    print("此脚本集成了自动学习功能，旨在帮助党员和党建工作者提高学习效率。")
    print("祝学习愉快！")
    print("===============================================")
    print("                    使用注意事项：            ")
    print("===============================================")
    print("1. 确保脚本运行环境稳定，避免在网络不稳定时运行。")
    print("2. 本脚本仅供学习和研究使用，任何不当用途由使用者自行负责。")
    print("3. 如需开启通知，请提前下载PushMe APP，并获取密钥。")
    print("4. APP地址：https://github.com/yafoo/pushme/releases/download/v3.0.0/PushMe-3.0.0.apk")
    print("5. 请确保你的账号和密码正确，否则无法正常登录。")
    print("6. 使用本脚本造成的后果由使用者自行承担，与脚本作者无关。")
    print("7. 如果遇到运行问题，重启电脑运行即可")
    print("===============================================")
    input("按回车键继续...")


def clear_screen():
    """清屏函数"""
    os.system('cls' if os.name == 'nt' else 'clear')


welcome_message()
clear_screen()

student_id ='2022401596'
password = "EUbDR!x9p9hCsT82"
push_key =  'VzfcFuHCbg72mlkRRTYL'
url_class = 'https://webvpn.jsu.edu.cn/https/77726476706e69737468656265737421f4f64f9b2d39695e30029ab9d650272032ba4b/web/pschool/party/center?pcid=271'


clear_screen()


# 发送通知
def send_notification(content):
    # 接口地址
    url = "https://push.i-i.me"
    push_params = {
        "push_key": push_key,
        "title": "智慧党建课程学习通知",
        "content": content,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": "text"
    }
    push_response = requests.post(url, data=push_params)
    # 检查推送请求是否成功
    if push_response.status_code == 200:
        print("推送成功")
    else:
        print("推送失败")


# 转化为秒
def time_to_seconds(time_video):
    time_next_str = time_video.split(" / ")[1]
    minutes, seconds = map(int, time_next_str.split(":"))

    return minutes * 60 + seconds

def login(tab, student_id, password):
    # 登录
    tab.get('https://i.jsu.edu.cn')
    if tab.title == '吉首大学公共信息服务平台':
        return
    tab.wait.doc_loaded()
    print("开始登录")
    tab.ele('t:input@@placeholder=学工号').input(student_id)
    tab.ele('t:input@@placeholder=密码').input(password)
    time.sleep(3)
    tab.ele('t:button@@class=el-button el-button--primary@@tx():立即登录').click()
    tab.wait.doc_loaded()
    print("登录成功")
    time.sleep(10)
    tab.refresh()
    time.sleep(20)

if __name__ == '__main__':
    co = ChromiumOptions()
    co.mute()
    co.incognito()
    co.set_user_agent(
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.101 Safari/537.36')
    browser = Chromium(co)
    while True:
        try:
            tab_qiangzhi_system = browser.latest_tab
            login(tab_qiangzhi_system,student_id,password)
            tab_qiangzhi_system.ele('t:a@@class=item-list-link@@tx():智慧党建').click()
            tab_qiangzhi_system.wait.doc_loaded()
            time.sleep(10)
            print("智慧党建登录成功")
            tab_smart_party =browser.latest_tab
            tab_smart_party.get(url_class)
            all_class= tab_smart_party.eles('@@class=list-wrapper')[1].eles('t:div@@class=list-box')
            for each_class in all_class:
                if '进度' in each_class.text:
                    print(each_class.text)
                    each_class.click(by_js=True)
                    time.sleep(15)
                    print("智慧党建课程页面加载成功")
                    if tab_smart_party.ele('t:div@@class=status-box@@tx():未开始'):
                        status_box_nostart = tab_smart_party.ele('t:div@@class=status-box@@tx():未开始')
                        time_video = tab_smart_party.ele('t:div@@class=time-box').text
                        status_box_nostart.click()
                        time.sleep(15)
                        time_next = time_to_seconds(time_video)
                        if push_key:
                            send_notification(f"下一个视频将于{time_next}秒后开始")
                        print(f"下一个视频将于{time_next}秒后开始")
                        time.sleep(time_next + 60)  # 等待下一个视频开始
                        print("视频播放完成准备退出")
                        break

                    elif tab_smart_party.ele('t:div@@class=status-box start@@tx():进行中'):
                        status_box_start = tab_smart_party.ele('t:div@@class=status-box start@@tx():进行中')
                        time_video = tab_smart_party.ele('t:div@@class=time-box').text
                        status_box_start.click()
                        time.sleep(15)
                        time_next = time_to_seconds(time_video)
                        if push_key:
                            send_notification(f"下一个视频将于{time_next}秒后开始")
                        print(f"下一个视频将于{time_next}秒后开始")
                        time.sleep(time_next + 60)
                        print("视频播放完成准备退出")
                        break

                    else:
                        print("该板块已全部完成")
                        if push_key:
                            send_notification("智慧党建任务已完成")
                        break
                else:
                    continue
        except Exception as e:
            pass
        finally:
            time.sleep(5)
            tab = browser.latest_tab
            tab.close()
            clear_screen()

    browser.quit()


