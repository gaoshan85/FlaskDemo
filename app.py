"""
touch命令-创建一个或者多个空文件
stat命令-查看文件的属性状态信息
chmod命令-修改权限，chomd 777 test.txt
"""
# 导入包
from flask import Flask, url_for
# escape转义字符函数库
from flask import escape

#
app = Flask(__name__)


# @app.route('/')
# def hello():
#     # 函数返回值作为响应的主体，默认会被浏览器作为 HTML 格式解析，
#     return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'

# app.route装饰器里的URL规则字符串可自定义，但要注意以斜线/作为开头。
# 一个视图函数也可以绑定多个 URL，这通过附加多个装饰器实现
@app.route('/')
@app.route('/index')
@app.route('/home')
def hello():
    return 'Welcome to My Watchlist!'


# URL规则字符串可带参数，比如视图函数会处理所有类似 /user/<name> 的请求
# 用户输入的数据会包含恶意代码，所以不能直接作为响应返回，需要使用Flask提供的escape()函数对name变量进行转义处理，比如把 < 转换成 &lt;。
@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % escape(name)


# 视图函数的名称可自由定义，和 URL规则无关。
# 视图函数的名称作为代表某个路由的端点（endpoint），同时用来生成 URL。
@app.route('/test')
def test_url_for():
    # 下面是一些调用示例（请在命令行窗口查看输出的 URL）：
    print(url_for('hello'))  # 输出：/
    # 注意下面两个调用是如何生成包含 URL 变量的 URL 的
    print(url_for('user_page', name='greyli'))  # 输出：/user/greyli
    print(url_for('user_page', name='peter'))  # 输出：/user/peter
    print(url_for('test_url_for'))  # 输出：/test
    # 下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到 URL 后面。
    print(url_for('test_url_for', num=2))  # 输出：/test?num=2
    return 'Test page'
