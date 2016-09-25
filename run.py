import discord
import asyncio
import subprocess
import os

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!clearall'):
        if str(message.author) == 'TheGooDFeelinG#4615':
            def my_message(m):
                return m.author == client.user
            deleted = await client.purge_from(message.channel)
            await client.send_message(message.channel, 'Deleted {} messages!'.format(len(deleted)))
            await asyncio.sleep(2)
            await client.purge_from(message.channel, check=my_message)

    if message.content.startswith('!search '):
        arg = str(message.content.split('!search ')[1])
        query = "~" + arg + "|"
        print('Query: ' + query) #Debug
        with open('list.txt') as f:
            for num, line in enumerate(f, 1):
                if query.lower() in line.lower():
                    #await bot.send_message(message.channel, 'Found at line ' + str(num)) #Debug
                    error = False
                    break
                else:
                    error = True
        print(error) #Debug
        #There must be a better way than a bool check, but fuck it
        if error is True:
            await client.send_message(message.channel, 'Not found! Try an exact show name, please.')
        elif error is False:
            print(num) #Debug
            print(line) #Debug
            show = arg
            files = int(line.rstrip('\n').split('|')[1])
            #await bot.send_message(message.channel, 'Number of files: ' + str(files)) #Debug
            f=open('list.txt')
            lines=f.readlines()
            i = num
            choice = 1
            p = 1
            await client.send_message(message.channel, 'Show found, check your DMs!')
            await client.send_message(message.author, 'Found ``' + str(files) + '`` doujinshi')
            await client.send_typing(message.author)
            pages = (int(files / 11)) + 1
            await client.send_message(message.author, '[DEBUG] Pages: ' + str(pages))
            if pages == 1:
                print('inside 1 page condition')
                while i < num + files:
                    print(i)
                    currentline = lines[i]
                    name = currentline.rstrip('\n').split(':')[0]
                    await client.send_message(message.author, '``' +str(choice) + '``) ' + name)
                    await client.send_typing(message.author)
                    #await bot.send_message(message.channel, currentline) #Debug
                    choice = choice + 1
                    i = i + 1
                    if choice == files:
                        break
                        await client.send_message(message.author, 'Type a selection to continue...')
                        pick = await client.wait_for_message(timeout=20.0, author=message.author)
                        if pick is None:
                            await client.send_message(message.author, 'Timed out, try again!')
                            return
                        if int(pick.content) <= files:
                            doujinshiline = num + int(pick.content) - 1
                            dump_doujinshi(doujinshiline, message, lines, num)
                            return
                    else:
                        continue
            else: #when there is more than one page
                print('inside +1 page condition!')
                choice = 1
                currentpage = 1
                while currentpage <= pages:
                    print(currentpage)
                    while choice < currentpage * 10 + 1:
                        await client.send_message(message.author, 'Page number ``' + str(currentpage) + '``/``' + str(pages) + '``:')
                        while i < num + files: #for kill la kill is "i < 68 + 13" (which is 81, last line) so this is :ok_hand:
                            print('i: ' + str(i))
                            print('choice: ' + str(choice))
                            print('files; ' + str(files))
                            currentline = lines[i] #starts at index 0, be careful!
                            name = currentline.rstrip('\n').split(':')[0]
                            await client.send_message(message.author, '``' +str(choice) + '``) ' + name)
                            await client.send_typing(message.author)
                            #await bot.send_message(message.channel, currentline) #Debug
                            choice = choice + 1
                            i = i + 1
                            pagesleft = pages - currentpage
                            print('currentpage: ' + str(currentpage * 10 + 1))
                            if choice > currentpage * 10:
                                await client.send_message(message.author, '**Page end reached** (``' + str(pagesleft) + '`` pages left).\nType a selection to continue.\nIf you want to countinue type ``next``. If you want to stop, type ``exit`` instead!')
                                pick = await client.wait_for_message(timeout=20.0, author=message.author)
                                if pick is None:
                                    await client.send_message(message.author, 'Timed out, try again!')
                                    return
                                if pick.content  == "exit":
                                    await client.send_message(message.author, 'Dump cancelled')
                                    return
                                if pick.content == "next":
                                    currentpage = currentpage + 1
                                    break
                                if int(pick.content) <= files:
                                        doujinshiline = num + int(pick.content) - 1
                                        await dump_doujinshi(doujinshiline, message, lines, num)
                                        return
                            if choice > currentpage * 10 or choice == files + 1 and pagesleft == 0:
                                await client.send_message(message.author, '**Last page reached.**\nType a selection to continue or type ``exit`` to cancel')
                                pick = await client.wait_for_message(timeout=20.0, author=message.author)
                                if pick is None:
                                    await client.send_message(message.author, 'Timed out, try again!')
                                    return
                                if pick.content  == "exit":
                                    await client.send_message(message.author, 'Dump cancelled')
                                    return
                                if int(pick.content) <= files:
                                        doujinshiline = num + int(pick.content) - 1
                                        await dump_doujinshi(doujinshiline, message, lines, num)
                                        return

    if message.content.startswith('!listshows'):
        await client.send_message(message.channel, 'Shows in my database: (this might take a while)')
        i = 0
        with open('list.txt') as f:
            lines=f.readlines()
            num_lines = file_len('list.txt')
            l = 0
            i = 1
            print(num_lines)
            while l < num_lines + 1:
                await client.send_typing(message.channel)
                currentline = lines[l]
                print(currentline)
                name = currentline.rstrip('\n').split('|')[0]
                name = name.split('~')[1]
                files = currentline.rstrip('\n').split('|')[1]
                await client.send_message(message.channel, "**·** ``" + name + '`` (``' + files + '`` doujinshis!)')
                l = l + int(files) + 2
                i = i + 1
                pages = (int(i / 11)) + 1
                if i >= 10:
                    howdoicallthis = int(str(i)[:-1])
                else:
                    howdoicallthis = 0
                if pages < howdoicallthis:
                    await client.send_message(message.channel, 'Type ``next`` to show next page or ``exit`` to stop.')
                    pick = await client.wait_for_message(timeout=20.0, author=message.author)
                    if pick.content == "exit":
                        return
                    if pick.content == None:
                        await client.send_message(message.author, 'Timed out, automatically exited!')
                        return
                    if pick.content == "next":
                        continue
                else:
                    pass
        #await client.send_message(message.channel, '[DEBUG] howdoicallthis value: ' + str(howdoicallthis))
        #await client.send_message(message.channel, '[DEBUG] pages value: ' + str (pages))
        #await client.send_message(message.channel, '[DEBUG] i value: ' + str(i))
        await client.send_message(message.channel, 'If you want a show added, use ``!suggest <show name>``')

    if message.content.startswith('!suggest '):
        arg = str(message.content.split('!suggest ')[1])
        await client.send_message(message.channel, 'Running script, searching for ``' + arg + '``...')
        try:
            subprocess.run(["bash", "/media/ero-bot/unpack.bash", arg], cwd="/media/ero-bot", check=True)
        except subprocess.CalledProcessError:
            print('error on script')
            await client.send_message(message.channel, "Bash script error: Couldn't find ``" + arg + '`` Or there was a problem extracting. Try another show name.')
        else:
            await client.send_message(message.channel, 'Doujinshi ``' + arg + '`` successfully added!')
        
    if message.content.startswith('!help '):
        arg = str(message.content.split('!help ')[1])
        commands = ['help', 'search']
        helptext = ['Shows this help message', '''Searchs through all the database with the show name as an argument.```
    Example: ``!search Date A Live`` will show all the ``Date A Live`` doujinshi.''']
        i = 0
        await client.send_message(message.channel, 'Command number: ' + str(len(commands)))
        while i <= int(len(commands)):
            if arg == int(commands[i]):
                error = False
                await client.send_message(message.channel, helptext[i])
                pass
            else:
                await client.send_message(message.channel, '[DEBUG] i after: ' + str(i))
                error = True
                await client.send_message(message.channel, '[DEBUG] error?: ' + str(error))
                i = i + 1
                await client.send_message(message.channel, '[DEBUG] i before: ' + str(i))
        await client.send_message(message.channel, '[DEBUG] arg: ' + arg)
        await client.send_message(message.channel, '[DEBUG] commands: ' + str(commands).strip('[]'))
        if error is True or arg is None:
            await client.send_message(message.channel, '''Commands aviable: ``%s``.
            Use ``!help <command>`` for further help!''') % commands

    if message.content.startswith('!exact'):
        arg = message.content.split('!exact ')[1]
        await client.send_message(message.channel, arg) #Debug
        show = arg.split('; ')[0]
        try:
            name = arg.split('; ')[1]
        except IndexError:
            await client.send_message(message.channel, 'Only one argument given. Try ``!exact <show>; <doujinshi>`` next time!')
            return
        else:
            pass
        #await client.send_message(message.channel, 'Show name: ``' + show + '``\nDoujinshi name: ``' + name + '``') #Debug
        showquery = '~' + show + '|'
        with open('list.txt') as f:
            lines=f.readlines()
            num_lines = file_len('list.txt')
            l = 0
            while l < num_lines:
                currentline = lines[l]
                print(currentline) #Debug
                files = int(currentline.split('|')[1])
                await client.send_typing(message.channel)
                if showquery.lower() in currentline.lower():
                    show = currentline.split('~')[1]
                    show = show.split('|')[0]
                    error = False
                    break
                else:
                    l += files + 2
                    error = True
            if error == True:
                await client.send_message(message.channel, 'Show not found, check show names using ``!listshows``')
                return
            if error == False:
                l = l + 1
                showline = l
                await client.send_message(message.channel, 'Show found!')
                await client.send_message(message.channel, 'Current line: ``' + currentline + '``') #Debug
                await client.send_message(message.channel, '[DEBUG] Max: ' + str(showline + files - 1))
                while l <= showline + files - 1:
                    currentline = lines[l]
                    await client.send_typing(message.channel)
                    if name.lower() in currentline.lower():
                        await client.send_message(message.channel, 'Name found too!')
                        await dump_doujinshi(l, message, lines, showline)
                        return
                    else:
                        #await client.send_message(message.channel, '[DEBUG] Not found, current line is ``' + currentline + '`` and l is ``' + str(l) + '``')
                        l = l + 1


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

