import httpx
import requests
from .RiotConfig import config

IIIHeNaIII = 'IIIHeNaIII'


class RiotAPI(object):
	"""docstring for RiotAPI"""
	summoners_skils = {
		1: '1',
		2: '2',
		3: 'Exhaust',
		4: 'Flesh',
		5: '5',
		6: 'Ghost',
		7: 'Heal',
		8: '8',
		9: '9',
		10: '10',
		11: 'Smite',
		12: 'Teleport',
		13: '13',
		14: 'Ignite',
		21: 'Barrier'
	}
	languages = {
		'eun1': 'en_US',
		'ru': 'ru_RU',
		'euw1': 'en_US',
		'kr': 'ko_KR',
	}
	regions_v5 = {
		'americas': ['la2', 'na1', 'oc1'],
		'asia': ['jp1', 'kr', 'tr1'],
		'europe': ['eun1', 'ru', 'euw1', 'br1'],
		'sea': ['la1'],
	}

	def __init__(self, region):
		self.token = config['token']
		self.HOST = f'https://{region}.api.riotgames.com'
		for k, r in self.regions_v5.items():
			if region in r:
				self.HOST_V5 = f'https://{k}.api.riotgames.com'
				break
		self.language = self.languages[region]

# user statistic and other general data
	def get_user_data(self, user_name):
		URL = self.HOST + f'/lol/summoner/v4/summoners/by-name/{user_name}?api_key={self.token}'
		respons = requests.get(URL).json()
		return respons

	def get_user_by_puuid(self, puuid):
		URL = self.HOST + f'/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={self.token}'
		respons = requests.get(URL).json()
		return respons

	def user_rank(self, user_id):
		URL = self.HOST + f'/lol/league/v4/entries/by-summoner/{user_id}?api_key={self.token}'
		respons = requests.get(URL).json()
		return respons

	def user_stat_on_champ(self, champ_id, user_id):
		URL = self.HOST + f'/lol/champion-mastery/v4/champion-masteries/by-summoner/{user_id}/by-champion/{champ_id}?api_key={self.token}'
		respons = requests.get(URL).json()
		return respons

# matchs info
	def match_info_v5(self, game_id):
		URL = self.HOST_V5 + f'/lol/match/v5/matches/{game_id}?api_key={self.token}'
		respons = requests.get(URL).json()
		return respons

	def matche_timeline_v5(self, game_id):
		URL = self.HOST_V5 + f'/lol/match/v5/matches/{game_id}/timeline?api_key={self.token}'
		respons = requests.get(URL).json()
		return respons

	def user_last_games(self, user_puuid, start=0):
		URL = self.HOST_V5 + f'/lol/match/v5/matches/by-puuid/{user_puuid}/ids?count=10&start={start}&api_key={self.token}'
		respons = requests.get(URL).json()
		return respons

	def user_stat_in_game(self, game_id, user_name):
		URL = self.HOST_V5 + f'/lol/match/v5/matches/{game_id}?api_key={self.token}'
		respons = requests.get(URL).json()
		User_game_stat = list(filter(lambda x: x['summonerName']==user_name, respons["info"]["participants"]))[0]
		User_game_stat['gameStartTimestamp'] = respons["info"]["gameStartTimestamp"]
		return User_game_stat

# info about current games
	def current_game(self, user_id):
		URL = self.HOST + f'/lol/spectator/v4/active-games/by-summoner/{user_id}?api_key={self.token}'
		respons = requests.get(URL).json()
		return respons

# static info
	def champion(self, champion_name):
		URL = f'http://ddragon.leagueoflegends.com/cdn/12.12.1/data/{self.language}/champion/{champion_name}.json'
		respons = requests.get(URL).json()['data']
		return respons

# ASYNC
# async user statistic and other general data
	async def get_user_data_async(self, user_name):
		async with httpx.AsyncClient() as client:
			URL = self.HOST + f'/lol/summoner/v4/summoners/by-name/{user_name}?api_key={self.token}'
			respons = await client.get(URL)
		return respons.json()

	async def get_user_by_puuid_async(self, puuid):
		async with httpx.AsyncClient() as client:
			URL = self.HOST + f'/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={self.token}'
			respons = await client.get(URL)
		return respons.json()

	async def user_rank_async(self, user_id):
		async with httpx.AsyncClient() as client:
			URL = self.HOST + f'/lol/league/v4/entries/by-summoner/{user_id}?api_key={self.token}'
			respons = await client.get(URL)
		return respons.json()

	async def user_stat_on_champ_async(self, champ_id, user_id):
		async with httpx.AsyncClient() as client:
			URL = self.HOST + f'/lol/champion-mastery/v4/champion-masteries/by-summoner/{user_id}/by-champion/{champ_id}?api_key={self.token}'
			respons = await client.get(URL)
		return respons.json()

# async matchs info
	async def match_info_v5_async(self, game_id):
		async with httpx.AsyncClient() as client:
			URL = self.HOST_V5 + f'/lol/match/v5/matches/{game_id}?api_key={self.token}'
			respons = await client.get(URL)
		return respons.json()

	async def matche_timeline_v5_async(self, game_id):
		async with httpx.AsyncClient() as client:
			URL = self.HOST_V5 + f'/lol/match/v5/matches/{game_id}/timeline?api_key={self.token}'
			respons = await client.get(URL)
		return respons.json()

	async def user_last_games_async(self, user_puuid, start=0):
		async with httpx.AsyncClient() as client:
			URL = self.HOST_V5 + f'/lol/match/v5/matches/by-puuid/{user_puuid}/ids?count=10&start={start}&api_key={self.token}'
			respons = await client.get(URL)
		return respons.json()

	async def user_stat_in_game_async(self, game_id, user_name):
		async with httpx.AsyncClient() as client:
			URL = self.HOST_V5 + f'/lol/match/v5/matches/{game_id}?api_key={self.token}'
			respons = await client.get(URL)
		respons = respons.json()
		User_game_stat = list(filter(lambda x: x['summonerName'] == user_name, respons["info"]["participants"]))[0]
		User_game_stat['gameStartTimestamp'] = respons["info"]["gameStartTimestamp"]
		return User_game_stat

# async info about current games
	async def current_game_async(self, user_id):
		async with httpx.AsyncClient() as client:
			URL = self.HOST + f'/lol/spectator/v4/active-games/by-summoner/{user_id}?api_key={self.token}'
			respons = await client.get(URL)
		return respons.json()

# async static info
	async def champion_async(self, champion_name):
		async with httpx.AsyncClient() as client:
			URL = f'http://ddragon.leagueoflegends.com/cdn/12.12.1/data/{self.language}/champion/{champion_name}.json'
			respons = await client.get(URL)
		return respons.json()['data']
