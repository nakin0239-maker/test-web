from flask import Flask, request, send_from_directory
import html

app = Flask(__name__, static_folder='.')

# กล่องเก็บข้อความทั้งหมด
posts = []

@app.route('/', methods=['GET', 'POST'])
def home():
    step = request.form.get('step', '1')

    # สเต็ปที่ 2: พิมพ์ข้อความที่อยากบอก
    if step == '2':
        nickname = request.form.get('nickname', '').strip()
        grade = request.form.get('grade', '').strip()
        return f"""
        <!DOCTYPE html>
        <html lang="th">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>อยากบอกอะไร</title>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                    margin: 0; min-height: 100vh;
                    display: flex; justify-content: center; align-items: center;
                    background-color: #f0f2f5; padding: 16px; box-sizing: border-box;
                }}
                .card {{
                    background: white; padding: 24px; border-radius: 16px;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.08); max-width: 380px; width: 100%;
                    text-align: center;
                }}
                img {{ width: 80px; margin-bottom: 12px; }}
                h2 {{ margin: 0 0 8px 0; color: #1a73e8; font-size: 20px; }}
                .tag {{
                    display: inline-block; background: #e8f0fe; color: #1a73e8;
                    padding: 4px 12px; border-radius: 20px; font-size: 14px;
                    font-weight: bold; margin-bottom: 18px;
                }}
                textarea {{
                    width: 100%; height: 110px; padding: 12px; border: 1.5px solid #dcdfe6;
                    border-radius: 10px; font-size: 15px; box-sizing: border-box;
                    resize: none; font-family: inherit; margin-bottom: 16px;
                }}
                textarea:focus {{ border-color: #1a73e8; outline: none; }}
                button {{
                    width: 100%; padding: 13px; background: #1a73e8; color: white;
                    border: none; border-radius: 10px; font-size: 16px;
                    font-weight: bold; cursor: pointer;
                }}
            </style>
        </head>
        <body>
            <div class="card">
                <img src="/mh_logo.png" alt="โลโก้">
                <h2>ยินดีต้อนรับ!</h2>
                <div class="tag">👤 {html.escape(nickname)} • {html.escape(grade)}</div>
                
                <form method="POST">
                    <input type="hidden" name="step" value="3">
                    <input type="hidden" name="nickname" value="{html.escape(nickname)}">
                    <input type="hidden" name="grade" value="{html.escape(grade)}">
                    
                    <textarea name="message" placeholder="พิมพ์ข้อความที่อยากบอกลงที่นี่..." required></textarea>
                    <button type="submit">🚀 ส่งข้อความ</button>
                </form>
            </div>
        </body>
        </html>
        """

    # สเต็ปที่ 3: บันทึกและแสดงผลกระดานข้อความ
    if step == '3':
        nickname = request.form.get('nickname', '').strip()
        grade = request.form.get('grade', '').strip()
        message = request.form.get('message', '').strip()

        if message:
            # เพิ่มข้อความใหม่ไว้บนสุด
            posts.insert(0, {
                'nickname': html.escape(nickname),
                'grade': html.escape(grade),
                'message': html.escape(message)
            })

        # สร้างกล่องข้อความแสดงผล
        posts_html = ""
        for p in posts:
            posts_html += f"""
            <div class="post-item">
                <div class="post-header">
                    <span class="post-user">👤 {p['nickname']}</span>
                    <span class="post-grade">{p['grade']}</span>
                </div>
                <div class="post-text">{p['message']}</div>
            </div>
            """

        return f"""
        <!DOCTYPE html>
        <html lang="th">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>กระดานบอกต่อ</title>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                    margin: 0; min-height: 100vh; background-color: #f0f2f5;
                    padding: 16px; box-sizing: border-box; display: flex;
                    justify-content: center;
                }}
                .container {{ max-width: 400px; width: 100%; }}
                .top-bar {{
                    background: white; padding: 18px; border-radius: 14px;
                    text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05);
                    margin-bottom: 16px;
                }}
                .top-bar img {{ width: 60px; }}
                .top-bar h2 {{ margin: 8px 0; font-size: 18px; color: #1a73e8; }}
                .btn-new {{
                    display: inline-block; padding: 10px 18px; background: #1a73e8;
                    color: white; text-decoration: none; border-radius: 8px;
                    font-size: 14px; font-weight: bold; margin-top: 6px;
                }}
                .post-item {{
                    background: white; padding: 16px; border-radius: 12px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 12px;
                }}
                .post-header {{
                    display: flex; justify-content: space-between; align-items: center;
                    border-bottom: 1px solid #f0f0f0; padding-bottom: 8px; margin-bottom: 10px;
                }}
                .post-user {{ font-weight: bold; color: #202124; }}
                .post-grade {{
                    background: #e8f0fe; color: #1a73e8; font-size: 12px;
                    padding: 3px 8px; border-radius: 12px; font-weight: bold;
                }}
                .post-text {{ font-size: 15px; color: #3c4043; line-height: 1.5; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="top-bar">
                    <img src="/mh_logo.png" alt="โลโก้">
                    <h2>🎉 โพสต์สำเร็จแล้ว!</h2>
                    <a href="/" class="btn-new">✍️ เขียนข้อความใหม่</a>
                </div>
                {posts_html}
            </div>
        </body>
        </html>
        """

    # สเต็ปที่ 1: หน้าแรกสุด กรอก ม. อะไร กับ ชื่อเล่น
    return """
    <!DOCTYPE html>
    <html lang="th">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>บอกต่อ</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                margin: 0; min-height: 100vh; display: flex; justify-content: center;
                align-items: center; background-color: #f0f2f5; padding: 16px; box-sizing: border-box;
            }
            .card {
                background: white; padding: 26px 20px; border-radius: 16px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.08); max-width: 360px; width: 100%;
                text-align: center;
            }
            img { width: 90px; margin-bottom: 12px; }
            h2 { margin: 0 0 20px 0; color: #202124; font-size: 20px; }
            label {
                display: block; text-align: left; font-size: 14px;
                font-weight: bold; color: #444; margin-bottom: 6px;
            }
            input {
                width: 100%; padding: 12px; margin-bottom: 16px;
                border: 1.5px solid #dcdfe6; border-radius: 10px;
                box-sizing: border-box; font-size: 15px;
            }
            input:focus { border-color: #1a73e8; outline: none; }
            button {
                width: 100%; padding: 13px; background: #1a73e8; color: white;
                border: none; border-radius: 10px; font-size: 16px;
                font-weight: bold; cursor: pointer; margin-top: 4px;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <img src="/mh_logo.png" alt="โลโก้">
            <h2>ยินดีต้อนรับ</h2>
            <form method="POST">
                <input type="hidden" name="step" value="2">
                
                <label>อยู่ ม. อะไร?</label>
                <input type="text" name="grade" placeholder="เช่น ม.3, ม.5/1" required>
                
                <label>ชื่อเล่นของคุณ</label>
                <input type="text" name="nickname" placeholder="เช่น บอส, มิ้นต์" required>
                
                <button type="submit">ถัดไป ➔</button>
            </form>
        </div>
    </body>
    </html>
    """

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
