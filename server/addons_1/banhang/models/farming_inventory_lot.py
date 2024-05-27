from odoo import api, fields, models, _
import datetime
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

class FarmingLot(models.Model):
    _name = 'stock.lot'
    _inherit = 'stock.lot'

    qr_code = fields.Binary('QR Code tại kho', attachment=True, compute="_generate_qr")
    qr_code_shop = fields.Binary('QR Code tại cửa hàng', attachment=True, compute="_generate_qr_shop")
    
    ngaysx = fields.Date(string="Ngày sản xuất", required=True)
    expiration_date = fields.Datetime(
        string='Ngày hết hạn', compute='_compute_expiration_date', store=True, readonly=False,
        help='Đây là ngày mà hàng hóa có Số sê-ri này có thể trở nên nguy hiểm và không được tiêu thụ.')

    @api.depends('ngaysx', 'product_qty', 'location_id', 'use_date')
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
                data = (
                    f"Lot: {rec.name}\n"
                    f"Sản phẩm: {rec.product_id.name}\n"
                    f"Số lượng: {rec.product_qty} {rec.product_uom_id.name}\n"
                    f"Ngày sản xuất: {rec.ngaysx}\n"
                    f"Ngày hết hạn: {rec.expiration_date}\n"
                    f"Vị trí: {rec.location_id.complete_name}\n"
                )
                qr.add_data(data)
                qr.make(fit=True)
                img = qr.make_image()
                temp = BytesIO()
                img.save(temp, format="PNG")
                qr_image = base64.b64encode(temp.getvalue())
                rec.update({'qr_code': qr_image})
            else:
                raise UserError(_('Necessary requirements to run this operation are not satisfied'))
    @api.depends('ngaysx', 'product_qty', 'location_id', 'use_date')
    def _generate_qr_shop(self):
        "method to generate QR code"
        for rec in self:
            if qrcode and base64:
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=3,
                    border=4,
                )
                tieuchuan_display = dict(self.env['product.template'].fields_get(allfields=['tieuchuan'])['tieuchuan']['selection']).get(rec.product_id.tieuchuan, '')
                data = (
                    f"Sản phẩm: {rec.product_id.name}\n"
                    f"giá: {rec.product_id.list_price} VNĐ / {rec.product_uom_id.name}\n"
                    f"Ngày sản xuất: {rec.ngaysx}\n"
                    f"Ngày hết hạn: {rec.expiration_date}\n"
                    f"Nhà cung cấp: {rec.product_id.ncc.name}\n"
                    f"Tiêu chuẩn : {tieuchuan_display}\n"
                    
                )
                qr.add_data(data)
                qr.make(fit=True)
                img = qr.make_image()
                temp = BytesIO()
                img.save(temp, format="PNG")
                qr_image = base64.b64encode(temp.getvalue())
                rec.update({'qr_code_shop': qr_image})
            else:
                raise UserError(_('Necessary requirements to run this operation are not satisfied'))
    @api.depends('product_id', 'ngaysx')
    def _compute_expiration_date(self):
        self.expiration_date = False
        for lot in self:
            if lot.product_id.use_expiration_date and not lot.expiration_date:
                duration = lot.product_id.product_tmpl_id.expiration_time
                lot.expiration_date = lot.ngaysx + datetime.timedelta(days=duration)