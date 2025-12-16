"""
An eCommerce website with payment processing.
"""
from flask import Flask, render_template, redirect, url_for, flash, session, request, jsonify
from flask_ckeditor import CKEditor
from flask_login import UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from werkzeug.security import generate_password_hash, check_password_hash
from collections import Counter

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)

login_manager = LoginManager()
login_manager.init_app(app)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///member.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Create a User table for all your registered users
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    # return db.get_or_404(User, user_id)
    for user_data in User.values():
        if str(user_data['id']) == str(user_id):
            return User(user_data['id'], user_data['email'], user_data['password'], user_data['first_name'])
    return None

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    user_name = session.get("user")  # 這裡抓到登入時存的名字
    cart = session.get('cart', [])
    return render_template("index.html", user=user_name, art_count=len(cart))

@app.route("/shop")
def shop():
    user_name = session.get("user")  # 這裡抓到登入時存的名字
    cart = session.get('cart', [])
    return render_template("shop.html", user=user_name, art_count=len(cart))

@app.get('/cart_count')
def cart_count():
    cart = session.get('cart', [])
    return jsonify({"count": len(cart)})

@app.route('/cart_data')
def cart_data():
    cart_session = session.get('cart', [])
    # 假設你的商品資料庫
    products = {
        "1": {"name": "Nordic Chair", "price": 50.0, "image": "product-3.png"},
        "2": {"name": "Eames Lounge Chair", "price": 50.0, "image": "product-1.png"},
        "3": {"name": "Kruzo Aero Chair", "price": 78.0, "image": "product-2.png"},
        "4": {"name": "Ergonomic Chair", "price": 43.0, "image": "product-3.png"},
        "5": {"name": "Wishbone Chair", "price": 50.0, "image": "product-3.png"},
        "6": {"name": "Acapulco Chair", "price": 50.0, "image": "product-1.png"},
        "7": {"name": "Papasan Chair", "price": 78.0, "image": "product-2.png"},
        "8": {"name": "Lounge Chair", "price": 43.0, "image": "product-3.png"},
    }

    # 統計每個商品 ID 的數量
    counts = Counter(cart_session)

    cart_items = []
    for pid, qty in counts.items():
        product = products.get(pid)
        if product:
            cart_items.append({
                "id": pid,
                "name": product["name"],
                "price": product["price"],
                "image": product["image"],
                "qty": qty  # 數量用計數
            })
    return jsonify(cart_items)

@app.route("/services")
def services():
    user_name = session.get("user")  # 這裡抓到登入時存的名字
    cart = session.get('cart', [])
    return render_template("services.html", user=user_name, art_count=len(cart))

@app.route("/blog")
def blog():
    user_name = session.get("user")  # 這裡抓到登入時存的名字
    cart = session.get('cart', [])
    return render_template("blog.html", user=user_name, art_count=len(cart))

@app.route("/about")
def about():
    user_name = session.get("user")  # 這裡抓到登入時存的名字
    cart = session.get('cart', [])
    return render_template("about.html", user=user_name, art_count=len(cart))

@app.route("/contact")
def contact():
    user_name = session.get("user")  # 這裡抓到登入時存的名字
    cart = session.get('cart', [])
    return render_template("contact.html", user=user_name, art_count=len(cart))

@app.route("/cart")
def cart():
    cart = session.get('cart', [])
    user_name = session.get("user")  # 這裡抓到登入時存的名字
    return render_template("cart.html", user=user_name, art_count=len(cart))

@app.post('/add_to_cart')
def add_to_cart():
    data = request.get_json()
    product_id = data.get("product_id")

    # 建立購物車 session
    cart = session.get('cart', [])

    cart.append(product_id)
    session['cart'] = cart

    return jsonify({"message": "商品已加入購物車!", "count": len(cart)})

@app.post('/cart/remove_from_cart')
def remove_from_cart():
    data = request.get_json()
    product_id = data.get("product_id")

    cart = session.get('cart', [])
    # 移除購物車中所有該商品
    cart = [pid for pid in cart if pid != product_id]
    session['cart'] = cart

    return jsonify({"message": "商品已從購物車移除", "count": len(cart)})

@app.route("/checkout")
def checkout():
    # 檢查是否登入
    if 'user' not in session:
        # 沒登入就導向 login 頁面
        return redirect(url_for('login'))

    # 已登入就渲染 checkout 頁面
    user_name = session.get("user")  # 這裡抓到登入時存的名字
    cart = session.get('cart', [])
    return render_template("checkout.html", user=user_name, art_count=len(cart))

@app.route("/thankyou")
def thankyou():
    user_name = session.get("user")  # 這裡抓到登入時存的名字
    cart = session.get('cart', [])
    return render_template("thankyou.html", user=user_name, art_count=len(cart))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # 驗證欄位完整
        if not email or not password:
            flash("請輸入 Email 與密碼")
            return redirect(url_for("login"))

        # 查詢使用者
        # result = db.session.execute(db.select(User).where(User.email == email))
        user = User.query.filter_by(email=email).first()

        if not user:
            print("🚫 Email 尚未註冊")
            # flash("此 Email 尚未註冊")
            return redirect(url_for("login"))

        # 密碼比對
        if not check_password_hash(user.password, password):
            print("密碼錯誤")
            # flash("密碼錯誤")
            return redirect(url_for("login"))

        # 登入成功，設定 session
        print("--- 登入成功，準備重導向 ---")
        session["user"] = user.first_name
        return redirect(url_for("login_success"))

    return render_template("login.html")

@app.route("/login_success")
def login_success():
    user_name = session.get("user")  # 讀 session
    cart = session.get('cart', [])
    return render_template("login_success.html", user=user_name, art_count=len(cart))

@app.route('/logout')
def logout():
    session.pop("user", None)
    print("登出成功")
    return redirect(url_for("login"))

@app.route("/change_password")
def change_password():
    cart = session.get('cart', [])
    return render_template("change_password.html", art_count=len(cart))

@app.route("/register_completed", methods=["GET", "POST"])
def register_completed():
    if request.method == "POST":
        country = request.form.get("country")
        email = request.form.get("email").lower()  # 統一小寫
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        password = request.form.get("password")

        # 🔹 檢查 Email 是否已存在
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print("此 Email 已經註冊過，請直接登入")
            return redirect(url_for("login"))

        # 🔹 加密密碼
        hash_and_salted_password = generate_password_hash(
            password,
            method='pbkdf2:sha256',
            salt_length=8
        )

        # 🔹 新增用戶
        new_user = User(
            email=email,
            password=hash_and_salted_password,
            first_name=first_name,
            last_name=last_name,
            country=country
        )
        db.session.add(new_user)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("DB Error:", e)
            return redirect(url_for("login"))

        # 🔹 註冊成功，存 session 並跳轉
        session["user"] = first_name
        print("註冊成功")
        return redirect(url_for("register_completed"))

    # GET 顯示註冊頁
    cart = session.get('cart', [])
    return render_template("register_completed.html", user=session["user"], art_count=len(cart))


if __name__ == "__main__":
  app.run(debug=True, port=8000)