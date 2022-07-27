# -*- coding: utf-8 -*-

from odoo import models, fields, api


class UsersCodeInherit(models.Model):
    _inherit = 'res.users'

    helpdesk_team_id = fields.Many2many('helpdesk.team', string='Helpdesk Team', index=True)