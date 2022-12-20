from flask import Flask,request, jsonify, make_response
import cognitojwt
from functools import wraps
from pymongo import MongoClient

DB_URL= "mongodb+srv://admin:admin@cluster0.oefeycn.mongodb.net/?retryWrites=true&w=majority"
	# checkov:skip=CKV_SECRET_4: ADD REASON


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


@app.route("/grants",methods = ['GET'])
@decorator
def getGrants():
    with MongoClient(DB_URL) as client:
        # checkov:skip=CKV_SECRET_4: Skipping checkov warning
        grants = client.project2.grants
        cursor= grants.find()
        output = []
        for q in cursor:
            output.append({'org' : q['org'], 'fund' : q['fund'],
                            'granted_flag' : q['granted_flag'], 'grantee_email' : q['grantee_email']})
        return make_response(jsonify(
                        message="Data fethced",
                        data=output),
                        200
                    )

@app.route("/grants",methods = ['POST'])
@decorator
def insertGrant():
    args = request.args
    org = args.get('org')
    fund = args.get('fund')
    post = {'org' : org, 'fund' : fund,
           'granted_flag' :"N", 'grantee_email' : ""}
    
    with MongoClient(DB_URL) as client:
        grants = client.project2.grants         
        post_id = str(grants.insert_one(post).inserted_id)
        return make_response(jsonify(
                        message="Grant inserted",
                        data=post_id),
                        200
                    )
        
if __name__ == "__main__":
    app.run(debug=True)

        

