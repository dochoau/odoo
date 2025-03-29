{
    'name': "Customize Project",
    'version': '1.0',
    'summary': "Modifica los proyectos y las cotizaciones",
    'category': 'Project',
    'author': "David Ochoa",
    'depends': ['project', 'sale','mrp'],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/project_views.xml',
        'views/kanban_view.xml',
         'views/cotizacion_view.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': True
}