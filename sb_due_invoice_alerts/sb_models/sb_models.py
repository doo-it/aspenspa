from odoo import models, fields, api, _
from odoo import tools
from datetime import datetime, date, time, timedelta
from odoo.exceptions import UserError, AccessError
from dateutil import relativedelta
from datetime import date
from datetime import datetime
import datetime
from datetime import *


# class calendar_event(models.Model):
#     _inherit="calendar.event"

#     stop = fields.Datetime('Stop', required=False, help="Stop date of an event, without time for full days events")


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
            name = "Due Invoice: %s on %s"%(self.number,datetime.strptime(str(self.date_due), '%Y-%m-%d').strftime(date_format))
            entry_date = str(self.date_due) + " 04:30:00"
            # stop_date = str(self.date_due) + " 04:29:59"
            partner_id = self.user_id.partner_id.id
            if self.user_id:
                invitee_ids.append(self.user_id.partner_id.id)
            vals = {
                    'partner_ids': [[6, False, [partner_id]]], 
                    'allday': False, 
                    'interval': 1, 
                    'end_type': 'count', 
                    'count': 1, 
                    'month_by': 'date', 
                    'day': 1, 
                    'privacy': 'confidential', 
                    'show_as': 'free', 
                    'user_id': 2, 
                    'res_id': 0, 
                    'name': name, 
                    'start': entry_date, 
                    'stop': entry_date, 
                    'start_date': False, 
                    'stop_date': False, 
                    'start_datetime': entry_date, 
                    'stop_datetime': entry_date, 
                    'duration': 24.0, 
                    'categ_ids': [[6, False, []]], 
                    'alarm_ids': [(4,x) for x in alarm_ids], 
                    'location': False, 
                    'description': False, 
                    'recurrency': False, 
                    'rrule_type': False, 
                    'final_date': False, 
                    'mo': False, 
                    'tu': False, 
                    'we': False, 
                    'th': False, 
                    'fr': False, 
                    'sa': False, 
                    'su': False, 
                    'byday': False, 
                    'week_list': False, 
                    'recurrent_id': 0, 
                    'message_attachment_count': 0
                }
            new_event_obj = _cal.sudo().create(vals)
            self.env.cr.commit()
            if new_event_obj: 
                for i in self.message_follower_ids:
                    new_attendee = _att.sudo().create({
                            'common_name':i.partner_id.name,
                            'partner_id':i.partner_id.id,
                            'email':i.partner_id.email,
                            'event_id':new_event_obj.id,
                        })
                new_event_obj.duration = 24.0
                # new_event_obj.stop = entry_date
                self.calendar_event_alert_id = new_event_obj.id
        return obj


