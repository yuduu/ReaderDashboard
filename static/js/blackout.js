that.blackout = new function(screendle) {
    var that = this;

    that.$body = null;

    /**
     * Attach to HTML Body
     * @access private
     * @param {DOMNode} body - DOM Node of HTML body element
     */
    that._attach = function(body) {
        that.$body = $(body);
    };

    /**
     * black out the entire body
     * @access private
     */
    that._blackout = function() {
        that.$body.css('background', '#000').css('opacity', 0);
    };

    /**
     * reactivate the body (undoes the blackout)
     * @access private
     */
    that._reactivate = function() {
        that.$body.css('background', '').css('opacity', 1)
    };

    /**
     * black out and reactivate after a short period
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

}(that);   