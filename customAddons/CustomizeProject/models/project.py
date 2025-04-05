from odoo import models, fields, api

class ProjectProject(models.Model):
    _inherit = 'project.project'

    #Relaciona el proyecto con las ordenes de producción
    quotation_ids = fields.One2many('sale.order', 'project_id', string="Cotizaciones")
    
    #Relaciona el proyecto coon los clientes
    partner_id = fields.Many2one(
        'res.partner',  # Relación con la tabla de clientes
        string="Cliente",
        required=True,  # Opcional: si quieres que siempre se seleccione un cliente
        help="Cliente asociado a este proyecto."
    )

    #Sobre escribe el método Create
    def create(self, vals_list):
        """Sobrescribe create para agregar las etapas en un orden específico."""
        stage_model = self.env['project.task.type']
        
        # Definir las etapas necesarias con su secuencia
        stage_names = ['Cotizar', 'Por Fabricar', 'Fabricando', 'Terminado', 'Instalación', 'Entregado']
        stages = {}

        # Buscar o crear las etapas en el orden correcto
        for index, stage_name in enumerate(stage_names):
            stage = stage_model.search([('name', '=', stage_name)], limit=1)
            if not stage:
                stage = stage_model.create({
                    'name': stage_name,
                    'sequence': index  # Asegurar que se mantenga el orden correcto
                })
            else:
                # Si ya existe, aseguramos que la secuencia sea la correcta
                stage.write({'sequence': index}, cond = False)
            stages[stage_name] = stage

        # Crear los proyectos normalmente
        projects = super().create(vals_list)

        for project in projects:
            # Asociar las etapas al proyecto
            for stage in stages.values():
                stage.write({'project_ids': [(4, project.id)]}, cond = False)

            # Crear la tarea "Cotizar" en la etapa "Cotizar"
            self.env['project.task'].create({
                'name': 'Cotizar',
                'project_id': project.id,
                'stage_id': stages['Cotizar'].id  # Asignar a la etapa "Cotizar"
            }, cond = False)

        return projects
