# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import datetime
# from openerp.exceptions import AccessError
##############################################################################
#
#    NEW API
#
##############################################################################
from odoo import models, fields, api, _


class Employee(models.Model):
    _name = 'prof.zaouia.employee'

    id = fields.Integer(required=True)
    image = fields.Binary()
    name = fields.Char(string='Nom', required=True)
    prenom = fields.Char(string='Prénom', required=True)
    charge = fields.Integer(string='personnes à charge', required=True)
    situation = fields.Selection([('M', 'M'), ('C', 'C')], default='M')
    nombre_jours = fields.Integer(string='nombre de jours travaillés', default=26)
    periode = fields.Date(string='salaire au', default=fields.Date.today())
    nationality = fields.Many2one(string='Nationalité', comodel_name='prof.zaouia.nationality')
    salaire_brutm = fields.Float(string='Salaire brut mensuel')
    salaire_bdu = fields.Float(string='Salaire brut dû', compute='_compute_salaire_bdu', store=True)
    specializations = fields.Many2one(string='Métier', comodel_name='prof.zaouia.specialization')
    state = fields.Selection([('draft', 'Draft'), ('recruited', 'Recruited'), ('cancelled', 'Cancelled')],
                             default='draft')
    cnss_af = fields.Float(string='cnss allocations familiales', compute='_compute_cnss_af')
    cnss_afp = fields.Float(string='cnss A F', compute='_compute_cnss_afp')
    cnss_amo = fields.Float(string='cnss AMO', compute='_compute_cnss_amo')
    cnss_amop = fields.Float(string='cnss A.M.O', compute='_compute_cnss_amop')
    cimr = fields.Float(string='retraite CIMR', compute='_compute_cimr')
    cimrp = fields.Float(string='retraite C.I.M.R', compute='_compute_cimrp')
    fraispro = fields.Float(string='frais professionnels', compute='_compute_fraispro')
    si = fields.Float(string='salaire imposable', compute='_compute_si')
    ir = fields.Float(string='impôt sur le revenu 0', compute='_compute_ir')
    irr = fields.Float(string='impôt sur le revenu r', compute='_compute_irr', store=True)
    ira = fields.Float(string='impôt sur le revenu a', compute='_compute_ira')
    irp = fields.Float(string='impôt sur le revenu', compute='_compute_irp')
    total_personnes_a_charge = fields.Float(string='total des personnes à charge ', compute='_compute_totalp_acharge')
    total_des_reductions_ir = fields.Float(string='total des reductions IR ', compute='_compute_total_reductions_ir')
    salaire_net = fields.Float(string='Salaire net', compute='_compute_salaire_net')
    reservation_id = fields.Many2many(comodel_name="roombooking", string="responsable for")
    @api.depends('salaire_brutm', 'nombre_jours')
    def _compute_salaire_bdu(self):
        for rec in self:
            rec.salaire_bdu = (rec.salaire_brutm * rec.nombre_jours) / 26

    @api.depends('salaire_brutm')
    def _compute_cnss_af(self):
        for rec in self:
            x = rec.salaire_brutm
            # Calcul du montant CNSS en tenant compte du plafond fixé à6000dh
            if x > 6000:
                rec.cnss_af = 6000 * 0.0448
            else:
                rec.cnss_af = x * 0.0448

    @api.depends('cnss_af', 'nombre_jours')
    def _compute_cnss_afp(self):
        for rec in self:
            rec.cnss_afp = (rec.cnss_af * rec.nombre_jours) / 26

    @api.depends('salaire_brutm')
    def _compute_cnss_amo(self):
        for rec in self:
            rec.cnss_amo = rec.salaire_brutm * 0.02

    @api.depends('cnss_amo', 'nombre_jours')
    def _compute_cnss_amop(self):
        for rec in self:
            rec.cnss_amop = (rec.cnss_amo * rec.nombre_jours) / 26

    @api.depends('salaire_brutm')
    def _compute_cimr(self):
        for rec in self:
            rec.cimr = rec.salaire_brutm * 0.06

    @api.depends('cimr', 'nombre_jours')
    def _compute_cimrp(self):
        for rec in self:
            rec.cimrp = (rec.cimr * rec.nombre_jours) / 26

    def cancel_button(self):
        self.write({'state': 'cancelled'})

    def recruit_button(self):
        self.write({'state': 'recruited'})

    def draft_button(self):
        self.write({'state': 'draft'})

    def m_button(self):
        self.write({'situation': 'M'})

    def c_button(self):
        self.write({'situation': 'C'})

    @api.depends('charge', 'situation')
    def _compute_totalp_acharge(self):
        for rec in self:
            x = rec.charge
            if rec.situation == 'M':
                rec.total_personnes_a_charge = x + 1
            elif rec.situation == 'C':
                rec.total_personnes_a_charge = x

    @api.depends('total_personnes_a_charge')
    def _compute_total_reductions_ir(self):
        for rec in self:
            y = rec.total_personnes_a_charge
            if y >= 6:
                rec.total_des_reductions_ir = 6 * 30
            else:
                rec.total_des_reductions_ir = y * 30

    @api.depends('salaire_brutm')
    def _compute_fraispro(self):
        for rec in self:
            y = rec.salaire_brutm * 0.2  # Calcul des frais professionels=min(salaire brut*0.2,2500)
            if y >= 2500:
                rec.fraispro = 2500
            else:
                rec.fraispro = y

    @api.depends('salaire_brutm', 'cnss_af', 'fraispro', 'cimr', 'cnss_amo')
    def _compute_si(self):
        for rec in self:
            rec.si = rec.salaire_brutm - rec.cnss_af - rec.fraispro - rec.cimr - rec.cnss_amo  # Calcul du salaire Imposable

    @api.depends(
        'si')  # Calcul de l'impot sur revenu,on utilise une liste des tuples pour modéliser les tranches le taux et l'abbatement correpsendant
    def _compute_ir(self):
        for rec in self:
            mygrid = [(0.0, 2500.0, 0.0, 0.0), (2500.01, 4166.67, 0.1, 250.0), (4166.68, 5000.0, 0.2, 666.67),
                      (5000.01, 6666.67, 0.3, 1166.67), (6666.68, 15000.0, 0.34, 1433.33)]
            if rec.si >= 15000.01:  # on vérifie si le salaire imposable est supérieur à la valeur 15000
                rec.ir = rec.si * 0.38 - 2033.33
            else:
                for i in mygrid:
                    if i[0] <= rec.si <= i[
                        1]:  # on vérifie si le salaire imposable est entre les bornes du tranche et on applique le taux et l'abbatement correspendant
                        rec.ir = rec.si * i[2] - i[3]

    @api.depends('ir', 'total_personnes_a_charge')
    def _compute_irr(self):
        for rec in self:
            rec.irr = rec.ir - rec.total_des_reductions_ir

    @api.depends('irr')
    def _compute_ira(self):
        for rec in self:
            z = rec.irr  # impôt sur le revenu >= à zéro
            if z > 0:
                rec.ira = rec.irr
            else:
                rec.ira = 0

    @api.depends('ira', 'nombre_jours')
    def _compute_irp(self):
        for rec in self:
            rec.irp = (rec.ira * rec.nombre_jours) / 26

    @api.depends('salaire_bdu', 'cnss_afp', 'cnss_amop', 'cimrp', 'irp')
    def _compute_salaire_net(self):
        for rec in self:
            rec.salaire_net = rec.salaire_bdu - rec.cnss_afp - rec.cnss_amop - rec.cimrp - rec.irp


class Nationality(models.Model):
    _name = 'prof.zaouia.nationality'

    name = fields.Char(string='Title', required=True,
                       help="This is your Nationality not the where you are living!")


class Specialization(models.Model):
    _name = 'prof.zaouia.specialization'

    name = fields.Char(string='Nom de la spécialisation', required=True)
