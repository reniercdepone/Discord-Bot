import discord
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Constants
DISCORD_TOKEN = 'MTA4NTc2MjMwNzk2OTI1MzQ1Ng.GKllUs.7fOChWnfRpxkSv3HKlrhyddrSLRr0dDQpGbnrE'
GSPREAD_CREDS = 'google_sheet_credentials.json'
GSPREAD_SHEET_NAME = 'attendance_sheet'
SIGN_IN_CHANNEL_ID = 1085761773333913761
ONSITE_CHANNEL_ID = 1092229176699932832
SIGN_OUT_CHANNEL_ID = 1085761773333913761
BREAK_CHANNEL_ID = 1085761773333913761
SIGN_IN_EMOJI = '✅'
SIGN_OUT_EMOJI = '🟥'
BREAK_EMOJI = '🍎'
END_BREAK_EMOJI = '🍊'
ERROR_EMOJI = '❌'
COLUMNS = ['Date', 'Name', 'Role', 'TimeIn', 'TimeOut', 'Mode','StartBreak', 'Endbreak', 'HoursWorked']

# placeholder dictionary/hash table for user infos
placeholder = {}

# Google Sheets API credentials
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(GSPREAD_CREDS, scope)
client_sheet = gspread.authorize(creds)

# Get the Google Sheet and worksheet
#sheet = client.open(GSPREAD_SHEET_NAME).worksheet(sheet_name)

# Discord bot client
intents = discord.Intents.all()
client = discord.Client(intents=intents)

# Event listener for when the bot is ready
@client.event
async def on_ready():
    print('Bot is ready')
    channel = client.get_channel(SIGN_IN_CHANNEL_ID)
    #channel2 = client.get_channel(ONSITE_CHANNEL_ID)
    await channel.send('Attendance bot is now online!')
    #await channel2.send('Attendance bot (onsite) is now online!')

# Event listener for when a message is received
@client.event
async def on_message(message):

    # get current month and year. Make those the sheetnames
    cur_month = datetime.today().month
    cur_year = datetime.today().year
    sheet_name = f"{cur_month}-{cur_year}"

    # Create a new Google Sheets worksheet if it doesn't already exist
    try:
        worksheet = client_sheet.open(GSPREAD_SHEET_NAME).worksheet(sheet_name)
    except gspread.WorksheetNotFound:
        worksheet = client_sheet.open(GSPREAD_SHEET_NAME).add_worksheet(title=sheet_name, rows="100", cols="20")
        worksheet.append_row(COLUMNS)

    sheet = client_sheet.open(GSPREAD_SHEET_NAME).worksheet(sheet_name)

    # Sign in command for attendance channel - Online
    if message.content.lower() in ['sign in', 'signin'] and message.channel.id == SIGN_IN_CHANNEL_ID:
        # Get user information
        user = message.author.name
        role = message.author.top_role.name
        date = datetime.now().date()
        timein = datetime.now()

        # store in placeholder first - this is to reduce api calls on sheet
        # we will only put values on the sheets once they sign out
        if user in placeholder:
            await message.channel.send(f"{user}, you are already signed in. Did you mean to sign out? {ERROR_EMOJI}")
        else:
            placeholder[user] = {'role':role, 'date':date, 'timein':timein, 'break':False, 'startbreak':None, 'endbreak':None}
            await message.channel.send(f"{user} has signed in.")

    # start break command | attendance channel - Online
    if message.content.lower() == 'break' and message.channel.id == SIGN_IN_CHANNEL_ID:
        user_break = message.author.name
        break_start = datetime.now()
        if user_break not in placeholder:
            await message.channel.send(f"{user_break}, you are not signed in yet. Sign in first before taking a break. {ERROR_EMOJI}")
        elif placeholder[user_break]['break'] == True:
            await message.channel.send(f"{user_break}, you already started/used your break at {placeholder[user_break]['startbreak']} {ERROR_EMOJI}.")
        else:
            placeholder[user_break]['break'] = True
            placeholder[user_break]['startbreak'] = break_start
            await message.channel.send(f"{user_break} is now on a break. {BREAK_EMOJI}")
    
    # end break command | attendance channel - Online
    elif message.content.lower() == 'end break' and message.channel.id == SIGN_IN_CHANNEL_ID:
        user_break2 = message.author.name
        break_end = datetime.now()
        if user_break2 not in placeholder:          
            await message.channel.send(f"{user_break2}, you are not signed in yet. Sign in first. {ERROR_EMOJI}")
        if placeholder[user_break2]['break'] == False:
            await message.channel.send(f"{user_break2}, you need to start your break first before ending it. {ERROR_EMOJI}")
        else:
            placeholder[user_break2]['endbreak'] = break_end
            placeholder[user_break2]['break'] = False
            await message.channel.send(f"{user_break2} finished their break. {END_BREAK_EMOJI}")

    # Sign out command | attendance channel - Online
    elif message.content.lower() in ['sign out', 'signout'] and message.channel.id == SIGN_OUT_CHANNEL_ID:
        user_out = message.author.name
        if user_out not in placeholder:
            await message.channel.send(f"{user_out}, you are not signed in yet. Sign in first before signing out. {ERROR_EMOJI}")
        elif 'break' in placeholder[user_out] and placeholder[user_out]['break'] == True:
            await message.channel.send(f"{user_out}, you need to end your break first before signing out {ERROR_EMOJI}")
        else:
            timeout = datetime.now()
            placeholder[user_out]['timeout'] = timeout
            hours_worked = timeout - placeholder[user_out]['timein']
            placeholder[user_out]['hours'] = hours_worked
            
            row = [placeholder[user_out]['date'].strftime('%Y-%m-%d'), user_out, placeholder[user_out]['role'], placeholder[user_out]['timein'].strftime('%H:%M:%S'),
                    placeholder[user_out]['timeout'].strftime('%H:%M:%S'), 'Online',
                    None if placeholder[user_out]['startbreak'] == None else placeholder[user_out]['startbreak'].strftime('%H:%M:%S'),
                    None if placeholder[user_out]['endbreak'] == None else placeholder[user_out]['endbreak'].strftime('%H:%M:%S'),
                    str(hours_worked)]
            
            sheet.append_row(row)
            await message.channel.send(f"{user_out} has signed out. {SIGN_OUT_EMOJI}")
            del placeholder[user_out]


# Start the bot
client.run(DISCORD_TOKEN)

