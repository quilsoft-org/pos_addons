odoo.define('pos_proxy_service.NCButton', function(require) {
'use strict';
   
   const PosComponent = require('point_of_sale.PosComponent');
   const { posbus } = require('point_of_sale.utils');
   const ProductScreen = require('point_of_sale.ProductScreen');
   const { useListener } = require('web.custom_hooks');
   const Registries = require('point_of_sale.Registries');
   var nc=localStorage['es_nc'];



   class NCButton extends PosComponent {
    constructor() {
            super(...arguments);
            useListener('click', this.onClick);
        }

        



       async onClick() {



        

        $('.js_nc').toggleClass('highlight');

        var get_cssclass=$('#js_nc').attr('class');
        if(get_cssclass.indexOf("highlight") > -1)
          {
            localStorage['go_nc']=110;
          }else
          {
            localStorage['go_nc']=0;
          }


       }
   }
    NCButton.template = 'NCButton';

    ProductScreen.addControlButton({
    component: NCButton,
    condition: function() {
    return this.env.pos.config.use_fiscal_printer;
    },
    });

   Registries.Component.add(NCButton);
   return NCButton;
});
