import json

import discord
import datetime, pytz
import requests

# header
headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36"}
# requests
targetID = 'b24a3bc8d6c5479b20ae69148bd79934'
url = f'https://api.chzzk.naver.com/service/v2/channels/{targetID}/live-detail'
developerThumbnail = "https://cdn.discordapp.com/avatars/353394236093104128/e466935082f2992d49a8461aff8a731d.webp?size=160"

# RGB 색상을 지정합니다.
r = 255
g = 170
b = 170

# Embed에 적용할 색상을 생성합니다.
color = discord.Color.from_rgb(r, g, b)

def streamEmbed():
    # API
    ChzzkAPI = requests.get(url=url, headers=headers).json()
    # 라이브 제목
    liveTitle = str(ChzzkAPI["content"]["liveTitle"])
    # 라이브 카테고리(게임)
    category = str(ChzzkAPI["content"]["liveCategoryValue"])
    # 시청자 수
    viewerCount = str(ChzzkAPI["content"]["concurrentUserCount"])
    # 라이브 태그
    tagsData = ChzzkAPI["content"]["tags"]
    tags_str = json.dumps(tagsData, ensure_ascii=False)[1:-1]
    tags_str = tags_str.replace('"', '')
    liveTags = tags_str
    # 스트리머 썸네일
    targetThumbnail = str(ChzzkAPI["content"]["channel"]["channelImageUrl"])


    stream_embed = discord.Embed(title=f"{liveTitle}", url=f"https://chzzk.naver.com/live/{targetID}", timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=color)
    stream_embed.set_author(name="치지직 방송 알림!", icon_url="https://ssl.pstatic.net/static/nng/glive/icon/favicon.png", url="https://chzzk.naver.com")
    stream_embed.add_field(name="카테고리", value=f"{category}", inline=True)
    stream_embed.add_field(name="시청자", value=f"{viewerCount}", inline=True)
    stream_embed.add_field(name="태그", value=f"{liveTags}", inline=False)
    stream_embed.set_image(url=(ChzzkAPI['content']['liveImageUrl'] or ChzzkAPI['content']['channel']['channelImageUrl'] or "").replace("_{type}", "_1080"))
    stream_embed.set_footer(text="Made by. 주쿠 #6220", icon_url=f"{developerThumbnail}")
    stream_embed.set_thumbnail(url=f"{targetThumbnail}")

    return stream_embed






