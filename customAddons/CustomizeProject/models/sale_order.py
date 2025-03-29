from odoo import models, fields, api
import logging



class SaleOrder(models.Model):
    _inherit = 'sale.order'

    project_id = fields.Many2one('project.project', string="Proyecto")
    task_id = fields.Many2one('project.task', string="Tarea Relacionada")

    @api.model_create_multi
    def create(self, vals):
        if isinstance(vals, list):  # Si recibe una lista (varias cotizaciones)
            for val in vals:
                if val.get("task_id"):
                    task = self.env["project.task"].browse(val["task_id"])
                    val["partner_id"] = task.partner_id.id  # Asignar cliente de la tarea
                    val["task_id"] = task.id  # Asegurar que task_id se asigne en la cotización

            sale_orders = super(SaleOrder, self).create(vals)  # Crear cotizaciones
            
            for order in sale_orders:
                if order.task_id:
                    order.task_id.sale_order_id = order.id  # Asignar la cotización a la tarea

            return sale_orders

        else:  # Si solo se crea una única cotización
            if vals.get("task_id"):
                task = self.env["project.task"].browse(vals["task_id"])
                vals["partner_id"] = task.partner_id.id  # Asignar cliente de la tarea
                vals["task_id"] = task.id  # Asignar task_id a la cotización

            sale_order = super(SaleOrder, self).create(vals)  # Crear cotización

            if sale_order.task_id:
                sale_order.task_id.sale_order_id = sale_order.id  # Asignar la cotización a la tarea


            return sale_order