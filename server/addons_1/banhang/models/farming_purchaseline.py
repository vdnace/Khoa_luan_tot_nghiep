from odoo import api, fields, models, _
import qrcode
import base64
from io import BytesIO
from odoo.exceptions import UserError

class Orderline(models.Model):
    _name = "purchase.order.line"
    _inherit = "purchase.order.line"
    _description = "Extend purchase order line model"

    ngaysx = fields.Date(string="Ngày sản xuất", default=lambda self: fields.Datetime.now(), required=True)