from odoo import models, fields, api

class MrpProduction(models.Model):
    _inherit = "mrp.production"

    sale_order_id = fields.Many2one("sale.order", string="Cotización Relacionada")