# -*- coding: utf-8 -*-

from odoo import api, fields, models

class DispConfig(models.Model):
    _name = 'disp.config'
    _description = u'Disp Config'

    name = fields.Char(string="配置名称", default="Disp Service 连接")
    api_url = fields.Char(string="Disp API 地址")
    api_key = fields.Char(string="Disp API Key")
    login_url = fields.Char(string="登录地址")
    type = fields.Selection([('disp', 'Disp')], default='disp')
    expiration_minutes = fields.Integer(string="过期时间")

