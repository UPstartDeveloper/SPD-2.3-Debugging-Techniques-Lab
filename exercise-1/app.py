from flask import Flask, flash, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import enum

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
db = SQLAlchemy(app, session_options={"autoflush": False})

###############################################
### MODELS
###############################################

class PizzaSize(enum.Enum):
    SMALL = '12 Inch'
    MEDIUM = '16 Inch'
    LARGE = '20 Inch'

class CrustType(enum.Enum):
    THIN = 'Thin'
    THICK = 'Thick'
    GLUTEN_FREE = 'Gluten Free'

class ToppingType(enum.Enum):
    SOY_CHEESE = 'Soy Cheese'
    MUSHROOMS = 'Mushrooms'
    ONIONS = 'Onions'
    SPINACH = 'Spinach'
    PINEAPPLE = 'Pineapple'

class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_name = db.Column(db.String(80), unique=False, nullable=False)
    size = db.Column(db.Enum(PizzaSize), nullable=False)
    crust_type = db.Column(db.Enum(CrustType), nullable=False)
    toppings = db.relationship('PizzaTopping')
    fulfilled = db.Column(db.Boolean, default=False)

class PizzaTopping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topping_type = db.Column(db.Enum(ToppingType))
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'))

with app.app_context():
    db.create_all()

###############################################
### ROUTES
###############################################

@app.route('/')
def home():
    with app.app_context():
        all_pizzas = Pizza.query.filter_by(fulfilled=False)
    print(all_pizzas)
    return render_template('home.html', pizza_orders=all_pizzas)

@app.route('/order', methods=['GET'])
def pizza_order_form():
    return render_template(
        'order.html',
        sizes=PizzaSize,
        crust_types=CrustType,
        toppings=ToppingType)

@app.route('/order', methods=['POST'])
def pizza_order_submit():
    '''Add the Pizza order details to the database.'''
    # get data from the order form
    order_name = request.form.get('order_name')
    pizza_size_str = request.form.get('pizza_size')
    crust_type_str = request.form.get('crust_type')
    toppings_list = request.form.getlist('toppings')
    # add the pizza order to the db
    pizza = Pizza(
        order_name=order_name,
        size=pizza_size_str,
        crust_type=crust_type_str,
        fulfilled=False
    )
    # save the id of the new pizza
    pizza_id = -1
    with app.app_context():
        db.session.add(pizza)
        db.session.commit()
        pizza_id = pizza.id
    # make the pizza toppings, using the id of the order above
    toppings = list()
    for topping_str in toppings_list:
        new_topping = PizzaTopping(topping_type=topping_str, pizza_id=pizza_id)
        with app.app_context():
            db.session.add(new_topping)
        toppings.append(new_topping)
    # update the toppings on the order
    with app.app_context():
        pizza = Pizza.query.filter_by(id=pizza.id).one()
        pizza.toppings = toppings
        db.session.add(pizza)
        db.session.commit()
    flash('Your order has been submitted!')
    return redirect(url_for('home'))

@app.route('/fulfill', methods=['POST'])
def fulfill_order():
    """TODO: add the id of the pizza for the route to work"""
    pizza_id = request.form.get('pizza_id')
    pizza = Pizza.query.filter_by(id=pizza_id).one()

    pizza.fulfilled = True
    db.session.add(pizza)
    db.session.commit()
    
    flash(f'The order for {pizza.order_name} has been fulfilled.')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)