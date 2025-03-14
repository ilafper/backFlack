from flask import Flask, jsonify, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas

# Conectar a MongoDB Atlas
uri = "mongodb+srv://ialfper:ialfper21@alumnos.zoinj.mongodb.net/?retryWrites=true&w=majority&appName=alumnos"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["despliegue"]
collection = db["usuarios"]

# Función para convertir los ObjectId a cadenas en un documento
def convert_id_to_string(document):
    if "_id" in document:
        document["_id"] = str(document["_id"])  # Convertir ObjectId a string
    return document

# Ruta para buscar usuarios
@app.route('/api/buscar', methods=["GET"])
def buscar():
    buscar = request.args.get('buscar', '').lower()
    if not buscar:
        return jsonify({"error": "Falta el parámetro de búsqueda 'buscar'"}), 400

    # Búsqueda solo por el campo 'nombre'
    resultados = list(collection.find({"nombre": {"$regex": buscar, "$options": "i"}}))  # 'i' para que sea insensible a mayúsculas/minúsculas
    
    if resultados:
        resultados = [convert_id_to_string(user) for user in resultados]
        response = jsonify(resultados)
    else:
        response = jsonify({"message": "No se encontraron coincidencias"}), 404
    response.headers.add("Access-Control-Allow-Origin", "*")  # Agregar encabezado CORS
    return response


# Ruta para agregar un nuevo usuario
@app.route('/api/nuevo', methods=["POST"])
def nuevo():
    nuevoUser = request.get_json()
    if not nuevoUser.get('nombre'):
        return jsonify({"error": "Faltan datos requeridos ('nombre'"}), 400

    result = collection.insert_one(nuevoUser)
    nuevoUser["_id"] = str(result.inserted_id)
    
    response = jsonify(nuevoUser), 201
    response[0].headers.add("Access-Control-Allow-Origin", "*")  # Agregar encabezado CORS
    return response

# Ruta para obtener todos los usuarios
@app.route('/api/users', methods=["GET"])
def users():
    usuarios = list(collection.find())
    usuarios = [convert_id_to_string(user) for user in usuarios]
    
    response = jsonify(usuarios)
    response.headers.add("Access-Control-Allow-Origin", "*")  # Agregar encabezado CORS
    return response

@app.route('/api')
def home():
    response = jsonify({'message': 'Hello, World!'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/api/about')
def about():
    response = jsonify({'message': 'About'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
