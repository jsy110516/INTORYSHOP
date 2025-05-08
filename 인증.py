import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import aiohttp
 
SETTINGS_FILE = 'settings.json'
 
def load_settings():
    try:
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"log_webhook_url": None, "auth_role_id": None}
 
def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)
 
settings = load_settings()
 
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
 
bot = commands.Bot(command_prefix="!", intents=intents)
 
@bot.event
async def on_ready():
    print(f'로그인 완료! 봇 이름: {bot.user.name}')
    print(f'봇 ID: {bot.user.id}')
 
    client_id = bot.user.id
    permissions = 268717056
 
    invite_link = f"https://discord.com/api/oauth2/authorize?client_id={client_id}&permissions={permissions}&scope=bot%20applications.commands"
 
    print(f'\n봇 초대 링크: {invite_link}')
    print("이 링크로 봇을 서버에 초대할 수 있습니다.")
 
    print('슬래시 커맨드 동기화 시작...')
    try:
        synced = await bot.tree.sync()
        print(f'{len(synced)}개 커맨드 동기화 완료!')
    except Exception as e:
        print(f'슬래시 커맨드 동기화 실패: {e}')
    print('------')
 
@bot.tree.command(name="로그웹훅", description="인증 로그를 받을 웹훅 URL을 설정합니다.")
@app_commands.default_permissions(administrator=True)
async def logwebhook(interaction: discord.Interaction, url: str):
    settings['log_webhook_url'] = url
    save_settings(settings)
    await interaction.response.send_message(f'인증 로그 웹훅 URL이 `{url}` 로 설정되었습니다.', ephemeral=True)
 
@bot.tree.command(name="역할", description="인증 완료 시 지급할 역할을 설정합니다.")
@app_commands.default_permissions(administrator=True)
async def authrole(interaction: discord.Interaction, 역할: discord.Role):
    settings['auth_role_id'] = 역할.id
    save_settings(settings)
    await interaction.response.send_message(f'인증 역할이 `{역할.name}` 으로 설정되었습니다.', ephemeral=True)
 
@bot.tree.command(name="인증", description="인증 메시지와 버튼을 생성합니다.")
@app_commands.default_permissions(administrator=True)
async def authmsg(interaction: discord.Interaction, 제목: str, 본문: str):
    embed = discord.Embed(title=제목, description=본문, color=discord.Color.green())
 
    auth_button = discord.ui.Button(label="인증하기", style=discord.ButtonStyle.success, emoji="✅", custom_id="auth_button")
 
    async def auth_button_callback(interaction: discord.Interaction):
        role_id = settings.get('auth_role_id')
        webhook_url = settings.get('log_webhook_url')
 
        if not role_id or not webhook_url:
            await interaction.response.send_message("인증 역할 또는 로그 웹훅이 설정되지 않았습니다. 관리자에게 문의하세요.", ephemeral=True)
            return
 
        guild = interaction.guild
        member = interaction.user
        auth_role = guild.get_role(role_id)
 
        if not auth_role:
            await interaction.response.send_message("설정된 인증 역할을 찾을 수 없습니다. 관리자에게 문의하세요.", ephemeral=True)
            return
 
        if auth_role in member.roles:
             await interaction.response.send_message("이미 인증되었습니다!", ephemeral=True)
             return
 
        try:
            await member.add_roles(auth_role)
 
            log_embed = discord.Embed(title="인증 완료", color=discord.Color.blue())
            log_embed.add_field(name="유저 ID", value=member.id, inline=False)
            log_embed.add_field(name="유저 이름", value=str(member), inline=False)
            log_embed.add_field(name="계정 생성일", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
            log_embed.add_field(name="인증 시간", value=discord.utils.utcnow().strftime("%Y-%m-%d %H:%M:%S"), inline=False)
 
            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(webhook_url, session=session)
                await webhook.send(embed=log_embed)
 
            await interaction.response.send_message("인증이 완료되었습니다! 🎉", ephemeral=True)
 
        except Exception as e:
            print(f"인증 중 오류 발생: {e}")
            await interaction.response.send_message("인증 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.", ephemeral=True)
 
    auth_button.callback = auth_button_callback
 
    view = discord.ui.View()
    view.add_item(auth_button)
 
    await interaction.response.send_message(embed=embed, view=view)
 
bot.run('봇 토큰 여기다가 넣어주세요!')
