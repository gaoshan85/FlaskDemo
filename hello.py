"""
编写一个简单的主页。主页的 URL 一般就是根地址，即 /。当用户访问根地址的时候，我们需要返回一行欢迎文字。
"""
# 导入包，创建一个程序对象 app
from flask import Flask

app = Flask(__name__)


# 我们要注册一个处理函数，这个函数是处理某个请求的处理函数，Flask官方把它叫做视图函数（view funciton），你可以理解为“请求处理函数”。
@app.route('/')  # "/"指根目录,对应的是主机名后面的路径部分，完整URL就是 http://localhost:5000/
def hello():
    return "Welcome to My Watchlist!'"


# app.route() 装饰器来为这个函数绑定对应的 URL，当用户在浏览器访问这个 URL 的时候，就会触发这个函数，获取返回值，并把返回值显示到浏览器窗口：
@app.route('/hello')  # /hello，那么完整 URL 就是 http://localhost:5000/hello。
def search():
    return "Hell, Welcome to My Watchlist!"
