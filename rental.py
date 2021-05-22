from flask import Flask, render_template, request, redirect, url_for, session
import pymongo
from bson.objectid import ObjectId
import os
from bson import ObjectId
from flask import jsonify
from pymongo.collation import CollationAlternate
# from flask_pymongo import Pymongo

# query = {"_id": ObjectId(id)}
#             result = userCollection.find_one(query)

#conexion
myClient = pymongo.MongoClient("mongodb://localhost:27017")
myDb = myClient["RentalDb"] #database
userCollection = myDb["user"] #myCollection
propertyCollection = myDb["property"]

app = Flask(__name__)
app.secret_key = "pass1234"
app.config['UPLOAD_FOLDER'] = './static/images'
           

@app.route('/getProperty', methods=['GET'])
def getProperty():
    result = []
    for doc in propertyCollection.find():
        result.append({
        '_id': str(doc['_id']),
        'cityP':doc['cityP'],
        'countryP': doc['countryP'],
        'adressP': doc['adressP'],
        'ubication': doc['ubication'],
        'roomNumber': doc['roomNumber'],
        # 'imageP': doc['imageP'],
        'priceDay': doc['priceDay'],
        'Description': doc['Description']
        # 'listimage':doc['listimage']
    })
    
    return jsonify(result)

@app.route('/getPropertyById/<id>')
def editUser(id):
    property = propertyCollection.find_one({'_id': ObjectId(id)})
    result = []
    result.append({
        'cityP':property['cityP'],
        'countryP': property['countryP'],
        'adressP': property['adressP'],
        'ubication': property['ubication'],
        'roomNumber': property['roomNumber'],
        'imageP': property['imageP'],
        'priceDay': property['priceDay'],
        'Description': property['Description']
    })
    return jsonify(result)

@app.route('/Addproperty', methods=["POST"])
def Addproperty():
    
        cityP = request.form.get('cityP')
        countryP = request.form.get('countryP')
        adressP = request.form.get('adressP')
        ubication = request.form.get('ubication')
        roomNumber = request.form.get('roomNumber')
        # imageP = request.files['imageP']
        priceDay = request.form.get('priceDay')
        Description = request.form.get('Description')
        # imageMain = request.files.getlist('imageMain[]')
        # mainimage = imageP.filename
        # imageP.save(os.path.join(app.config['UPLOAD_FOLDER'], mainimage))
        # name_images =[]
        # for image in imageMain:
        #     image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
        #     name_images.append(image.filename)
        # insertProperty={'cityP': cityP, 'countryP': countryP, 'adressP': adressP, 'ubication': ubication, 'roomNumber': roomNumber, 'imageP': mainimage, 'priceDay': priceDay, 'Description': Description,'listimage':name_images}
        insertProperty={'cityP': cityP, 'countryP': countryP, 'adressP': adressP, 'ubication': ubication, 'roomNumber': roomNumber,  'priceDay': priceDay, 'Description': Description}

        save = propertyCollection.insert_one(insertProperty)
        return (save)

#Guardar datos de ususario editado en base de datos
@app.route('/editProperty/<id>', methods=['POST'])
def editProperty(id):
        cityP = request.form.get('cityP')
        countryP = request.form.get('countryP')
        adressP = request.form.get('adressP')
        ubication = request.form.get('ubication')
        roomNumber = request.form.get('roomNumber')
        # imageP = request.files['imageP']
        priceDay = request.form.get('priceDay')
        Description = request.form.get('Description')
        # imageMain = request.files.getlist('imageMain[]')
        # mainimage = imageP.filename
        # imageP.save(os.path.join(app.config['UPLOAD_FOLDER'], mainimage))
        # name_images =[]
        # for image in imageMain:
        #     image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
        #     name_images.append(image.filename)
        propertyCollection.update_one({'_id': ObjectId(id)}, {"$set": {
            'cityP': cityP,
            'countryP': countryP,
            'adressP': adressP,
            'ubication': ubication,
            'roomNumber': roomNumber,
            # 'imageP': mainimage,
            'priceDay': priceDay,
            'Description': Description,
            # 'listimage': name_images
        }})
        return ('property edit successful', id)

@app.route('/deleteProperty/<id>',methods=['DELETE'])
def deleteProperty(id):
        propertyCollection.delete_one({'_id': ObjectId(id)})
        return ('Registro eliminado exitosamente' + '' + id)             

if __name__ == '__main__':
    app.run(debug=True) #se genera el servidor local