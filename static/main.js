var config = {
  "graphite-url" : "http://tools.calendr.labs.hugeinc.com:8000",
  "bucket" : "stats.gauges.coffee.cups",
  "pycoffeed-url" : "http://192.168.1.101:5000",
};

$(function() {
  $("#github").show();
  updateStats();
});

function updateStats() {
  $("#graph").prop("src", config["graphite-url"] + "/render/?width=612&height=350&_salt=1349559210.774&target=" + config["bucket"] + "&yMax=10.9&from=-2hour&yMin=0&hideGrid=true&hideAxes=false&graphOnly=false&title=Cups&hideLegend=true&tz=America/New_York&lineWidth=2&bgcolor=white&fgcolor=black");

  //$.getJSON(config["pycoffeed-url"] + "/stats", function(json) { 
  //  console.log(json);
  //  if (json && json.hasOwnProperty('cups')) {

  //    $(".hero-unit h1").text("There are " + json['cups'] + " cups of coffee left.");
  //    $(".hero-unit h2").text("(That's " + json['caffeine'] + " of caffeine.)");
  //    $("#blocker").hide();
  //  }
  //  else {
  //    $(".hero-unit h1").text("There was a problem retrieving the data.");
  //    $(".hero-unit h2").text("");
  //    $("#blocker").hide();
  //  }
  //});

  $.getJSON("/getStats.php", function(json) { 
    json = json[0];
    console.log(json);
    if (json && json.hasOwnProperty('datapoints') && json.datapoints.length > 0) {
      var cups = Math.round(100 * json['datapoints'][json.datapoints.length-2][0])/100;
      var caffeine = Math.round(100 * ((cups * 8)/8.5) * 49)/100;
      $(".hero-unit h1").text("There are " + cups + " cups of coffee left.");
      $(".hero-unit h2").text("(That's ~" + caffeine + "mg of caffeine.)");
      $("#blocker").hide();
    }
    else {
      $(".hero-unit h1").text("There was a problem retrieving the data.");
      $(".hero-unit h2").text("");
      $("#blocker").hide();
    }
  });

}

