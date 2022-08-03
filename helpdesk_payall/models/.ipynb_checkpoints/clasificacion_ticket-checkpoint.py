# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

from odoo import models, fields, api
import time

class ResCanales(models.Model):
    _name = 'clasificacion.ticket'
    _description = 'Clasificación de los tickets'

    #tag_ids = fields.Many2one('helpdesk.tag', string='Helpdesk Team', default=_default_team_id, index=True)
    name = fields.Char(string='Clasificacion', store=True)
    clasificacion_ticket_ids = fields.One2many(string='Clasificación', comodel_name='helpdesk.ticket',
                                           inverse_name='clasificacion_ticket', store=True)
    contar = fields.Float("MeasureCuentaClasifc", compute='_calculate_percentage', compute_sudo=True, store=True)

 #   @api.depends('partner_id')
 #   def _filtro_emails(self):
# for ticket in self:
            #if ticket.partner_id:
             #   ticket.partner_id.email =

#    @api.depends('partner_id')
#    def _get_correos_ticket(self):
#        for ticket in self:
#            correos_users = self.env['res.partner'].search([()])
#            for correos in correos_users:
#                if ticket.partner_email != correos:
#                    print('Proceso Stop')
#                    #correos_ticket = self.env['helpdesk.ticket'].search([('partner_email', '=', correos.email)])

    @api.model
    def _calculate_percentage(self):
        for record in self:
            contar = self.env['helpdesk.ticket'].search_count(['clasificacion_ticket', '=', 1])
            record.contar = contar



