$(function() {
  $("#github").show();
  updateStats();
  var timerId = setInterval(updateStats, 60000); 
});

function updateStats() {
  $("#graph").prop("src", config["graphite-url"] + "/render/?width=612&height=350&_salt=1349559210.774&target=" + config["bucket"] + "&yMax=10.9&from=-2hour&yMin=0&hideGrid=true&hideAxes=false&graphOnly=false&title=Cups&hideLegend=true&tz=America/New_York&lineWidth=2&bgcolor=white&fgcolor=black");

  //$.getJSON(config["pycoffeed-url"] + "/stats", function(json) { 
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
    if (json && json.hasOwnProperty('datapoints') && json.datapoints.length > 0) {

      //For some reason graphite occasionally returns null for the most recent statistic.
      var cups = json['datapoints'][json.datapoints.length-1][0];

      if (!cups) {
        cups = json['datapoints'][json.datapoints.length-2][0];
      }

      cups = Math.round(100 * cups)/100;
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

