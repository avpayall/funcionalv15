# -*- coding: utf-8 -*-

from odoo import models, fields, api
import time


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""


class ResTimer(models.Model):
    _name = 'res.timer'
    _description = 'Timer'

    status_ticket = fields.Selection(
        [('new', 'Nuevo'), ('progress', 'En Progreso'), ('completed', 'Completada'), ('anulated', 'Anulada')], 'Type')
    start_timer = fields.Float(string='Timer')
    start = fields.Float(string='Start')
    stop = fields.Float(string='Stop')

    @api.onchange("status_ticket")
    def stopping(self):
        if self.status_ticket == 'completed' or self.status_ticket == 'anulated':
            elapsed_time = time.time() - self.start
            self.start_timer = elapsed_time

    @api.model
    def create(self, vals):
        vals['start'] = time.time()
        result = super(ResTimer, self).create(vals)
        return result