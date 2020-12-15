from flask_restful import Resource, reqparse
from models.hotel import HotelModel

class Hoteis(Resource):
    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left blank.")
    atributos.add_argument('estrelas', type=float, required=True, help="The field 'estrelas' cannot be left blank.")
    atributos.add_argument('diaria')
    atributos.add_argument('cidade')

    def get(self, hotel_id):
        hotel = HotelModel.fing_hotel(hotel_id)
        if hotel:
            return hotel.json(), 200
        return {'message':'Hotel not found.'}, 404 #not found

    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {'message':"Hotel id '{}' already exists.".format(hotel_id)}, 400 # bad request
        dados = self.atributos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message':'An internal error ocurred trying to save hotel.'}, 500 # internal server error
        return hotel.json(),


    def put(self, hotel_id):
        dados = self.atributos.parse_args()
        hotel_encontrado = HotelModel.fing_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            try:
                hotel_encontrado.save_hotel()
            except:
                return {'message':'An internal error ocurred trying to save hotel.'}, 500 # internal server error
            return hotel_encontrado.json(), 200
        novo_hotel = HotelModel(hotel_id, **dados)
        novo_hotel.save_hotel()
        return novo_hotel.json(), 201 # criated

    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message':'An error ocurred trying to delete hotel.'}, 500
            return {'message': 'Hotel deleted.'}
        return {'message':'Hotel not found.'}, 404