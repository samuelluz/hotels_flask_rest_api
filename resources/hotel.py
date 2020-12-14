from flask_restful import Resource, reqparse
from models.hotel import HotelModel

hoteis = [
    {
    'hotel_id':'alpha',
    'nome':'Alpha Hotel',
    'estrelas':4.3,
    'diaria':420.34,
    'cidade':'Rio de Janeiro'
    },
    {
    'hotel_id':'bravo',
    'nome':'Bravo Hotel',
    'estrelas':4.4,
    'diaria':380.90,
    'cidade':'Santa Catarina'
    },
    {
    'hotel_id':'charlie',
    'nome':'Charlie Hotel',
    'estrelas':3.9,
    'diaria':320.20,
    'cidade':'Santa Catarina'
    }
]

class Hoteis(Resource):
    def get(self):
        return {'hoteis': hoteis}

class Hotel(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('nome')
    atributos.add_argument('estrelas')
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
        hotel.save_hotel()
        return hotel.json(),


    def put(self, hotel_id):
        dados = self.atributos.parse_args()
        hotel_encontrado = HotelModel.fing_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200
        novo_hotel = HotelModel(hotel_id, **dados)
        novo_hotel.save_hotel()
        return novo_hotel.json(), 201 # criated

    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            hotel.delete_hotel()
            return {'message': 'Hotel deleted.'}
        return {'message':'Hotel not found.'}, 404