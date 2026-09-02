from flask import Flask, request, send_from_directory, redirect
import html
import os

app = Flask(__name__)

# กล่องเก็บข้อความทั้งหมด
posts = []

@app.route('/', methods=['GET', 'POST'])
def home():
    # ----------------------------------------
    # โหมดที่ 1: โหลดหน้าเว็บ (GET)
    # ----------------------------------------
    if request.method == 'GET':
        action = request.args.get('action')
        
        # ถ้ากดปุ่ม "ดูกระดาน" หรือ "รีเฟรช" ให้แสดงหน้านี้
        if action == 'board':
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
            if not posts_html:
                posts_html = "<p style='text-align:center; color:#555; margin-top:20px;'>ยังไม่มีข้อความ เริ่มพิมพ์คนแรกเลย!</p>"

            return f"""
            <!DOCTYPE html>
            <html lang="th">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>กระดานบอกต่อ</title>
                <style>
                    body {{ font-family: -apple-system, sans-serif; margin: 0; min-height: 100vh; background-color: #f0f2f5; padding: 16px; box-sizing: border-box; display: flex; justify-content: center; }}
                    .container {{ max-width: 400px; width: 100%; }}
                    .top-bar {{ background: white; padding: 18px; border-radius: 14px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 16px; }}
                    .top-bar img {{ width: 60px; }}
                    .top-bar h2 {{ margin: 8px 0; font-size: 18px; color: #1a73e8; }}
                    .btn-group {{ display: flex; gap: 10px; justify-content: center; margin-top: 10px; }}
                    .btn {{ padding: 10px 18px; color: white; text-decoration: none; border-radius: 8px; font-size: 14px; font-weight: bold; flex: 1; }}
                    .btn-new {{ background: #1a73e8; }}
                    .btn-refresh {{ background: #34a853; }}
                    .post-item {{ background: white; padding: 16px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 12px; }}
                    .post-header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0; padding-bottom: 8px; margin-bottom: 10px; }}
                    .post-user {{ font-weight: bold; color: #202124; }}
                    .post-grade {{ background: #e8f0fe; color: #1a73e8; font-size: 12px; padding: 3px 8px; border-radius: 12px; font-weight: bold; }}
                    .post-text {{ font-size: 15px; color: #3c4043; line-height: 1.5; word-wrap: break-word; white-space: pre-wrap; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="top-bar">
                        <img src="/mh_logo.png" alt="โลโก้">
                        <h2>กระดานข้อความ</h2>
                        <div class="btn-group">
                            <a href="/" class="btn btn-new">✍️ เขียนใหม่</a>
                            <a href="/?action=board" class="btn btn-refresh">🔄 รีเฟรชหน้าเว็บ</a>
                        </div>
                    </div>
                    {posts_html}
                </div>
            </body>
            </html>
            """
        
        # หน้าแรกสุด: สเต็ป 1
        return """
        <!DOCTYPE html>
        <html lang="th">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>บอกต่อ</title>
            <style>
                body { font-family: -apple-system, sans-serif; margin: 0; min-height: 100vh; display: flex; justify-content: center; align-items: center; background-color: #f0f2f5; padding: 16px; box-sizing: border-box; }
                .card { background: white; padding: 26px 20px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); max-width: 360px; width: 100%; text-align: center; }
                img { width: 90px; margin-bottom: 12px; }
                h2 { margin: 0 0 20px 0; color: #202124; font-size: 20px; }
                label { display: block; text-align: left; font-size: 14px; font-weight: bold; color: #444; margin-bottom: 6px; }
                input, select { width: 100%; padding: 12px; margin-bottom: 16px; border: 1.5px solid #dcdfe6; border-radius: 10px; box-sizing: border-box; font-size: 15px; background: white; }
                input:focus, select:focus { border-color: #1a73e8; outline: none; }
                .row { display: flex; gap: 10px; }
                button { width: 100%; padding: 13px; background: #1a73e8; color: white; border: none; border-radius: 10px; font-size: 16px; font-weight: bold; cursor: pointer; margin-top: 4px; }
                .btn-view { display: inline-block; margin-top: 16px; color: #1a73e8; text-decoration: none; font-size: 14px; font-weight: bold; background: #e8f0fe; padding: 8px 16px; border-radius: 20px; }
            </style>
        </head>
        <body>
            <div class="card">
                <img src="/mh_logo.png" alt="โลโก้">
                <h2>ยินดีต้อนรับ</h2>
                <form method="POST">
                    <input type="hidden" name="step" value="2">
                    
                    <label>ระดับชั้น (บังคับเลือก)</label>
                    <div class="row">
                        <select name="m_level" required>
                            <option value="" disabled selected>เลือกชั้น</option>
                            <option value="ม.1">ม.1</option>
                            <option value="ม.2">ม.2</option>
                            <option value="ม.3">ม.3</option>
                            <option value="ม.4">ม.4</option>
                            <option value="ม.5">ม.5</option>
                            <option value="ม.6">ม.6</option>
                        </select>
                        <select name="room" required>
                            <option value="" disabled selected>เลือกห้อง</option>
                            <option value="1">ห้อง 1</option>
                            <option value="2">ห้อง 2</option>
                            <option value="3">ห้อง 3</option>
                            <option value="4">ห้อง 4</option>
                            <option value="5">ห้อง 5</option>
                            <option value="6">ห้อง 6</option>
                            <option value="7">ห้อง 7</option>
                            <option value="8">ห้อง 8</option>
                        </select>
                    </div>
                    
                    <label>ชื่อเล่นของคุณ</label>
                    <input type="text" name="nickname" placeholder="เช่น บอส, มิ้นต์ (ห้ามใส่ตัวเลข)" pattern="^[^0-9]+$" title="ห้ามพิมพ์ตัวเลขนะ!" required>
                    
                    <button type="submit">ถัดไป ➔</button>
                </form>
                <a href="/?action=board" class="btn-view">👀 ดูกระดานข้อความ</a>
            </div>
        </body>
        </html>
        """

    # ----------------------------------------
    # โหมดที่ 2: ระบบบันทึกข้อมูล (POST)
    # ----------------------------------------
    step = request.form.get('step')

    # สเต็ป 2: หน้าพิมพ์ข้อความ
    if step == '2':
        nickname = request.form.get('nickname', '').strip()
        m_level = request.form.get('m_level', '').strip()
        room = request.form.get('room', '').strip()
        grade = f"{m_level}/{room}" # จับคำมาเชื่อมกันเป็น ม.X/Y

        return f"""
        <!DOCTYPE html>
        <html lang="th">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>อยากบอกอะไร</title>
            <style>
                body {{ font-family: -apple-system, sans-serif; margin: 0; min-height: 100vh; display: flex; justify-content: center; align-items: center; background-color: #f0f2f5; padding: 16px; box-sizing: border-box; }}
                .card {{ background: white; padding: 24px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); max-width: 380px; width: 100%; text-align: center; }}
                img {{ width: 80px; margin-bottom: 12px; }}
                h2 {{ margin: 0 0 8px 0; color: #1a73e8; font-size: 20px; }}
                .tag {{ display: inline-block; background: #e8f0fe; color: #1a73e8; padding: 4px 12px; border-radius: 20px; font-size: 14px; font-weight: bold; margin-bottom: 18px; }}
                textarea {{ width: 100%; height: 110px; padding: 12px; border: 1.5px solid #dcdfe6; border-radius: 10px; font-size: 15px; box-sizing: border-box; resize: none; font-family: inherit; margin-bottom: 16px; }}
                textarea:focus {{ border-color: #1a73e8; outline: none; }}
                button {{ width: 100%; padding: 13px; background: #1a73e8; color: white; border: none; border-radius: 10px; font-size: 16px; font-weight: bold; cursor: pointer; }}
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

    # สเต็ป 3: รับข้อความแล้วเด้งกลับไปหน้ากระดาน
    if step == '3':
        nickname = request.form.get('nickname', '').strip()
        grade = request.form.get('grade', '').strip()
        message = request.form.get('message', '').strip()

        if message:
            posts.insert(0, {
                'nickname': html.escape(nickname),
                'grade': html.escape(grade),
                'message': html.escape(message)
            })

        # สั่งให้เด้งไปหน้า รีเฟรช (เพื่อกันคนกดย้อนหลังแล้วข้อความซ้ำ)
        return redirect('/?action=board')

@app.route('/<path:filename>')
def serve_static(filename):
    # แก้ไขให้ระบบถอยไปหาไฟล์รูปที่โฟลเดอร์หลัก (Root Directory)
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return send_from_directory(root_dir, filename)
