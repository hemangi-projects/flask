from flask import Flask, jsonify, request, render_template

app = Flask(__name__)
stores = [
    {
        'name':'My Wonderful Store',
         'items':[
             {
                 'name':'My Item',
                 'price': 15.99
             }
         ]
     }
]

@app.route('/') # 'http://www.google.com'
def home():
    return render_template('index.html')

@app.route('/store',methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name':request_data['name'],
        'items':[]
    }
    stores.append(new_store)
    return jsonify(new_store)
@app.route('/store/<string:name>')
def get_store(name):
    # Iterate over stores
    # if the store name matches return it
    # If none match, return an error message
    for store in stores:
        if store['name'] == 'name':
            return jsonify(store)
    return jsonify({'message':'Store Not Found'})

@app.route('/store')
@app.route('/storehemangi')
def get_all_store():
    return jsonify({'stores':stores})

@app.route('/store/<string:name>/item',methods=['POST'])
def create_item(name):
    request_date = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item={
                'name':request_date['name'],
                'price':request_date['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message':'store not found'})

@app.route('/store/<string:name>/item')
def get_item(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items':store['items']})
    return jsonify({'message':'Store not Found'})

app.run(port=5000)
