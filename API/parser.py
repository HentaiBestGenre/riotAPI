from io import BytesIO
import time, base64, json, math

import asyncio
import httpx
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from RiotAPI import RiotAPI
from RiotAPI.RiotConfig import config

class APIClient(RiotAPI):

    def __init__(self, region, user_name):
        super().__init__(region)

        self.user_data = pd.Series(self.get_user_data(user_name=user_name))

    def get_games_ids(self, num_ids_cof):
        if num_ids_cof < 0:
            return []

        games_ids = [self.user_last_games(self.user_data['puuid'], start=(10 * coff)) for coff in
                     np.arange(num_ids_cof)]
        games_ids = np.concatenate(games_ids, axis=None)
        return games_ids

    def get_participants(self, games_ids):
        matchs_info = [self.match_info_v5(i) for i in games_ids]
        participants_ids = []
        for info in matchs_info:
            print(info['metadata']['participants'])
            participants_ids += info['metadata']['participants']
        return np.array(participants_ids)

    def p_data(self, participants_ids):
        c = 20
        offset = math.ceil(len(participants_ids) / c)
        participants_data = []
        for i in np.arange(offset):
            matchs_info = [self.get_user_by_puuid(i) for i in participants_ids[c * i: c * (i + 1)]]
            print(matchs_info)
            participants_data += matchs_info
            time.sleep(20)
        return participants_data

    async def get_games_ids_async(self, num_ids_cof):
        if num_ids_cof < 0:
            return []

        task_list = [asyncio.create_task(self.user_last_games_async(self.user_data['puuid'], start=(10 * coff)))\
                     for coff in np.arange(num_ids_cof)]

        games_ids = await asyncio.gather(*task_list, return_exceptions=True)
        games_ids = np.concatenate(games_ids, axis=None)
        return games_ids

    async def get_participants_async(self, games_ids):
        task_list = [asyncio.create_task(self.match_info_v5_async(i)) for i in games_ids]
        matchs_info = await asyncio.gather(*task_list, return_exceptions=True)
        participants_ids = []
        for info in matchs_info:
            participants_ids += info['metadata']['participants']
        return np.array(participants_ids)

    async def p_data_async(self, participants_id):
        c = 20
        offset = math.ceil(len(participants_ids) / c)
        participants_data = []
        for i in np.arange(offset):
            task_list = [asyncio.create_task(self.get_user_by_puuid_async(i))for i in participants_id[c * i: c * (i + 1)]]
            participants_data += await asyncio.gather(*task_list, return_exceptions=True)
            time.sleep(21)
        return participants_data

    async def rait_test(self, participants_ids):
        task_list = [asyncio.create_task(self.get_user_by_puuid_async(i)) for i in participants_ids]
        matchs_info = await asyncio.gather(*task_list, return_exceptions=True)
        return matchs_info


if __name__ == '__main__':
    gs = time.time()
    client = APIClient('ru', 'IIIHeNaIII')


    games_ids = client.get_games_ids(num_ids_cof=1)
    # print('game_ids len: ', len(games_ids))
    #
    # time.sleep(15)
    #
    participants_ids = client.get_participants(games_ids)
    time.sleep(60)
    data = asyncio.run(client.rait_test(participants_ids[:31]))
    for i in data:
        print(json.dumps(i, indent=5))
    # participants_ids = pd.Series(participants_ids).unique()
    # print('participants_ids len: ', len(participants_ids))
    #
    # time.sleep(15)
    #
    # participants_data = client.p_data(participants_ids)
    # print('participants_data len: ', len(participants_data))
    # print('participants_data: ', np.array(participants_data))


    # time.sleep(60)
    # gs = time.time()
    # client = APIClient('ru', 'IIIHeNaIII')
    #
    # s = time.time()
    # games_ids = asyncio.run(client.get_games_ids_async(num_ids_cof=2))
    # print('game_ids len: ', len(games_ids))
    # print(time.time() - s)
    #
    # time.sleep(15)
    #
    # s = time.time()
    # participants_ids = asyncio.run(client.get_participants_async(games_ids))
    # participants_ids = pd.Series(participants_ids).unique()
    # print('participants_ids len: ', len(participants_ids))
    # # print('participants_ids: ', participants_ids)
    # print(time.time() - s)
    #
    # time.sleep(15)
    #
    # s = time.time()
    # participants_data = asyncio.run(client.p_data_async(participants_ids))
    # print('participants_data len: ', len(participants_data))
    # print('participants_data: ', np.array(participants_data))
    # print(time.time() - s)
