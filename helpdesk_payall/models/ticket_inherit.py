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
    
    
    
    @api.model_create_multi
    def create(self, list_value):
        now = fields.Datetime.now()
        # determine user_id and stage_id if not given. Done in batch.
        teams = self.env['helpdesk.team'].browse([vals['team_id'] for vals in list_value if vals.get('team_id')])
        team_default_map = dict.fromkeys(teams.ids, dict())
        for team in teams:
            team_default_map[team.id] = {
                'stage_id': team._determine_stage()[team.id].id,
                'user_id': team._determine_user_to_assign()[team.id].id
            }

        # Manually create a partner now since 'generate_recipients' doesn't keep the name. This is
        # to avoid intrusive changes in the 'mail' module
        for vals in list_value:
            partner_id = vals.get('partner_id', False)
            partner_name = vals.get('partner_name', False)
            partner_email = vals.get('partner_email', False)
            if partner_name and partner_email and not partner_id:
                try:
                    vals['partner_id'] = self.env['res.partner'].find_or_create(
                        tools.formataddr((partner_name, partner_email))
                    ).id
                except UnicodeEncodeError:
                    # 'formataddr' doesn't support non-ascii characters in email. Therefore, we fall
                    # back on a simple partner creation.
                    vals['partner_id'] = self.env['res.partner'].create({
                        'name': partner_name,
                        'email': partner_email,
                    }).id

        # determine partner email for ticket with partner but no email given
        partners = self.env['res.partner'].browse([vals['partner_id'] for vals in list_value if 'partner_id' in vals and vals.get('partner_id') and 'partner_email' not in vals])
        partner_email_map = {partner.id: partner.email for partner in partners}
        partner_name_map = {partner.id: partner.name for partner in partners}

        for vals in list_value:
            if vals.get('team_id'):
                team_default = team_default_map[vals['team_id']]
                if 'stage_id' not in vals:
                    vals['stage_id'] = team_default['stage_id']
                # Note: this will break the randomly distributed user assignment. Indeed, it will be too difficult to
                # equally assigned user when creating ticket in batch, as it requires to search after the last assigned
                # after every ticket creation, which is not very performant. We decided to not cover this user case.
                if 'user_id' not in vals:
                    vals['user_id'] = team_default['user_id']
                if vals.get('user_id'):  # if a user is finally assigned, force ticket assign_date and reset assign_hours
                    vals['assign_date'] = fields.Datetime.now()
                    vals['assign_hours'] = 0

            # set partner email if in map of not given
            if vals.get('partner_id') in partner_email_map:
                vals['partner_email'] = partner_email_map.get(vals['partner_id'])
            # set partner name if in map of not given
            if vals.get('partner_id') in partner_name_map:
                vals['partner_name'] = partner_name_map.get(vals['partner_id'])

            if vals.get('stage_id'):
                vals['date_last_stage_update'] = now

        # context: no_log, because subtype already handle this
        tickets = super(HelpdeskTicket, self).create(list_value)

        # make customer follower
        for ticket in tickets:
            if ticket.partner_id:
                ticket.message_subscribe(partner_ids=ticket.partner_id.ids)

            ticket._portal_ensure_token()

        # apply SLA
        tickets.sudo()._sla_apply()

        return tickets

# PASAR ESTO A ODOO SH PARA PROBAR LA CREACION DE USUARIOS DESDE HELPDESK, VER SI NO FUNCIONA, LA IDEA ES QUE NO SE GENEREN
