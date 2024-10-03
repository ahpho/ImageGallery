# ImageGallery

## 提示词Prompt
帮我写一个网页，可以展示 N * M 个图片（注意图片可能是GIF格式），
图片来源是：从我本地磁盘的某个目录动态枚举特定后缀名的图片文件得到。
如果图片文件很多，那么需要展示的图片也很多，这个网页需要支持滚轮。


## 如何运行
### 确保你安装了Python以及Flask
pip install Flask

### 修改Python脚本中的IMAGE_DIRECTORY为你本地存储图片的目录。

### 运行Python脚本：
python app.py<br>
打开浏览器访问 http://127.0.0.1:5000/ ，即可看到本地目录中的图片。

