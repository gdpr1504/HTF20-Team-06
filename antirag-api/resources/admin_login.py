from flask_restful import Resource, reqparse
from db import query
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import safe_str_cmp

class Admin():
    def __init__(self,aid,pword):
        self.aid=aid
        self.pword=pword

    @classmethod
    def getAdminByAid(cls,aid):
        result=query(f"""SELECT aid,pword FROM Admin WHERE aid='{aid}'""",return_json=False)
        if len(result)>0: return Admin(result[0]['aid'],result[0]['pword'])
        return None


class AdminLogin(Resource):
    
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('aid', type=str, help="aid cannot be left blank!")
        parser.add_argument('pword', type=str, help="pword cannot be left blank!")
        
        data = parser.parse_args()

        #create query string
        qstr = f""" 
        select * from Admin
        WHERE aid='{data['aid']}';
        """
        try:
            return query(qstr)
        except Exception as e:
            return {
                "message" : "There was an error connecting to the database while retrieving." + str(e)
            }, 500

class AdminLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('aid', type=str, required=True,
                            help="aid cannot be left blank!")
        parser.add_argument('pword', type=str, required=True,
                            help="pword cannot be left blank!")
        data=parser.parse_args()
        admin=Admin.getAdminByAid(data['aid'])
        if admin and safe_str_cmp(admin.pword,data['pword']):
            access_token=create_access_token(identity=admin.aid,expires_delta=False)
            return {'aid': data['aid'], 'access_token':access_token, 'admin': 1},200
        return {"message":"Invalid Credentials!"}, 401
