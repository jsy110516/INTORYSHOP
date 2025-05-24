import discord
from discord.ext import commands
from discord.ui import Button, View

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(Button(label="구매문의", style=discord.ButtonStyle.green, custom_id="purchase_inquiry"))
        self.add_item(Button(label="충전문의", style=discord.ButtonStyle.blurple, custom_id="recharge_inquiry"))
        self.add_item(Button(label="일반문의", style=discord.ButtonStyle.gray, custom_id="general_inquiry"))
        self.add_item(Button(label="버그문의", style=discord.ButtonStyle.red, custom_id="bug_inquiry"))

@bot.event
async def on_ready():
    print(f"{bot.user}에 로그인되었습니다!")
    # 특정 채널에 버튼 전송
    channel = bot.get_channel(YOUR_CHANNEL_ID)  # 채널 ID를 입력하세요
    await channel.send("문의할 버튼을 클릭하세요:", view=TicketView())

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component:
        if interaction.data["custom_id"] == "purchase_inquiry":
            await interaction.response.send_message("구매 문의 티켓이 생성되었습니다!", ephemeral=True)
        elif interaction.data["custom_id"] == "recharge_inquiry":
            await interaction.response.send_message("충전 문의 티켓이 생성되었습니다!", ephemeral=True)
        elif interaction.data["custom_id"] == "general_inquiry":
            await interaction.response.send_message("일반 문의 티켓이 생성되었습니다!", ephemeral=True)
        elif interaction.data["custom_id"] == "bug_inquiry":
            await interaction.response.send_message("버그 문의 티켓이 생성되었습니다!", ephemeral=True)

bot.run("MTM3MzIxMTA3OTEwMjE3MzI0NQ.GwZ9hf.iEgdlA4zjuNva5zKg3Nu1D-HVj8qMqqxxxjW4k")
