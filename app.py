from flask import Flask, render_template, send_from_directory, jsonify, request
import os

app = Flask(__name__)

# 定义图片所在的本地目录
IMAGE_DIRECTORY = "C:/path/to/your/images"

# 每页的默认图片数量
IMAGES_PER_PAGE = 20

# 返回网页主页面
@app.route('/')
def index():
    return render_template('index.html')

# 递归枚举指定目录及其子目录下的图片文件并支持分页
@app.route('/images')
def get_images():
    images = []
    for root, dirs, files in os.walk(IMAGE_DIRECTORY):
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                # 构建相对路径（保留目录结构）
                relative_path = os.path.relpath(os.path.join(root, file), IMAGE_DIRECTORY)
                images.append(relative_path)
    
    # 获取请求参数 page 和 limit，控制分页
    page = int(request.args.get('page', 1))  # 默认第1页
    limit = int(request.args.get('limit', IMAGES_PER_PAGE))  # 默认每页数量
    start = (page - 1) * limit
    end = start + limit
    
    # 分页后的图片子集
    paginated_images = images[start:end]
    
    # 返回分页后的图片以及图片总数，以便前端知道有多少页
    return jsonify({
        'images': paginated_images,
        'total': len(images)
    })

# 提供图片文件给前端
@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMAGE_DIRECTORY, filename)

if __name__ == "__main__":
    app.run(debug=True)
