from datetime import timedelta
from odoo import models, fields, api
import requests
from ..utils.jwt_utils import get_valid_token, get_jwt_config
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class Department(models.Model):
    _inherit = 'hr.department'

    def send_to_disp(self, departments):
        disp_config = get_jwt_config(self.env.user)
        token = get_valid_token(self.env.user)
        headers = {"Authorization": f"Bearer {token}"}

        now = fields.Datetime.now()
        env_start_datetime = now.strftime("%Y-%m-%dT%H:%M:%S")
        horizon_start_datetime = (now + timedelta(hours=8)).strftime("%Y-%m-%dT%H:%M:%S")
        for department in departments:
            payload = {
                "code": department.name, 
                "name": department.complete_name, 
                "geo_longitude": 120.114749, 
                "geo_latitude": 35.932908,
                "planner_service": {"code": "single_area_code_cvrp"}, 
                "flex_form_data": {
                    "fixed_horizon_flag": "1", 
                    "env_start_datetime": env_start_datetime,
                    "horizon_start_datetime": horizon_start_datetime,
                    "nbr_minutes_planning_windows_duration": 1440,
                    "enable_skills": "1",
                }
            }

            try:
                response = requests.post(disp_config.api_url + '/teams/', json=payload, headers=headers)
                response.raise_for_status()
            except Exception as e:
                raise UserError(f"DISP同步失败：{e}")

    @api.model_create_multi
    def create(self, vals_list):
        departments = super().create(vals_list)
        self.send_to_disp(departments=departments)
        return departments

    # def write(self, vals):
    #     res = super().write(vals)
    #     # 只有在更新关键字段时才调用API
    #     important_fields = ['name', 'complete_name']
    #     if any(field in vals for field in important_fields):
    #         self.send_to_disp(departments=self)
    #     return res 