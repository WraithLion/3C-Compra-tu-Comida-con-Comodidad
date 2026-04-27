from flask import Flask,jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
##Aquí es donde deberían cambiar por sus datos. 
@app.route('/persona', methods=['GET'])
def get_persona():
    persona = {
        'nombre': 'Haans', 
        'lastname': 'Lopez',
        'email': 'jesuslopez@fciencias.unam.mx',
        'blog': 'https://haanslopez.com',
        'author': 'Haans Lopez',
        'socialMedia':
        {
            'facebookUser': 'HaansLopez.94',
            'instagramUser': 'haans_lopez',
            'xUser': 'HaansiLopez',
            'linkedin': 'in/haansilopez94',
            'githubUser': 'JesusHaans'
        }
    }
    return jsonify(persona)

if(__name__ == '__main__'):
    app.run(port=5000)
    