{
    "name": "CustomizeSaleOrder",
    "version": "1.0",
    "depends": ["sale", "mrp", "project","CustomizeMRP"],
    'license': 'LGPL-3',
    'author': "David Ochoa",
    "data": [
        'reports/report_sale_order_custom_pdf.xml',
        'reports/custom_sale_order_buttons.xml',
        "views/cotizacion_view.xml",
     ],
    "installable": True,
    "auto_install": False,
}