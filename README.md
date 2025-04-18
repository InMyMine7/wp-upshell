# WordPress Automation Upload Shell

This Python script automates the process of logging into WordPress sites, uploading plugins or themes, and injecting code via the plugin editor. It is designed for bulk operations on multiple sites using a list of URLs and credentials.

**Note**: This script is intended for educational purposes and authorized security testing only. Unauthorized use on systems you do not own or have explicit permission to test is illegal and unethical. Ensure compliance with all applicable laws and regulations.

## Features

- **Multi-threaded Processing**: Processes multiple sites concurrently using Python's `ThreadPoolExecutor`.
- **Login Automation**: Attempts to log into WordPress admin panels using provided credentials.
- **File Upload**: Uploads plugin (`plugin-inmymine.zip`) or theme (`theme-inmymine.zip`) files to WordPress sites.
- **Plugin Editor Injection**: Injects custom code into existing plugins via the WordPress plugin editor.
- **Shell Verification**: Verifies uploaded or injected files by checking for specific markers in the response.
- **Error Handling**: Logs failed attempts to `failed.txt` and successful uploads to `plugin.txt` or `theme.txt`.

## Prerequisites

- Python 3.6+
- Required Python libraries:
  - `requests`
  - `beautifulsoup4`
  - `urllib3`
- Install dependencies using:

  ```bash
  pip install requests beautifulsoup4
  ```

## Installation

1. Clone or download this repository:

   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```
2. Install the required Python libraries:

   ```bash
   pip install -r requirements.txt
   ```
3. Ensure the following files are in the same directory as the script:
   - `plugin-inmymine.zip` (plugin file to upload)
   - `theme-inmymine.zip` (theme file to upload)
   - A text file containing the list of sites and credentials (e.g., `list.txt`).

## Usage

1. Prepare a text file (e.g., `list.txt`) with the following format for each line:

   ```
   http://example.com/wp-login.php#username@password
   ```

   Example:

   ```
   http://site1.com/wp-login.php#admin@pass123
   http://site2.com/wp-login.php#user@pass456
   ```

2. Run the script:

   ```bash
   python script.py
   ```

3. Follow the prompts:

   - Enter the name of the input file (e.g., `list.txt`).
   - Specify the number of threads for concurrent processing.

4. The script will:

   - Attempt to log into each site.
   - Upload the plugin or theme if the respective `.zip` files exist.
   - Attempt to inject code via the plugin editor.
   - Save successful plugin/theme uploads to `plugin.txt` or `theme.txt`.
   - Save failed attempts to `failed.txt`.

## Output Files

- `plugin.txt`: URLs of successfully uploaded and verified plugins.
- `theme.txt`: URLs of successfully uploaded and verified themes.
- `failed.txt`: URLs and reasons for failed attempts (e.g., login failure or upload failure).

## Example

```bash
$ python script.py
Masukkan nama file list URL (contoh: list.txt): list.txt
Masukkan jumlah thread: 10

🚀 Mulai upload ke 50 site dengan 10 thread...

[SUCCESS] Plugin berhasil di-upload dan aktif di http://example.com/wp-content/plugins/random123/install.php
[FAILED] Login gagal ke http://site2.com/wp-login.php
...

✅ Selesai dalam 45.23 detik.
📄 Hasil disimpan ke plugin.txt, theme.txt, dan failed.txt
```

## Notes

- The script uses a random 8-character filename for uploaded `.zip` files to avoid conflicts.
- It includes a user-agent mimicking an iPhone browser for requests.
- The shell verification checks for specific strings (`InMyMine7`, `Priv8 Uploader`, etc.) to confirm successful uploads.
- Ensure the `plugin-inmymine.zip` and `theme-inmymine.zip` files are valid WordPress plugin/theme packages.
- The plugin editor injection adds a PHP uploader code snippet, which is only for authorized testing purposes.

## Disclaimer

This script is provided for educational and research purposes only. The author is not responsible for any misuse or damage caused by this script. Use it only on systems you have explicit permission to test.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.