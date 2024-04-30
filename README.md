#  mta_monitor

### Continuously monitors the status of MTA service to see whether a line is delayed or not.
### When a line transitions from not delayed → delayed, you should print the following message to console or to a logfile: “Line <line_name> is experiencing delays”.
### Similarly, when a line transitions from delayed → not delayed, you should print the following message to console or to a logfile: “Line <line_name> is now recovered”.
### Exposes an endpoint called /status, which takes the name of a particular line as an argument and returns whether or not the line is currently delayed.
### Exposes an endpoint called /uptime, which also takes the name of a particular line as an argument and returns the fraction of time that it has not been delayed since inception.
###       - More concretely, “uptime” is defined as 1 - (total_time_delayed / total_time)


#### Run `python base.py` in the backend folder to start the backend server
#### Run `npm start` in the main folder to view in browser
