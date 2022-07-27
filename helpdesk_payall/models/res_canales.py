# -*- coding: utf-8 -*-

from odoo import models, fields, api
import time

class ResCanales(models.Model):
    _name = 'res.canales'
    _description = 'Tipos de Canales por los que pasan los tickets'

    #tag_ids = fields.Many2one('helpdesk.tag', string='Helpdesk Team', default=_default_team_id, index=True)
    name = fields.Char(string='Canal')
    canal_type_ids = fields.One2many(string='Ticket del Canal', comodel_name='helpdesk.ticket',
                                           inverse_name='canal_type')