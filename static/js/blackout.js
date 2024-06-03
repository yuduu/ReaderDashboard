(function() {
    var blackout = function() {
        var that = this;

        that.body = null;

        /**
         * Attach to HTML Body
         * @access private
         * @param {DOMNode} body - DOM Node of HTML body element
         */
        that._attach = function(body) {
            that.body = body;
        };

        /**
         * Black out the entire body
         * @access private
         */
        that._blackout = function() {
            that.body.style.background = '#000';
            that.body.style.opacity = 0;
        };

        /**
         * Reactivate the body (undoes the blackout)
         * @access private
         */
        that._reactivate = function() {
            that.body.style.background = '';
            that.body.style.opacity = 1;
        };

        /**
         * Black out and reactivate after a short period
         * @access private
         */
        that._tick = function() {
            that._blackout();
            window.setTimeout(that._reactivate, 500);
        };

        /**
         * Start the blackout module
         * @param {DOMNode} body - DOM Node of HTML body element
         */
        that.start = function(body) {
            that._attach(body);
            window.setInterval(that._tick, 3 * 60 * 60 * 1000);
        };
    };

    // Create a new instance and start it with the body element
    var blackoutInstance = new blackout();
    blackoutInstance.start(document.body);

})();
