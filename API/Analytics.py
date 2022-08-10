import asyncio
import httpx
import requests
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from .RiotAPI.RiotConfig import config
from .RiotAPI import RiotAPI
# from RiotAPI.RiotConfig import config
# from RiotAPI import RiotAPI
import time


class GameAnalytics(RiotAPI):

	def __init__(self, region, match_id):
		super().__init__(region)
		self.time_line = super().matche_timeline_v5(match_id)
		self.match_info = super().match_info_v5(match_id)
		summoners = self.match_info['info']['participants']
		self.summonersDataFrame = pd.DataFrame(
			summoners,
			columns=['participantId', 'puuid', 'summonerId', 'summonerName', 'summonerLevel', 'championName', 'teamPosition'],
			index=np.arange(10)+1
		)
		self.match_id = match_id
		self.last_frame = self.time_line['info']['frames'][-1]
		self.game_duration = self.last_frame['timestamp'] / 60000  # in min

	def summoners_stat(self):
		clean_summs_stat = [
			{
				'match_id': self.match_id,
				'scor': {
					'kills': user_game_data['kills'],
					'assists': user_game_data['assists'],
					'deaths': user_game_data['deaths'],
					# 'kda': '{0:.2f}'.format((int(user_game_data["assists"]) + int(user_game_data["kills"])) / int(user_game_data["deaths"]))
				},
				'champ_data': {
					'participantId': user_game_data['participantId'],
					'champion_name': user_game_data['championName'],
					'position': user_game_data['individualPosition'],
					'champ_icon_url': 'http://ddragon.leagueoflegends.com/cdn/12.14.1/img/champion/{0}.png'.format(user_game_data["championName"])
				},
				'items': [
					f'http://ddragon.leagueoflegends.com/cdn/12.14.1/img/item/{user_game_data["item0"]}.png',
					f'http://ddragon.leagueoflegends.com/cdn/12.14.1/img/item/{user_game_data["item1"]}.png',
					f'http://ddragon.leagueoflegends.com/cdn/12.14.1/img/item/{user_game_data["item2"]}.png',
					f'http://ddragon.leagueoflegends.com/cdn/12.14.1/img/item/{user_game_data["item3"]}.png',
					f'http://ddragon.leagueoflegends.com/cdn/12.14.1/img/item/{user_game_data["item4"]}.png',
					f'http://ddragon.leagueoflegends.com/cdn/12.14.1/img/item/{user_game_data["item5"]}.png',
				],
				'summoner_spals': {
					'1': f'{self.summoners_skils[user_game_data["summoner1Id"]]}',
					'2': f'{self.summoners_skils[user_game_data["summoner2Id"]]}'
				}
			}
			for user_game_data in self.match_info['info']['participants']
		]
		return clean_summs_stat


class UserAnalytics(RiotAPI):
	"""docstring for User"""
	def __init__(self, user_name, region):
		super().__init__(region=region)
		user_data = super().get_user_data(user_name)
		self.user_data = user_data
		self.id = user_data['id']
		self.accountId = user_data['accountId']
		self.puuid = user_data['puuid']
		self.name = user_data['name']

	def __str__(self):
		return f'name: {self.name}\nid: {self.id}\naccountId: {self.accountId}\npuuid: {self.puuid}'

# user statistic and other general data

	def user_rank(self):
		return super().user_rank(self.id)

	def user_stat_on_champ(self, champ_id):
		return super().user_stat_on_champ(champ_id, self.id)

# matchs info
	def match_info_v5(self, game_id):
		return super().match_info_v5(game_id)

	def matche_timeline_v5(self, game_id):
		return super().matche_timeline_v5(game_id)

	def user_last_games(self):
		return super().user_last_games(self.puuid)

	def user_stat_in_game(self, game_id):
		return super().user_stat_in_game(game_id, self.name)

	def short_stat_in_game(self, game_id):
		user_game_data = super().user_stat_in_game(game_id, self.name)
		clean_data = {
			'game_id': game_id,
			'scor': {
				'kills': user_game_data['kills'],
				'assists': user_game_data['assists'],
				'deaths': user_game_data['deaths'],
				# 'kda': '{0:.2f}'.format((user_game_data["assists"] + user_game_data["kills"]) / user_game_data["deaths"])
			},
			'champ_data': {
				'champion_name': user_game_data['championName'],
				'position': user_game_data['individualPosition'],
				'champ_icon_url': 'http://ddragon.leagueoflegends.com/cdn/12.14.1/img/champion/{0}.png'.format(user_game_data["championName"])
			},
			'items':[
				f'http://ddragon.leagueoflegends.com/cdn/12.14.1/img/item/{user_game_data["item0"]}.png',
				f'http://ddragon.leagueoflegends.com/cdn/12.14.1/img/item/{user_game_data["item1"]}.png',
				f'http://ddragon.leagueoflegends.com/cdn/12.14.1/img/item/{user_game_data["item2"]}.png',
				f'http://ddragon.leagueoflegends.com/cdn/12.14.1/img/item/{user_game_data["item3"]}.png',
				f'http://ddragon.leagueoflegends.com/cdn/12.14.1/img/item/{user_game_data["item4"]}.png',
				f'http://ddragon.leagueoflegends.com/cdn/12.14.1/img/item/{user_game_data["item5"]}.png',
			],
			'summoner_spals': {
				'1': f'{self.summoners_skils[user_game_data["summoner1Id"]]}',
				'2': f'{self.summoners_skils[user_game_data["summoner2Id"]]}'
			}
		}
		return clean_data

