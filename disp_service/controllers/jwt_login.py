import jwt
import datetime
from odoo import http
from odoo.http import request
from uuid import uuid4

from ..utils.jwt_utils import get_valid_token


# SECRET_KEY = "duanqiyanghaibaoddduanqiyanghaibaoddduanqiyanghaibaoddd"  # 放到系统参数更安全
# EXPIRATION_MINUTES = 30
# MES_LOGIN_URL = "http://localhost:8881/ed/login"  # FastAPI 登录入口

class JWTLogin(http.Controller):

    @http.route('/disp/jwt/login', type='http', auth='user', website=False)
    def jwt_login(self):
        user = request.env.user
        _config = request.env['disp.config'].sudo().search([('type', '=', 'disp')],limit=1)

        if not _config:
            return request.render('mes.config', {'error': '未设置mes config信息'})

        login_url = _config.login_url

        # mes_user = request.env['mes.user'].sudo().search([('user_id', '=', user.id)], limit=1)
        # if not mes_user:
        #     return request.render('web.login', {'error': '未绑定 MES 用户'})
        #
        # if not mes_user.session_id:
        #     mes_user.session_id = str(uuid4())
        #
        # payload = {
        #     "email": mes_user.email,
        #     "exp": datetime.datetime.now() + datetime.timedelta(minutes=EXPIRATION_MINUTES),
        #     "session_id": mes_user.session_id
        # }
        # token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        token = get_valid_token(user=user)


        redirect_url = f"{login_url}?token={token}"
        print("redirect_url",redirect_url)
        return request.redirect(redirect_url,local=False)