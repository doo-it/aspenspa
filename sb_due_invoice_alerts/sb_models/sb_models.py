from odoo import models, fields, api, _
from odoo import tools
from datetime import datetime, date, time, timedelta
from odoo.exceptions import UserError, AccessError
from dateutil import relativedelta
from datetime import date
from datetime import datetime
import datetime
from datetime import *


class account_invoice(models.Model):
    _inherit="account.invoice"

    calendar_event_alert_id = fields.Many2one('calendar.event',string="Calendar Alert")


    @api.multi
    def action_invoice_open(self):
        _cal = self.env['calendar.event']
        _alarm = self.env['calendar.alarm']
        _att = self.env['calendar.attendee']
        alarm_ids = []
        invitee_ids = []
        obj = super(account_invoice, self).action_invoice_open()
        if self.date_due and self.number:
            min_15 = _alarm.sudo().search([('name','=','15 Minute(s)'),('type','=','notification')],limit=1).id
            if min_15:
                alarm_ids.append(min_15)
            hour_1 = _alarm.sudo().search([('name','=','1 Hour(s)'),('type','=','notification')],limit=1).id
            if hour_1:
                alarm_ids.append(hour_1)
            day_1 = _alarm.sudo().search([('name','=','1 Day(s)'),('type','=','notification')],limit=1).id
            if day_1:
                alarm_ids.append(day_1)
            date_format = self.env['res.lang'].sudo().search([('active','=',True)],limit=1).date_format
            name = "Due Invoice: %s on %s"%(self.number,datetime.strptime(self.date_due, '%Y-%m-%d').strftime(date_format))
            entry_date = str(self.date_due) + " 04:30:00"
            if self.user_id:
                invitee_ids.append(self.user_id.partner_id.id)
            new_event_obj = _cal.sudo().create({
                        'name':name,
                        'start_datetime':entry_date,
                        'start':entry_date,
                        'stop':entry_date,
                        'alarm_ids':[(4,x) for x in alarm_ids],
                        'privacy':'confidential',
                        'show_as':'free',
                })
            if new_event_obj: 
                for i in self.message_follower_ids:
                    new_attendee = _att.sudo().create({
                            'common_name':i.partner_id.name,
                            'partner_id':i.partner_id.id,
                            'email':i.partner_id.email,
                            'event_id':new_event_obj.id,
                        })
                new_event_obj.duration = 8.5
                self.calendar_event_alert_id = new_event_obj.id

        return obj


