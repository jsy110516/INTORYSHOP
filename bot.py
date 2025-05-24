import disnake
from disnake.ext import commands
import setting

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

owner = 502862517043724288 
임베드컬러 = 0xFFFFFF  

@bot.event
async def on_button_click(interaction: disnake.Interaction):
    await interaction.response.defer()

    cid = interaction.component.custom_id

    custom_ids = {
        "main:1": {"name": "구매문의", "message": "<a:027:1354454339875377395> **토스뱅크 1001-7192-4590 최현빈 미리 입금 부탁드립니다.**"},
        "main:2": {"name": "배너문의", "message": "**- 온라인 토큰: o/x\n- 복구키: o/x\n- 최대 온라인: 명\n- 판매물품: \n- 서버링크: **"},
        "main:3": {"name": "보상수령", "message": "<a:027:1354454339875377395> **당첨되신 이벤트 보내주세요.**"},
        "main:4": {"name": "자료기부", "message": "<a:027:1354454339875377395> **자료기부 티켓입니다.**"}
    }

    if cid in custom_ids:
        overwrites = {
            interaction.guild.default_role: disnake.PermissionOverwrite(read_messages=False, send_messages=False),
            interaction.user: disnake.PermissionOverwrite(read_messages=True, send_messages=True),
        }
        specific_role_ids = [1338001396187795649]
        for role_id in specific_role_ids:
            specific_role = interaction.guild.get_role(role_id)
            if specific_role:
                overwrites[specific_role] = disnake.PermissionOverwrite(read_messages=True, send_messages=True)

        category = interaction.guild.get_channel(1354458315064606972)
        if category and len(category.channels) >= 50:
            return await interaction.followup.send(embed=disnake.Embed(description=f"<a:027:1354454339875377395> 해당 카테고리의 채널 수를 줄여주세요.", color=0xFFFFFF), ephemeral=True)

        channel_name = f"{custom_ids[cid]['name']}ㅣ{interaction.user.name}"
        channel = await interaction.guild.create_text_channel(name=channel_name, overwrites=overwrites, category=category)
        m = await channel.send(
            embed=disnake.Embed(title="", description=f"{custom_ids[cid]['message']}", color=0xFFFFFF)
            .set_author(name=interaction.guild.name, icon_url=interaction.guild.icon.url),
            components=[disnake.ui.Button(label="티켓닫기", style=disnake.ButtonStyle.danger, custom_id="close")])
        await m.pin()
        embed_to_button_channel = disnake.Embed(description=f"<a:04:1354460116690276442> <#{channel.id}>로 이동해주세요.", color=0xFFFFFF)
        embed_to_button_channel.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon.url)
        await interaction.followup.send(embed=embed_to_button_channel, ephemeral=True)

        for member in channel.members:
            if member != interaction.guild.me and member != interaction.user:
                if channel.permissions_for(member).send_messages:
                    try:
                        dm_channel = await member.create_dm()
                        if dm_channel.permissions_for(member).send_messages:
                            dm_embed = disnake.Embed(description=f"<a:04:1354460116690276442> <#{channel.id}>로 이동해주세요.", color=0xFFFFFF)
                            dm_embed.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon.url)
                            await dm_channel.send(embed=dm_embed)
                    except disnake.errors.Forbidden:
                        pass
                    except disnake.errors.HTTPException as e:
                        pass

    elif cid == "close":
        await interaction.channel.delete()

@bot.event
async def on_ready():
    print(f"{bot.user}\n초대 링크: https://discord.com/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot")
    await bot.change_presence(status=disnake.Status.online,activity=disnake.Game(""))

@bot.slash_command(description="티켓문구를 전송합니다.")
async def 티켓문구(interaction: disnake.ApplicationCommandInteraction):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("관리자만 사용 가능합니다.", ephemeral=True)

    embed = disnake.Embed(title="<a:041:1354768738699837471> **999 Ticket**",color=0xffffff).set_author(name=interaction.guild.name, icon_url=interaction.guild.icon.url)
    embed.add_field(name='', value=f"<a:027:1354454339875377395> `장난문의 시 서버차단`\n", inline=True) 
    embed.set_image(url="https://media.discordapp.net/attachments/1337955576034099201/1354461794869051523/999_1.gif?ex=67e60918&is=67e4b798&hm=7f474f520ae3f92ac88c669dc44b42c3a0ccadc80bcfbbf839a93ac26009297b&=")
    buttons1 = [
        disnake.ui.Button(label="구매문의", emoji="<a:04:1354460116690276442>", style=disnake.ButtonStyle.gray, custom_id="main:1"),
        disnake.ui.Button(label="배너문의", emoji="<a:04:1354460116690276442>", style=disnake.ButtonStyle.gray, custom_id="main:2"),
    ]
    buttons2 = [
        disnake.ui.Button(label="보상수령", emoji="<a:04:1354460116690276442", style=disnake.ButtonStyle.gray, custom_id="main:4"),
        disnake.ui.Button(label="자료기부", emoji="<a:04:1354460116690276442", style=disnake.ButtonStyle.gray, custom_id="main:3"),
    ]
    await interaction.channel.send(embed=embed, components=[disnake.ui.ActionRow(*buttons1), disnake.ui.ActionRow(*buttons2)])
    await interaction.response.send_message("**전송 성공**", ephemeral=True)

bot.run(setting.token)