# Python Discord Bot
## This Discord bot can handle user time in and time outs. 

### Notes
MAIN program is test_attendance2.py
The program is made and tested on a test server using test google service accounts.
Also tested and ran locally on my computer. I haven't quite figured out how and where
to host the bot on the cloud for 24/7 bot uptime.

### General Instruction
1. Create a new Discord bot and add it to your server. You can use the ***Discord Developer Portal*** to create a new bot (new application) and generate a token that you can use to authenticate the bot. In the ***Bot*** section of your new application, click ***Add Bot*** and confirm. This will generate a token for your bot.

2. Set up the necessary libraries and dependencies for the bot. You will need to use the Discord.py library for interfacing with Discord, the Google Sheets API for accessing Google Sheets, and the datetime library for handling dates and times.

3. Create a new Google Sheets spreadsheet and give it a name. Then, create a new Google API project and enable the Google Sheets API for the project. Create a new service account with ***Editor*** permissions and download the JSON credentials file. Rename this file to ***google_sheet_credentials.json*** and place it in the same directory as the Python code.

4. Using the given code, Change the values on the necessary Constants such as:
```
- DISCORD_TOKEN : this is the bot token from the 'new application' from the discord dev portal
- GSPREAD_CREDS : json file from the service account to work with Sheets API
- GSPREAD_SHEET_NAME : the given file name of the sheets created
- SIGN_IN_CHANNEL_ID : get this by right clicking the channel then choose 'Copy ID'
- SIGN_IN_EMOJI : this is to give a color pop for each bot response for easier identification
- COLUMNS : column names or header for the sheets. This can be changed later when necessary
```


### more in-depth guide on creating a new Google API Project:
```
-Go to the Google Cloud Console.
-If you haven't already, create a new Google account or sign in to your existing account.
-Once you're signed in, click the project dropdown menu at the top of the page and select "New Project".
-Give your new project a name and click "Create".
-Once your new project has been created, select it from the project dropdown menu at the top of the page.
-In the left sidebar, click on "APIs & Services" > "Dashboard".
-Click on the "+ ENABLE APIS AND SERVICES" button at the top of the page.
-Search for "Google Sheets API" and select it from the results.
-Click the "Enable" button to enable the Google Sheets API for your project.
-In the left sidebar, click on "APIs & Services" > "Credentials".
-Click the "+ CREATE CREDENTIALS" button at the top of the page and select "Service Account Key".
-Fill out the "Create a service account" form with a name and a role of "Editor".
-Click the "Create" button to create the service account.
-Your browser will automatically download a JSON file containing your service account's private key. 
Rename this file to google_sheet_credentials.json and save it in the same directory as your Python code.
```


### some basic troubleshooting for Google Sheets error ie. Not Found:
```
-Check that the name of the spreadsheet in the GSPREAD_SHEET_NAME constant in your Python code exactly matches the name of 
the spreadsheet in your Google Drive.
-Make sure that you've shared the spreadsheet with the email address associated with the service account you created in the Google Cloud Console.
To do this, open your Google Sheets spreadsheet and click the "Share" button in the top right corner. Then, 
add the email address associated with your service account and give it "Editor" access.
-If you recently created the spreadsheet, make sure that it has fully propagated through Google's servers before trying
to access it with your Python code. This can sometimes take a few minutes.
-Double-check that your google_sheet_credentials.json file is in the correct location and is named correctly. 
It should be in the same directory as your Python code, and the filename should be google_sheet_credentials.json.
```

### some basic troubleshooting for Bot not working properly:
```
-The bot may not be online. Make sure that the bot is running and connected to Discord.
-The bot may not have the necessary permissions to read messages or send messages in the channel. 
Make sure that the bot has the "Read Messages" and "Send Messages" permissions in the channel where you want to use it.
-The bot may not be listening to the correct channel. Double-check that the channel ID in the code matches the one you expect.
-There may be issues with the API keys or authentication credentials for the Google Sheets API. Check that you 
have set up the API keys correctly and that the bot has the necessary permissions to access the Google Sheets API.
```


## sample test runs
![Screenshot of a cmd running the bot](/test0.png)
![Screenshot of a discord commands and bot response_1](/test1.png)
![Screenshot of a discord commands and bot response_2](/test2.png)
