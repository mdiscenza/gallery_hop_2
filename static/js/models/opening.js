/*global Backbone */
var app = app || {};

(function () {
  'use strict';

  // Todo Model
  // ----------

  // Our basic **Todo** model has `title`, `order`, and `completed` attributes.
  app.Opening = Backbone.Model.extend({
    // Default attributes for the todo
    // and ensure that each todo created has `title` and `completed` keys.
    defaults: {
      venue: '',
      event_title: '',
      artist: '',
      date_and_time: '',
      coor1: 0,
      coor2: 0,
    },


  });
})
();
