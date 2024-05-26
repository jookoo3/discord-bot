import datetime

from discord.ext import commands, tasks
import discord
import requests

from API import *

DISCORD_ALARM_CHANNEL_ID = 1110588195101495336
DISCORD_LOG_CHANNEL_ID = 1243244754389438554
DISCORD_CHATTING_CHANNEL_ID = 1103667206593716376
DISCORD_BOT_TOKEN = ""

hide_text = "||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​|| _ _ _ _ _ _"

intents = discord.Intents.all()

# 시간설정
def formatKoreanTime():
    current_time = datetime.datetime.now(pytz.timezone('Asia/Seoul'))
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]
    return formatted_time

printed_yn = False  # 초기에는 False로 설정합니다.
alarm = False

bot = commands.Bot(command_prefix='$', intents=intents)

@tasks.loop(seconds=60)
async def send_stream_notification():
    alarm_channel = bot.get_channel(DISCORD_ALARM_CHANNEL_ID)
    log_channel = bot.get_channel(DISCORD_LOG_CHANNEL_ID)
    chatting_channel = bot.get_channel(DISCORD_CHATTING_CHANNEL_ID)

    global printed_yn  # printed_yn 변수를 전역 변수로 사용하기 위해 선언합니다.
    global alarm

    if alarm == False:
        await log_channel.send("Bot이 준비되었습니다.")
        print('Bot이 준비되었습니다.\n'+'----------------------------------')
        alarm = True

    chzzk_api = requests.get(url=url, headers=headers).json()
    on_live = str(chzzk_api["content"]["status"])

    if on_live == 'OPEN' and printed_yn == False:  # 방송이 시작되고 출력된 적이 없다면 알림을 보냅니다.
        print(f"방송알림을 보냅니다. {formatKoreanTime()}")
        await log_channel.send(f"방송알림을 보냅니다. **{formatKoreanTime()}**")
        await alarm_channel.send(content="@everyone", embed=streamEmbed())
        printed_yn = True  # 알림이 출력되었음을 표시합니다.
    elif on_live == "OPEN" and printed_yn == True:
        print(f"이미 알림이 전송되었습니다. {formatKoreanTime()}")
        await log_channel.send(f"이미 알림이 전송되었습니다. **{formatKoreanTime()}**")
    elif on_live == 'CLOSE' and printed_yn == True:  # 방송이 종료되었고 출력된 적이 있다면 printed_yn을 재설정합니다.
        print(f"방송이 종료되었습니다. {formatKoreanTime()}")
        await log_channel.send(f"방송이 종료되었습니다. **{formatKoreanTime()}**")
        printed_yn = False
    elif on_live == 'CLOSE' and printed_yn == False:
        print(f"방송이 종료되었습니다. {formatKoreanTime()}")
        await log_channel.send(f"방송이 종료되어있습니다. **{formatKoreanTime()}**")

def StatusEmbed():
    alarm_channel = bot.get_channel(DISCORD_ALARM_CHANNEL_ID)
    log_channel = bot.get_channel(DISCORD_LOG_CHANNEL_ID)
    chatting_channel = bot.get_channel(DISCORD_CHATTING_CHANNEL_ID)
    ChzzkAPI = requests.get(url=url, headers=headers).json()

    StatusEmbed = discord.Embed(title="봇 상태", timestamp=datetime.datetime.now(pytz.timezone('Asia/Seoul')), color=discord.Color.blue())
    StatusEmbed.set_author(name=f"{bot.user.name}", icon_url=f"{bot.user.avatar}")
    StatusEmbed.add_field(name="봇 이름", value=f"{bot.user.name}", inline=True)
    StatusEmbed.add_field(name="봇 ID", value=f"{bot.user.id}", inline=True)
    StatusEmbed.add_field(name="봇 버전", value=f"{discord.__version__}", inline=True)
    StatusEmbed.add_field(name="API 상태", value=f"{ChzzkAPI["code"]}", inline=True)
    StatusEmbed.add_field(name="연결된 채널", value=f"{ChzzkAPI["content"]["channel"]["channelName"]}" ,inline=True)
    StatusEmbed.add_field(name="방송중 여부", value=f"{ChzzkAPI["content"]["status"]}", inline=True)
    StatusEmbed.add_field(name="연결된 알림채널", value=f"{alarm_channel}", inline=True)
    StatusEmbed.add_field(name="연결된 로그채널", value=f"{log_channel}", inline=True)
    StatusEmbed.add_field(name="연결된 채팅채널", value=f"{chatting_channel}", inline=True)
    StatusEmbed.set_footer(text="Made by. 주쿠 #6220", icon_url=f"{developerThumbnail}")
    StatusEmbed.set_thumbnail(url=f"{developerThumbnail}")

    return StatusEmbed

