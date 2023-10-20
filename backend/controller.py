from flask import Flask, flash, jsonify, redirect, render_template, request, session, abort
from flask_cors import CORS
from flask_bcrypt import Bcrypt, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sqlalchemy import text


app = Flask(__name__, template_folder='../templates/')
app.config['SECRET_KEY'] = 'password' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  # Use your database URI
db = SQLAlchemy(app)  # Create a single instance of SQLAlchemy
bcrypt = Bcrypt(app)
CORS(app)
login_manager = LoginManager(app)
login_manager.login_view = "login" 

#********************** PAra app segura **********************
#from sqlalchemy import text

# Use parâmetros preparados
#stmt = text("SELECT * FROM users WHERE username = :username")
#result = db.engine.execute(stmt, username=input_username) desta forma asseguramos que a pesquisa a bd é + segura, pq somos nos a mandar a query
# *************************************************************

################################################### LOAD PAGES ###################################################################

@app.route('/register', methods=[ 'POST']) #função p registo (testada)
def register():
    
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if not name or not email or not password:
        flash('Please enter all the fields', 'error')
    elif password != confirm_password:
        flash('Passwords do not match', 'error')
    else:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = users(first_name=name, email=email, password=hashed_password, type='normal')
        db.session.add(user)
        db.session.commit()

        flash('Registration successful', 'success')

    return redirect('http://127.0.0.1:5500/templates/reg_log.html')  # Redirecione para a página de login ou qualquer outra página desejada após o registro



@app.route('/reg_log', methods=['POST']) #função p login (nao testada)
def log():
    email = request.form['email']
    password = request.form['password']
    user = users.query.filter_by(email=email).first()

    if not email or not password:
        flash('Please enter all the fields', 'error')
    elif not user:
        flash('Email not found', 'error')
    elif not check_password_hash(user.password, password):
        flash('Wrong Password', 'error')
    else:
        login_user(user)  
        return  redirect('http://127.0.0.1:5500/templates/index.html')

@login_manager.user_loader
def load_user(user_id):  # Função para carregar o usuário a partir do banco de dados
    return users.query.get(int(user_id))


@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile(): # Apenas usuários autenticados podem acessar esta rota
    # Você pode acessar os dados do usuário atual usando 'current_user'
    if current_user.type == 'normal':
        return render_template('http://127.0.0.1:5500/templates/userdashboard.html')
    elif current_user.type == 'admin':
        return redirect('http://127.0.0.1:5500/templates/adminpage.html') #falta fazer esta página
    else:
        abort(403)  # Acesso negado


@app.route('/changepswd', methods=['POST','GET']) #função p mudar pass (nao testada)
def changepswd():

    email = request.form['email']
    old_password = request.form['password']
    new_password = request.form['new_password']
    logger = users.query.filter_by(email=email)
    if not old_password or not new_password:
        flash('Please enter all the fields', 'error')
    elif old_password != logger.password:
        flash('Wrong Password', 'error')
    else: 
        logger.password = new_password
        db.session.commit()

    return render_template('user.html') #falta fazer esta página

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('http://127.0.0.1:5500/templates/index.html')



######### Products #########

@app.route('/product')
def list_products():
    product = products.query.all()
    product_data = []

    for p in product:
        product_data.append({
            'id': p.id,  # Use o ID para obter detalhes do produto'                                                
            'name': p.name,
            'price': str(p.price),
            'photo': p.photo
        })
    return jsonify(products=product_data)


@app.route('/add_product', methods=['POST'])
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        stock = request.form.get('stock')
        photo = request.form.get('photo')

        # Crie um novo produto
        product1 = products(name=name, price=price, stock=stock, photo=photo)

        # Adicione o produto ao banco de dados
        db.session.add(product1)
        db.session.commit()

        flash('Product added successfully')

    return render_template('add_product.html')

###################################################### SQL #######################################################################


class users(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=False)
    
class orders(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    order_status = db.Column(db.String(255), nullable=False)


class products(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    photo = db.Column(db.String(255))

class order_items(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)


class categories(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)


class payments(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, nullable=False)
    payment_status = db.Column(db.String(255), nullable=False)  # Mude para String
    payment_method = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

class product_comments(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

class favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

 

###################################################### RUN #######################################################################

if __name__ == '__main__':
    
    app.run()

