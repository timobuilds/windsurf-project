from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import Column, Integer, String, Text, Float
import os

app = Flask(__name__, static_folder='../static', template_folder='../templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healthcare_products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class HealthcareProduct(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    manufacturer = Column(String(200), nullable=True)
    rating = Column(Float, nullable=True)
    image_url = Column(String(500), nullable=True)

class HealthcareProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = HealthcareProduct

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products', methods=['GET'])
def get_products():
    category = request.args.get('category')
    if category:
        products = HealthcareProduct.query.filter_by(category=category).all()
    else:
        products = HealthcareProduct.query.all()
    
    product_schema = HealthcareProductSchema(many=True)
    return jsonify(product_schema.dump(products))

@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.json
    new_product = HealthcareProduct(
        name=data['name'],
        category=data['category'],
        description=data.get('description', ''),
        price=data['price'],
        manufacturer=data.get('manufacturer', ''),
        rating=data.get('rating'),
        image_url=data.get('image_url', '')
    )
    
    db.session.add(new_product)
    db.session.commit()
    
    product_schema = HealthcareProductSchema()
    return jsonify(product_schema.dump(new_product)), 201

@app.route('/search', methods=['GET'])
def search_products():
    query = request.args.get('q', '').lower()
    products = HealthcareProduct.query.filter(
        (HealthcareProduct.name.ilike(f'%{query}%')) | 
        (HealthcareProduct.description.ilike(f'%{query}%')) |
        (HealthcareProduct.category.ilike(f'%{query}%'))
    ).all()
    
    product_schema = HealthcareProductSchema(many=True)
    return jsonify(product_schema.dump(products))

@app.route('/static/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(os.path.join(app.root_path, '../static/images'), filename)

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

def init_db():
    with app.app_context():
        db.create_all()
        # Optional: Add some initial products
        if not HealthcareProduct.query.first():
            sample_products = [
                HealthcareProduct(name='Advanced Blood Pressure Monitor', category='Medical Devices', 
                                  description='Accurate digital blood pressure monitor with heart rate tracking', 
                                  price=79.99, manufacturer='HealthTech', rating=4.5, 
                                  image_url='/static/images/blood-pressure-monitor.jpg'),
                HealthcareProduct(name='Organic Multivitamin Supplement', category='Supplements', 
                                  description='Complete daily multivitamin for optimal health', 
                                  price=24.99, manufacturer='NutriWell', rating=4.7, 
                                  image_url='/static/images/multivitamin.jpg')
            ]
            db.session.bulk_save_objects(sample_products)
            db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=8080)
