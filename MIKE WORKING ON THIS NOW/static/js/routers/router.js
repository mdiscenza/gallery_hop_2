/*global Backbone */
var app = app || {};

(function () {
	'use strict';

	// Todo Router
	// ----------
	var OpeningRouter = Backbone.Router.extend({
		routes: {
			'*filter': 'setFilter'
		},

		setFilter: function (param) {
			// Set the current filter to be used

			// Trigger a collection filter event, causing hiding/unhiding
			// of Todo view items
		}
	});

	app.OpeningRouter = new OpeningRouter();
	Backbone.history.start();
})();
