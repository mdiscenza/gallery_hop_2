/*global Backbone */
var app = app || {};

(function () {
  'use strict';


  var Openings = Backbone.Collection.extend({

    model: app.Opening,
    url: '/openings',

    parse: function(response){
        return response.result;
    }

  //   render: function(){
  //     this.collection.each(function(opening){
  //         var openingView = new app.OpeningView({ model: opening });
  //         this.$el.append(openingView.el);
  //     }, this);
  // }


  });

  // Create our global collection of **Todos**.
  app.openings = new Openings();
  // console.log(app.openings.fetch());
  // console.log(app.openings);

  app.openings.fetch({
  success : function(collection, response) {
    //console.log(collection);
    //console.log(response);
    //console.log(response.result);

    for (var i=0; i<response.result.length; i++) {
      //var openingView = new app.OpeningView({ model: response.result[i] });
      alert(response.result[i].artist);
    }

    //resp.each(function(response){
     // console.log(response);
      //var openingView = new app.OpeningView({ model: response });
    //});
  },

  error : function(collection, response) {
    // code here
  }
  });

  })();