def naverCafeEmbed():
    ChzzkAPI = requests.get(url=url, headers=headers).json()
    targetThumbnail = str(ChzzkAPI["content"]["channel"]["channelImageUrl"])

    embed = discord.Embed()
    embed.set_author(name="매화령님 네이버 카페", icon_url="https://cafe.naver.com/favicon.ico")
    embed.add_field(name="PC 사용자!", value="**[[■■■■■](https://cafe.naver.com/maehwalyeong)]**", inline=True)
    embed.add_field(name="모바일 사용자!", value="**[[■■■■■](https://m.cafe.naver.com/maehwalyeong)]**", inline=True)
    embed.set_thumbnail(url=f"{targetThumbnail}")

    return embed

def commandHelpEmbed():

    embed = discord.Embed()
    embed.set_author(name="명령어 도움말", icon_url=f"{bot.user.avatar}")
    embed.add_field(name="", value="", inline=False)
    embed.add_field(name="**$명령어**", value="이 봇에서 사용 가능한 명령어를 보여줍니다!", inline=False)
    embed.add_field(name="", value="", inline=False)
    embed.add_field(name="**$치지직**",value="치지직 채널 링크를 보여줍니다!", inline=False)
    embed.add_field(name="", value="", inline=False)
    embed.add_field(name="**$유튜브**",value="유튜브 채널 링크를 보여줍니다!", inline=False)
    embed.add_field(name="", value="", inline=False)
    embed.add_field(name="**$네이버카페**",value="네이버카페 링크를 보여줍니다!", inline=False)
    embed.add_field(name="", value="", inline=False)
    embed.add_field(name="**$매화령**",value="||~~바보를 출력합니다.~~||", inline=False)

    return embed

@send_stream_notification.before_loop
async def before_send_stream_notification():
    log_channel = bot.get_channel(DISCORD_LOG_CHANNEL_ID)

    print('Bot이 준비되기까지 기다리는중...')
    await log_channel.send("Bot이 준비되기까지 기다리는중...")
    await bot.wait_until_ready()

@bot.event
async def on_ready():
    alarm_channel = bot.get_channel(DISCORD_ALARM_CHANNEL_ID)
    log_channel = bot.get_channel(DISCORD_LOG_CHANNEL_ID)
    chatting_channel = bot.get_channel(DISCORD_CHATTING_CHANNEL_ID)
    print("----------------------------------\n"+"디스코드 봇 로그인이 완료되었습니다.")
    print("디스코드봇 이름:" + bot.user.name)
    print("디스코드봇 ID:" + str(bot.user.id))
    print("디스코드봇 버전:" + str(discord.__version__))
    print('----------------------------------')

    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="방송알림 | $명령어"))

    if alarm_channel is None:
        print('알림 채널을 확인할 수 없습니다.')
        return
    if log_channel is None:
        print('로그 채널을 확인할 수 없습니다.')
        return
    if chatting_channel is None:
        print('채팅 채널을 확인할 수 없습니다.')
        return
    print(f'{alarm_channel} 채널을 정상적으로 확인하였습니다..')
    print('채널 ID: '+str(DISCORD_ALARM_CHANNEL_ID)+"\n")
    print(f'{log_channel} 채널을 정상적으로 확인하였습니다..')
    print('채널 ID: '+str(DISCORD_ALARM_CHANNEL_ID)+"\n")
    print(f'{chatting_channel} 채널을 정상적으로 확인하였습니다..')
    print('채널 ID: '+str(DISCORD_ALARM_CHANNEL_ID)+"\n")
    print('----------------------------------')
    await log_channel.send(embed=StatusEmbed())
    await send_stream_notification.start()

