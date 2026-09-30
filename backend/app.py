from flask import Flask, request
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import jwt
import psycopg2

load_dotenv()
CHAVE = os.getenv("SECRET_KEY")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

def get_db_connection():
    return psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)

app = Flask(__name__)
user_test = {"username": "john", "password": "87654321"}

@app.route("/login", methods=["POST"])
def login():
    dados = request.get_json()
    if dados.get("username") == user_test["username"] and dados.get("password") == user_test["password"]:
        payload = {"username":dados.get("username"),"exp":datetime.now()+timedelta(hours=20)}
        token = jwt.encode(payload, CHAVE, algorithm="HS256")
        return token
    else:
        return "Usuário e/ou senha incorretos", 401

@app.route("/dashboard", methods=["GET"])
def dashboard():
    header = request.headers.get("Authorization")
    if header is None:
        return "Deu errado!", 401
    else:
        token = header.split(" ")[1]
        try:
            cracha = jwt.decode(token, CHAVE, algorithms=["HS256"])
            return cracha

        except jwt.ExpiredSignatureError:
            return "Tempo expirado! Faça login novamente.", 401
        
        except jwt.InvalidTokenError:            
            return "Houve um erro. . .", 401

if __name__ == "__main__":
    app.run(debug = True)