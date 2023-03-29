from flask import Flask, request, jsonify
import json
import random
# import os

from data import db_session
from data.sessions import Sessions


app = Flask(__name__)


@app.route("/update/<int:id>", methods=["POST", "GET"])
def update(id):
    data = request.json
    db_sess = db_session.create_session()
    session = db_sess.query(Sessions).filter(Sessions.id == id).first()
    session.state = data["state"]
    db_sess.commit()
    response = {
        "id": session.id,
        "state": session.state,
    }
    return jsonify(response)


@app.route("/get/<int:id>", methods=["POST", "GET"])
def get(id) -> json:
    db_sess = db_session.create_session()
    session = db_sess.query(Sessions).filter(Sessions.id == id).first()
    response = {
        "id": id,
        "state": session.state,
    }
    return jsonify(response)



@app.route("/start", methods=["POST", "GET"])
def start() -> json:
    db_sess = db_session.create_session()
    session = Sessions()
    session.state = ''
    db_sess.add(session)
    db_sess.commit()
    response = {
        "id": session.id,
        "state": session.state,
    }
    return jsonify(response)


def main():
    db_session.global_init("server.db")
    app.run()


if __name__ == '__main__':
    main()
