from functools import wraps
from pathlib import Path
import pandas as pd
import io
from flask import Flask, flash, jsonify, redirect, render_template,send_file, request, session, url_for

from services.data_service import load_dashboard_data
from services.qa_service import answer_question


BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)
app.config["SECRET_KEY"] = "day07-classroom-demo-key"


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "username" not in session:
            flash("请先登录后再访问数据看板。", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped_view


@app.route("/")
def index():
    return redirect(url_for("dashboard") if "username" in session else url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if username == "student" and password == "day07":
            session["username"] = username
            flash("登录成功，欢迎进入电商用户分析系统。", "success")
            return redirect(url_for("dashboard"))
        flash("账号或密码错误。演示账号：student / day07", "danger")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("你已安全退出。", "success")
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    category = request.args.get("category", "全部")
    dashboard_data = load_dashboard_data(BASE_DIR, category)
    return render_template(
        "dashboard.html",
        username=session["username"],
        selected_category=category,
        **dashboard_data,
    )


@app.route("/assistant")
@login_required
def assistant():
    return render_template("assistant.html", username=session["username"])


@app.route("/api/ask", methods=["POST"])
@login_required
def ask():
    payload = request.get_json(silent=True) or {}
    question = str(payload.get("question", "")).strip()
    if not question:
        return jsonify({"ok": False, "answer": "请输入一个与项目数据有关的问题。"}), 400
    return jsonify({"ok": True, "answer": answer_question(BASE_DIR, question)})

@app.route("/segments")
def segments():
    data = load_segment_data(base_dir)  # 需在 data_service.py 中实现此函数
    return render_template("segments.html", segments=data)

@app.route("/download")
def download_category():
    category = request.args.get("category", "")

    # 1. 读取品类数据
    data_dir = Path(__file__).parent / "data"
    df = pd.read_csv(data_dir / "category_analysis.csv", encoding="utf-8-sig")

    # 2. 按传入的品类筛选
    if category and category != "全部":
        filtered = df[df["PreferedOrderCat"] == category]
    else:
        filtered = df

    # 3. 若筛选结果为空，返回提示
    if filtered.empty:
        return f"未找到品类 '{category}' 的数据，请检查名称是否正确。", 404

    # 4. 将DataFrame转为CSV字节流并返回下载
    output = io.StringIO()
    filtered.to_csv(output, index=False, encoding="utf-8-sig")
    output.seek(0)

    filename = f"{category}_analysis.csv" if category else "all_categories.csv"
    return send_file(
        io.BytesIO(output.getvalue().encode("utf-8-sig")),
        mimetype="text/csv",
        as_attachment=True,
        download_name=filename
    )

@app.errorhandler(404)
def page_not_found(_error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=False, port=5000)
