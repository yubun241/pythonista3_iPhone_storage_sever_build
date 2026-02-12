from flask import Flask, render_template_string, request, send_from_directory, redirect
import os
import socket

app = Flask(__name__)

# 保存先ディレクトリ（Pythonista内のDocuments）
UPLOAD_FOLDER = os.path.expanduser('~/Documents')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# HTMLテンプレート（アップロードとダウンロードのインターフェース）
HTML_TEMPLATE = """
<!doctype html>
<html>
<head><title>Pythonista Storage</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
    <h1>iPhone Storage Server</h1>
    <h2>Upload New File</h2>
    <form method="post" enctype="multipart/form-data" action="/upload">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    <h2>Files</h2>
    <ul>
    {% for filename in files %}
      <li>
        <a href="/download/{{ filename }}">{{ filename }}</a>
      </li>
    {% endfor %}
    </ul>
</body>
</html>
"""

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template_string(HTML_TEMPLATE, files=files)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return redirect('/')

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

if __name__ == '__main__':
    ip_addr = get_ip()
    port = 8080
    print("="*30)
    print(f"サーバーを起動しました")
    print(f"会社PCのブラウザで以下を入力してください:")
    print(f"http://{ip_addr}:{port}")
    print("="*30)
    app.run(host='0.0.0.0', port=port, debug=False)
