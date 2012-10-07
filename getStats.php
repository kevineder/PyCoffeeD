<?
  $ch = curl_init(); 
  curl_setopt($ch, CURLOPT_URL, "http://tools.calendr.labs.hugeinc.com:8000/render/?width=612&height=350&_salt=1349559210.774&target=stats.gauges.coffee.cups&yMax=10.9&from=-2hour&yMin=0&hideGrid=true&hideAxes=false&graphOnly=false&title=Cups&hideLegend=true&tz=America/New_York&lineWidth=2&bgcolor=white&fgcolor=black&format=json"); 
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1); 
  $output = curl_exec($ch); 
  curl_close($ch);   

  print $output;
?>
