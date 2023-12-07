# strava-cli
Strava-cli is a command line tool for querying and parsing your Strava data. 
It's a standalone application using your personal API token. 
All client secrets and data are stored locally on your machine without the need to send them to a remote server or give access rights to any 3rd parties.

Strava-cli parser supports any Linux shell terminal, as well as the Windows PowerShell.


## Installation
Installation from source files is done by calling `make install`. 
It creates a pip distributable package and installs it to user path.

Binary distributable files are available from the `Releases` tab in the GitHub repo.


## Setup
First, we need to create a directory structure and all relevant files for the app. 
```shell
strava-cli authorize
```
Next step is to create a personal Strava API application at https://www.strava.com/settings/api. 
The app will ask you to fill in client secret and client ID to config located in the user home directory at `.config/strava-cli/config.json`. \ 
After that, we can rerun the command. 
```shell
strava-cli authorize
```
Follow the displayed link to authorize the app to access user's activity data.

Now we're ready to download activies to local storage. 
```shell
strava-cli download
``` 
Note that this may take a few seconds, depending on the quantity of activities. \
Rerun this command every time you want to update activities in the local storage.

## Usage examples
The tool follows common CLI argument standards and flags can be chained. \
`strava-cli --help` lists all possible flags. \
Running without any flags returns list of all activities present in the local storage. 

Show activities that match the name "Morning Run".  
```shell
strava-cli --name 'Morning Run'
```
Show only activities of a specific sport type.  
```shell
strava-cli --type 'Hike'
```
Limit the result to maximum number of *5* activities.
```shell
strava-cli --limit 5
```

### Filtering by specific attribute values
All attribute filters are specified as "symbol value" string where symbol is one of [>, <, ==, >=, <=] \
Available attributes to filter by: [distance, elevation_gain, average_heartrate, moving_time, average_speed, average_pace, date]


Show activities with distance greater than 100km.  
```shell
strava-cli --distance '> 100'
```
Show activities that happened after 6th December 2023.  
```shell
strava-cli --date '> 2023-12-06'
```
Show activities that took less than 30min.  
```shell
strava-cli --moving_time '< 0:30:00'
```
Show activities that took less than 30min.  
```shell
strava-cli --moving_time '< 0:30:00'
```

### Sorting
Resulting activities can also be sorted, by specifying attribute and order as 'attribute_name:[desc/asc]'.

Show activities sorted by distance from the largest to smallest.
```shell
strava-cli --sortby 'distance:desc'
```

## Contact
In case of any question, don't hesitate to contact me at radoslave0@gmail.com.
