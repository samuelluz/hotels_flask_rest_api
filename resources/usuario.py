from flask_restful import Resource, reqparse
from models.usuario import UserModel

class User(Resource):

    def get(self, user_id):
        user = UserModel.fing_user(user_id)
        if user:
            return user.json(), 200
        return {'message':'User not found.'}, 404 #not found

    def delete(self, user_id):
        user = UserModel.fing_user(user_id)
        if user:
            try:
                user.delete_hotel()
            except:
                return {'message':'An error ocurred trying to delete user.'}, 500
            return {'message': 'User deleted.'}
        return {'message':'User not found.'}, 404