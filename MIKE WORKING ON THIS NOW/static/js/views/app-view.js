/*global Backbone, jQuery, _, ENTER_KEY */
var app = app || {};

(function ($) {
	'use strict';

	// The Application
	// ---------------

	// Our overall **AppView** is the top-level piece of UI.
	app.AppView = Backbone.View.extend({

		// Instead of generating a new element, bind to the existing skeleton of
		// the App already present in the HTML.
		el: '#gh',

		// Our template for the line of statistics at the bottom of the app.
		//statsTemplate: _.template($('#stats-template').html()),
		openingTemplate: _.template($('#opening-template').html()),


		// Delegated events for creating new items, and clearing completed ones.
		events: {
			'keypress #new-todo': 'createOnEnter',
		},

		// At initialization we bind to the relevant events on the `Todos`
		// collection, when items are added or changed. Kick things off by
		// loading any preexisting todos that might be saved in *localStorage*.
		initialize: function () {


		},

		render: function () {
			console.log("app view rendered");
		},

		initiateOpeningsCollection: function(){
			console.log("getting openings")
		},

	});
})(jQuery);
