from flask import Flask, render_template, send_from_directory, jsonify
import os

app = Flask(__name__)

# 定义图片所在的本地目录
IMAGE_DIRECTORY = "C:/path/to/your/images"

# 返回网页主页面
@app.route('/')
def index():
    return render_template('index.html')

# 枚举指定目录下的图片文件（可以添加你想支持的后缀名）
@app.route('/images')
def get_images():
    images = []
    for file in os.listdir(IMAGE_DIRECTORY):
        if file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            images.append(file)
    return jsonify(images)

# 用于提供图片文件给前端
@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(IMAGE_DIRECTORY, filename)

if __name__ == "__main__":
    app.run(debug=True)
