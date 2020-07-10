# Runescape Grand Exchange Web Scrapper
A Python 3.7 webscrapper script that grabs information from Runescape Service and  Runescape Wiki to get daily prices and alchemy profits. The script will grab the prices of items and store them onto the Firebase Live Database.

## Usage Instruction
	1. Setup a Firebase account with instruction from [here](https://firebase.google.com/docs/database/web/start)
	2. In the setting of Firebase Console, go to project overview and grab the info from the Firebase SDK snippet and fill in the the `<config-template.py>` and rename it to `<config.py>` :
	![config_info](https://github.com/MisterSoandSo/RS_GE_Scrapper/media/config.png)
	3. Run '<python RS_FIRE_GE.py>' to populate your own database.

## Plans
-  [] Created an updated list of valid Exchange ID to speed up information gathering
-  [] Gather alchemy gp values to add into database
-  [] Create a gui to handle search and usage

## Dependency
- [RS Grand Exchange API Request](http://services.runescape.com/m=itemdb_rs/api/catalogue/detail.json?item=)
- [Firebase](https://console.firebase.google.com/)

## Bugs 
- 


