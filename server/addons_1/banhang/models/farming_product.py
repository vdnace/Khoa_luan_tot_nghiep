from odoo import api, fields, models, _
try:
    import qrcode
except ImportError:
    qrcode = None
try:
    import base64
except ImportError:
    base64 = None
from io import BytesIO
from odoo.exceptions import UserError, ValidationError
class Farmingproduct(models.Model):
    _name = "product.template"
    _inherit = "product.template"
    _description = "Extend product model"
    
    qr_code = fields.Binary('QR Code', attachment=True, compute="_generate_qr")
    listtieuchuan = [
        ('VietGAP', 'VietGAP [Vietnamese Good Agricultural Practices]'),
        ('GlobalGAP', 'GlobalGAP [Global Good Agricultural Practices]'),
        ('VCO', 'VCO [Vietnam Certified Organic]'),
        ('PGS', 'PGS [VParticipatory Guarantee System]'),
    ]
    tieuchuan = fields.Selection(listtieuchuan, string = 'Tiêu chuẩn')
    ncc = fields.Many2one("res.partner", string = "Nhà cung cấp")
    expiration_time = fields.Integer(string='Ngày hết hạn',
        help='Số ngày sau khi sản xuất sản phẩm (từ nhà cung cấp ' 
        'hoặc trong kho sau khi sản xuất) sau đó hàng hóa có thể trở nên nguy hiểm' 
        'và không được tiêu thụ. Nó sẽ được tính trên lô / số sê-ri.')
    tracking = fields.Selection([
        ('serial', 'By Unique Serial Number'),
        ('lot', 'By Lots'),
        ('none', 'No Tracking')],
        string="Tracking", required=True, default='lot', # Not having a default value here causes issues when migrating.
        compute='_compute_tracking', store=True, readonly=False, precompute=True,
        help="Ensure the traceability of a storable product in your warehouse.")
    @api.depends('name', 'list_price', 'qty_available', 'ncc.name', 'tieuchuan')
    def _generate_qr(self):
       "method to generate QR code"
       for rec in self:
           if qrcode and base64:
               qr = qrcode.QRCode(
                   version=1,
                   error_correction=qrcode.constants.ERROR_CORRECT_L,
                   box_size=3,
                   border=4,
               )
               tieuchuan_display = dict(self.fields_get(allfields=['tieuchuan'])['tieuchuan']['selection']).get(rec.tieuchuan, '')
               data = f"Sản phẩm : {rec.name}\ngiá : {rec.list_price} VNĐ\nNhà cung cấp: {rec.ncc.name}\nTiêu chuẩn : {tieuchuan_display}\nHạn sử dụng : {rec.expiration_time} ngày"
               qr.add_data(data)
               qr.make(fit=True)
               img = qr.make_image()
               temp = BytesIO()
               img.save(temp, format="PNG")
               qr_image = base64.b64encode(temp.getvalue())
               rec.update({'qr_code':qr_image})
           else:
               raise UserError(_('Necessary Requirements To Run This Operation Is Not Satisfied'))