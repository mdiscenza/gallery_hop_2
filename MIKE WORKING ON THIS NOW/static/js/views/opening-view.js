/*global Backbone, jQuery, _, ENTER_KEY, ESC_KEY */
var app = app || {};

(function ($) {
  'use strict';
   app.OpeningView = Backbone.View.extend({
    
    tagName:  'div',

    events: {
        'mouseover': 'showOnMap'
    },
     
    
    initialize: function () {
            
    },

    render: function(){
        // console.log("rendering opening template")
        var template = _.template($('#opening-template').html());
        this.$el.html(template(this.model.toJSON()));
        return this;
    },

    showOnMap: function() {
      // debugger
        // console.log(this.model.attributes);
        // console.log(this.model.attributes.artist);
        // console.log(this.model.attributes.venue);
        // console.log($('#map'));
        
       var text = '<b>this.model.attributes.artist</b>'.concat('<br>this.model.attributes.venue');
       // console.log(L.marker)
       L.marker([this.model.attributes.lat, this.model.attributes.long]).addTo($('#map')).bindPopup(text).openPopup();
  // }
  //   catch (e){
  //   alert("Error");
  // }
    }





  });
})(jQuery);
