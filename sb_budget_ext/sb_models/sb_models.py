from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
import time



class crossovered_budget_lines(models.Model):
    _inherit="crossovered.budget.lines"

    estimated_amount = fields.Monetary(
        compute='_compute_estimate_amount', string='Estimated Amount', help="Estimated Amount.",store=True)   

    @api.multi
    def _compute_estimate_amount(self):
        for i in self:
            i.estimated_amount = i.planned_amount - i.practical_amount
