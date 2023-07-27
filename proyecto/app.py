import psycopg2
import os

from flask import Flask

app = Flask(__name__)

# Método para retornar las credenciales para conectar a la DB
def get_conexion():
    info = ''
    # GETENV Obtiene las variables de entorno, en caso de no existir tomará el segundo parametro
    user = os.getenv('DB_USER','gmfqxtjr')
    password = os.getenv('DB_PASS','uhAmgqUuk4hVAgMAeRvHovJIa94DeG1x')
    host = os.getenv('DB_HOST','tuffi.db.elephantsql.com')
    port = os.getenv('DB_PORT','5432')
    database = os.getenv('DB_NAME','gmfqxtjr')
    try:
        connection = psycopg2.connect(
        user=user, password=password,
        host=host, port=port, database=database)
        info = str(connection.get_dsn_parameters())
        connection.close()
    except:
        info = 'ERROR'
    return info

@app.route('/', methods=['GET'])
# método que retorna un objeto JSON con las keys mensaje y conexión
def index():
    conexion = get_conexion()
    return {
        'mensaje': 'Hola mundo',
        'conexion': conexion
    }

# Levantamos el servidor con Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)