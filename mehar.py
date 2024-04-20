from flask import *
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__, static_url_path='/static')  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///logininfo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'mehar'
db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@app.route('/')
def homelog():
    return render_template("homelog.html")

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/contactlog')
def contactlog():
    return render_template("contactlog.html")

@app.route('/serviceslog')
def serviceslog():
    return render_template("servicelog.html")

@app.route('/redirected_page', methods=['POST'])
def redirected_page():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        session['username'] = username
        if user and check_password_hash(user.password, password):
            return render_template('home.html', username=username)
        else:
            return "Invalid username or password"
    else:
        return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']
        if User.query.filter_by(username=new_username).first():
            return "Username already taken. Choose a different one."
        hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256', salt_length=8)
        new_user = User(username=new_username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = new_username
        return redirect(url_for('home'))
    return render_template('signup.html')

@app.route('/home')
def home():
    return render_template("home.html", username=session.get('username', 'new_username'))

@app.route('/shop')
def Shop():
    return render_template("Shop.html", username=session.get('username', 'new_username'))

@app.route('/services')
def services():
    return render_template("Services.html", username=session.get('username', 'new_username'))

@app.route('/contact')  
def contact():  
    return render_template("contact.html", username=session.get('username', 'new_username'))

@app.route('/cart')
def cart():
    return render_template("Cart.html", username=session.get('username', 'new_username'))

@app.route('/generate_receipt', methods=['POST'])
def generate_receipt():
    cart_data = request.form.get('cartData')
    cart = json.loads(cart_data)
    total_price = sum(item['price'] * item['quantity'] for item in cart)
    receipt_html = render_template('receipt.html', cart=cart, total=total_price)
    response = make_response(receipt_html)
    response.headers["Content-Disposition"] = "attachment; filename=receipt.html"
    response.headers["Content-Type"] = "text/html"
    return response

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True)