from openerp import models,fields,api
import datetime

class openacademy_course(models.Model):
    _name="openacademy.course"
    name=fields.Char(string='Name',size=32,required=True)
    description=fields.Text("Description")
    session_ids=fields.One2many("openacademy.session","course_id",string="Courses")
    responsible_id=fields.Many2one("res.users",string="Responsible")
    
class openacademy_session(models.Model):
    @api.one
    @api.depends('duration','start_date')
    def _end_date(self):
        #esta funcion es para el calculo de la fecha inicio a fin
        if not self.start_date:
            return
        start = datetime.datetime.strptime(self.start_date,'%Y-%m-%d %H:%M:%S')
        duration = datetime.timedelta(days=self.duration/8)
        self.end_date = start + duration
    
    def _inverse_end_date(self):
        #esta funcion es para editar/escribir la fecha de fin
        if not (self.end_date or self.start_date):
            return
        start = datetime.datetime.strptime(self.start_date,'%Y-%m-%d %H:%M:%S')
        end = datetime.datetime.strptime(self.end_date,'%Y-%m-%d %H:%M:%S')
        duration = end - start
        self.duration = duration.days*8
    
    @api.depends('attendee_ids','attendee_ids.session_id')
    #el api depends es para enlazar los datos de una tabla con otra
    def _attendee_count(self):
        #esta funcion calculara la cantidad de matriculados
        self.attendee_count = len(self.attendee_ids)
    
        
    _name="openacademy.session"
    name=fields.Char(string='Name',size=32,required=True)
    duration=fields.Float("Duration", help="duration in hours")
    seats=fields.Integer(string='Seats')
    start_date=fields.Datetime("Start Date")
    course_id=fields.Many2one('openacademy.course',string="Course")
    attendee_ids=fields.One2many('openacademy.attendee',"session_id",string="Attendees")
    instructor_id=fields.Many2one('res.partner',string="Instructor", 
                                  domain=[('is_instructor','=',True)])
    end_date = fields.Datetime("End Date",compute='_end_date',inverse='_inverse_end_date')
    attendee_count=fields.Integer("Attendee Count",compute='_attendee_count')
    
class openacademy_attendee(models.Model):
    _name="openacademy.attendee"
    name=fields.Char(string='Name',size=32,required=False)
    session_id=fields.Many2one('openacademy.session',string="Session")
    partner_id=fields.Many2one('res.partner',string="Partner")