from odoo import models, fields, api, exceptions

class ProjectTask(models.Model):
    _inherit = 'project.task'

    is_default_task = fields.Boolean(string="Tarea por defecto", default=False)

    @api.model_create_multi
    def create(self, vals):
        task = super().create(vals)
        if task.name in ['Cotizar', 'Fabricación', 'Entrega']:
            task.is_default_task = True
        return task

    def write(self, vals):
        for task in self:
            if task.is_default_task and any(field in vals for field in ['name', 'project_id']):
                raise exceptions.UserError("No puedes modificar una tarea predefinida.")
        return super().write(vals)

    # def unlink(self):
    #     for task in self:
    #         if task.is_default_task:
    #             raise exceptions.UserError("No puedes eliminar una tarea predefinida.")
    #     return super().unlink()