# info about current games
	def current_game(self):
		return super().current_game(self.id)

	def activeplayer_data_local(self):
		URL = f"https://127.0.0.1:2999/liveclientdata/activeplayer"
		respons = requests.get(URL, verify=False).json()
		return respons


# ASYNC
# async user statistic and other general data

	async def user_rank_async(self):
		return await super().user_rank_async(self.id)

	async def user_stat_on_champ_async(self, champ_id):
		return await super().user_stat_on_champ_async(champ_id, self.id)

# async matchs info
	async def match_info_v5_async(self, game_id):
		return await super().match_info_v5_async(game_id)

	async def matche_timeline_v5_async(self, game_id):
		return await super().matche_timeline_v5_async(game_id)

	async def user_last_games_async(self):
		return await super().user_last_games_async(self.puuid)

	async def user_stat_in_game_async(self, game_id):
		return await super().user_stat_in_game_async(game_id, self.name)

	async def short_stat_in_game_async(self, game_id):
		user_game_data = await super().user_stat_in_game_async(game_id, self.name)
		clean_data = {
			'game_id': game_id,
			'gameStartTimestamp': user_game_data['gameStartTimestamp'],
			'scor': {
				'kills': user_game_data['kills'],
				'assists': user_game_data['assists'],
				'deaths': user_game_data['deaths'],
				# 'kda': '{0:.2f}'.format((user_game_data["assists"] + user_game_data["kills"]) / user_game_data["deaths"])
			},
			'champ_data': {
				'champion_name': user_game_data['championName'],
				'position': user_game_data['individualPosition'],
				'champ_icon_url': 'http://ddragon.leagueoflegends.com/cdn/12.14.1/img/champion/{0}.png'.format(user_game_data["championName"])
			},
			'items':[
				f'http://ddragon.leagueoflegends.com/cdn/12.14.1/img/item/{user_game_data["item0"]}.png',
				f'http://ddragon.leagueoflegends.com/cdn/12.14.1/img/item/{user_game_data["item1"]}.png',
				f'http://ddragon.leagueoflegends.com/cdn/12.14.1/img/item/{user_game_data["item2"]}.png',
				f'http://ddragon.leagueoflegends.com/cdn/12.14.1/img/item/{user_game_data["item3"]}.png',
				f'http://ddragon.leagueoflegends.com/cdn/12.14.1/img/item/{user_game_data["item4"]}.png',
				f'http://ddragon.leagueoflegends.com/cdn/12.14.1/img/item/{user_game_data["item5"]}.png',
			],
			'summoner_spals': {
				'1': f'{self.summoners_skils[user_game_data["summoner1Id"]]}',
				'2': f'{self.summoners_skils[user_game_data["summoner2Id"]]}'
			}
		}
		return clean_data

# async info about current games
	async def current_game_async(self):
		return await super().current_game_async(self.id)


I = 'IIIHeNaIII'
game_id = 'RU_403490124'

if __name__ == '__main__':
	client = GameAnalytics('ru', game_id)
	print(client.summoners_stat())
	# user_data = {'status_code': 'da',
	# 			 's_name': I,
	# 			 'region': 'ru'}
	# last_games_data = {'games_data': [client.short_stat_in_game(game_id) for game_id in client.user_last_games()]}

	# kills # assists # deaths # champLevel
	# championName
	# individualPosition
	# "item0": 3152,
	# "item1": 3020,
	# "item2": 1056,
	# "item3": 3135,
	# "item4": 3157,
	# "item5": 1058,
	# "item6": 3340,
	# Item Assets
	# http://ddragon.leagueoflegends.com/cdn/12.14.1/img/item/1001.png
	#
	# champ icon
	# http: // ddragon.leagueoflegends.com / cdn / 12.14.1 / img / champion / Aatrox.png
	#
	# SummonerSpells
	# http: // ddragon.leagueoflegends.com / cdn / 12.14.1 / img / spell / SummonerFlash.png
	#
	# runs
	# http://ddragon.leagueoflegends.com/cdn/12.14.1/data/en_US/runesReforged.json
