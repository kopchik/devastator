"use strict";

// Bootstrap leftovers
// <!-- Latest compiled and minified CSS -->
// <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
// <!-- Optional theme -->
// <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css">
// <!-- Latest compiled and minified JavaScript -->
// <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>


var $ = require('jquery/jquery:dist/jquery.js')
var d3 = require('mbostock/d3@v3.5.3');
// var swfobject = require('fredsterss/swfobject');

var log = {
  info: function(msg) {
    d3.select("#logWindow")
    .insert("div", "*")
    .text(msg);
  }
}


function startStream() {
  var parameters = { src: "rtmp://" + window.location.hostname + "/rtmp/live" };
  swfobject.embedSWF
  ( "/static/StrobeMediaPlayback.swf"
  , "strobeMediaPlayback"
  , 640
  , 480
  , "10.1.0"
  , {}
  , parameters
  , { allowFullScreen: "true"}
  , { name: "strobeMediaPlayback" }
  );
}


function Joystick(svg, id, color) {
  this.svg = svg;
  this.id = id;
  this.color = color;
  this.pos = undefined;  // TODO: move to widget namespace
  this.diameter = 100;   // TODO: move to widget namespace
  this.widget = {
    center: undefined,
    circle: undefined,
    pointer: undefined,
  }
  this.value = [0.0, 0.0];
}

Joystick.prototype.constructor = Joystick;
Joystick.prototype.constructor.prototype.toString = function() {
  return "Joystick";
}


Joystick.prototype.start = function(pos) {
  this.stop();  // reset everything;
  this.pos = pos;

  var widget = this.widget;
  widget.center = this.svg.append("circle")
    .attr("cx", pos[0])
    .attr("cy", pos[1])
    .attr("r", 2)
  ;

  widget.circle = this.svg.append("circle")
    .attr("class", "circle")
    .attr("cx", pos[0])
    .attr("cy", pos[1])
    .attr("r", this.diameter)
    .style("fill", this.color)
  ;

  widget.pointer = this.svg.append("circle")
    .attr("cx", pos[0])
    .attr("cy", pos[1])
    .attr("r", 40)
  ;
}


// TODO: rename to sendUpdate
Joystick.prototype.onTimer = function() {
  if (!this.canSend) {
    log.info("previous message not ACKed, throttling timer")
    return;
  }
  log.info("timer fired");
  this.canSend = false;
  var joystick = this
  var data = JSON.stringify(joystick.value)
  log.info("sending " + data)
  d3.xhr("/cam/set")
    .header("Content-Type", "application/json")
    .post(data, function(err, resp) {
      if (err) {
        log.info("request error: " + err.status + " " + err.statusText);
        joystick.stop()
        return
      }
      joystick.canSend = true;
      log.info("got control response: " + resp);
    });
}


Joystick.prototype.move = function(pos) {
  var dx = pos[0] - this.pos[0];
  var dy = pos[1] - this.pos[1];
  var r = Math.sqrt(dx*dx + dy*dy);
  if (r > this.diameter) {
    var factor = r / this.diameter;
    dx = dx / factor;
    dy = dy / factor;
  }

  // '-' because we invert Y axis
  this.value = [dx/this.diameter, -dy/this.diameter];

  this.widget.pointer
    .attr("cx", this.pos[0] + dx)
    .attr("cy", this.pos[1] + dy)
  ;
}


Joystick.prototype.stop = function() {
  var widget = this.widget;
  if (widget.center)  { widget.center.remove();  }
  if (widget.circle)  { widget.circle.remove();  }
  if (widget.pointer) { widget.pointer.remove(); }

  this.pos = undefined;
  this.value = [0.0, 0.0];
}

var timer = {
  cb: undefined,
  timerEvent: undefined,
  updateFreq: 3.0,
  start: function() {
    if (this.timerEvent) { return; }
    this.timerEvent = setInterval(this.cb,
                                  1.0/this.updateFreq*1000);
  },
  stop: function() {
    if (!this.timerEvent) { return; }
    clearInterval(this.timerEvent);
    this.timerEvent = undefined;
  }
}


$(function() {
  log.info("started!");
  var svg = d3.select("#controls");
  var svgwidth = parseInt(svg.style("width"));

  var mousestick;
  var sticks = {
    move: new Joystick(svg, "move", "green"),
    look: new Joystick(svg, "look", "white")
  }
  var stickmap = d3.map()

  var guard = true;  // throttle server if it is slow to respond
  function timercb() {
    if (!guard) {
      log.info("server hasn't respond to the previous message, throttling");
      return;
    }
    guard = false;
    var data = d3.map();
    stickmap.forEach(function(key, value) {
      data.set(value.id, value.value);
      // data.push({id: value.id, value: value.value})
    });
    log.info("DATA " + data);
    var json = JSON.stringify(data['_']);  // TODO: dirty hack
    d3.xhr("/cam/set")
    .header("Content-Type", "application/json")
    .post(json, function(err, resp) {
      if (err) {
        log.info("request error: " + err.status + " " + err.statusText);
        return
      }
      guard = true;
      // log.info("got control response: " + resp);
    });
  }
  timer.cb = timercb;

  function apply(meth) {
    d3.event.preventDefault();
    d3.touches(this).forEach(function(touch) {
      // log.info("action:" + meth + " " + touch.identifier);
      stickmap.get(touch.identifier)[meth](touch);
    })
  }

  function selectstick(pos) {
    var stick;
    if (pos[0] < svgwidth / 2) {
      stick = sticks.move;
    } else {
      stick = sticks.look;
    }
    return stick;
  }

  svg
    .on("mousedown", function() {
      d3.event.preventDefault();
      var pos = d3.mouse(this);
      mousestick = selectstick(pos);
      mousestick.start(pos);
    })
    .on("mousemove", function() {
      if (mousestick) {
        mousestick.move(d3.mouse(this));
      }
    })
    .on("mouseup", function() {
      if (mousestick) {
        mousestick.stop();
        mousestick = undefined;
      }
    })
    // TODO: duplicate methods
    .on("mouseleave", function() {
      if (mousestick) {
        log.info("mouse leave");
        mousestick.stop();
        mousestick = undefined;
      }
    })

    .on("touchstart", function() {
      d3.event.preventDefault();
      d3.touches(this).forEach(function(touch) {
        var stick;
        if (touch[0] < svgwidth / 2) {
          stick = sticks.move;
        } else {
          stick = sticks.look;
        }
        stick.start(touch);
        stickmap.set(touch.identifier, stick);
        timer.start();
      })
    })
    .on("touchmove", function() {
      apply.apply(this, ["move"]);
    })
    .on("touchcancel", function() {
      apply.apply(this, ["stop"]);
    })
    .on("touchleave", function() {
      apply.apply(this, ["stop"]);
    })
    .on("touchend", function() {
      d3.event.preventDefault();
      var active = [];  // touches ids that still active
      d3.touches(this).forEach(function(touch) {
        active.push(touch.identifier);
      });
      stickmap.forEach(function(key, value) {
        if (active.indexOf(parseInt(key)) == -1) {
          value.stop();
          stickmap.remove(key);
        }
      });
      if (stickmap.empty()) {
        log.info("no touches left");
        timer.stop();
      }
    })
  ;
})
