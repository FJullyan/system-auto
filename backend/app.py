from flask import Flask, request
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import jwt

load_dotenv()
chave = os.getenv("SECRET_KEY")
app = Flask(__name__)
user_test = {"username": "john", "password": "87654321"}

@app.route("/login", methods=["POST"])
def teste():
    dados = request.get_json()
    if dados.get("username") == user_test["username"] and dados.get("password") == user_test["password"]:
        payload = {"username":dados.get("username"),"exp":datetime.now()+timedelta(hours=20)}
        token = jwt.encode(payload, chave, algorithm="HS256")
        return token
    else:
        return "Usuário e/ou senha incorretos", 401


if __name__ == "__main__":
    app.run(debug = True)