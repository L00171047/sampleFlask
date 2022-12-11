# from flask import Flask
from flask import Flask,request, jsonify
import cognitojwt
from functools import wraps


app = Flask(__name__)

def decorator(takes_a_function):
    @wraps(takes_a_function)
    def wrapper(*args, **kwargs):
        print("inside decorator")
        try:
            verified_claims: dict = cognitojwt.decode(
            request.args.get('token'),
            'us-east-1',
            'us-east-1_o31OP0xMK',
            )
        except Exception as e:
                return jsonify(
                    message="Unauthorized request. Client does not have access to the content.",
                    # category="error",
                    status=403
                    )
        return takes_a_function(*args, **kwargs)
    return wrapper


@app.route("/")
@decorator
def home():
    # return "Hello, Flask!"
    data={"List of users":[{"user1":"Ankhush","User2":"Ganesh"}]}
    return jsonify(
                    message="Valid token and Verified",
                    # category="error",
                    status=200,
                    data=data
                )

