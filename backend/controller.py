from flask import Flask, flash, jsonify, redirect, render_template, request, session, abort
from flask_cors import CORS
from flask_bcrypt import Bcrypt, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, text
import jwt
from datetime import datetime, timedelta

app = Flask(__name__, template_folder='../templates/')
app.config['SESSION_USE_COOKIES'] = True
CORS(app)  # Use this if your frontend and backend is on different domains
app.config['SECRET_KEY'] = 'password' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  # Use your database URI
db = SQLAlchemy(app)  # Create a single instance of SQLAlchemy
bcrypt = Bcrypt(app)


#********************** PAra app segura **********************
#from sqlalchemy import text

# Use parâmetros preparados
#stmt = text("SELECT * FROM users WHERE username = :username")
#result = db.engine.execute(stmt, username=input_username) desta forma asseguramos que a pesquisa a bd é + segura, pq somos nos a mandar a query
# *************************************************************
############### TOKEN #####################
def generate_token(user_id, user_type):
    payload = {
        'user_id': user_id,
        'user_type': user_type,
        'exp': datetime.utcnow() + timedelta(hours=1)  # Token expira após 1 hora
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token

# Função para verificar um token JWT
def verify_token(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        # Token expirou
        return False
    except jwt.InvalidTokenError:
        # Token inválido
        return False
################################################### LOAD PAGES ###################################################################
@app.route('/user_info', methods=['GET'])
def get_user_info(): #função p saber se user está logado ( testada)
    token = request.headers.get('Authorization')
    
    if not token:
        user_info = {
            'is_authenticated': False
        }
        return jsonify(user_info)

    payload = verify_token(token)

    if not payload:
        user_info = {
            'is_authenticated': False
        }
        return jsonify(user_info)

    user_info = {
        'is_authenticated': True,
        'user_type': payload['user_type']
    }
    return jsonify(user_info)

@app.route('/reg_log', methods=['POST']) #função p login ( testada)
def log():
    email = request.form['email']
    password = request.form['password']
    user = users.query.filter_by(email=email).first()

    if not email or not password:
        flash('Please enter all the fields', 'error')
        return jsonify({'isauthenticated': False})
    elif not user:
        flash('Email not found', 'error')
        return jsonify({'isauthenticated': False})
    elif not check_password_hash(user.password, password):
        flash('Wrong Password', 'error')
        return jsonify({'isauthenticated': False})

    else:
        token = generate_token(user.id, user.type)
        return jsonify({'token': token, 'isauthenticated': True, 'user_type': user.type})
        

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

@app.route('/user', methods=['POST','GET']) #função p user (nao testada)
def user():
    pass

@app.route('/admin', methods=['POST','GET']) #função p admin (nao testada)
def admin():
    pass


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

@app.route('/logout', methods=['POST']) #função p logout (nao testada)
def logout():
    pass


######### Products #########
@app.route('/product/<int:product_id>')
def get_product(product_id):
    product = products.query.get(product_id)
    # lista de todas as reviews do produto
    reviews = product_comments.query.filter_by(product_id=product_id).all()
    print(reviews)
    category = categories.query.get(product.category_id)

    product_data = {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': str(product.price),
        'stock': product.stock,
        'category_id': category.id,
        'category_name': category.name,
        'photo': product.photo,
        'reviews': []
    }

    for r in reviews:
        user = users.query.get(r.user_id)
        product_data['reviews'].append({
            'user_id': user.id,
            'user_name': user.first_name,
            'rating': r.rating,
            'comment': r.comment,
            'date': r.date
        })
    return jsonify(product_data)

@app.route('/category')
def list_categories():
    category = categories.query.all()
    category_data = []
    for c in category:
        category_data.append({
            'id': c.id,
            'name': c.name
        })
    return jsonify(category=category_data)

@app.route('/product')
def list_products():
    product = products.query.all()
    product_data = []

    for p in product:
        name_categories = categories.query.get(p.category_id)
        product_data.append({
            'id': p.id,  # Use o ID para obter detalhes do produto'                                                
            'name': p.name,
            'category': name_categories.name,
            'price': str(p.price),
            'photo': p.photo,
            'stock': p.stock,
            'description': p.description         
        })
    return jsonify(products=product_data)

@app.route('/initial_products')
def list_initial_products():
    product = products.query.order_by(func.random()).limit(3).all()
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
        data = request.json  # Access JSON data from the request
        print(data)
        name = data.get('name')
        price = data.get('price')
        stock = data.get('stock')
        photo = data.get('photo')
        categories_id = data.get('categories_id')
        description = data.get('description')

        if not name or not price or not stock or not description:
            flash('Please enter all the fields', 'error')
            return jsonify({"success": False})
        
        # Crie um novo produto (caso nao tenha nada cai com null)
        if not photo:
            photo = ""
        if not categories_id:
            categories_id = None
        else:
            #atraves do id da categoria, vamos buscar o nome da categoria
            categories_name = categories.query.get(categories_id).name
        product1 = products(name=name, price=price, stock=stock, photo=photo, category_id=categories_id, description=description)
        # Adicione o produto ao banco de dados
        db.session.add(product1)
        db.session.commit()

        flash('Product added successfully')

    return jsonify({"success": True, "categories_name": categories_name})

@app.route('/update_product', methods=['POST'])
def update_product():
    if request.method == 'POST':
        product_id = request.json.get('id')  # Obtenha o ID do produto da solicitação JSON
        updated_product_name = request.json.get('name')
        updated_product_category = request.json.get('category')
        updated_quantity = request.json.get('quantity')
        updated_product_photo = request.json.get('photo')
        updated_product_description = request.json.get('description')
        updated_product_price = request.json.get('price')

        # Valide os dados conforme necessário
        if not updated_product_name or not  updated_quantity  or not updated_product_description or not updated_product_price:
            flash('Please enter all the fields', 'error')
            return jsonify({"success": False})

        # Atualize o produto no banco de dados
        product = products.query.get(product_id)
        if product:
            product.name = updated_product_name
            product.category = updated_product_category
            product.quantity = updated_quantity
            product.photo = updated_product_photo
            product.description = updated_product_description
            product.price = updated_product_price

            db.session.commit()
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "message": "Product not found"})


@app.route('/delete_product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = products.query.get(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully')
    return jsonify({"success": True})

###################################################### SQL #######################################################################


class users(db.Model):
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

