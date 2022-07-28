# -*- coding: utf-8 -*-

from odoo import models, fields, api
import time


class HelpdeskTicketInherit(models.Model):
    _inherit = 'helpdesk.ticket'

    # tag_ids = fields.Many2one('helpdesk.tag', string='Helpdesk Team', default=_default_team_id, index=True)

    canal_type = fields.Many2one('res.canales', string='Canal', index=True)
    clasificacion_ticket = fields.Many2one('clasificacion.ticket', string='Clasificación', index=True)
    # team_id = fields.Many2one('helpdesk.team', string='Helpdesk Team', default=_default_team_id, index=True)
    user_id = fields.Many2one(
        'res.users', string='Assigned to', default=lambda self: self._get_user())
    contar = fields.Float("MeasureCuenta", compute='_calculate_percentage', compute_sudo=True, store=True)

    @api.onchange('team_id')
    def _get_user(self):
        for record in self:
            return {'domain': {'user_id': [('helpdesk_team_id', '=', record.team_id.id)]}}

    @api.model
    def _calculate_percentage(self):
        for record in self:
            contar = self.env['helpdesk.ticket'].search_count([])
            record.contar = contar

    
    
    
    

# PASAR ESTO A ODOO SH PARA PROBAR LA CREACION DE USUARIOS DESDE HELPDESK, VER SI NO FUNCIONA, LA IDEA ES QUE NO SE GENEREN
