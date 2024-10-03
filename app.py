from flask import Flask, render_template, send_from_directory, jsonify
import os

app = Flask(__name__)

# 定义图片所在的本地目录
IMAGE_DIRECTORY = "C:/path/to/your/images"

# 返回网页主页面
@app.route('/')
def index():
    return render_template('index.html')

# 递归枚举指定目录及其子目录下的图片文件
@app.route('/images')
def get_images():
    images = []
    for root, dirs, files in os.walk(IMAGE_DIRECTORY):
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                # 构建相对路径（保留目录结构）
                relative_path = os.path.relpath(os.path.join(root, file), IMAGE_DIRECTORY)
                images.append(relative_path)
    return jsonify(images)

# 提供图片文件给前端
@app.route('/images/<path:filename>')
def serve_image(filename):
    # 使用 send_from_directory 提供图片文件
    return send_from_directory(IMAGE_DIRECTORY, filename)

if __name__ == "__main__":
    app.run(debug=True)