async def dump_doujinshi(doujinshiline, message, lines, num):
    currentline = lines[doujinshiline]
    name = currentline.rstrip('\n').split(':')[0]
    await client.send_message(message.author, 'Dumping doujinshi ``' + name + '``! :wink:')
    filename = currentline.rstrip('\n').split(':')[1]
    pages = int(currentline.rstrip('\n').split(':')[2])
    extension = currentline.rstrip('\n').split(':')[3]
    currentline = lines[num - 1]
    print(currentline)
    show = currentline.split('~')[1]
    show = show.split('|')[0]
    #await client.send_message(message.author, '[DEBUG] Line number: ' + str(num))
    #await client.send_message(message.author, '[DEBUG] Full line: ' + line)
    #await client.send_message(message.author, 'Show: ``' + show + '``')
    #await client.send_message(message.author, 'Doujinshi name: ``' + name + '``')
    #await client.send_message(message.author, 'Pages: ``' + str(pages) + '``')
    await client.send_message(message.author, '''Show: ``{}``\nDoujinshi name: ``{}``\nPages: ``{}``'''.format(show, name, str(pages)))
    i = 1
    while i < pages + 1:
        path = "{}/{}/{}{}.{}".format(show, name, filename, str(i), extension)
        #await asyncio.sleep(1) #lib handles ratelimits
        #await client.send_message(message.author, 'Page number ``' + str(i) + '``')
        #await client.send_file(message.author, show + '/' + name + '/' + filename + str(i) + '.' + extension)
        content = "Page ``{}``".format(str(i))
        await client.send_file(message.author, path, content=content)
        print('Sent file ' + str(i))
        i = i + 1
    await client.send_message(message.author, 'Dump finished! :ok_hand:')
    print('Dump finished!')

            
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name + ' (id: ' + client.user.id + ')')
    print('------')
    #print('Opening list.txt')
    #f = open('list.txt', 'r')
    #print('Everything done!')
    #print('------')
    
    
    await client.change_status(discord.Game(name='with doujinshi!'))
token = os.getenv('TOKEN')
client.run(token)