@bot.command(name='명령어')
async def command_help(ctx):
    log_channel = bot.get_channel(DISCORD_LOG_CHANNEL_ID)
    print(f"명령어 {command_help.name} 이 실행되었습니다. 사용자: {ctx.author}")
    await log_channel.send(f"명령어 **『{command_help.name}』** 이(가) **『{ctx.channel}』** 채널 에서 실행되었습니다. 사용자: **{ctx.author.name}**")
    await ctx.send(content=f"{ctx.author.mention}", embed=commandHelpEmbed())

@bot.command(name='매화령')
async def command_1(ctx):
    log_channel = bot.get_channel(DISCORD_LOG_CHANNEL_ID)
    print(f"명령어 {command_1.name} 이 실행되었습니다. 사용자: {ctx.author}")
    await log_channel.send(f"명령어 **『{command_1.name}』** 이(가) **『{ctx.channel}』** 채널 에서 실행되었습니다. 사용자: **{ctx.author.name}**")
    await ctx.send("바보")

@bot.command(name='치지직')
async def command_2(ctx):
    log_channel = bot.get_channel(DISCORD_LOG_CHANNEL_ID)
    print(f"명령어 {command_2.name} 이 실행되었습니다. 사용자: {ctx.author}")
    await log_channel.send(f"명령어 **『{command_2.name}』** 이(가) **『{ctx.channel}』** 채널 에서 실행되었습니다. 사용자: **{ctx.author.name}**")
    await ctx.send(f"{ctx.author.mention} ▼ 파란글씨 클릭! ▼ {hide_text}https://chzzk.naver.com/live/{targetID}")

@bot.command(name='네이버카페')
async def command_3(ctx):
    log_channel = bot.get_channel(DISCORD_LOG_CHANNEL_ID)
    print(f"명령어 {command_3.name} 이 실행되었습니다. 사용자: {ctx.author}")
    await log_channel.send(f"명령어 **『{command_3.name}』** 이(가) **『{ctx.channel}』** 채널 에서 실행되었습니다. 사용자: **{ctx.author.name}**")
    await ctx.send(content=f"{ctx.author.mention} ▼ 파란네모 클릭! ▼",embed=naverCafeEmbed())

@bot.command(name='유튜브')
async def command_4(ctx):
    log_channel = bot.get_channel(DISCORD_LOG_CHANNEL_ID)
    print(f"명령어 {command_4.name} 이 실행되었습니다. 사용자: {ctx.author}")
    await log_channel.send(f"명령어 **『{command_4.name}』** 이(가) **『{ctx.channel}』** 채널 에서 실행되었습니다. 사용자: **{ctx.author.name}**")
    await ctx.send(f"{ctx.author.mention} ▼ 파란글씨 클릭! ▼ {hide_text}https://www.youtube.com/@maehwalyeong")

@bot.command(name="봇상태")
async def bot_status(ctx):
    print(123123123123)
    log_channel = bot.get_channel(DISCORD_LOG_CHANNEL_ID)
    if ctx.channel.id == DISCORD_LOG_CHANNEL_ID:
        await log_channel.send(embed=StatusEmbed())
    else:
        await ctx.send(f"{ctx.channel.name} 채널은 봇 관리 채널이 아닙니다.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"{ctx.author.mention}, 존재하지 않는 명령어입니다!")
    else:
        log_channel = bot.get_channel(DISCORD_LOG_CHANNEL_ID)
        await log_channel.send(f"명령어 실행 중 오류가 발생했습니다: {error}")


bot.run(DISCORD_BOT_TOKEN)
