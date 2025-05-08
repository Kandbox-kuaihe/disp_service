# -*- coding: utf-8 -*-

from odoo import api, fields, models

class DispUser(models.Model):
    _name = 'disp.user'
    _description = u'Disp User'

    name = fields.Char(string="用户名称")
    user_id = fields.Many2one(
        comodel_name='res.users',
        string="odoo 用户",
        )
    company_id = fields.Many2one('res.company', related='user_id.company_id', store=True, readonly=True)
    email = fields.Char(string="用户名")
    password = fields.Char(string="密码")
    role = fields.Char(string="角色")
    session_id = fields.Char(string="Session ID")

    jwt_token = fields.Char(" JWT Token")
    jwt_token_expire_time = fields.Datetime(" JWT Token Expiry")

