from odoo import models, fields

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    custom_description = fields.Text(
        string="Descripción del producto",
        help="Descripción personalizada para esta línea de producto."
    )