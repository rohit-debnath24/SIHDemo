from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  

DOGS_FILE = 'dogs.json'

def read_dogs():
   
    if not os.path.exists(DOGS_FILE):
        return []
    with open(DOGS_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def write_dogs(dogs):
   
    with open(DOGS_FILE, 'w') as f:
        json.dump(dogs, f, indent=4)

@app.route('/api/dogs', methods=['GET'])
def get_dogs():
   
    dogs = read_dogs()
    return jsonify(dogs)

@app.route('/api/dogs/<int:dog_id>', methods=['GET'])
def get_dog(dog_id):
  
    dogs = read_dogs()
    dog = next((d for d in dogs if d['id'] == dog_id), None)
    if dog:
        return jsonify(dog)
    return jsonify({'error': 'Dog not found'}), 404

@app.route('/api/dogs', methods=['POST'])
def add_dog():
   
    new_dog_data = request.json
    if not new_dog_data:
        return jsonify({'error': 'Invalid data'}), 400

    dogs = read_dogs()
    
   
    new_dog_data['id'] = dogs[-1]['id'] + 1 if dogs else 1
    
    dogs.append(new_dog_data)
    write_dogs(dogs)
    
    return jsonify(new_dog_data), 201

if __name__ == '__main__':
   
    app.run(debug=True, port=5000)
