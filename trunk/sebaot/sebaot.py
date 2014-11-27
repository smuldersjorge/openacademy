from openerp import models,fields,api

class sebaot_seccion(models.Model):
    _name = "sebaot.seccion"
    
    name = fields.Char('Name')
    code = fields.Integer('Code')
    active = fields.Boolean('Active')

class sebaot_marca(models.Model):
    @api.one
    def _display_name(self):
        self.name = "%s-%s"%(self.marca,self.modelo)
    _name = "sebaot.marca"
    
    marca = fields.Char('Marca')
    modelo = fields.Char('Modelo')
    name = fields.Char("Name",compute='_display_name')

class sebaot_bien(models.Model):
    _name = "sebaot.bien"
    
    name = fields.Char('Name')
    
class sebaot_automovil(models.Model):
    @api.one
    def _display_name(self):
        self.name = "%s-%s-%s"%(self.marca_id.name,self.chapa,self.color)
        
    @api.one
    @api.depends('articulo_ids','articulo_ids.automovil_id','articulo_ids.siniestro_ids.total_facturado','articulo_ids.siniestro_ids.articulo_id')
    def _siniestro_total_facturado(self):
        total = 0.0
        for articulo in self.articulo_ids:
            for siniestro in articulo.siniestro_ids:
                total += siniestro.total_facturado
        self.siniestro_total_facturado = total
    
    _name = "sebaot.automovil"
    
    marca_id = fields.Many2one('sebaot.marca', string="Marca")
    motor = fields.Char('Motor')
    chasis = fields.Char('Chasis')
    anho = fields.Integer('Anho')
    country_id = fields.Many2one('res.country', string="Procedencia")
    via = fields.Char('Via Importacion')
    chapa = fields.Char('Chapa')
    state_id = fields.Many2one('res.country.state', string="Area Circulacion")
    coche = fields.Char('Coche')
    pasajeros = fields.Integer('Pasajeros')
    tonelaje = fields.Float('Tonelaje')
    color = fields.Char('Color')
    uso = fields.Char('Destino Uso')
    gps = fields.Char('GPS')
    name = fields.Char("Name",compute='_display_name')
    articulo_ids = fields.One2many('sebaot.articulo','automovil_id',string="Articulos")
    
    #aca se define el id para la funcion de calcular siniestralidad de vehiculos
    siniestro_total_facturado = fields.Float('Siniestro Total Facturado',
                                             compute='_siniestro_total_facturado', store=True)
    
class sebaot_cobertura(models.Model):
    _name = "sebaot.cobertura"
    
    name = fields.Char('Name')

class sebaot_clausula(models.Model):
    _name = "sebaot.clausula"
    
    name = fields.Char('Name')

class sebaot_servicio(models.Model):
    _name = "sebaot.servicio"
    
    poliza_id = fields.Many2one('sebaot.poliza', string="Poliza")
    
    name = fields.Char('Name')
    costo = fields.Float('Costo')
    moneda = fields.Many2one('res.currency', string="Moneda")
    prestador_id = fields.Many2one('res.partner',string='Prestador')

class sebaot_cuota(models.Model):
    _name = "sebaot.cuota"
    
    poliza_id = fields.Many2one('sebaot.poliza', string="Poliza")
    
    cuota_numero = fields.Integer('Numero')
    recibo_serie =  fields.Char('Serie')
    recibo_numero =  fields.Char('Recibo')
    
    vencimiento = fields.Date('Fecha Vencimiento')
    monto = fields.Float('Monto')
    parcial = fields.Integer('Parciales')
    tipo =  fields.Char('Tipo')
    pagado = fields.Float('Pagado')
    pagado_fecha = fields.Date('Fecha Pago')
    pagado_en = fields.Char('PAgado en')
    saldo = fields.Float('Saldo')
    
    cobrador_id = fields.Many2one('res.partner', string="Cobrador")

class sebaot_articulo_cobertura(models.Model):
    _name = "sebaot.articulo.cobertura"
    
    articulo_id = fields.Many2one('sebaot.articulo', string="Articulo")
    cobertura_id  = fields.Many2one('sebaot.cobertura', string="Cobertura")
    suma_asegurada = fields.Float('Suma Asegurada')
    franquicia = fields.Float('Franquicia')

class sebaot_articulo_clausula(models.Model):
    _name = "sebaot.articulo.clausula"
    
    articulo_id = fields.Many2one('sebaot.articulo', string="Articulo")
    cobertura_id  = fields.Many2one('sebaot.clausula', string="Clausula")

class sebaot_articulo_automovil(models.Model):
    _name = "sebaot.articulo.automovil"
    
    articulo_id = fields.Many2one('sebaot.articulo', string="Articulo")
    automovil_id  = fields.Many2one('sebaot.automovil', string="Automovil")
    

