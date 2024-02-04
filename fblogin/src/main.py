import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import pytz

MAX_ACCOUNTS_PER_URL = 5

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
        WebDriverWait(driver, 10).until(EC.url_to_be("https://www.facebook.com/"))
    except Exception as e:
        print(f"[Lỗi đăng nhập] {e}")
        raise e

def visit_second_url(driver, second_url, xpath_to_click, users_data):
    driver.get(second_url)

    try:
        num_accounts_logged_in = count_accounts_logged_in(second_url)

        if num_accounts_logged_in >= MAX_ACCOUNTS_PER_URL:
            raise Exception(f"Số lượng tài khoản đã đăng nhập vào URL {second_url} vượt quá tài nguyên")
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath_to_click))
        )
        element.click()

        save_to_check_json(second_url, users_data)
    except Exception as e:
        print(f"[Lỗi] {e}")

def count_accounts_logged_in(url):
    try:
        with open(r"z:\code\fblogin\fblogin\src\core\check.json", "r") as check_file:
            check_json = json.load(check_file)
    except FileNotFoundError:
        check_json = []

    for item in check_json:
        if item["url"] == url:
            return len(item["accounts"])

    return 0

def save_to_check_json(url, users_data):
    try:
        with open(r"z:\code\fblogin\fblogin\src\core\check.json", "r") as check_file:
            check_json = json.load(check_file)
    except FileNotFoundError:
        check_json = []

    url_exists, index = check_url_exists(url, check_json)

    if url_exists:
        for account in users_data:
            if account not in check_json[index]["accounts"]:
                check_json[index]["accounts"].append(account)
                break
    else:
        check_data = {
            "url": url,
            "accounts": users_data,
            "time": datetime.now(pytz.timezone("Asia/Ho_Chi_Minh")).strftime("%H:%M - %d/%m/%Y"),
        }
        check_json.append(check_data)

    with open(r"z:\code\fblogin\fblogin\src\core\check.json", "w") as check_file:
        json.dump(check_json, check_file, indent=2)
        print("Dữ liệu đã được lưu vào check.json")

def check_url_exists(url, check_json):
    url_exists = False
    index = -1
    for i, item in enumerate(check_json):
        if item["url"] == url:
            url_exists = True
            index = i
            break
    return url_exists, index

def count_unused_accounts(users, check_json, second_url):
    unused_accounts = []
    for user in users:
        found = False
        for item in check_json:
            if user["user"] == item["accounts"][0]["user"] and item["url"] == second_url:
                found = True
                break
        if not found:
            unused_accounts.append(user)
    return unused_accounts, len(unused_accounts)

def process_existing_url(check_json, second_url):
    for i, item in enumerate(check_json):
        if item["url"] == second_url and len(item["accounts"]) >= MAX_ACCOUNTS_PER_URL:
            print(f"URL {second_url} đã đầy tài khoản.")
            choice = input("Chọn 'y' để xóa dữ liệu, 'n' để giữ nguyên: ")
            if choice.lower() == 'y':
                del check_json[i]
            break

def main():
    users = load_users("z:/code/fblogin/fblogin/src/core/users.json")

    num_accounts = int(input("Nhập số lượng tài khoản cần chạy: "))

    second_url = "https://www.facebook.com/photo/?fbid=384064007471196&set=a.101231119087821"
    xpath_to_click = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div[1]/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/div[2]"

    with open(r"z:\code\fblogin\fblogin\src\core\check.json", "r") as check_file:
        check_json = json.load(check_file)

    unused_accounts, num_unused_accounts = count_unused_accounts(users, check_json, second_url)
    print(f"Số lượng tài khoản chưa sử dụng: {num_unused_accounts}")

    process_existing_url(check_json, second_url)
    for user in unused_accounts[:num_accounts]:
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        driver = webdriver.Chrome(options=chrome_options)

        try:
            login(driver, user["user"], user["pass"])
            visit_second_url(driver, second_url, xpath_to_click, [{"user": user["user"], "pass": user["pass"]}])
            driver.quit()
        except Exception as e:
            print(f"[Lỗi] {e}")

if __name__ == "__main__":
    main()
