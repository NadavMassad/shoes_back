import json
from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"
 
db = SQLAlchemy(app)

class Shoes(db.Model):
    id = db.Column('animal_id', db.Integer, primary_key = True)
    brand = db.Column(db.String(100))
    color = db.Column(db.String(50))
    price = db.Column(db.Integer)

    def __init__(self, brand, color, price):
        self.brand = brand
        self.color = color
        self.price = price


@app.route('/shoes/<id>', methods = ['GET', 'POST', 'DELETE', 'PUT'])
@app.route('/shoes/', methods = ['GET', 'POST', 'DELETE', 'PUT'])
def crud_shoes(id=id):
    if request.method == 'GET':
        res = []
        for shoe in Shoes.query.all():
            res.append({'id': shoe.id, 'brand': shoe.brand, 'color': shoe.color, 'price': shoe.price})
        return (json.dumps(res))
    if request.method == 'POST':
        request_data = request.get_json()
        brand = request_data['brand']
        color = request_data['color']
        price = request_data['price']
        new_car = Shoes(brand, color, price)
        db.session.add (new_car)
        db.session.commit()
        return 'New Shoe Was Added'
    if request.method == 'DELETE':
        del_car = Shoes.query.get(id)
        db.session.delete(del_car)
        db.session.commit()
        return {"msg": 'A Shoe Was Deleted'}
    if request.method == 'PUT':
        update_car = Shoes.query.get(id)
        brand = request.json['brand']
        color = request.json['color']
        price = request.json['price']
        update_car.brand = brand
        update_car.color = color
        update_car.price = price
        db.session.commit()
        return  {"msg: 'A Shoe Was Edited'"}

@app.route('/')
def test():
    return 'Test'
 
if __name__ == '__main__':
    with app.app_context():db.create_all()
    app.run(debug = True)
