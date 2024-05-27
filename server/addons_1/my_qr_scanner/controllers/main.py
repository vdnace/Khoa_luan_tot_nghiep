from odoo import http
from odoo.http import request

class QrScannerController(http.Controller):

    @http.route('/qr_code', type='http', auth='public', website=True)
    def qr_scanner(self, **kwargs):
        return request.render('my_qr_scanner.qr_scan_template')