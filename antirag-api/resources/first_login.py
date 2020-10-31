from flask_restful import Resource, reqparse
from db import connectToHost, query
import base64
import pymysql
from flask_jwt_extended import jwt_required



class FirstLogin(Resource):
    #@jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('roll', type=str, required=True, help="roll cannot be left blank!")
        parser.add_argument('phone', type=str, required=True, help="phone cannot be left blank!")
        parser.add_argument('pphone', type=str, required=True, help="pphone cannot be left blank!")
        parser.add_argument('address', type=str, required=True, help="address cannot be left blank!")
        parser.add_argument('pword', type=str, required=True, help="pword cannot be left blank!")
        data = parser.parse_args()

        qstr = f"""update Student
        set phone = '{ data['phone'] }' , 
        pphone = '{ data['pphone'] }' , 
        address = '{ data['address'] }' , 
        pword = '{ data['pword'] }'
        where roll = '{ data['roll'] }' ;"""

        try:
            query(qstr)
        except Exception as e:
            return {
                "message" : "Cannot add the details."
            }, 500
        
        return {
            "message" : "Succesfully added details."
        }, 200