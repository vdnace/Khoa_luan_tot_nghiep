import datetime
from odoo import api, fields, models

class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    ngaysx = fields.Date(string="Ngày sản xuất", related='move_id.ngaysx', store=True, required=True)

    @api.depends('ngaysx', 'lot_id.expiration_date')
    def _compute_expiration_date(self):
        for move_line in self:
            if not move_line.expiration_date and move_line.lot_id.expiration_date:
                move_line.expiration_date = move_line.lot_id.expiration_date
            elif move_line.picking_type_use_create_lots:
                if move_line.product_id.use_expiration_date:
                    if move_line.ngaysx:
                        move_line.expiration_date = move_line.ngaysx + datetime.timedelta(days=move_line.product_id.expiration_time)
                    else:
                        move_line.expiration_date = False
                else:
                    move_line.expiration_date = False

    @api.onchange('lot_id')
    def _onchange_lot_id(self):
        if not self.picking_type_use_existing_lots or not self.product_id.use_expiration_date:
            return
        if self.lot_id:
            self.expiration_date = self.lot_id.expiration_date
        else:
            self.expiration_date = False

    @api.onchange('product_id', 'product_uom_id')
    def _onchange_product_id(self):
        res = super()._onchange_product_id()
        if self.picking_type_use_create_lots:
            if self.product_id.use_expiration_date:
                if self.ngaysx:
                    self.expiration_date = self.ngaysx + datetime.timedelta(days=self.product_id.expiration_time)
                else:
                    self.expiration_date = False
            else:
                self.expiration_date = False
        return res

    def _prepare_new_lot_vals(self):
        vals = super()._prepare_new_lot_vals()
        if self.expiration_date:
            vals['expiration_date'] = self.expiration_date
        return vals