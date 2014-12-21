/*global $ */
/*jshint unused:false */
var app = app || {};
var ENTER_KEY = 13;
var ESC_KEY = 27;

$(function () {
	'use strict';

	// kick things off by creating the `App`
	new app.AppView();
    // Create our global collection of **Todos**.

  app.openings.fetch({
  success : function(collection, response) {
    // var resp = response;  
    console.log(collection);
    app.openings_view = new app.OpeningsView;

    // for (var i=0; i<resp.result.length; i++) {
    //   var openingView = new app.OpeningView({ model: resp.result[i] });
    //   alert(resp.result[i]);
    // }

    //resp.each(function(response){
     // console.log(response);
      //var openingView = new app.OpeningView({ model: response });
    //});
  },

  error : function(collection, response) {
    // code here
  }
  });

});


