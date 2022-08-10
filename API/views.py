import asyncio
import pandas as pd
from django.shortcuts import render, redirect
from .Analytics import UserAnalytics, GameAnalytics
import json, time


def index(request):
    import pdb; pdb.set_trace()
    print('request.method: ', request.method)
    if request.method == 'POST':
        print('request.POST[region]: ', request.POST['region'])
        print('request.POST[summoner_name]: ', request.POST['summoner_name'])
        return redirect('API:summoner', region=request.POST['region'], s_name=request.POST['summoner_name'])
    import pdb; pdb.set_trace()
    return render(request, 'API/index.html', {})


async def summoner(request, region, s_name):
    s = time.time()
    queue = asyncio.Queue()
    client = UserAnalytics(s_name, region)
    user_data = {'status_code': 'da',
                 's_name': s_name,
                 'region': region}
    rank = user_rank_stat(client.user_rank())
    task_list = [asyncio.create_task(client.short_stat_in_game_async(game_id)) for game_id in client.user_last_games()]
    import pdb; pdb.set_trace()
    await queue.join()
    last_games_data = {'games_data': await asyncio.gather(*task_list, return_exceptions=False)}
    import pdb; pdb.set_trace()
    print(time.time() - s)
    return render(request, 'API/summoner_page.html', {'user_data': user_data, 'rank': rank, 'games_data': last_games_data})


def match(request, match_id):
    s = time.time()
    import pdb; pdb.set_trace()
    client = GameAnalytics(match_id.split('_')[0].lower(), match_id)
    clean_summs_stat = client.summoners_stat()
    import pdb; pdb.set_trace()
    print(time.time() - s)
    return render(request, 'API/match.html', {'clean_summs_stat': clean_summs_stat})


def user_rank_stat(rank_info):
    clean_user_rank = {
        'rank': rank_info[0]['tier'] + rank_info[0]['rank'],
        'lp': rank_info[0]['leaguePoints'],
        'winRate': '{0:.2f}%'.format(rank_info[0]['wins'] * 100 / (rank_info[0]['wins'] + rank_info[0]['losses']))
    }
    return clean_user_rank

