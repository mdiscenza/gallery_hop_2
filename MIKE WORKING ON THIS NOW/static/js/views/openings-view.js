/*global Backbone */
var app = app || {};

(function () {
  'use strict';

  var app.OpeningsView = Backbone.View.extend({
    tagName: 'ul',

    initialize: function(){
        console.log(this.collection);
    },

    render: function(){
      this.collection.each(function(opening){
              console.log(opening);
    });
}});