class sebaot_articulo(models.Model):
    @api.one
    def _display_name(self):
        self.name = "%s-%s-%s"%(self.poliza_id.name,self.tipo,self.id)
    
    @api.one
    @api.depends('siniestro_ids','siniestro_ids.total_facturado','siniestro_ids.articulo_id')
    def _siniestro_total_facturado(self):
        total = 0.0
        for siniestro in self.siniestro_ids:
            total += siniestro.total_facturado
        self.siniestro_total_facturado = total
    
    _name = "sebaot.articulo"
    
    poliza_id = fields.Many2one('sebaot.poliza', string="Poliza")
    tipo = fields.Selection([('automovil','Automovil'),
                             ('incendio','Incendio'),
                             ('terceros','Terceros')],string="Tipo")
    asegurado_id =  fields.Many2one('res.partner', string="Asegurado",related="poliza_id.asegurado_id")
    cobertura_ids = fields.One2many('sebaot.articulo.cobertura','articulo_id', string="Coberturas")
    clausula_ids = fields.One2many('sebaot.articulo.clausula','articulo_id', string="Clausula")
    automovil_id = fields.Many2one('sebaot.automovil', string="Automovil")
    dislay_name = fields.Char('Name',compute='_display_name')
    name = fields.Char('Name')
    suma_asegurada = fields.Float('Suma Asegurada')
    franquicia = fields.Float('Franquicia')
    siniestro_ids = fields.One2many('sebaot.siniestro','articulo_id', 
                                    string="Siniestros")
    #estirar campos relacionales
    seccion_id = fields.Many2one('sebaot.seccion',string="Seccion",related="poliza_id.seccion_id",readonly=True,store=True)
    active = fields.Boolean('Active', default=True)
    
    siniestro_total_facturado = fields.Float('Siniestro Total Facturado',
                                             compute='_siniestro_total_facturado',store=True)
    

class sebaot_poliza(models.Model):
    @api.one
    def _display_name(self):
        self.name = "%s-%s-%s"%(self.seccion_id.code,self.poliza,self.endoso)
    
    _name = "sebaot.poliza"
    #esto es para el chater
    _inherit = ['mail.thread','ir.needaction_mixin']
    poliza = fields.Integer('Poliza')
    endoso = fields.Integer('Endoso')
    parent_id = fields.Many2one('sebaot.poliza', string="Poliza Padre")
    child_ids = fields.One2many('sebaot.poliza', 'parent_id', string="Poliza Hijas")
    seccion_id =  fields.Many2one('sebaot.seccion', string="Seccion")
    asegurado_id = fields.Many2one('res.partner', string="Asegurado")
    plan =  fields.Char('Plan')
    name = fields.Char("Name",compute='_display_name')
    
    sucursal_carga =  fields.Char('Sucursal Carga')
    vendedor_id = fields.Many2one('res.partner', string="Vendedor")
    cobrador_id = fields.Many2one('res.partner', string="Cobrador")
    
    factura_numero = fields.Char('Factura Numero')
    factura_fecha = fields.Date('Fecha Emision')
    factura_monto = fields.Float('Monto')
    cuota_ids = fields.One2many('sebaot.cuota','poliza_id',string='Pagos')
    articulo_ids = fields.One2many('sebaot.articulo','poliza_id',string='Articulos')
    
    pagado_monto = fields.Float('Pagado')
    saldo_actual = fields.Float('Saldo Actual')
    
    emision_fecha = fields.Date('Fecha Emision')
    vigencia_inicio  = fields.Date('Vigencia Inicio')
    vigencia_fin  = fields.Date('Vigencia Fin')
    
    moneda = fields.Many2one('res.currency', string="Moneda")
    
    capital = fields.Float('Capital')
    prima_tecnica = fields.Float('Prima Tecnica')
    servicio = fields.Float('Costo Servicio')
    prima = fields.Float('Prima')
    rpf = fields.Float('RPF')
    sub_total = fields.Float('Sub Total')
    iva = fields.Float('IVA')
    premio = fields.Float('Premio')
    franquicia = fields.Float('Franquicia')
    
    servicio_ids = fields.One2many('sebaot.servicio','poliza_id', string="Servicios")
    
    operador = fields.Many2one('res.users', string="Operador")
    autorizado = fields.Many2one('res.users', string="Autorizado")
    autorizado_fecha = fields.Date('Fecha Autorizado')
    state = fields.Selection([('Nueva', 'Nueva'),
                              ('renovacion','Renovacion'),
                              ('emdoso_modificacion','Endoso Modificacion'),
                              ('anulado_parcial','Anulado Parcial'),
                              ('anulado_total','Anulado Total')], string="Estado")
    
    
