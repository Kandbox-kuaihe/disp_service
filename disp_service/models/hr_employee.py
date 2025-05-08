from odoo import models, fields, api
import requests
from ..utils.jwt_utils import get_valid_token, get_jwt_config
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)


class Employee(models.Model):
    _inherit = 'hr.employee'

    def send_to_disp(self, employees):
        disp_config = get_jwt_config(self.env.user)
        token = get_valid_token(self.env.user)
        headers = {"Authorization": f"Bearer {token}"}

        for employee in employees:
            # 获取员工所属部门的编码，如果有的话
            team_code = employee.department_id.name if employee.department_id else None
            payload = {
                "code": f"{team_code}${employee.name}",
                "name": employee.name,
                "team": {"code": team_code}, 
                "geo_longitude": 120.114749, 
                "geo_latitude": 35.932908, 
                "flex_form_data": {"area_code": "A", "capacity_volume": 0, "max_nbr_order": 0}, 
                "business_hour": {
                    "monday": [{"open": "0005", "close": "2330", "id": "a0", "isOpen": True}], 
                    "tuesday": [{"open": "0005", "close": "2330", "id": "a1", "isOpen": True}], 
                    "wednesday": [{"open": "0005", "close": "2330", "id": "a2", "isOpen": True}], 
                    "thursday": [{"open": "0005", "close": "2330", "id": "a3", "isOpen": True}], 
                    "friday": [{"open": "0005", "close": "2330", "id": "a4", "isOpen": True}], 
                    "saturday": [{"open": "0005", "close": "2330", "id": "a5", "isOpen": True}], 
                    "sunday": [{"open": "0005", "close": "2330", "id": "a6", "isOpen": True}]
                }, 
                "auto_planning": True,
                "is_active": True,
                "skills": [ skill.name for skill in employee.skill_ids ]
            }
            print(payload)

            try:
                response = requests.post(disp_config.api_url + '/workers/', json=payload, headers=headers)
                response.raise_for_status()

                reset = requests.post(disp_config.api_url + '/planner_service/reset_planning_window/', headers=headers)
                reset.raise_for_status()
            except Exception as e:
                raise UserError(f"DISP员工同步失败：{e}")

    @api.model_create_multi
    def create(self, vals_list):
        employees = super().create(vals_list)
        self.send_to_disp(employees=employees)
        return employees

    # def write(self, vals):
    #     res = super().write(vals)
    #     # 只有在更新关键字段时才调用API
    #     important_fields = ['name', 'work_email', 'work_phone', 'mobile_phone', 'department_id']
    #     if any(field in vals for field in important_fields):
    #         self.send_to_disp(employees=self)
    #     return res 