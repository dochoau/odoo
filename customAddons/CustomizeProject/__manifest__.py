{
    'name': "Customize Project",
    'version': '1.0',
    'summary': "Modifica los proyectos y las cotizaciones",
    'category': 'Project',
    'author': "David Ochoa",
    'depends': ['project', 'sale'],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/project_views.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': True
}