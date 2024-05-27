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

class StockPicking(models.Model):
    _inherit = "stock.picking"

    qr_code = fields.Binary('QR Code', attachment=True, compute='_generate_qr')
    
    def _generate_qr(self):
        for picking in self:
            if qrcode and base64:
                picking_info = (
                    f"Số phiếu: {picking.name}\n"
                    f"Ngày tạo: {picking.scheduled_date}\n"
                    f"Hạn giao: {picking.date_deadline}\n"
                    f"Loại phiếu: {picking.picking_type_id.name}\n"
                    f"Đối tác: {picking.partner_id.name}\n"
                    f"Nguồn (Mã phiếu nhập hàng): {picking.origin}\n"
                    f"Danh sách sản phẩm:\n"
                )
                for move in picking.move_ids_without_package:
                    picking_info += f" - Tên sản phẩm: {move.product_id.name}\n"
                    picking_info += f"   Số lượng cần: {move.product_uom_qty}\n"
                    picking_info += f"   Số lượng nhập: {move.quantity}\n"
                
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=3,
                    border=4,
                )
                qr.add_data(picking_info)
                qr.make(fit=True)
                img = qr.make_image()
                temp = BytesIO()
                img.save(temp, format="PNG")
                qr_image = base64.b64encode(temp.getvalue())
                picking.update({'qr_code': qr_image})
            else:
                raise UserError(_('Necessary Requirements To Run This Operation Is Not Satisfied'))