# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PartnerCodeInherit(models.Model):
    _inherit = 'res.partner'

    rif_aliado = fields.Char(string = 'RIF')