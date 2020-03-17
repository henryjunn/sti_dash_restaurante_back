from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from flask_cors import CORS
import datetime
import json
import os

app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Cupom(db.Model):
    idCupom = Column(Integer, primary_key=True)
    nomeCupom = db.Column(db.String(50), unique=False)
    descricao = db.Column(db.String(500), unique=False)
    quantidade = db.Column(db.String(50), unique=False)
    desconto = db.Column(db.String(3), unique=False)
    validade = db.Column(db.String(50), unique=False)#(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, nomeCupom, descricao, quantidade, desconto, validade):
        self.nomeCupom = nomeCupom
        self.descricao = descricao
        self.quantidade = quantidade
        self.desconto = desconto
        self.validade = validade
    
    def toDict(self):
        response = {
            "idCupom": self.idCupom,
            "nomeCupom": self.nomeCupom,
            "descricao": self.descricao,
            "quantidade": self.quantidade,
            "desconto": self.desconto,
            "validade": self.validade
        }
        return response

class CupomSchema(ma.Schema):
   class Meta:
       # Fields to expose
       fields = ('nomeCupom', 'descricao', 'quantidade', 'desconto', 'validade')
       
cupom_schema = CupomSchema()
cupoms_schema = CupomSchema(many=True)
################################################## R O U T E S ##################################################

# endpoint to create new line
@app.route("/cupom", methods=["POST"])
def add_cupom():
    nomeCupom = request.json['nomeCupom']
    descricao = request.json['descricao']
    quantidade = request.json['quantidade']
    desconto = request.json['desconto']
    validade = request.json['validade']
    new_cupom = User(nomeCupom, descricao, quantidade, desconto, validade)
    db.session.add(new_cupom)
    db.session.commit()

    #result = cupom_schema.dump(new_cupom).data  
    #return jsonify(result)

    #return jsonify(new_cupom)
    #return cupom_schema.jsonify(new_cupom)

    response = new_cupom.to_dict()
    print(response)
    return response
# endpoint to show all lines
@app.route("/cupom", methods=["GET"])
def get_cupom():
    all_cupons = Cupom.query.all()
    dict_result = {}
    for entry in all_cupons:
        user_dict = entry.to_dict()
        dict_result[user_dict['id']] = user_dict
    return json.loads(json.dumps(dict_result))
    #result = cupoms_schema.dump(all_cupons)
    #return jsonify(result.data)
# endpoint to get line detail by id
@app.route("/cupom/<id>", methods=["GET"])
def cupom_detail(id):
    cupom = Cupom.query.get(id)
    response = cupom.to_dict()
    return response
    #return cupom_schema.jsonify(cupom)
# endpoint to update line
@app.route("/cupom/<id>", methods=["PUT"])
def cupom_update(id):
    cupom = Cupom.query.get(id)
    if 'nomeCupom' in request.json.keys():
        cupom.nomeCupom = request.json['nomeCupom'] 
    if 'descricao' in request.json.keys():
        cupom.descricao = request.json['descricao']
    if 'quantidade' in request.json.keys():
        cupom.quantidade = request.json['quantidade']
    if 'desconto' in request.json.keys():
        cupom.desconto = request.json['desconto']
    if 'validade' in request.json.keys():
        cupom.validade = request.json['validade']
    db.session.commit()
    return cupom_schema.jsonify(cupom)
# endpoint to delete line
@app.route("/cupom/<id>", methods=["DELETE"])
def user_delete(id):
    cupom = Cupom.query.get(id)
    db.session.delete(cupom)
    db.session.commit()
    return cupom_schema.jsonify(cupom)
############################################################################################################
if __name__ == '__main__':
    app.run(debug=True)