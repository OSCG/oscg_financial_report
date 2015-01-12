# -*- encoding: utf-8 -*-
import time
import pooler
import logging
import netsvc
import tools
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
logger = netsvc.Logger()
from datetime import timedelta, date
from datetime import datetime
from osv import fields,osv
from lxml import etree
from tools.translate import _


class account_report(osv.osv):
    _inherit = 'accounting.report'


    def check_report(self, cr, uid, ids, context=None):

        if context is None:
            context = {}
        
        enable_filter = self.browse(cr, uid, ids[0]).enable_filter
        debit_credit = self.browse(cr, uid, ids[0]).debit_credit
        filter = self.browse(cr, uid, ids[0]).filter
        
        data = {}
        data['enable_filter'] = enable_filter
        data['debit_credit'] = debit_credit
        data['filter'] = filter
        if enable_filter:
            data['comparison_value'] = self.browse(cr, uid, ids[0]).label_filter
        data['ids'] = context.get('active_ids', [])
        data['model'] = context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(cr, uid, ids, ['date_from',  'date_to',  'fiscalyear_id', 'journal_ids', 'period_from', 'period_to',  'filter',  'chart_account_id', 'target_move'], context=context)[0]
        for field in ['fiscalyear_id', 'chart_account_id', 'period_from', 'period_to']:
            if isinstance(data['form'][field], tuple):
                data['form'][field] = data['form'][field][0]
        used_context = self._build_contexts(cr, uid, ids, data, context=context)
        data['form']['periods'] = used_context.get('periods', False) and used_context['periods'] or []
        data['form']['used_context'] = used_context
        
        if context.get('oscg_financial_report',False) == 'Yes':

            res = self._print_report_a(cr, uid, ids, data, context=context)
        else:

            res = self._print_report(cr, uid, ids, data, context=context)
        data = {}
        data['form'] = self.read(cr, uid, ids, ['account_report_id', 'date_from_cmp',  'date_to_cmp',  'fiscalyear_id_cmp', 'journal_ids', 'period_from_cmp', 'period_to_cmp',  'filter_cmp',  'chart_account_id', 'target_move'], context=context)[0]
        for field in ['fiscalyear_id_cmp', 'chart_account_id', 'period_from_cmp', 'period_to_cmp', 'account_report_id']:
            if isinstance(data['form'][field], tuple):
                data['form'][field] = data['form'][field][0]
        comparison_context = self._build_comparison_context(cr, uid, ids, data, context=context)
        res['datas']['form']['comparison_context'] = comparison_context
        return res

    def _print_report_a(self, cr, uid, ids, data, context=None):
        data['form'].update(self.read(cr, uid, ids, ['date_from_cmp',  'debit_credit', 'date_to_cmp',  'fiscalyear_id_cmp', 'period_from_cmp', 'period_to_cmp',  'filter_cmp', 'account_report_id', 'enable_filter', 'label_filter'], context=context)[0])
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'oscg_financial_report_excel',
            'datas': data,
        }
        
    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        res = super(account_report, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar,submenu=False)
        for field in res['fields']:
            if field == 'filter':
                res['fields'][field]['selection'] = [('filter_no', 'filter_period')]
        #if view_type == 'form':
            #if context and context.get('kaertech_financial_report'):
                #res['arch'] = res['arch'].replace('<separator string="Dates" colspan="4"/>','<separator string="Dates" colspan="4" invisible="1"/>')
                #res['arch'] = res['arch'].replace(""" <field name="date_from" attrs="{'readonly':[('filter', '!=', 'filter_date')], 'required':[('filter', '=', 'filter_date')]}" colspan="4" modifiers="{&quot;readonly&quot;: [[&quot;filter&quot;, &quot;!=&quot;, &quot;filter_date&quot;]], &quot;required&quot;: [[&quot;filter&quot;, &quot;=&quot;, &quot;filter_date&quot;]]}"/>""",""" <field name="date_from" attrs="{'readonly':[('filter', '!=', 'filter_date')], 'required':[('filter', '=', 'filter_date')]}" colspan="4" modifiers="{&quot;readonly&quot;: [[&quot;filter&quot;, &quot;!=&quot;, &quot;filter_date&quot;]], &quot;required&quot;: [[&quot;filter&quot;, &quot;=&quot;, &quot;filter_date&quot;]]}" invisible="1"/>""")
                #res['arch'] = res['arch'].replace("""<field name="date_to" attrs="{'readonly':[('filter', '!=', 'filter_date')], 'required':[('filter', '=', 'filter_date')]}" colspan="4" modifiers="{&quot;readonly&quot;: [[&quot;filter&quot;, &quot;!=&quot;, &quot;filter_date&quot;]], &quot;required&quot;: [[&quot;filter&quot;, &quot;=&quot;, &quot;filter_date&quot;]]}"/>""","""<field name="date_to" attrs="{'readonly':[('filter', '!=', 'filter_date')], 'required':[('filter', '=', 'filter_date')]}" colspan="4" modifiers="{&quot;readonly&quot;: [[&quot;filter&quot;, &quot;!=&quot;, &quot;filter_date&quot;]], &quot;required&quot;: [[&quot;filter&quot;, &quot;=&quot;, &quot;filter_date&quot;]]}" invisible="1"/>""")
        doc = etree.fromstring(res['arch'].encode('utf8'))
        xarch, xfields = self._view_look_dom_arch(cr, uid, doc, view_id, context=context)
        res['arch'] = xarch
        res['fields'] = xfields
        return res
account_report()



class account_common_report(osv.osv):
    _inherit = 'accounting.report'

    def check_report_a(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        res = super(accounting_report, self).check_report(cr, uid, ids, context=context)
        data = {}
        data['form'] = self.read(cr, uid, ids, ['account_report_id', 'date_from_cmp',  'date_to_cmp',  'fiscalyear_id_cmp', 'journal_ids', 'period_from_cmp', 'period_to_cmp',  'filter_cmp',  'chart_account_id', 'target_move'], context=context)[0]
        for field in ['fiscalyear_id_cmp', 'chart_account_id', 'period_from_cmp', 'period_to_cmp', 'account_report_id']:
            if isinstance(data['form'][field], tuple):
                data['form'][field] = data['form'][field][0]
        comparison_context = self._build_comparison_context(cr, uid, ids, data, context=context)
        res['datas']['form']['comparison_context'] = comparison_context
        return res




    def _print_report_a(self, cr, uid, ids, data, context=None):
        data['form'].update(self.read(cr, uid, ids, ['date_from_cmp',  'debit_credit', 'date_to_cmp',  'fiscalyear_id_cmp', 'period_from_cmp', 'period_to_cmp',  'filter_cmp', 'account_report_id', 'enable_filter', 'label_filter'], context=context)[0])
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'oscg_financial_report_excel',
            'datas': data,
        }
account_common_report()