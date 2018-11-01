#
# Change id for your location
# Toronto : 6167865
# Tokyo : 1850147
# Osaka : 1853909
#
# Change appid - get your API KEY from https://openweathermap.org 
#
SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
wget -O ${SCRIPTPATH}/current-data.json 'http://api.openweathermap.org/data/2.5/weather?id=6167865&&units=metric&appid=TYPE_YOUR_API_KEY_HERE'
wget -O ${SCRIPTPATH}/forecast-data.json 'http://api.openweathermap.org/data/2.5/forecast?id=6167865&units=metric&appid=TYPE_YOUR_API_KEY_HERE'

