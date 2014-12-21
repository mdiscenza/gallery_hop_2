/*global Backbone */
var app = app || {};

(function () {
  'use strict';


  var Openings = Backbone.Collection.extend({

    model: app.Opening,
    url: '/openings',

    // parse: function(response){
    //     console.log("parse called")
    //     return response.collection;
    // }


  });

  // Create our global collection of **Todos**.
  app.openings = new Openings();
  console.log(app.openings.fetch());
  })();