from flask import Flask, jsonify, request
from models import db, Local

app = Flask(__name__)

# Database  configuration - uso PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost:5433/Locales'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemy configuration
db.init_app(app)

# RETURN ALL THE LOCALS as json
@app.route('/locals', methods=['GET'])
def get_locals():
    locals = Local.query.all() 
    locals_list = [local.to_dict() for local in locals]  
    return jsonify(locals_list)  

# RETURN A LOCAL WITH SPECIFIC ID
@app.route('/locals/<int:id_local>', methods=['GET'])
def get_local(id_local):
    local = Local.query.get(id_local)
    if local:
        return jsonify(local.to_dict())
    return jsonify({'error': 'Local not found'}), 404

# CREATE A NEW LOCAL
@app.route('/locals', methods=['POST'])
def create_local():
    data = request.get_json()  # Parse the incoming JSON data

    # Validate that all required fields are provided
    required_fields = ['name', 'city', 'address']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400

    name = data['name']
    city = data['city']
    address = data['address']
    events = data.get('events', [])  # Use an empty list if events is not provided

    # Create a new Local object
    new_local = Local(
        name=name,
        city=city,
        address=address,
        events=events
    )

    db.session.add(new_local)
    db.session.commit()

    return jsonify(new_local.to_dict()), 201

# UPDATE AN EXISTING LOCAL
@app.route('/locals/<int:id_local>', methods=['PUT'])
def update_local(id_local):
    data = request.get_json()  
    local = Local.query.get(id_local)

    if not local:
        return jsonify({'error': 'Local not found'}), 404

    # Update fields if provided in the request body 
    if 'name' in data:
        local.name = data['name']
    if 'city' in data:
        local.city = data['city']
    if 'address' in data:
        local.address = data['address']
    if 'events' in data:
        local.events = data['events']

    db.session.commit()
    return jsonify(local.to_dict()), 200

# DELETE A LOCAL GIVEN ITS ID
@app.route('/locals/<int:id_local>', methods=['DELETE'])
def delete_local(id_local):
    local = Local.query.get(id_local)
    if local:
        db.session.delete(local)
        db.session.commit()
        return jsonify({'success': f'Local with id {id_local} deleted'}), 200
    return jsonify({'error': 'Local not found'}), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure tables are created (only runs if not existing)
    app.run(debug=True)