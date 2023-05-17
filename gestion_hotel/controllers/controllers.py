# -*- coding: utf-8 -*-
# from odoo import http


# class GestionHotel(http.Controller):
#     @http.route('/gestion_hotel/gestion_hotel', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestion_hotel/gestion_hotel/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestion_hotel.listing', {
#             'root': '/gestion_hotel/gestion_hotel',
#             'objects': http.request.env['gestion_hotel.gestion_hotel'].search([]),
#         })

#     @http.route('/gestion_hotel/gestion_hotel/objects/<model("gestion_hotel.gestion_hotel"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestion_hotel.object', {
#             'object': obj
#         })
