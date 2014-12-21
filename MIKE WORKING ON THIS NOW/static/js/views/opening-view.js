/*global Backbone, jQuery, _, ENTER_KEY, ESC_KEY */
var app = app || {};

(function ($) {
  'use strict';
  app.OpeningView = Backbone.View.extend({
    //... is a list tag.
    tagName:  'li',

     // template: _.template($('#opening-template').html()),
    
    initialize: function () {
      this.render();
    },

    render: function(){
        console.log("rendering opening template")
        // this.$el.html( this.template(this.model.toJSON()));
        // return this;
    }






  });
})(jQuery);
