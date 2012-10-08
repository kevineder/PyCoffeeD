$(function() {
  $("#github").show();
  updateStats();
  var timerId = setInterval(updateStats, 60000); 
});

function updateStats() {
  $("#graph").prop("src", config["graphite-url"] + "/render/?width=612&height=350&_salt=1349559210.774&target=" + config["bucket"] + "&yMax=10.9&from=-2hour&yMin=0&hideGrid=true&hideAxes=false&graphOnly=false&title=Cups&hideLegend=true&tz=America/New_York&lineWidth=2&bgcolor=white&fgcolor=black");

  $.getJSON(config["pycoffeed-url"] + "/stats", function(json) { 
    if (json && json.hasOwnProperty('cups')) {

      $(".hero-unit h1").text("There are " + json['cups'] + " cups of coffee left.");
      $(".hero-unit h2").text("(That's ~" + json['caffeine'] + " of caffeine.)");
      $("#blocker").hide();
    }
    else {
      error();
    }
  }).error(error);

}

function error() {
  $(".hero-unit h1").text("There was a problem retrieving the data.");
  $(".hero-unit h2").text("");
  $("#blocker").hide();
}

