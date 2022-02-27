import requests
import csv
from discord_webhook import DiscordWebhook, DiscordEmbed
import json


class Webhook:
    def __init__(self,webhook):
        self.webhook = webhook

    def send_webhook(self,description,params={}):
        webhook = DiscordWebhook(url=self.webhook, username="GenesisAIO Logger")

        embed = DiscordEmbed(title=params['title'], description=description, color=10038562)
        embed.set_author(name='GenesisAIO', icon_url='https://media.discordapp.net/attachments/904022469512396861/904022677109497907/Genesis_AIO_logo_black.png?width=676&height=676')
        embed.set_footer(text='GenesisAIO',icon_url='https://media.discordapp.net/attachments/904022469512396861/904022681043759104/Genesis_AIO_logo_final.png?width=676&height=676')
        embed.set_timestamp()

        for i in params:
            if params[i] == 'title':
                continue

            embed.add_embed_field(name=params[i], value=i[0],inline=i[1])

        webhook.add_embed(embed)
        response = webhook.execute()



class Data:
    def loadProxies(self,directory):
        proxies = []
        with open(directory,'r') as e:
            e = e.readlines()
            for i in e:
                i = i.strip().split(':')
                proxies.append({'http':'http://{}:{}@{}:{}/'.format(i[2],i[3],i[0],i[1]),'https':'https://{}:{}@{}:{}/'.format(i[2],i[3],i[0],i[1])})

        if proxies == []:
            proxies.append(None)
        return proxies

    def csvToJson(self,directory):
        count = -1
        headers = []

        json_file = {}
        with open(directory,'r') as e:
            csvreader = csv.reader(e)
            
            for i in csvreader:
                count += 1
                if count == 0:
                    headers = i
                    continue
                
                count_2 = -1
                json_file[str(count)] = {}

                for k in i:
                    count_2 += 1
                    
                    
                    json_file[str(count)][headers[count_2]] = k

        return json_file

    def txtToList(self,directory):
        l = []
        with open(directory,'r') as e:
            e = e.readlines()
            for i in e:
                i = i.strip()
                l.append(i)

        return l

    def loadJson(self,directory):
        with open(directory) as e:
            return json.load(e)