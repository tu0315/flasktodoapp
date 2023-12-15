# 各インポート
from datetime import datetime, date
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # クラス(設計書)のインスタンス(実体)化
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite:///todo.db"  # db名の宣言（SQliteを使って、todoというDBを作る）

db = SQLAlchemy(app)  # db情報


class Post(db.Model):  # dbに追加するPostテーブルのクラス宣言
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    detail = db.Column(db.String(100))
    due = db.Column(db.DateTime, nullable=False)


@app.route("/", methods=["GET", "POST"])  # /にアクセスした際の処理。Indexページ
def index():  # index関数
    if request.method == "GET":  # GETの場合(単純にアクセスした時)
        posts = Post.query.order_by(Post.due).all()  # Postを期限順に全取得
        return render_template(
            "index.html", posts=posts, today=date.today()
        )  # templateを読み込む、引数で変数をセット
    else:  # CreateよりPOSTでIndexにリダイレクトされた場合の処理
        title = request.form.get("title")  # Requestからtitle取得
        detail = request.form.get("detail")  # Requestからdetail取得
        due = request.form.get("due")  # Requestからdue取得

        due = datetime.strptime(due, "%Y-%m-%d")  # 文字列で取得したdueをdate型にフォーマットする

        new_post = Post(title=title, detail=detail, due=due)  # 新しいPostを生成
        db.session.add(new_post)  # 追加
        db.session.commit()  # 実行
        return redirect("/")  # リダイレクト


@app.route("/create")  # 新規作成
def create():  # create関数
    return render_template("create.html")  # templateのcreate.htmlへ


@app.route("/detail/<int:id>")  # 詳細
def detail(id):  # detail関数。idを渡す
    post = Post.query.get(id)  # idからPostを取得する
    return render_template(
        "detail.html", post=post
    )  # templateのcreate.htmlへ。取得したPostもセット


@app.route("/update/<int:id>", methods=["GET", "POST"])  # 更新
@app.route("/detail/update/<int:id>", methods=["GET", "POST"])  # 詳細->更新
def update(id):  # update関数。idを渡す
    post = Post.query.get(id)  # idからPostを取得する

    if request.method == "GET":  # GETの場合はupdateのページへ
        return render_template(
            "update.html", post=post
        )  # templateのcreate.htmlへ。取得したPostもセット
    else:  # POSTの場合はDBに反映
        post.title = request.form.get("title")  # requestのフォームよりtitle取得
        post.detail = request.form.get("detail")  # requestのフォームよりdetail取得
        post.due = datetime.strptime(
            request.form.get("due"), "%Y-%m-%d"
        )  # requestのフォームよりdue取得、文字列をキャストする
        db.session.commit()  # 実行
        return redirect("/")  # トップページにリダイレクト


@app.route("/delete/<int:id>")  # 削除
def delete(id):  # delete関数。idを渡す
    post = Post.query.get(id)  # Postをidから取得
    db.session.delete(post)  # 削除
    db.session.commit()  # 実行
    return redirect("/")  # トップページへ


if __name__ == "__name__":
    app.run(debug=True)  # appをdebug:onで走らせる
