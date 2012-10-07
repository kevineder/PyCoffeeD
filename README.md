PyCoffeeD
=========

PyCoffeeD is a fork of the CoffeeD project, rewritten in Python. Like the original CoffeeD, it measures the number of cups of coffee remaining in a coffee pot, using a USB scale and [StatsD](https://github.com/etsy/statsd). It can also tweet. 

This fork was created in tandem with the original CoffeeD author, [morria](https://github.com/morria).

Tested against [DYMO by Pelouze 10 lb. USB Mailing Scale](http://www.amazon.com/DYMO-Pelouze-lb-Mailing-Scale/dp/B001B0EYSW/)

Installation
------------
These instructions assume you already have a [StatsD](https://github.com/etsy/statsd)/[Graphite](http://graphite.wikidot.com/) server in place.
* Clone the repo.
* Install the dependencies
				`sudo pip install -r ./requirements.txt`
* Update CoffeeD.py with the vendor / product ID of your USB scale. Find this info using:
				`sudo lsusb -v`
* Copy config.ini.sample to config.ini and update it with your Twitter info, StatsD server URL, and webapp URL.
* Copy static/config.js.sample to static/config.js and update it with your Graphite server URL, Graphite bucket key, and webapp URL.

Run the web app
------
	python CoffeeD.py

Stats job
--------
* A seperate script can be executed to keep your StatsD server and Twitter handle up-to-date. You'll need to kickoff the job once manually to validate with Twitter:
				`python stats-job/StatsJob.py`
* After that the first run a cron job can kick it off:
				`* * * * *  /usr/bin/python /project/dir/stats-job/StatsJob.py > /project/dir/stats-job/log.txt`
