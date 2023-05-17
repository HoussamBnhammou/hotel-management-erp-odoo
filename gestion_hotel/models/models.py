# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class gestion_hotel(models.Model):
#     _name = 'gestion_hotel.gestion_hotel'
#     _description = 'gestion_hotel.gestion_hotel'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
