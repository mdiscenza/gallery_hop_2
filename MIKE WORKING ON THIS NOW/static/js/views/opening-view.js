/*global Backbone, jQuery, _, ENTER_KEY, ESC_KEY */
var app = app || {};

(function ($) {
  'use strict';

  // Todo Item View
  // --------------

  // The DOM element for a todo item...
  app.Opening = Backbone.View.extend({
    //... is a list tag.
    tagName:  'div',

    // Cache the template function for a single item.
    template: _.template($('#opening-template').html()),

    // The DOM events specific to an item.
    events: {
      // 'click .toggle': 'toggleCompleted',
      // 'dblclick label': 'edit',
      // 'click .destroy': 'clear',
      // 'keypress .edit': 'updateOnEnter',
      // 'keydown .edit': 'revertOnEscape',
      // 'blur .edit': 'close'
    },

    // The TodoView listens for changes to its model, re-rendering. Since there's
    // a one-to-one correspondence between a **Todo** and a **TodoView** in this
    // app, we set a direct reference on the model for convenience.
    initialize: function () {
      console.log("opening view created");
    },

    // Re-render the titles of the todo item.
    render: function () {

      this.$input = this.$('.edit');
      return this;
    },
  });
})(jQuery);
