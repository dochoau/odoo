from odoo import models, fields

class ResUsers(models.Model):
    _inherit = "res.users"

    lang = fields.Selection(default="es_CO")  