from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError

class ProjectTask(models.Model):
    _inherit = 'project.task'

    #Genera la marca de tarea por defecto
    is_default_task = fields.Boolean(string="Tarea por defecto", default=False)

    #Crea la relación entre la tarea y las cotizaciones y ordenes de producción
    sale_order_id = fields.Many2one('sale.order', string="Cotización")
    manufacturing_order_id = fields.Many2one('mrp.production', string="Orden de Producción")


    #A futuro hay que corregir esta tarea para que no permita crear algo que no sea una cotización
    # @api.model_create_multi
    # def create(self, vals):
    #     task = super().create(vals)
    #     if task.name in ['Cotizar', 'Fabricación', 'Entrega']:
    #         task.is_default_task = True
    #     return task

    def write(self, vals):
        for task in self:
            if task.is_default_task and any(field in vals for field in ['name', 'project_id']):
                raise exceptions.UserError("No puedes modificar una tarea predefinida.")
        return super().write(vals)

    #Hay que revisar a futuro esta función para eliminar productos que no se vayan a fabricar
    # def unlink(self):
    #     for task in self:
    #         if task.is_default_task:
    #             raise exceptions.UserError("No puedes eliminar una tarea predefinida.")
    #     return super().unlink()


    def open_related_document(self):
        """ Abre la cotización o la orden de producción asociada a la tarea, si existe. 
            - Si la tarea está en la etapa 'Cotización' y tiene una cotización asignada → Abre la cotización.  
            - Si la tarea está en 'Cotización' pero no tiene cotización → Abre la pantalla de nueva cotización.  
            - Si la tarea tiene una orden de producción asignada → Abre la orden de producción.  
            - Si no tiene ninguna de las anteriores → Muestra un mensaje.  
        """
        self.ensure_one()

        # Obtener el nombre del stage en el que está la tarea
        stage_name = self.stage_id.name.lower()
        if stage_name == "cotizar":
            if self.sale_order_id:
                return {
                    'name': "Cotización",
                    'type': 'ir.actions.act_window',
                    'res_model': 'sale.order',
                    'view_mode': 'form',
                    'res_id': self.sale_order_id.id,
                    'target': 'new',
                    'force_context': True
                }
            else:
                return {
                    'name': "Crear Cotización",
                    'type': 'ir.actions.act_window',
                    'res_model': 'sale.order',
                    'view_mode': 'form',
                    'context': {
                        'default_partner_id': self.partner_id.id, 
                        'default_project_id': self.project_id.id, 
                        'default_task_id': self.id,
                        'target': 'new',
                        'force_context': True
                    },
                }

        elif stage_name == "por fabricar":
            return {
                'name': "Orden de Producción",
                'type': 'ir.actions.act_window',
                'res_model': 'mrp.production',
                'view_mode': 'form',
                'res_id': self.manufacturing_order_id.id,
                'target': 'new',
                'force_context': True
            }

        else:
            raise UserError("No hay documentos asociados a esta tarea.")
