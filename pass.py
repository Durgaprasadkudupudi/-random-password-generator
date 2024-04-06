from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import random

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['passwords_db']
collection = db['passwords']

lower = 'qwertyuiopasdfghjkzxcvbnm'
upper = lower.upper()
numbers = '1234567890'
special = '!@#$%^&*?|*-/'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_password', methods=['POST'])
def generate_password():
    data = request.get_json()
    nlowers = data['nlowers']
    nuppers = data['nuppers']
    nnumbers = data['nnumbers']
    nspl = data['nspl']
    
    password = []
    
    for i in range(nlowers):
        char = random.choice(lower)
        password.append(char)
    
    for i in range(nuppers):
        char = random.choice(upper)
        password.append(char)
    
    for i in range(nnumbers):
        char = random.choice(numbers)
        password.append(char)
    
    for i in range(nspl):
        char = random.choice(special)
        password.append(char)
    
    random.shuffle(password)
    generated_password = ''.join(password)
    
    # Save the generated password to MongoDB
    collection.insert_one({'password': generated_password})
    
    return jsonify({'password': generated_password})


@app.route('/check_password', methods=['POST'])
def check_password():
    data = request.get_json()
    password = data['password']
    
    count1 = sum(1 for i in password if i in numbers)
    count2 = sum(1 for j in password if j in upper)
    count3 = sum(1 for k in password if k in lower)
    count4 = sum(1 for l in password if l in special)
    
    if count1 >= 2 and count2 >= 2 and count3 >= 2 and count4 >= 2 and len(password) >= 8:
        return jsonify({'message': 'Valid password'})
    else:
        return jsonify({'message': 'Invalid password, please try again'})




if __name__ == '__main__':
    app.run(debug=True)
