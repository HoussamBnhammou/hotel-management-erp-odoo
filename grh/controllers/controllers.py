# -*- coding: utf-8 -*-
# from odoo import http


# class Grh(http.Controller):
#     @http.route('/grh/grh', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/grh/grh/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('grh.listing', {
#             'root': '/grh/grh',
#             'objects': http.request.env['grh.grh'].search([]),
#         })

#     @http.route('/grh/grh/objects/<model("grh.grh"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('grh.object', {
#             'object': obj
#         })
