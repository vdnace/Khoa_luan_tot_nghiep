from odoo import api, fields, models, _
class StockMove(models.Model):
    _inherit = 'stock.move'

    ngaysx = fields.Date(string="Ngày sản xuất", related='purchase_line_id.ngaysx', required=True)

    @api.model
    def create(self, vals):
        move = super(StockMove, self).create(vals)
        move._set_lot_ngaysx()
        return move

    def write(self, vals):
        res = super(StockMove, self).write(vals)
        self._set_lot_ngaysx()
        return res

    def _set_lot_ngaysx(self):
        for move in self:
            if move.lot_ids and move.ngaysx:
                for lot in move.lot_ids:
                    if not lot.ngaysx:
                        lot.ngaysx = move.ngaysx