from flask import Flask, render_template, send_from_directory, jsonify, request
import os
import subprocess
import sys

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
            if file.endswith(('.png', '.jpg', '.jpeg', '.gif')):#其实可以只是.gif
                relative_path = os.path.relpath(os.path.join(root, file), IMAGE_DIRECTORY)
                filename = os.path.basename(relative_path)
                # 如果文件是 .gif 结尾，去掉 .gif 扩展名
                if filename.endswith('.gif'):
                    filename = os.path.splitext(filename)[0]
                images.append({
                    'path': relative_path,
                    'filename': filename
                })

    # 确保顺序稳定
    # images.sort(key=lambda x: x['path']) # 按目录
    # images.sort(key=lambda x: x['filename']) # 按文件名
    # images.sort(key=lambda x: os.path.getsize(os.path.join(IMAGE_DIRECTORY, x['path']))) # 按文件大小
    # images.sort(key=lambda x: os.path.getmtime(os.path.join(IMAGE_DIRECTORY, x['path']))) # 按修改时间
    images.sort( # 按文件修改时间降序排序（新到旧）
        key=lambda x: os.path.getmtime(os.path.join(IMAGE_DIRECTORY, x['path'])),
        reverse=True
    )

    # 获取请求参数 page 和 limit，控制分页
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', IMAGES_PER_PAGE))
    start = (page - 1) * limit
    end = start + limit

    # 分页后的图片子集
    paginated_images = images[start:end]

    # 返回分页后的图片以及图片总数
    return jsonify({
        'images': paginated_images,
        'total': len(images)
    })

# 提供图片文件给前端
@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMAGE_DIRECTORY, filename)

# 新增: 使用 explorer.exe 打开图片所在目录并选中图片
@app.route('/open-image-dir', methods=['POST'])
def open_image_dir():
    data = request.json
    image_path = data.get('path')
    
    if image_path:
        # 构建图片的绝对路径
        full_image_path = os.path.join(IMAGE_DIRECTORY, image_path)
        full_image_path = os.path.abspath(full_image_path)
        
        if sys.platform == "win32":  # Windows 系统
            # 我们不打开gif所在的folder_path, 而是打开同名.path文件指向的目录
            folder_path = os.path.dirname(full_image_path)
            path_file = full_image_path + '.path'
            with open(path_file, 'r') as f:
                full_image_path = f.read().strip()

            # 使用 explorer.exe 打开目录并选中文件
            subprocess.run(f'explorer /select,"{full_image_path}"')
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "failed", "message": "Not supported on this platform"}), 400
    
    return jsonify({"status": "failed", "message": "Invalid image path"}), 400

if __name__ == "__main__":
    app.run(debug=True)
