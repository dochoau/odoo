from odoo import models, fields, api, exceptions
import logging


logger = logging.getLogger(__name__)

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
                    val["project_id"] = task.project_id.id
                    project = self.env["project.project"].browse(vals["project_id"])
                    val["project_id"] = project.id
                    val["status"] = True

            sale_orders = super(SaleOrder, self).create(vals)  # Crear cotizaciones
            
            for order in sale_orders:
                if order.task_id:
                    order.task_id.sale_order_id = order.id  # Asignar la cotización a la tarea

            return sale_orders

        
    def action_create_production_orders(self):
        """ Crea órdenes de producción y tareas en el proyecto asignado """
        if self.state == 'draft':
            raise exceptions.UserError(("Primero Confirma la Cotización"))
        stage = self.env["project.task.type"].search([("name", "=", "Por Fabricar")], limit=1)

        if not stage:
            raise ValueError("No existe la etapa 'Por Fabricar' en proyectos.")

        for line in self.order_line:
            if not line.product_id:
                continue

            # Crear la orden de producción
            production_order = self.env["mrp.production"].create({
                "product_id": line.product_id.id,
                "product_qty": line.product_uom_qty,
                "sale_order_id": self.id,
            })

            # Crear la tarea en el proyecto asociado
            if self.project_id:
                self.env["project.task"].create({
                    "name": f"Fabricar {line.product_id.display_name}",
                    "project_id": self.project_id.id,
                    "stage_id": stage.id,
                    "description": f"Orden de producción creada: {production_order.name}",
                    "manufacturing_order_id" : production_order.id
                }, cond = False)
