from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# db名の宣言（SQliteを使って、todoというDBを作る）
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(app)


# Postクラス宣言
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    detail = db.Column(db.String(100))
    due = db.Column(db.DateTime, nullable=False)


# index
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        # GETの場合(単純にアクセスした時)は全取得
        posts = Post.query.order_by(Post.due).all()
        return render_template("index.html", posts=posts, today=date.today())
    else:
        title = request.form.get("title")
        detail = request.form.get("detail")
        due = request.form.get("due")

        # date型にキャストする
        due = datetime.strptime(due, "%Y-%m-%d")

        post = Post(title=title, detail=detail, due=due)
        db.session.add(post)
        db.session.commit()
        return redirect("/")


# 新規作成
@app.route("/create")
def create():
    return render_template("create.html")


# 詳細
@app.route("/detail/<int:id>")
def detail(id):  # idを渡す
    post = Post.query.get(id)
    return render_template("detail.html", post=post)


# 編集
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):  # idを渡す
    post = Post.query.get(id)

    if request.method == "GET":
        # updateに送る情報
        return render_template("update.html", post=post)
    else:
        # 更新内容
        post.title = request.form.get("title")
        post.detail = request.form.get("detail")
        post.due = datetime.strptime(request.form.get("due"), "%Y-%m-%d")
        db.session.commit()
        # トップページに戻る
        return redirect("/")


# 削除
@app.route("/delete/<int:id>")
def delete(id):  # idを渡す
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect("/")
