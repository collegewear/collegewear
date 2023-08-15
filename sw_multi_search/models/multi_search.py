# -*- coding: utf-8 -*-

import logging

_logger = logging.getLogger(__name__)

from odoo.models import BaseModel, api
from odoo import models


class Base(models.AbstractModel):
    _inherit = 'base'

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        new_args = []
        for domain in args:
            if len(domain) == 3 and type(domain[2]) is str and domain[2].startswith('{') and domain[2].endswith('}'):
                field, op, val = domain
                lop = (op.startswith('!') or op.startswith('not')) and '&' or '|'
                val = val[1:-1]
                new_domain = []
                for v in val.split():
                    new_domain.extend([lop, (field, op, v)])
                new_domain and new_domain.pop(-2)
                new_args.extend(new_domain)
            else:
                new_args.append(domain)
        return super(Base, self)._search(new_args, offset, limit, order, count, access_rights_uid)
