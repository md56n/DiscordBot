import discord
import asyncio
from random import randint
import time

#save token to text file
token = open('token.txt', 'r').read()

#start discord client
client = discord.Client()

#when connected
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

#when message is sent
@client.event
async def on_message(message):

    print(f'{message.channel}: {message.author}: {message.author.name}: {message.content}')

    #if the message was sent by an account other than this bot
    if message.author.name != 'GambleBot':
        
        #save username
        username = message.author.name+message.author.discriminator
        users = []
        money = 0

        #read saved user data
        inf = open('users.txt', 'w+')
        newa = inf.readlines()
        if len(newa) > 0:
            for line in newa:
                line=line.rstrip('\n')
                currentline = line.split(',')
                users.append([currentline[0], currentline[1]])
        inf.close()

        #if no user information, add message author
        if len(users) == 0:
            users.append([username, 100])
            print(users)
            with open('users.txt', 'w') as f:
                for _string in users:
                    f.write(_string[0]+','+str(_string[1])+'\n')
        else:
            #if message author not in data, add
            valid = False
            for x in users:
                if x[0] == username:
                    valid = True
            if valid == False:
                users.append([username, 100])
                print(users)
                with open('users.txt', 'w') as f:
                    for _string in users:
                        f.write(_string[0]+','+str(_string[1])+'\n')


        #if message author gives bot a commend
        if 'bot' in message.content.lower():
            
            #save message author's money
            for i in users:
                if i[0] == username:
                    money = int(i[1])

            #limit message author's bet ammount
            possible_numbers = []
            for i in range(1, 1001):
                possible_numbers.append(str(i))

            #if message author's bet is valid, save bet
            if len(message.content) > 0:
                for i in possible_numbers:
                    if i in message.content:
                        if int(i)<=money:
                            bet = int(i)
                        else:
                            await message.channel.send(content='You cannot bet more than you have')

            #if message author asks for rules
            if 'rules' in message.content.lower():
                await message.channel.send(content= (
                    'bot money = see your balance \n'
                    'bot top = scoreboard \nbot coin = coinflip \n'
                    'bot slots = slots \n'
                    'bot guess = guess a letter between a and e \n'
                    'bot rps = rock paper scissors \n'
                    'bot light = red light green light'))

            #if message author wants to see the scoreboard
            if 'top' in message.content.lower():
                users.sort(key=lambda x: int(x[1]), reverse=True)
                print(users)
                stre = ''
                for x in users:
                    stre+=x[0]+': '+x[1]+'\n'
                await message.channel.send(content='SCORES: \n'+stre)

            #if message author wants to play a guessing game
            if 'guess' in message.content.lower():
                answer = randint(0, 4)
                
                #if the message author correctly guessed 'a'
                if (answer == 0) and ('a' in message.content.lower()):
                    await message.channel.send(content='You won '+str(bet*1000))
                    money += (bet*1000)

                #if the message author correctly guessed 'b'
                elif (answer == 1) and ('b' in message.content.lower()):
                    await message.channel.send(content='You won '+str(bet*1000))
                    money += (bet*1000)

                #if the message author correctly guessed 'c'
                elif (answer == 2) and ('c' in message.content.lower()):
                    await message.channel.send(content='You won '+str(bet*1000))
                    money += (bet*1000)

                #if the message author correctly guessed 'd'
                elif (answer == 3) and ('d' in message.content.lower()):
                    await message.channel.send(content='You won '+str(bet*1000))
                    money += (bet*1000)

                #if the message author correctly guessed 'e'
                elif (answer == 4) and ('e' in message.content.lower()):
                    await message.channel.send(content='You won '+str(bet*1000))
                    money += (bet*1000)
                            
                #if message author guessed incorrectly
                else:
                    await message.channel.send(content='You lost '+str(bet))
                    money -= bet


            #if message author wants to check their balance
            if 'money' in message.content.lower():
                await message.channel.send(content='You have '+str(money))

                #if message author is broke, add more
                if money < 1:
                    money = 100
                    for i in users:
                        if i[0] == username:
                            i[1] = money
                    with open('users.txt', 'w') as f:
                        for _string in users:
                            f.write(_string[0]+','+str(_string[1])+'\n')
                    await message.channel.send(content='Restart. Now you have '+str(money))

            #if message author wants to play flip a coin
            if 'coin' in message.content.lower():

                #save message author's guess
                if 'heads' in message.content.lower():
                    guess='heads'
                if 'tails' in message.content.lower():
                    guess='tails'

                #play animation
                message = await message.channel.send(content=':full_moon:')
                time.sleep(0.5)
                await message.edit(content=':new_moon:')
                time.sleep(0.5)
                await message.edit(content=':full_moon:')
                time.sleep(0.5)
                await message.edit(content=':new_moon:')
                time.sleep(0.5)
                await message.edit(content=':full_moon:')

                #flip coin
                value = randint(0, 1)

                #if the coin is heads
                if value == 0:
                    
                    #if message author correctly guessed heads
                    if guess == 'heads':
                        await message.channel.send(content='Heads! You won '+str(bet))
                        money += bet

                    #if message author incorrectly guessed tails
                    else:
                        await message.channel.send(content='Heads! You lost '+str(bet))
                        money -= bet

                #if the coin is tails
                elif value == 1:

                    #if message author correctly guessed tails
                    if guess == 'tails':
                        await message.channel.send(content='Tails! You won '+str(bet))
                        money += bet

                    #if message author incorrectly guessed heads
                    else:
                        await message.channel.send(content='Tails! You lost '+str(bet))
                        money -= bet

                #update and save users money to text file
                for i in users:
                    if i[0] == username:
                        i[1] = money
                with open('users.txt', 'w') as f:
                    for _string in users:
                        f.write(_string[0]+','+str(_string[1])+'\n')

                #if message author is out of money, add more
                if money<= 1:
                    await message.channel.send(content='You are broke')
                    money = 100

                        
            #if message author wants to play slots                      
            if 'slots' in message.content.lower():

                #print slots on discord
                slots=[]
                message = await message.channel.send(content=slots)
                for i in range(0, 3):
                    value = randint(0, 3)
                    if value == 0:
                        slots.append(':tangerine:')
                        await message.edit(content=slots)
                    if value == 1:
                        slots.append(':banana:')
                        await message.edit(content=slots)
                    if value == 2:
                        slots.append(':watermelon:')
                        await message.edit(content=slots)
                    if value == 3:
                        slots.append(':strawberry:')
                        await message.edit(content=slots)

                #if slots matches on tangerine
                if slots[0] == slots[1] == slots[2] == ':tangerine:':
                    money += bet
                    await message.channel.send(content='You won '+str(bet))

                #if slots matches on banana
                elif slots[0] == slots[1] == slots[2] == ':banana:':
                    money += (bet*2)
                    await message.channel.send(content='You won '+str(bet))

                #if slots matches on watermelon
                elif slots[0] == slots[1] == slots[2] == ':watermelon:':
                    money += (bet*2)
                    await message.channel.send(content='You won '+str(bet*2))

                #if slots matches on strawberry
                elif slots[0] == slots[1] == slots[2] == ':strawberry:':
                    money += (bet*3)
                    await message.channel.send(content='You won '+str(bet*3))

                #if slots did not match
                else:
                    await message.channel.send(content='You lost '+str(bet))
                    money -= bet


            #if message author wants to play rock paper scissors
            if 'rps' in message.content.lower():            
                userplays=''
                pcplays=''
                userid = str(message.author.id)
                choices = ['🗿', '📄', '✂']

                #print game and wait for response
                message = await message.channel.send(content='Rock, Paper, Scissors \nChoose one:')
                for i in choices:
                    await message.add_reaction(i)

                def checkfor(reaction, user):
                    return str(user.id) == userid and str(reaction.emoji) in choices
                
                loopclose = 0
                while loopclose == 0:
                    try:
                        reaction, user = await client.wait_for('reaction_add', timeout=10, check=checkfor)

                        #if message author plays rock
                        if reaction.emoji == '🗿':
                            userplays = '🗿'

                            #get bot move
                            value = randint(0, 2)

                            #if bot plays rock
                            if value == 0:
                                pcplays = '🗿'
                                await message.edit(content=userplays+' vs '+pcplays+'\nTie')

                            #if bot plays paper
                            elif value == 1:
                                pcplays = '📄'
                                money -= (bet)
                                await message.edit(content=userplays+' vs '+pcplays+'\nYou lost '+str(bet))

                            #if bot plays scissors
                            elif value == 2:
                                pcplays = '✂'
                                money += (bet)
                                await message.edit(content=userplays+' vs '+pcplays+'\nYou won '+str(bet))

                        #if message author plays paper
                        elif reaction.emoji == '📄':
                            userplays = '📄'

                            #get bot move
                            value = randint(0, 2)
                            if value == 0:
                                pcplays = '🗿'
                                money += (bet)
                                await message.edit(content=userplays+' vs '+pcplays+'\nYou won '+str(bet))
                            elif value == 1:
                                pcplays = '📄'
                                await message.edit(content=userplays+' vs '+pcplays+'\nTie')
                            elif value == 2:
                                pcplays = '✂'
                                money -= (bet)
                                await message.edit(content=userplays+' vs '+pcplays+'\nYou lost '+str(bet))

                        #if message author plays rock
                        elif reaction.emoji == '✂':
                            userplays = '✂'

                            #get bot move
                            value = randint(0, 2)
                            if value == 0:
                                pcplays = '🗿'
                                money -= (bet)
                                await message.edit(content=userplays+' vs '+pcplays+'\nYou lost '+str(bet))
                            elif value == 1:
                                pcplays = '📄'
                                money += (bet)
                                await message.edit(content=userplays+' vs '+pcplays+'\nYou won '+str(bet))
                            elif value == 2:
                                pcplays = '✂'
                                await message.edit(content=userplays+' vs '+pcplays+'\nTie')
                    
                    #if message author does not play in time
                    except asyncio.TimeoutError:
                        if userplays == '':
                           await message.edit(content='timeout')
                        loopclose = 1


            #if message author wants to play red light green light
            if 'light' in message.content.lower():
                userid = str(message.author.id)

                #print game and wait for response
                message = await message.channel.send(content='Light: \n:green_circle:')
                await message.add_reaction('👍')
                    
                def checkfor(reaction, user):
                    return str(user.id) == userid and str(reaction.emoji) in ['👍']
                
                loopclose = 0
                count = 0
                timer = randint(3, 10)
                while loopclose == 0:
                    #count message author's input
                    try:
                        reaction, user = await client.wait_for('reaction_add', timeout=timer, check=checkfor)
                        if reaction.emoji == '👍':
                            count += 1

                    #when time runs out
                    except asyncio.TimeoutError:
                        await message.edit(content='Light: \n:red_circle:')
                        loopc = 0
                        donec = count
                        while loopc == 0:
                            #if message author gives input after game ends, take away points
                            try:
                                reaction, user = await client.wait_for('reaction_add', timeout=2, check=checkfor)
                                if reaction.emoji == '👍':
                                    donec = 0
                            
                            except asyncio.TimeoutError:                            
                                loopc = 1
                        
                        if donec == 0 :
                            money -= (bet)
                            await message.edit(content='You lost '+str(bet))
                        elif donec > 0:
                            money += (bet*donec)
                            await message.edit(content='You got '+str(donec)+' clicks \nYou won '+str(bet*donec))
                        loopclose = 1


            #update and save users money to text file
            for i in users:
                if i[0] == username:
                    i[1] = money
            with open('users.txt', 'w') as f:
                for _string in users:
                    f.write(_string[0]+','+str(_string[1])+'\n')


client.run(token)  # recall token saved

#client id 775090461152116816
#permission int 8
