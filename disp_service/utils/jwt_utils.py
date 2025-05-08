from odoo import fields, _
import datetime
import jwt
from uuid import uuid4
from odoo.exceptions import (
    UserError
)

def get_jwt_config(user):
    _config = user.env['disp.config'].sudo().search([('type', '=', 'disp')], limit=1)

    if not _config:
        return UserError(_("未设置 Config 信息"))
    return _config

def get_valid_token(user):
    mes_config = get_jwt_config(user)

    jwt_secret_key = mes_config.api_key
    jwt_expiration_minutes= mes_config.expiration_minutes

    now = fields.Datetime.now()
    _user = user.env['disp.user'].sudo().search([('user_id', '=', user.id)], limit=1)
    if not _user:
        return UserError(_("未绑定  用户"))

    if not _user.session_id:
        _user.session_id = str(uuid4())

    if _user.jwt_token and _user.jwt_token_expire_time > now:
        return _user.jwt_token

    exp_time = now + datetime.timedelta(days=jwt_expiration_minutes)

    payload = {
        "email": _user.email,
        "exp": exp_time,
        "session_id": _user.session_id
    }

    token = jwt.encode(payload, jwt_secret_key, algorithm="HS256")

    _user.jwt_token = token
    _user.jwt_token_expire_time = exp_time
    return token