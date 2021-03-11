"""
touch命令-创建一个或者多个空文件
stat命令-查看文件的属性状态信息
chmod命令-修改权限，chomd 777 test.txt
"""
# 导入包
import os
import sys
from flask import Flask, url_for, render_template, flash, redirect
# escape转义字符函数库
from flask import escape
# 导入数据库工具类SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
# 导入请求包
from flask import request

#
# app = Flask(__name__)
# db = SQLAlchemy(app)  # 初始化扩展，传入程序实例 app
# 判断当前平台是否为window系统
WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

app = Flask(__name__)
# 设置数据库 URI
# Flask提供了一个统一的接口来写入和获取这些配置变量：Flask.config 字典。配置变量的名称必须使用大写，写入配置的语句一般会放到扩展类实例化语句之前。
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)


# @app.route('/')
# def hello():
#     # 函数返回值作为响应的主体，默认会被浏览器作为 HTML 格式解析，
#     return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'

# app.route装饰器里的URL规则字符串可自定义，但要注意以斜线/作为开头。
# 一个视图函数也可以绑定多个 URL，这通过附加多个装饰器实现
# @app.route('/')
@app.route('/index')
@app.route('/hello')
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


# name = 'Grey Li'
# movies = [
#     {'title': 'My Neighbor Totoro', 'year': '1988'},
#     {'title': 'Dead Poets Society', 'year': '1989'},
#     {'title': 'A Perfect World', 'year': '1993'},
#     {'title': 'Leon', 'year': '1994'},
#     {'title': 'Mahjong', 'year': '1996'},
#     {'title': 'Swallowtail Butterfly', 'year': '1996'},
#     {'title': 'King of Comedy', 'year': '1999'},
#     {'title': 'Devils on the Doorstep', 'year': '1999'},
#     {'title': 'WALL-E', 'year': '2008'},
#     {'title': 'The Pork of Music', 'year': '2012'},
# ]


# 使用render_template() 函数渲染模板
# 第一个参数必须是传入的参数为模板文件名（相对于 templates 根目录的文件路径），这里即'index.html'。
# 其它参数通过关键字参数传入函数，支持多种类型，列表、元组、字典、函数等。
@app.route('/', methods=['POST', 'GET'])
def index():
    # user = User.query.first()  # 读取用户记录
    # movies = Movie.query.all()  # 读取所有电影记录
    # return render_template('index01.html', name=user.name, movies=movies)
    # request对象包含了请求的信息，比如请求的路径（request.path）、请求的方法（request.method）、表单数据（request.form）、查询字符串（request.args）等等。
    if request.method == 'POST':
        # 获取表单数据
        title = request.form.get('title')  # 传入表单对应输入字段的 name 值
        year = request.form.get('year')
        # 验证数据
        if not title or not year or len(year) > 4 or len(title) > 60:
            # flash()函数用来在视图函数里向模板传递提示消息，
            flash('Invalid input.')  # 显示错误提示
            # Flask 提供了redirect() 函数来快捷生成这种响应，传入重定向的目标 URL 作为参数
            return redirect(url_for('index'))  # 重定向回主页
        # 保存表单数据到数据库
        movie = Movie(title=title, year=year)  # 创建记录
        db.session.add(movie)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        flash('Item created.')  # 显示成功创建的提示
        return redirect(url_for('index'))  # 重定向回主页

    movies = Movie.query.all()
    return render_template('index.html', movies=movies)


# movie_id请求参数
@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    # get_or_404() 方法，它会返回对应主键的记录，如果没有找到，则返回 404 错误响应。
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':  # 处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))  # 重定向回对应的编辑页面

        movie.title = title  # 更新标题
        movie.year = year  # 更新年份
        db.session.commit()  # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('index'))  # 重定向回主页
    return render_template('edit.html', movie=movie)  # 传入被编辑的电影记录


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受 POST 请求
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index'))  # 重定向回主页


@app.route('/home')
def home():
    return render_template('child_page.html', )


# methods关键字指定请求方式，默认Get
@app.route('/addInfo', methods=['POST', 'GET'])
def addInfo():
    # 导入request类
    from flask import request
    if request.method == 'POST':
        # 获取请求中的表单数据
        name = request.form.get('name')
        occupation = request.form.get('occupation')
        print("姓名：%s-职业：%s" % (name, occupation))
        print("姓名：{0}-职业：{1}".format(name, occupation))
    return render_template('add_info_page.html')


@app.route('/login')
def login():
    return render_template('login.html', )


# 定义模板上下文处理函数，
@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)


# 自定义错误页面，注册错误处理函数
# @app.errorhandler(404)  # 传入要处理的错误代码
# def page_not_found(e):  # 接受异常对象作为参数
#     user = User.query.first()
#     return render_template('404_old.html', user=user), 404  # 返回模板和状态码


@app.errorhandler(400)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    # 通过定义模板上下文处理函数，可以直接在模板上使用注入的变量。
    return render_template('400.html', ), 400  # 返回模板和状态码


@app.errorhandler(500)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    return render_template('500.html', ), 500  # 返回模板和状态码


"""
通过定义模型类，创建数据库模型
注意：
（1）模型类要声明继承 db.Model。
（2）每一个类属性（字段）要实例化 db.Column，传入的参数为字段的类型：
    db.Integer整型
    db.String (size)字符串，size 为最大长度，比如 db.String(20)
    db.Text长文本
    db.DateTime时间日期，Python datetime 对象
    db.Float浮点数
    db.Boolean布尔值
（3）常用的选项还有 nullable（布尔值，是否允许为空值）、index（布尔值，是否设置索引）、unique（布尔值，是否允许重复值）、default（设置默认值）等。
"""


class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20), nullable=False, unique=False)  # 名字


class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60), nullable=False)  # 电影标题
    year = db.Column(db.String(4))  # 电影年份


import click


# 注册为命令
@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息


@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()
    # 全局的两个变量移动到这个函数内
    name = 'Grey Li'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('Done.')
