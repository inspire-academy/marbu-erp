odoo.define('bi_stock_transfer_backdate.add_new_validation_button', function (require) {
"use strict";

    var config = require('web.config');
    var core = require('web.core');

    var _t = core._t;
    var qweb = core.qweb;

    var ListController = require('web.ListController');
    var ListView = require('web.ListView');

    var ValidateInvMixin = {
        init: function (viewInfo, params) {
           var ValInv = 'button_validate_inventory_test' in params ? params.button_validate_inventory_test : true;
            if(viewInfo.base_model === 'stock.inventory.line'){
                ValInv = false
            }

            this.controllerParams.ValInv = ValInv && !config.device.isMobile;
            },
        };


    var InvValidationControllerMixin = {
        init: function (parent, model, renderer, params) {
            this.ValInv = params.ValInv;
        },

        _bindInvValidation: function () {
        if (!this.$buttons) {
            return;
        }
        var self = this;
        this.$buttons.on('click', '.o_button_validate_inventory_custom', function () {
            var state = self.model.get(self.handle, {raw: true});
            self.do_action({
                name: 'Inventory Adjustments Backdate',
                type: 'ir.actions.act_window',
                view_mode: 'form',
                res_model: 'wizard.inventory.adjustment',
                target : 'new',
                model: state.context.active_model,
                context: {'default_inventory_id':state.context.active_id},
                views: [[false, 'form']],
            });
        });
    }
};


    ListView.include({
    init: function () {
        this._super.apply(this, arguments);
        ValidateInvMixin.init.apply(this, arguments);
            },
    });


    ListController.include({
        init: function () {
            this._super.apply(this, arguments);
            InvValidationControllerMixin.init.apply(this, arguments);
        },

        renderButtons: function () {
            this._super.apply(this, arguments);
            InvValidationControllerMixin._bindInvValidation.call(this);
        }
    });

});