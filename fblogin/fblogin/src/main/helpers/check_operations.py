# helpers/check_operations.py
import json
from termcolor import colored

def save_check_data(check_json, current_url):
    try:
        with open("../core/check.json", "r") as check_file:
            check_json = json.load(check_file)
    except FileNotFoundError:
        check_json = []

    check_data = {
        "url": current_url,
        "accounts": users_data,
    }

    # Kiểm tra xem URL đã tồn tại trong check.json chưa
    url_exists = False
    index = -1
    for i, item in enumerate(check_json):
        if item["url"] == current_url:
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
    with open("../core/check.json", "w") as check_file:
        json.dump(check_json, check_file, indent=2)
        display_message("Dữ liệu đã được lưu vào check.json", "green")

    if status:
        url_message = f"[{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]: {driver.current_url}"
        display_message(url_message, "blue")

def remove_data_from_check(check_json, current_url):
    try:
        with open("../core/check.json", "r") as check_file:
            check_json = json.load(check_file)
    except FileNotFoundError:
        check_json = []

    check_json = [item for item in check_json if item["url"] != current_url]

    with open("../core/check.json", "w") as check_file:
        json.dump(check_json, check_file, indent=2)
        display_message(f"Dữ liệu của URL {current_url} đã được xóa", "yellow")
