/*global Backbone */
var app = app || {};

(function () {
  'use strict';

  app.OpeningsView = Backbone.View.extend({
    tagName: 'ul',

    initialize: function(){
        console.log("collection view made");

        //this.render();
    },

    render: function(){
      // console.log(this);
      this.collection.each(function(opening){
        console.log(opening);
        var opening_view =  new app.OpeningView({ model: opening });
        this.$el.append(opening_view.render().el);
      }, this);
      return this;
    }
  });
})(jQuery);