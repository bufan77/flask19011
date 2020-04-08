from watchlistapp import app, db
from watchlistapp.models import User, Movie
from flask import url_for, render_template, flash, redirect, request
from flask_login import login_user, logout_user, login_required,current_user

#views
@app.route('/', methods=["GET", "POST"])
def index():
    
    #request在请求出发的时候才会包含数据
    if request.method == "POST":
        if not current_user.is_authenticated:
            return redirect(url_for('index'))
        title = request.form.get("title")
        year = request.form.get("year")
        #验证数据
        if not title or not year or len(year)>4 or len(title)>60:
            flash("不能为空或超过最大长度")
            return redirect(url_for("index"))
        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash("创建成功")
        return redirect(url_for("index"))

    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', user=user, movies=movies)


#更新电影信息
@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == "POST":
        title = request.form["title"]
        year = request.form["year"]
        if not title or not year or len(year)>4 or len(title)>60:
            flash("不能为空或超过最大长度")
            return redirect(url_for("index"))
        movie.title = title
        movie.year = year
        db.session.commit()
        flash("更新完成")
        return redirect(url_for("index"))
    return render_template("edit.html", movie=movie)


#删除电影信息
@app.route('/movie/delete/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash("删除成功")
    return redirect(url_for('index'))




#登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    #request在请求出发的时候才会包含数据
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        #验证数据
        if not username or not password:
            flash("输入错误")
            return redirect(url_for("login"))
        user = User.query.first()
        if user.username == username and user.validate_password(password):
            login_user(user)
            flash("创建成功")
            return redirect(url_for("index"))
        flash('用户名或密码错误')
        return redirect(url_for("login"))
    return render_template('login.html')

    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', user=user, movies=movies)

#登出
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('拜拜')
    return render_template('index.html')


#settings 设置
@app.route('/settings', methods=['GET','POST'])
def settings():
    if request.method == 'POST':
        name = request.form['name']
        if not name or len(name)>20:
            flash('输入错误')
            return redirect(url_for('settings'))
        current_user.name = name
        db.session.commit()
        flash('名臣已更新')
        return redirect(url_for('index'))
    return render_template('settings.html')