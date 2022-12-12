# from flask import Flask
from flask import Flask,request, jsonify, make_response
import cognitojwt
from functools import wraps


app = Flask(__name__)

def decorator(takes_a_function):
    @wraps(takes_a_function)
    def wrapper(*args, **kwargs):
        try:
            cognitojwt.decode(
            request.headers.get('Authorization').split()[1],
            'us-east-1',
            'us-east-1_p7haSaF9Z',
            )
        except Exception as e:
            return make_response(jsonify(message="Unauthorized request. Client does not have access to the content."), 403)
        return takes_a_function(*args, **kwargs)
    return wrapper


@app.route("/")
@decorator
def home():
    data={"List of users":[{"user1":"Ankhush","User2":"Ganesh"}]}
    return make_response(jsonify(
                    message="Valid token and Verified",
                    data=data),
                    200
                )

