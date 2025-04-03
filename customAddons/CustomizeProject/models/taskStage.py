from odoo import models, exceptions

class ProjectTaskStage(models.Model):
    _inherit = 'project.task.type'  # Modelo correcto en Odoo 18


    # def write(self, vals):
    #     if 'name' in vals:
    #         raise exceptions.UserError(('Acción Inválida'))
    #     if 'sequence' in vals:
    #         raise exceptions.UserError(("Acción Inválida"))
    #     return super().write(vals)


    def unlink(self):
        """Bloquea la eliminación de cualquier stage"""
        raise exceptions.UserError(("No puedes eliminar las etapas."))