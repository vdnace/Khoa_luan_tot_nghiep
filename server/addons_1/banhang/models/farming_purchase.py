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
from odoo.exceptions import UserError

class Farmingpurchase(models.Model):
    _name = "purchase.order"
    _inherit = "purchase.order"
    _description = "Extend purchase model"
    qr_code = fields.Binary('QR Code', attachment=True, compute="_generate_qr")
    
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
               text = f"Mã lô hàng: {rec.name}\n"
               text += f"Ngày nhập: {rec.date_order.strftime('%H:%M:%S %d-%m-%Y ')}\n"
               text += f"Nhà cung cấp: {rec.partner_id.name}\n"
               text += "Sản phẩm:\n"
               for line in rec.order_line:
                   text += f" - Tên sản phẩm: {line.product_id.name}\n"
                   text += f"   Ngày sản xuất: {line.ngaysx}\n"
                   text += f"   Số lượng đặt: {line.product_qty}\n"
                   text += f"   Số lượng đã nhận: {line.qty_received}\n"
                   text += f"   Giá: {line.price_unit} VNĐ\n"
                   text += f"   Thành tiền: {line.price_subtotal}\n"
               text += f"\nTổng sau thuế: {rec.amount_total} VNĐ\n"
               qr.add_data(text)
               qr.make(fit=True)
               img = qr.make_image()
               temp = BytesIO()
               img.save(temp, format="PNG")
               qr_image = base64.b64encode(temp.getvalue())
               rec.update({'qr_code': qr_image})
           else:
               raise UserError(_('Necessary Requirements To Run This Operation Is Not Satisfied'))