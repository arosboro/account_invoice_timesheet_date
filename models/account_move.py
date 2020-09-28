# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models, tools, _

_logger = logging.getLogger(__name__)

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.model_create_multi
    def create(self, vals_list):
        # OVERRIDE
        # Link the timesheet from the SO lines to the corresponding draft invoice.
        # NOTE: Only the timesheets linked to an Sale Line with a product invoiced on delivered quantity
        # are concerned, since in ordered quantity, the timesheet quantity is not invoiced, but is simply
        # to compute the delivered one (for reporting).
        lines = super(AccountMoveLine, self).create(vals_list)
        lines_to_process = lines.filtered(lambda line: line.move_id.type == 'out_invoice'
                                                       and line.move_id.state == 'draft')
        for line in lines_to_process:
            sale_line_delivery = line.sale_line_ids.filtered(lambda sol: sol.product_id.invoice_policy == 'delivery' and sol.product_id.service_type == 'timesheet')
            if sale_line_delivery:
                domain = self._timesheet_domain_get_invoiced_lines(sale_line_delivery)
                period_start = self.env.context.get('invoice_period_start')\
                    .strftime(tools.misc.DEFAULT_SERVER_DATETIME_FORMAT)
                period_end = self.env.context.get('invoice_period_end')\
                    .strftime(tools.misc.DEFAULT_SERVER_DATETIME_FORMAT)
                if period_start and period_end:
                    _logger.info("Period Start: %s, Period End: %s" % (period_start, period_end))
                    domain += ['&', ('date', '>=', period_start), ('date', '<=', period_end)]
                _logger.info(domain)
                timesheets = self.env['account.analytic.line'].search(domain).sudo()
                _logger.info("%s timesheets" % len(timesheets))
                timesheets.write({
                    'timesheet_invoice_id': line.move_id.id,
                })
        return lines

    @api.model
    def _timesheet_domain_get_invoiced_lines(self, sale_line_delivery):
        """ Get the domain for the timesheet to link to the created invoice
            :param sale_line_delivery: recordset of sale.order.line to invoice
            :return a normalized domain
        """
        return [
            '&',
            ('so_line', 'in', sale_line_delivery.ids),
            '&',
            ('timesheet_invoice_id', '=', False),
            ('project_id', '!=', False)
        ]