class sebaot_siniestro(models.Model):
    @api.one
    def _display_name(self):
        self.name = "%s"%(self.articulo_id)
         
    _name = "sebaot.siniestro"
    #esto es para el chater
    _inherit = ['mail.thread','ir.needaction_mixin']
    anho = fields.Integer('Anho')
    numero = fields.Integer('Numero')
    parcial = fields.Integer('Parcial')
    
    articulo_id = fields.Many2one('sebaot.articulo', string="Articulo")
    
    denuncia_fecha  = fields.Date('Fecha Denuncia')
    siniestro_fecha  = fields.Date('Fecha Siniestro')
    declarante = fields.Char('Declarante')
    declarante_cedula = fields.Char('Cedula')
    como_ocurrio = fields.Text('Como Ocurrio')
    danhos = fields.Text('Danhos')
    causa = fields.Char('Causa')
    finiquitado_fecha  = fields.Date('Fecha Finiquitado')
    
    total_pendiente = fields.Float('Total Pendiente')
    total_facturado = fields.Float('Total Facturado')
    estimado_total = fields.Float('Estimado Total')
    estimado_cia = fields.Float('Estimado Cia')
    
    operador = fields.Many2one('res.users', string="Operador")
    state = fields.Selection([('Nueva', 'Nueva'),
                              ('proceso','En Proceso'),
                              ('liquidado','Liquidado'),
                              ('rechazado','Rechazado')], string="Estado")
    name = fields.Char("Name",compute='_display_name')
    cobertura_ids = fields.One2many('sebaot.siniestro.cobertura','siniestro_id', string="Coberturas")
    pago_ids = fields.One2many('sebaot.siniestro.pago','siniestro_id', string="Pagos")
    gasto_ids = fields.One2many('sebaot.siniestro.gasto','siniestro_id', string="Gastos")
    
    poliza_id = fields.Many2one('sebaot.poliza',string="Poliza",related="articulo_id.poliza_id",readonly=True,store=True)
    seccion_id = fields.Many2one('sebaot.seccion',string="Seccion",related="articulo_id.poliza_id.seccion_id",readonly=True,store=True)
    agente_id = fields.Many2one('res.partner',string="Agente",related="articulo_id.poliza_id.vendedor_id",readonly=True,store=True)
    asegurado_id = fields.Many2one('res.partner',string="Asegurado",related="articulo_id.poliza_id.asegurado_id",readonly=True,store=True)        
class sebaot_siniestro_cobertura(models.Model):
    _name = "sebaot.siniestro.cobertura"
    
    siniestro_id = fields.Many2one('sebaot.siniestro', string="Siniestro")
    cobertura_id  = fields.Many2one('sebaot.cobertura', string="Cobertura")
    suma_asegurada = fields.Float('Suma Asegurada')
    estimado = fields.Float('Estimado')
    saldo = fields.Float('Saldo')


class sebaot_siniestro_gasto(models.Model):
    _name = "sebaot.siniestro.gasto"
    
    siniestro_id = fields.Many2one('sebaot.siniestro', string="Siniestro")
    orden = fields.Integer('Orden')
    orden_fecha = fields.Date('Fecha Siniestro')
    monto = fields.Float('Monto')
    coaseguro = fields.Float('Monto')
    nuestra_parte = fields.Float('Nuestra Parte')
    moneda = fields.Many2one('res.currency', string="Moneda")
    autorizado = fields.Many2one('res.users', string="Autorizado")
    autorizado_fecha = fields.Date('Fecha Autorizado')
    proveedor_id = fields.Many2one('res.partner', string="Proveedor")
    factura_serie = fields.Char('Serie')
    factura_tipo = fields.Char('Factura Tipo')
    factura_numero = fields.Char('Numero Factura')
    

class sebaot_siniestro_pago(models.Model):
    _name = "sebaot.siniestro.pago"
    
    siniestro_id = fields.Many2one('sebaot.siniestro', string="Siniestro")
    orden = fields.Integer('Orden')
    orden_fecha = fields.Date('Fecha Siniestro')
    monto = fields.Float('Monto')
    coaseguro = fields.Float('Monto')
    nuestra_parte = fields.Float('Nuestra Parte')
    moneda = fields.Many2one('res.currency', string="Moneda")
    autorizado = fields.Many2one('res.users', string="Autorizado")
    autorizado_fecha = fields.Date('Fecha Autorizado')
    proveedor_id = fields.Many2one('res.partner', string="Proveedor")
    factura_serie = fields.Char('Serie')
    factura_tipo = fields.Char('Factura Tipo')
    factura_numero = fields.Char('Numero Factura')
