from flask import Flask, send_from_directory

app = Flask(__name__, static_folder='.')

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html lang="th">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>หน้าแรก</title>
        <style>
            body {
                margin: 0;
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                background-color: #f4f6f8;
            }
            img {
                max-width: 85%;
                max-height: 80vh;
                border-radius: 16px;
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
            }
        </style>
    </head>
    <body>
        <img src="/mh_logo.png" alt="โลโก้">
    </body>
    </html>
    """

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
  
  
