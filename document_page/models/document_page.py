# Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime

class DocumentPage(models.Model):
    """This class is use to manage Document."""

    _name = "document.page"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Document Page"
    _order = "name"

    _HTML_WIDGET_DEFAULT_VALUE = "<p><br></p>"

    name = fields.Char('Reference No')
    is_external = fields.Boolean(string='Is external communication?')
    type = fields.Selection(
        [("content", "Content"), ("category", "Category")],
        "Type",
        help="Page type",
        default="content",
    )
    active = fields.Boolean(default=True)
    parent_id = fields.Many2one(
        "document.page", "Category", domain=[("type", "=", "category")]
    )
    child_ids = fields.One2many("document.page", "parent_id", "Children")
    content = fields.Text(
        "Content",
        compute="_compute_content",
        inverse="_inverse_content",
        search="_search_content",
    )

    draft_name = fields.Char(
        string="Name",
        help="Name for the changes made",
        related="history_head.name",
        readonly=False,
    )

    draft_summary = fields.Char(
        string="Summary",
        help="Describe the changes made",
        related="history_head.summary",
        readonly=False,
    )
    template = fields.Html(
        "Template",
        help="Template that will be used as a content template "
        "for all new page of this category.",
    )
    history_head = fields.Many2one(
        "document.page.history",
        "HEAD",
        compute="_compute_history_head",
        store=True,
        auto_join=True,
    )
    history_ids = fields.One2many(
        "document.page.history",
        "page_id",
        "History",
        order="create_date DESC",
        readonly=True,
    )
    menu_id = fields.Many2one("ir.ui.menu", "Menu", readonly=True)
    content_date = fields.Datetime(
        "Last Contribution Date",
        related="history_head.create_date",
        store=True,
        index=True,
        readonly=True,
    )
    content_uid = fields.Many2one(
        "res.users",
        "Last Contributor",
        related="history_head.create_uid",
        store=True,
        index=True,
        readonly=True,
    )
    company_id = fields.Many2one(
        "res.company",
        "Company",
        help="If set, page is accessible only from this company",
        index=True,
        ondelete="cascade",
        default=lambda self: self.env.company,
    )
    backend_url = fields.Char(
        string="Backend URL",
        help="Use it to link resources univocally",
        compute="_compute_backend_url",
    )

    @api.depends("menu_id", "parent_id.menu_id")
    def _compute_backend_url(self):
        tmpl = "/web#id={}&model=document.page&view_type=form"
        for rec in self:
            url = tmpl.format(rec.id)
            # retrieve action
            action = None
            parent = rec
            while not action and parent:
                action = parent.menu_id.action
                parent = parent.parent_id
            if action:
                url += "&action={}".format(action.id)
            rec.backend_url = url

    @api.constrains("parent_id")
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(_("You cannot create recursive categories."))

    def _get_page_index(self, link=True):
        """Return the index of a document."""
        self.ensure_one()
        index = [
            "<li>" + subpage._get_page_index() + "</li>" for subpage in self.child_ids
        ]
        r = ""
        if link:
            r = '<a href="{}">{}</a>'.format(self.backend_url, self.name)
        if index:
            r += "<ul>" + "".join(index) + "</ul>"
        return r

    @api.depends("history_head")
    def _compute_content(self):
        for rec in self:
            if rec.type == "category":
                rec.content = rec._get_page_index(link=False)
            else:
                if rec.history_head:
                    rec.content = rec.history_head.content
                else:
                    # html widget's default, so it doesn't trigger ghost save
                    rec.content = self._HTML_WIDGET_DEFAULT_VALUE

    def _inverse_content(self):
        for rec in self:
            if rec.type == "content" and rec.content != rec.history_head.content:
                rec._create_history(
                    {
                        "name": rec.draft_name,
                        "summary": rec.draft_summary,
                        "content": rec.content,
                    }
                )
   
    
    def _create_history(self, vals):
        self.ensure_one()
        vals['page_id'] = self.id
        return self.env["document.page.history"].create(vals)

    def _search_content(self, operator, value):
        return [("history_head.content", operator, value)]

    @api.depends("history_ids")
    def _compute_history_head(self):
        for rec in self:
            if rec.history_ids:
                rec.history_head = rec.history_ids[0]

    @api.onchange("parent_id")
    def _onchange_parent_id(self):
        """We Set it the right content to the new parent."""
        if (
            self.content in (False, self._HTML_WIDGET_DEFAULT_VALUE)
            and self.parent_id.type == "category"
        ):
            self.content = self.parent_id.template

    def unlink(self):
        menus = self.mapped("menu_id")
        res = super().unlink()
        menus.unlink()
        return res

    @api.model
    def create(self, vals):
        if vals.get('type')=="content":
            if vals.get('is_external'):
                seq_code = self.env['ir.sequence'].next_by_code('doc.page.external')
            else:
                seq_code = self.env['ir.sequence'].next_by_code('doc.page.internal')
            suffix = datetime.today().strftime("/%m/%Y")
            vals['name'] = seq_code + suffix
        res= super(DocumentPage, self).create(vals)
        return res
    
    def get_base_url(self):
        return ''

    
    def _get_share_url(self, redirect=False, signup_partner=False, pid=None):
        return True
    
    def action_document_send(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            #template_id =  self.env.ref('document_page.document_email_template').id
            template_id = ir_model_data.get_object_reference('document_page','document_email_template')[1]
        except ValueError:
            template_id = False
        try:
            #compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
       
        ctx = {
            'default_model': 'document.page',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',               
            #'custom_layout': "mail.mail_notification_paynow",
            'force_email': True
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx
        }
    