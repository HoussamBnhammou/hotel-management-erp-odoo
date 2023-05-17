from odoo import models, fields



class Employee(models.Model):
    _name = "employee"
    _inherit = 'prof.zaouia.employee'






class Room(models.Model):
    _name = "room"

    room_number = fields.Integer("room_number")
    room_type = fields.Char("room_type")
    room_status = fields.Char("room_status")
    availability = fields.Boolean("availability")
    price_per_night = fields.Float("Price per night")
    roombooking_id = fields.Many2one("roombooking", string="reservation")
    state = fields.Selection([('draft', 'Draft'), ('recruited', 'Recruited'), ('cancelled', 'Cancelled')],
                             default='draft')

    def cancel_button(self):
        self.write({'state': 'cancelled'})

    def recruit_button(self):
        self.write({'state': 'recruited'})

    def draft_button(self):
        self.write({'state': 'draft'})


class Guest(models.Model):
    _name = "guest"
    name = fields.Char("name")
    adress = fields.Char("Adress")
    phone = fields.Char("Phone")
    email = fields.Char("email")


class RoomBooking(models.Model):
    _name = "roombooking"
    booking_id = fields.Integer("booking_ID")
    checkInDate = fields.Date("check_in")
    checkoutDate = fields.Date("check_out")
    payement_status = fields.Boolean("payement_status")
    totale_amount = fields.Float("total")
    rooms = fields.One2many("room", "roombooking_id", string="rooms")
    client_id = fields.Many2one("client", string="client")
    responsables = fields.Many2many(comodel_name = "prof.zaouia.employee", inverse_name = "reservation_id", String="responsables")

    state = fields.Selection([('draft', 'Draft'), ('recruited', 'Recruited'), ('cancelled', 'Cancelled')],
                             default='draft')

    def cancel_button(self):
        self.write({'state': 'cancelled'})

    def recruit_button(self):
        self.write({'state': 'recruited'})

    def draft_button(self):
        self.write({'state': 'draft'})


class PaymentDetails(models.Model):
    _name = "paymentdetails"
    payement_id = fields.Integer("payement_ID")
    payement_Date = fields.Date("payement_date")
    checkout_amount = fields.Date("amount")
    patement_method = fields.Char("payement_method")
    state = fields.Selection([('draft', 'Draft'), ('recruited', 'Recruited'), ('cancelled', 'Cancelled')],
                             default='draft')

    def cancel_button(self):
        self.write({'state': 'cancelled'})

    def recruit_button(self):
        self.write({'state': 'recruited'})

    def draft_button(self):
        self.write({'state': 'draft'})


class Client(models.Model):
    _name = "client"
    name = fields.Char("name")
    adress = fields.Char("Adress")
    phone = fields.Char("Phone")
    email = fields.Char("email")
    roombooking = fields.Many2one("roombooking", "client_id", String="reservation")

    state = fields.Selection([('draft', 'Draft'), ('recruited', 'Recruited'), ('cancelled', 'Cancelled')],
                             default='draft')

    def cancel_button(self):
        self.write({'state': 'cancelled'})

    def recruit_button(self):
        self.write({'state': 'recruited'})

    def draft_button(self):
        self.write({'state': 'draft'})
