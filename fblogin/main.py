import json
import time
from datetime import datetime
from termcolor import colored
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def load_users(users_file):
    with open(users_file, "r") as f:
        return json.load(f)

def login(driver, username, password):
    driver.get("https://www.facebook.com")
    try:
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        password_field = driver.find_element(By.NAME, "pass")

        username_field.send_keys(username)
        password_field.send_keys(password)

        login_button = driver.find_element(By.NAME, "login")
        login_button.click()
        time.sleep(5)

        global status
        status = driver.current_url == "https://www.facebook.com/"

    except Exception as e:
        print(e)
        print(colored(f"[Lỗi đăng nhập] {e}", "red", attrs=["bold"]))
        raise e

def display_message(message, color="yellow"):
    frame_top = "=" * 120
    frame_middle = f"| {message.center(118)} |"
    frame_bottom = "=" * 120
    framed_message = f"\n{frame_top}\n{frame_middle}\n{frame_bottom}"
    print(colored(framed_message, color, attrs=["bold"]))

def visit_profile(driver, url, users_data):
    driver.get(url)

    # Save data to check.json
    check_data = {
        "url": url,
        "accounts": users_data,
    }

    try:
        with open("../core/check.json", "r") as check_file:
            check_json = json.load(check_file)
    except FileNotFoundError:
        check_json = []

    # Check if the URL already exists in check.json
    url_exists = False
    index = -1
    for i, item in enumerate(check_json):
        if item["url"] == url:
            url_exists = True
            index = i
            break

    if url_exists:
        if all(account in item["accounts"] for account in users_data):
            display_message("Tất cả tài khoản đã truy cập vào URL, chuyển sang tài khoản khác", "yellow")
            return

        if any(account in item["accounts"] for account in users_data):
            for account in users_data:
                if account not in item["accounts"]:
                    display_message(f"Chuyển sang tài khoản {account['user']}", "green")
                    login(driver, account["user"], account["pass"])
                    display_message(f"Tài khoản {account['user']} đã truy cập vào URL", "yellow")
                    break

    check_json.append(check_data)
    with open("z:/code/fblogin/fblogin/src/core/check.json", "w") as check_file:
        json.dump(check_json, check_file, indent=2)
        display_message("Dữ liệu đã được lưu vào check.json", "green")

    if status:
        url_message = f"[{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]: {driver.current_url}"
        display_message(url_message, "blue")

def remove_data_from_check():
    try:
        with open("../core/check.json", "r") as check_file:
            check_json = json.load(check_file)
    except FileNotFoundError:
        check_json = []

    current_url = "https://www.facebook.com/photo?fbid=122100683054022532&set=pb.61550675973666.-2207520000"

    check_json = [item for item in check_json if item["url"] != current_url]

    with open("../core/check.json", "w") as check_file:
        json.dump(check_json, check_file, indent=2)
        display_message(f"Dữ liệu của URL {current_url} đã được xóa", "yellow")

def main():
    start_time = time.time()
    users = load_users("../core/users.json")
    success = 0
    error = 0
    for user in users:
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        driver = webdriver.Chrome(options=chrome_options)
        try:
            login(driver, user["user"], user["pass"])

            users_data = [{"user": user["user"], "pass": user["pass"]} for user in users]
            
            visit_profile(
                driver,
                "https://www.facebook.com/photo?fbid=122100683054022532&set=pb.61550675973666.-2207520000",
                #tôi muốn thên phần nhấn vào xpath của web này nếu tìm thấy đưỡ phần tử
                #sắp sếp lại code để dễ hiểu hơn
                # dùng hàm try expect
                users_data,
            )
            driver.quit()
            if status:
                success += 1
            else:
                error += 1
        except Exception as e:
            display_message(f"[Lỗi] {e}", "red")

    end_time = time.time()
    execution_time = end_time - start_time

    summary_message = f"[Tổng kết] Đăng nhập thành công: {success} | Lỗi đăng nhập: {error}"
    display_message(summary_message, "blue")
    time_message = f"Thời gian thực thi: {execution_time:.2f} giây"
    display_message(time_message, "yellow")

    restart = prompt_for_restart()
    if restart:
        main()

if __name__ == "__main__":
    main()
