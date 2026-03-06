import discord
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True  
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")
    await bot.tree.sync()


@bot.tree.command(name="ban", description="Bannir un membre du serveur")
@app_commands.describe(member="Membre à bannir", reason="Raison du ban")
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "Aucune raison fournie"):
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message("❌ Vous n'avez pas la permission de bannir des membres.", ephemeral=True)
        return
    if member.guild_permissions.administrator:
        await interaction.response.send_message("❌ Impossible de bannir un administrateur.", ephemeral=True)
        return

    embed = discord.Embed(
        title="🔨 Membre Banni",
        description=f"{member.mention} a été banni avec succès !",
        color=0xFF0000
    )
    embed.add_field(name="Banni par", value=interaction.user.mention, inline=True)
    embed.add_field(name="Raison", value=reason, inline=True)
    embed.set_thumbnail(url=member.display_avatar.url)
    await member.send(f"Vous avez été banni de **{interaction.guild.name}**.\nRaison : {reason}")
    await interaction.response.send_message(embed=embed)
    await interaction.guild.ban(member, reason=reason)


@bot.tree.command(name="unban", description="Débannir un membre du serveur")
@app_commands.describe(user_id="ID du membre à débannir")
async def unban(interaction: discord.Interaction, user_id: str):
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message("❌ Vous n'avez pas la permission de débannir des membres.", ephemeral=True)
        return
    try:
        user = await bot.fetch_user(int(user_id))
        await interaction.guild.unban(user)
        embed = discord.Embed(
            title="✅ Membre Débanni",
            description=f"{user.mention} a été débanni avec succès !",
            color=0x00FF00
        )
        embed.set_thumbnail(url=user.display_avatar.url)
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        await interaction.response.send_message(f"❌ Impossible de débannir ce membre. Erreur : {e}", ephemeral=True)

bot.run("INSERT_TOKEN_HERE")