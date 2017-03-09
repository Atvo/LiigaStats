'use strict';

if (typeof module !== 'undefined') module.exports = simpleheat;

function simpleheat(canvas) {
    if (!(this instanceof simpleheat)) return new simpleheat(canvas);

    this._canvas = canvas = typeof canvas === 'string' ? document.getElementById(canvas) : canvas;

    this._ctx = canvas.getContext('2d');
    this._width = canvas.width;
    this._height = canvas.height;

    this._max = 1;
    this._data = [];
}

simpleheat.prototype = {

    defaultRadius: 25,

    defaultGradient: {
        0.2: 'blue',
        0.4: 'cyan',
        0.6: 'lime',
        0.8: 'yellow',
        1.0: 'red'
    },

    /*defaultGradient: {
        0.4: 'blue',
        0.6: 'cyan',
        0.7: 'lime',
        0.8: 'yellow',
        1.0: 'red'
    },*/

    data: function (data) {
        this._data = data;
        return this;
    },

    max: function (max) {
        this._max = max;
        return this;
    },

    add: function (point) {
        this._data.push(point);
        return this;
    },

    clear: function () {
        this._data = [];
        return this;
    },

    radius: function (r, blur) {
        blur = blur === undefined ? 15 : blur;

        // create a grayscale blurred circle image that we'll use for drawing points
        var circle = this._circle = document.createElement('canvas'),
            ctx = circle.getContext('2d'),
            r2 = this._r = r + blur;

        circle.width = circle.height = r2 * 2;

        ctx.shadowOffsetX = ctx.shadowOffsetY = r2 * 2;
        ctx.shadowBlur = blur;
        ctx.shadowColor = 'black';

        ctx.beginPath();
        ctx.arc(-r2, -r2, r, 0, Math.PI * 2, true);
        ctx.closePath();
        ctx.fill();

        return this;
    },

    resize: function () {
        this._width = this._canvas.width;
        this._height = this._canvas.height;
    },

    gradient: function (grad) {
        // create a 256x1 gradient that we'll use to turn a grayscale heatmap into a colored one
        var canvas = document.createElement('canvas'),
            ctx = canvas.getContext('2d'),
            gradient = ctx.createLinearGradient(0, 0, 0, 256);

        canvas.width = 1;
        canvas.height = 256;

        for (var i in grad) {
            console.log(i);
            //console.log(grad[i][0]);
            gradient.addColorStop(i, grad[i]);
            //gradient.addColorStop(i, grad[i][0]);
        }

        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, 1, 256);

        this._grad = ctx.getImageData(0, 0, 1, 256).data;
        this._gradient_object = grad;

        return this;
    },

    draw: function (minOpacity) {
        if (!this._circle) this.radius(this.defaultRadius);
        if (!this._grad) this.gradient(this.defaultGradient);

        var ctx = this._ctx;

        ctx.clearRect(0, 0, this._width, this._height);

        // draw a grayscale heatmap by putting a blurred circle at each data point
        for (var i = 0, len = this._data.length, p; i < len; i++) {
            p = this._data[i];
            //ctx.globalAlpha = p[2] / 10;
            //ctx.globalAlpha = Math.max(p[2] / this._max, minOpacity === undefined ? 0.05 : minOpacity);
            //ctx.globalAlpha = this._calculate_opacity(p[2] / this._max);
            ctx.globalAlpha = (this._log(p[2] / this._max, 200000) + 1);
            ctx.drawImage(this._circle, p[0] - this._r, p[1] - this._r);
        }
        console.log(this._gradient_object);
        //return this;
        // colorize the heatmap, using opacity value of each pixel to get the right color from our gradient
        console.log(this._width);
        console.log(this._height);
        var colored = ctx.getImageData(0, 0, this._width, this._height);
        this._colorize(colored.data, this._grad);
        ctx.putImageData(colored, 0, 0);

        return this;
    },

    _colorize: function (pixels, gradient) {
        for (var i = 0, len = pixels.length, j; i < len; i += 4) {
            j = pixels[i + 3] * 4; // get gradient color from opacity value
            //console.log(j);

            if (j) {
                pixels[i] = gradient[j];
                pixels[i + 1] = gradient[j + 1];
                pixels[i + 2] = gradient[j + 2];
            }
        }
    },

    _calculate_opacity: function (data_value) {
        var opacity = 0;
        /*for (var i = 0; i < this._gradient_object.length; i++) {
            if (data_value > this._gradient_object[i]) {
                opacity = this._gradient_object[i][1];
            }
        }*/
        /*for (var grad in this._gradient_object) {
            console.log(grad);
            console.log(data_value);
            console.log(this._gradient_object[grad][1]);
            if (data_value > grad) {
                opacity = this._gradient_object[grad][1];
            }
        }*/

        console.log(opacity);
        return opacity;
    },

    _log: function (n, base) {
        var value = Math.log(n) / (base ? Math.log(base) : 1);
        //(value - 1) * Math.log(base)
        //console.log(value);
        if (value < -1) {
            //console.log(value);
            return -1;
        }
        //console.log(value);
        return value;
        /*Math.log = (function() {
        var log = Math.log;
        return function(n, base) {
        return log(n)/(base ? log(base) : 1);
        };
        })();*/
    }
};
