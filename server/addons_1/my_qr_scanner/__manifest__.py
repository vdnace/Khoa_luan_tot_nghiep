{
    'name': 'QR Code Scanner',
    'version': '1.0',
    'summary': 'A module to add QR code scanning functionality to Odoo website',
    'description': 'This module adds a QR code scanner to the Odoo website',
    'author': 'Nhat',
    'depends': ['website', 'website_sale'],
    'data': [
        'views/qr_scanner_template.xml',
        'views/templates.xml'
    ],
    'installable': True,
    'application': True,
}