from flask import Flask, jsonify, request
from models import db, Event

app = Flask(__name__)

# Database configuration - PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost:5433/Eventos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemy configuration
db.init_app(app)

# RETURN ALL EVENTS as JSON
@app.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    events_list = [event.to_dict() for event in events]
    return jsonify(events_list)

# RETURN AN EVENT WITH A SPECIFIC ID
@app.route('/events/<int:id_event>', methods=['GET'])
def get_event(id_event):
    event = Event.query.get(id_event)
    if event:
        return jsonify(event.to_dict())
    return jsonify({'error': 'Event not found'}), 404

# CREATE A NEW EVENT
@app.route('/events', methods=['POST'])
def create_event():
    data = request.get_json()  # Parse the incoming JSON data

    # Validate that all required fields are provided
    required_fields = ['name', 'description', 'city', 'max_capacity']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400

    name = data['name']
    description = data['description']
    city = data['city']
    max_capacity = data['max_capacity']
    subscribers = data.get('subscribers', [])  # Default to an empty list if not provided

    # Ensure subscribers do not exceed max_capacity
    if len(subscribers) > max_capacity:
        return jsonify({'error': 'Subscribers exceed maximum capacity'}), 400

    # Create a new Event object
    new_event = Event(
        name=name,
        description=description,
        city=city,
        max_capacity=max_capacity,
        subscribers=subscribers
    )

    db.session.add(new_event)
    db.session.commit()

    return jsonify(new_event.to_dict()), 201

# UPDATE AN EXISTING EVENT
@app.route('/events/<int:id_event>', methods=['PUT'])
def update_event(id_event):
    data = request.get_json()
    event = Event.query.get(id_event)

    if not event:
        return jsonify({'error': 'Event not found'}), 404

    # Update fields if provided in the request body
    if 'name' in data:
        event.name = data['name']
    if 'description' in data:
        event.description = data['description']
    if 'city' in data:
        event.city = data['city']
    if 'max_capacity' in data:
        if len(event.subscribers) > data['max_capacity']:
            return jsonify({'error': 'Subscribers exceed new maximum capacity'}), 400
        event.max_capacity = data['max_capacity']
    if 'subscribers' in data:
        if len(data['subscribers']) > event.max_capacity:
            return jsonify({'error': 'Subscribers exceed maximum capacity'}), 400
        event.subscribers = data['subscribers']

    db.session.commit()
    return jsonify(event.to_dict()), 200

# DELETE AN EVENT GIVEN ITS ID
@app.route('/events/<int:id_event>', methods=['DELETE'])
def delete_event(id_event):
    event = Event.query.get(id_event)
    if event:
        db.session.delete(event)
        db.session.commit()
        return jsonify({'success': f'Event with id {id_event} deleted'}), 200
    return jsonify({'error': 'Event not found'}), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure tables are created (only runs if not existing)
    app.run(debug=True)
