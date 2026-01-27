"""
ADVANCED DISCORD CRICKET SIMULATION BOT
========================================
"""

import discord
from discord.ext import commands
import random
import json
import os
from datetime import datetime
import asyncio
from difflib import get_close_matches

# Bot Setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Player Database
PLAYER_DATABASE = {
    # Indian Players
    "ViratKohli": {"batting": 95, "bowling": 20, "fielding": 92, "role": "batsman", "style": "right_hand"},
    "RohitSharma": {"batting": 94, "bowling": 25, "fielding": 85, "role": "batsman", "style": "right_hand"},
    "JaspritBumrah": {"batting": 35, "bowling": 98, "fielding": 80, "role": "bowler", "style": "fast"},
    "HardikPandya": {"batting": 82, "bowling": 78, "fielding": 88, "role": "all_rounder", "style": "right_hand"},
    "KLRahul": {"batting": 88, "bowling": 15, "fielding": 90, "role": "batsman", "style": "right_hand"},
    "RavindraJadeja": {"batting": 75, "bowling": 88, "fielding": 95, "role": "all_rounder", "style": "spin"},
    "MohammedShami": {"batting": 30, "bowling": 92, "fielding": 75, "role": "bowler", "style": "fast"},
    "RishabhPant": {"batting": 85, "bowling": 10, "fielding": 82, "role": "wicket_keeper", "style": "left_hand"},
    "SuryakumarYadav": {"batting": 90, "bowling": 20, "fielding": 87, "role": "batsman", "style": "right_hand"},
    "YuzvendraChahal": {"batting": 25, "bowling": 86, "fielding": 70, "role": "bowler", "style": "spin"},
    "RavichandranAshwin": {"batting": 55, "bowling": 90, "fielding": 78, "role": "all_rounder", "style": "spin"},

    # Australian Players
    "SteveSmith": {"batting": 93, "bowling": 30, "fielding": 88, "role": "batsman", "style": "right_hand"},
    "DavidWarner": {"batting": 91, "bowling": 15, "fielding": 84, "role": "batsman", "style": "left_hand"},
    "PatCummins": {"batting": 40, "bowling": 95, "fielding": 82, "role": "bowler", "style": "fast"},
    "GlennMaxwell": {"batting": 84, "bowling": 75, "fielding": 90, "role": "all_rounder", "style": "right_hand"},
    "MitchellStarc": {"batting": 35, "bowling": 94, "fielding": 78, "role": "bowler", "style": "fast"},
    "JoshHazlewood": {"batting": 28, "bowling": 91, "fielding": 76, "role": "bowler", "style": "fast"},
    "Ada Zampa": {"batting": 22, "bowling": 84, "fielding": 72, "role": "bowler", "style": "spin"},
    "TravisHead": {"batting": 86, "bowling": 35, "fielding": 83, "role": "batsman", "style": "left_hand"},
    "MarcusStoinis": {"batting": 80, "bowling": 72, "fielding": 85, "role": "all_rounder", "style": "right_hand"},
    "AlexCarey": {"batting": 78, "bowling": 10, "fielding": 88, "role": "wicket_keeper", "style": "left_hand"},
    
    # English Players
    "JoeRoot": {"batting": 94, "bowling": 35, "fielding": 86, "role": "batsman", "style": "right_hand"},
    "BenStokes": {"batting": 87, "bowling": 82, "fielding": 91, "role": "all_rounder", "style": "left_hand"},
    "JosButtler": {"batting": 89, "bowling": 10, "fielding": 85, "role": "wicket_keeper", "style": "right_hand"},
    "JofrArcher": {"batting": 32, "bowling": 93, "fielding": 80, "role": "bowler", "style": "fast"},
    "MarkWood": {"batting": 28, "bowling": 89, "fielding": 75, "role": "bowler", "style": "fast"},
    "AdilRashid": {"batting": 30, "bowling": 85, "fielding": 74, "role": "bowler", "style": "spin"},
    "JonnyBairstow": {"batting": 86, "bowling": 15, "fielding": 83, "role": "batsman", "style": "right_hand"},
    "SamCurran": {"batting": 68, "bowling": 79, "fielding": 82, "role": "all_rounder", "style": "left_hand"},
    "MoeenAli": {"batting": 76, "bowling": 78, "fielding": 80, "role": "all_rounder", "style": "left_hand"},
    
    # Pakistani Players
    "BabarAzam": {"batting": 96, "bowling": 20, "fielding": 89, "role": "batsman", "style": "right_hand"},
    "ShaheenAfridi": {"batting": 30, "bowling": 94, "fielding": 77, "role": "bowler", "style": "fast"},
    "MohammadRizwan": {"batting": 87, "bowling": 10, "fielding": 90, "role": "wicket_keeper", "style": "right_hand"},
    "ShadabKhan": {"batting": 65, "bowling": 81, "fielding": 88, "role": "all_rounder", "style": "spin"},
    "HarisRauf": {"batting": 25, "bowling": 88, "fielding": 73, "role": "bowler", "style": "fast"},

    # Bangladesh Players
    "ShakibAlHasan": {"batting": 82, "bowling": 85, "fielding": 83, "role": "all_rounder", "style": "spin"},
    "MushfiqurRahim": {"batting": 79, "bowling": 10, "fielding": 81, "role": "wicket_keeper", "style": "right_hand"},
    "TamimIqbal": {"batting": 81, "bowling": 15, "fielding": 76, "role": "batsman", "style": "left_hand"},
    "MustafizurRahman": {"batting": 22, "bowling": 82, "fielding": 70, "role": "bowler", "style": "fast"},
    "MehidyHasan": {"batting": 55, "bowling": 77, "fielding": 74, "role": "all_rounder", "style": "spin"},
    "TaskinAhmed": {"batting": 24, "bowling": 78, "fielding": 71, "role": "bowler", "style": "fast"},
    "LittonDas": {"batting": 76, "bowling": 10, "fielding": 79, "role": "wicket_keeper", "style": "right_hand"},
    "Mahmudullah": {"batting": 74, "bowling": 65, "fielding": 77, "role": "all_rounder", "style": "right_hand"},

# Afghanistan Players
    "RashidKhan": {"batting": 60, "bowling": 92, "fielding": 85, "role": "all_rounder", "style": "spin"},
    "MohammadNabi": {"batting": 72, "bowling": 80, "fielding": 81, "role": "all_rounder", "style": "spin"},
    "MujeebUrRahman": {"batting": 20, "bowling": 83, "fielding": 73, "role": "bowler", "style": "spin"},
    "RahmanullahGurbaz": {"batting": 78, "bowling": 10, "fielding": 80, "role": "wicket_keeper", "style": "right_hand"},
    "NaveenulHaq": {"batting": 25, "bowling": 79, "fielding": 72, "role": "bowler", "style": "fast"},
    "IbrahimZadran": {"batting": 74, "bowling": 15, "fielding": 76, "role": "batsman", "style": "right_hand"},
    "FazalhaqFarooqi": {"batting": 20, "bowling": 81, "fielding": 70, "role": "bowler", "style": "fast"},

# Ireland Players
    "PaulStirling": {"batting": 80, "bowling": 45, "fielding": 78, "role": "batsman", "style": "right_hand"},
    "AndrewBalbirnie": {"batting": 76, "bowling": 20, "fielding": 77, "role": "batsman", "style": "right_hand"},
    "HarryTector": {"batting": 77, "bowling": 25, "fielding": 79, "role": "batsman", "style": "right_hand"},
    "CurtisCampher": {"batting": 68, "bowling": 72, "fielding": 80, "role": "all_rounder", "style": "right_hand"},
    "MarkAdair": {"batting": 52, "bowling": 76, "fielding": 75, "role": "all_rounder", "style": "fast"},
    "JoshuaLittle": {"batting": 22, "bowling": 77, "fielding": 71, "role": "bowler", "style": "fast"},
    "LorcanTucker": {"batting": 70, "bowling": 10, "fielding": 78, "role": "wicket_keeper", "style": "right_hand"},

# Zimbabwe Players
    "SikandarRaza": {"batting": 78, "bowling": 74, "fielding": 79, "role": "all_rounder", "style": "spin"},
    "SeanWilliams": {"batting": 73, "bowling": 68, "fielding": 76, "role": "all_rounder", "style": "spin"},
    "BlessingMuzarabani": {"batting": 20, "bowling": 75, "fielding": 70, "role": "bowler", "style": "fast"},
    "RegisChakabva": {"batting": 69, "bowling": 10, "fielding": 77, "role": "wicket_keeper", "style": "right_hand"},
    "CraigErvine": {"batting": 74, "bowling": 30, "fielding": 75, "role": "batsman", "style": "left_hand"},
    "RichardNgarava": {"batting": 24, "bowling": 73, "fielding": 69, "role": "bowler", "style": "fast"}
    # Legends / Retired Players
    "SachinTendulkar": {"batting": 99, "bowling": 35, "fielding": 88, "role": "batsman", "style": "right_hand"},
    "BrianLara": {"batting": 98, "bowling": 25, "fielding": 85, "role": "batsman", "style": "left_hand"},
    "RickyPonting": {"batting": 96, "bowling": 30, "fielding": 94, "role": "batsman", "style": "right_hand"},
    "JacquesKallis": {"batting": 94, "bowling": 84, "fielding": 90, "role": "all_rounder", "style": "right_hand"},
    "KumarSangakkara": {"batting": 95, "bowling": 10, "fielding": 89, "role": "wicket_keeper", "style": "left_hand"},
    "ABdeVilliers": {"batting": 97, "bowling": 25, "fielding": 96, "role": "batsman", "style": "right_hand"},
    "MSDhoni": {"batting": 89, "bowling": 10, "fielding": 95, "role": "wicket_keeper", "style": "right_hand"},
    "WasimAkram": {"batting": 55, "bowling": 96, "fielding": 82, "role": "all_rounder", "style": "fast"},
    "ShaneWarne": {"batting": 50, "bowling": 98, "fielding": 80, "role": "bowler", "style": "spin"},
    "GlennMcGrath": {"batting": 25, "bowling": 97, "fielding": 78, "role": "bowler", "style": "fast"},
    "MuttiahMuralitharan": {"batting": 30, "bowling": 99, "fielding": 75, "role": "bowler", "style": "spin"},
    "DaleSteyn": {"batting": 35, "bowling": 96, "fielding": 83, "role": "bowler", "style": "fast"},
    "AdamGilchrist": {"batting": 91, "bowling": 10, "fielding": 93, "role": "wicket_keeper", "style": "left_hand"},
    "VivRichards": {"batting": 98, "bowling": 40, "fielding": 91, "role": "batsman", "style": "right_hand"},
    "ImranKhan": {"batting": 78, "bowling": 92, "fielding": 86, "role": "all_rounder", "style": "fast"},
    "KapilDev": {"batting": 75, "bowling": 88, "fielding": 85, "role": "all_rounder", "style": "fast"},
    "RichardHadlee": {"batting": 60, "bowling": 95, "fielding": 82, "role": "all_rounder", "style": "fast"},
    "IanBotham": {"batting": 76, "bowling": 87, "fielding": 84, "role": "all_rounder", "style": "fast"},
    "MalcolmMarshall": {"batting": 40, "bowling": 96, "fielding": 81, "role": "bowler", "style": "fast"},
    "CurtlyAmbrose": {"batting": 30, "bowling": 95, "fielding": 79, "role": "bowler", "style": "fast"},

    # Modern Indian Players
    "ShubmanGill": {"batting": 86, "bowling": 20, "fielding": 84, "role": "batsman", "style": "right_hand"},
    "IshanKishan": {"batting": 81, "bowling": 10, "fielding": 82, "role": "wicket_keeper", "style": "left_hand"},
    "ShreyasIyer": {"batting": 83, "bowling": 25, "fielding": 81, "role": "batsman", "style": "right_hand"},
    "WashingtonSundar": {"batting": 62, "bowling": 76, "fielding": 80, "role": "all_rounder", "style": "spin"},
    "AxarPatel": {"batting": 58, "bowling": 79, "fielding": 82, "role": "all_rounder", "style": "spin"},
    "KuldeepYadav": {"batting": 24, "bowling": 84, "fielding": 72, "role": "bowler", "style": "spin"},
    "ArshdeepSingh": {"batting": 26, "bowling": 80, "fielding": 74, "role": "bowler", "style": "fast"},
    "ShardulThakur": {"batting": 60, "bowling": 75, "fielding": 78, "role": "all_rounder", "style": "fast"},
    "DeepakChahar": {"batting": 48, "bowling": 77, "fielding": 75, "role": "all_rounder", "style": "fast"},
    "PrasidhKrishna": {"batting": 24, "bowling": 78, "fielding": 72, "role": "bowler", "style": "fast"}
    # More players (add the ones I provided earlier here)
}

# Utility Functions
def find_similar_player(name, threshold=0.6):
    all_players = list(PLAYER_DATABASE.keys())
    matches = get_close_matches(name, all_players, n=3, cutoff=threshold)
    return matches

def calculate_team_overall(squad):
    if not squad:
        return 0
    total_rating = 0
    for player in squad:
        if player in PLAYER_DATABASE:
            stats = PLAYER_DATABASE[player]
            overall = (stats['batting'] + stats['bowling'] + stats['fielding']) / 3
            total_rating += overall
        else:
            total_rating += 50
    return total_rating / len(squad)

def validate_squad(squad):
    if len(squad) != 11:
        return False, "Squad must have exactly 11 players"
    roles = {'batsman': 0, 'bowler': 0, 'all_rounder': 0, 'wicket_keeper': 0}
    for player in squad:
        if player in PLAYER_DATABASE:
            role = PLAYER_DATABASE[player]['role']
            roles[role] += 1
    if roles['wicket_keeper'] < 1:
        return False, "Squad must have at least 1 wicket keeper"
    if roles['bowler'] + roles['all_rounder'] < 4:
        return False, "Squad must have at least 4 bowlers/all-rounders"
    if roles['batsman'] + roles['all_rounder'] < 5:
        return False, "Squad must have at least 5 batsmen/all-rounders"
    return True, "Valid squad"

# Data Files
TEAMS_FILE = 'teams.json'
STATS_FILE = 'stats.json'

def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {}

def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

teams_data = load_data(TEAMS_FILE)
player_stats = load_data(STATS_FILE)

# Pitch and Weather
PITCH_CONDITIONS = {
    "Green Pitch": {"pace_bonus": 15, "spin_bonus": -10, "batting_difficulty": 10, "description": "Helps fast bowlers"},
    "Dry Pitch": {"pace_bonus": -5, "spin_bonus": 15, "batting_difficulty": 5, "description": "Assists spinners"},
    "Dusty Pitch": {"pace_bonus": -10, "spin_bonus": 20, "batting_difficulty": 8, "description": "Spin-friendly"},
    "Flat Pitch": {"pace_bonus": 0, "spin_bonus": 0, "batting_difficulty": -10, "description": "Batsman-friendly"}
}

WEATHER_CONDITIONS = {
    "Sunny": {"swing_factor": 0, "visibility": 100, "description": "Clear skies"},
    "Cloudy": {"swing_factor": 10, "visibility": 90, "description": "Helps swing bowling"},
    "Overcast": {"swing_factor": 20, "visibility": 80, "description": "Significant swing"}
}

# Simulation Functions
def simulate_ball(batsman, bowler, pitch, weather):
    bat_rating = PLAYER_DATABASE.get(batsman, {}).get("batting", 50)
    bowl_rating = PLAYER_DATABASE.get(bowler, {}).get("bowling", 50)
    
    bowler_style = PLAYER_DATABASE.get(bowler, {}).get("style", "fast")
    if bowler_style == "fast":
        bowl_rating += pitch["pace_bonus"]
    elif bowler_style == "spin":
        bowl_rating += pitch["spin_bonus"]
    
    net_rating = bat_rating - bowl_rating - pitch["batting_difficulty"]
    probability = 50 + (net_rating / 4)
    
    if probability > 70:
        weights = [15, 25, 18, 10, 15, 12, 5]
    elif probability > 50:
        weights = [25, 30, 15, 8, 10, 5, 7]
    else:
        weights = [30, 25, 12, 5, 8, 3, 17]
    
    outcomes = ['0', '1', '2', '3', '4', '6', 'W']
    return random.choices(outcomes, weights=weights)[0]

def get_bowlers(squad):
    bowlers = []
    all_rounders = []
    for player in squad:
        if player in PLAYER_DATABASE:
            role = PLAYER_DATABASE[player]["role"]
            if role == "bowler":
                bowlers.append(player)
            elif role == "all_rounder":
                all_rounders.append(player)
    bowling_lineup = bowlers + all_rounders
    if len(bowling_lineup) < 5:
        remaining = [p for p in squad if p not in bowling_lineup]
        remaining.sort(key=lambda x: PLAYER_DATABASE.get(x, {}).get('bowling', 0), reverse=True)
        bowling_lineup.extend(remaining[:5-len(bowling_lineup)])
    return bowling_lineup[:5]

def simulate_innings(team_name, squad, opp_squad, pitch, weather, target=None):
    batting_order = squad[:11]
    total_runs = 0
    wickets = 0
    overs = 0
    max_overs = 20
    
    batsman_scores = {}
    for batsman in batting_order:
        batsman_scores[batsman] = {'runs': 0, 'balls': 0, 'fours': 0, 'sixes': 0}
    
    bowlers = get_bowlers(opp_squad)
    bowler_stats = {}
    for bowler in bowlers:
        bowler_stats[bowler] = {'overs': 0, 'runs': 0, 'wickets': 0, 'economy': 0.0}
    
    current_batsmen = [batting_order[0], batting_order[1]]
    batsman_index = 2
    current_bowler_idx = 0
    
    while overs < max_overs and wickets < 10:
        if target and total_runs > target:
            break
        
        current_bowler = bowlers[current_bowler_idx % len(bowlers)]
        balls_in_over = 0
        over_runs = 0
        
        while balls_in_over < 6 and wickets < 10:
            if target and total_runs > target:
                break
            
            striker = current_batsmen[0]
            outcome = simulate_ball(striker, current_bowler, pitch, weather)
            
            if outcome == 'W':
                wickets += 1
                balls_in_over += 1
                bowler_stats[current_bowler]['wickets'] += 1
                if batsman_index < len(batting_order):
                    current_batsmen[0] = batting_order[batsman_index]
                    batsman_index += 1
            else:
                runs = int(outcome)
                total_runs += runs
                over_runs += runs
                batsman_scores[striker]['runs'] += runs
                batsman_scores[striker]['balls'] += 1
                bowler_stats[current_bowler]['runs'] += runs
                balls_in_over += 1
                
                if runs == 4:
                    batsman_scores[striker]['fours'] += 1
                elif runs == 6:
                    batsman_scores[striker]['sixes'] += 1
                
                if runs % 2 == 1:
                    current_batsmen[0], current_batsmen[1] = current_batsmen[1], current_batsmen[0]
        
        overs += 1
        bowler_stats[current_bowler]['overs'] += 1
        current_batsmen[0], current_batsmen[1] = current_batsmen[1], current_batsmen[0]
        current_bowler_idx += 1
    
    for bowler, stats in bowler_stats.items():
        if stats['overs'] > 0:
            stats['economy'] = stats['runs'] / stats['overs']
    
    return {
        'team': team_name,
        'total': total_runs,
        'wickets': wickets,
        'overs': overs,
        'batsmen': batsman_scores,
        'bowlers': bowler_stats
    }

# Bot Events
@bot.event
async def on_ready():
    print(f'{bot.user} is online!')
    print(f'Connected to {len(bot.guilds)} servers')

# Bot Commands
@bot.command(name='help_cricket')
async def help_cricket(ctx):
    """Show all cricket commands"""
    embed = discord.Embed(
        title="🏏 Cricket Simulation Bot Commands",
        description="Complete command list",
        color=0x00ff00
    )
    
    embed.add_field(
        name="📋 Team Management",
        value="**!teamadd <name> <p1> ... <p11>** - Create team\n**!teams** - Show all teams\n**!teamdelete <name>** - Delete team",
        inline=False
    )
    
    embed.add_field(
        name="🎮 Match Simulation",
        value="**!sim <team1> <team2>** - Simulate match\n**!quicksim <team1> <team2>** - Quick simulation",
        inline=False
    )
    
    embed.add_field(
        name="👤 Player Info",
        value="**!player <name>** - View player profile\n**!players** - List all players",
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.command(name='teamadd')
async def teamadd(ctx, team_name: str, *players):
    """Add a new team with player validation"""
    if len(players) != 11:
        await ctx.send(f"❌ Error: You must provide exactly 11 players. You provided {len(players)}.")
        return
    
    validated_players = []
    invalid_players = []
    
    for player in players:
        if player in PLAYER_DATABASE:
            validated_players.append(player)
        else:
            similar = find_similar_player(player, threshold=0.6)
            if similar:
                await ctx.send(f"❓ **{player}** not found. Did you mean: **{', '.join(similar)}**?")
            invalid_players.append(player)
    
    if invalid_players:
        await ctx.send(f"⚠️ **Team Registration Failed**\n\n💡 Use `!players` to see all available players.")
        return
    
    is_valid, message = validate_squad(validated_players)
    if not is_valid:
        await ctx.send(f"❌ Invalid squad composition: {message}")
        return
    
    team_overall = calculate_team_overall(validated_players)
    
    teams_data[team_name] = {
        'squad': validated_players,
        'created_by': str(ctx.author),
        'created_at': datetime.now().isoformat(),
        'overall': round(team_overall, 2),
        'matches_played': 0,
        'wins': 0,
        'losses': 0
    }
    
    save_data(TEAMS_FILE, teams_data)
    
    embed = discord.Embed(
        title=f"✅ Team '{team_name}' Created!",
        description=f"Overall Rating: **{team_overall:.1f}**",
        color=0x00ff00
    )
    
    embed.set_footer(text=f"Created by {ctx.author.name}")
    await ctx.send(embed=embed)

@bot.command(name='teams')
async def teams(ctx):
    """Show all registered teams"""
    if not teams_data:
        await ctx.send("❌ No teams registered yet! Use !teamadd to create a team.")
        return
    
    embed = discord.Embed(
        title="🏏 Registered Teams",
        description=f"Total Teams: {len(teams_data)}",
        color=0x3498db
    )
    
    for team_name, team_info in teams_data.items():
        overall = team_info.get('overall', 0)
        matches = team_info.get('matches_played', 0)
        wins = team_info.get('wins', 0)
        
        value = f"📊 Overall: **{overall:.1f}** | Matches: {matches} | Wins: {wins}"
        embed.add_field(name=f"🔵 {team_name}", value=value, inline=False)
    
    await ctx.send(embed=embed)

def simulate_innings_detailed(team_name, squad, opp_squad, pitch, weather, target=None):
    """Simulate innings with over-by-over details"""
    batting_order = squad[:11]
    total_runs = 0
    wickets = 0
    overs = 0
    max_overs = 20
    
    batsman_scores = {}
    for batsman in batting_order:
        batsman_scores[batsman] = {'runs': 0, 'balls': 0, 'fours': 0, 'sixes': 0, 'out': False, 'strike_rate': 0.0}
    
    bowlers = get_bowlers(opp_squad)
    bowler_stats = {}
    for bowler in bowlers:
        bowler_stats[bowler] = {'overs': 0, 'runs': 0, 'wickets': 0, 'maidens': 0, 'economy': 0.0}
    
    current_batsmen = [batting_order[0], batting_order[1]]
    batsman_index = 2
    current_bowler_idx = 0
    over_by_over = []
    
    while overs < max_overs and wickets < 10:
        if target and total_runs > target:
            break
        
        current_bowler = bowlers[current_bowler_idx % len(bowlers)]
        balls_in_over = 0
        over_runs = 0
        over_commentary = []
        
        while balls_in_over < 6 and wickets < 10:
            if target and total_runs > target:
                break
            
            striker = current_batsmen[0]
            outcome = simulate_ball(striker, current_bowler, pitch, weather)
            
            if outcome == 'W':
                batsman_scores[striker]['out'] = True
                wickets += 1
                balls_in_over += 1
                bowler_stats[current_bowler]['wickets'] += 1
                over_commentary.append(f"⚾ WICKET! {striker} OUT")
                
                if batsman_index < len(batting_order):
                    current_batsmen[0] = batting_order[batsman_index]
                    batsman_index += 1
            else:
                runs = int(outcome)
                total_runs += runs
                over_runs += runs
                batsman_scores[striker]['runs'] += runs
                batsman_scores[striker]['balls'] += 1
                bowler_stats[current_bowler]['runs'] += runs
                balls_in_over += 1
                
                if runs == 4:
                    batsman_scores[striker]['fours'] += 1
                    over_commentary.append(f"🔴 FOUR! {striker}")
                elif runs == 6:
                    batsman_scores[striker]['sixes'] += 1
                    over_commentary.append(f"🔥 SIX! {striker}")
                
                if runs % 2 == 1:
                    current_batsmen[0], current_batsmen[1] = current_batsmen[1], current_batsmen[0]
        
        overs += 1
        bowler_stats[current_bowler]['overs'] += 1
        
        if over_runs == 0:
            bowler_stats[current_bowler]['maidens'] += 1
        
        over_summary = f"Over {overs}: {over_runs} runs | Total: {total_runs}/{wickets}"
        over_by_over.append({
            'over': overs,
            'runs': over_runs,
            'total': total_runs,
            'wickets': wickets,
            'bowler': current_bowler,
            'commentary': over_commentary,
            'summary': over_summary
        })
        
        current_batsmen[0], current_batsmen[1] = current_batsmen[1], current_batsmen[0]
        current_bowler_idx += 1
    
    for batsman, stats in batsman_scores.items():
        if stats['balls'] > 0:
            stats['strike_rate'] = (stats['runs'] / stats['balls']) * 100
    
    for bowler, stats in bowler_stats.items():
        if stats['overs'] > 0:
            stats['economy'] = stats['runs'] / stats['overs']
    
    return {
        'team': team_name,
        'total': total_runs,
        'wickets': wickets,
        'overs': overs,
        'batsmen': batsman_scores,
        'bowlers': bowler_stats,
        'over_by_over': over_by_over
    }

def calculate_win_probability(team1_score, team1_wickets, team2_score, team2_wickets, overs_remaining):
    """Calculate win probability for chasing team"""
    if overs_remaining <= 0:
        return 100 if team2_score > team1_score else 0
    
    runs_needed = team1_score - team2_score + 1
    wickets_left = 10 - team2_wickets
    
    if runs_needed <= 0:
        return 100
    
    required_rr = runs_needed / overs_remaining
    wickets_factor = wickets_left / 10 * 100
    
    if required_rr > 15:
        base_prob = 10
    elif required_rr > 12:
        base_prob = 25
    elif required_rr > 9:
        base_prob = 50
    elif required_rr > 6:
        base_prob = 75
    else:
        base_prob = 90
    
    win_prob = (base_prob + wickets_factor) / 2
    return max(5, min(95, win_prob))

@bot.command(name='sim')
async def simulate_match(ctx, team1_name: str, team2_name: str):
    """Simulate a match with over-by-over updates"""
    if team1_name not in teams_data or team2_name not in teams_data:
        await ctx.send(f"❌ One or both teams not found! Use !teams to see registered teams.")
        return
    
    await ctx.send(f"🏏 **Preparing match: {team1_name} vs {team2_name}**")
    
    # Random conditions
    pitch_name = random.choice(list(PITCH_CONDITIONS.keys()))
    weather_name = random.choice(list(WEATHER_CONDITIONS.keys()))
    pitch = PITCH_CONDITIONS[pitch_name]
    weather = WEATHER_CONDITIONS[weather_name]
    
    # Show conditions
    conditions_embed = discord.Embed(title="🏏 Match Conditions", color=0x00ff88)
    conditions_embed.add_field(name="🌱 Pitch", value=f"{pitch_name}\n_{pitch['description']}_", inline=True)
    conditions_embed.add_field(name="🌤 Weather", value=f"{weather_name}\n_{weather['description']}_", inline=True)
    
    team1_overall = teams_data[team1_name]['overall']
    team2_overall = teams_data[team2_name]['overall']
    conditions_embed.add_field(
        name="💪 Team Strength",
        value=f"{team1_name}: **{team1_overall:.1f}**\n{team2_name}: **{team2_overall:.1f}**",
        inline=False
    )
    
    await ctx.send(embed=conditions_embed)
    await asyncio.sleep(2)
    
    # Toss
    toss_winner = random.choice([team1_name, team2_name])
    choice = random.choice(['bat', 'bowl'])
    
    toss_msg = f"🪙 **{toss_winner}** won the toss and chose to **{choice}**"
    await ctx.send(toss_msg)
    await asyncio.sleep(2)
    
    # Determine batting order
    if (toss_winner == team1_name and choice == 'bat') or (toss_winner == team2_name and choice == 'bowl'):
        first_bat_name, first_bat_squad = team1_name, teams_data[team1_name]['squad']
        second_bat_name, second_bat_squad = team2_name, teams_data[team2_name]['squad']
    else:
        first_bat_name, first_bat_squad = team2_name, teams_data[team2_name]['squad']
        second_bat_name, second_bat_squad = team1_name, teams_data[team1_name]['squad']
    
    # First Innings
    await ctx.send(f"\n**🏏 FIRST INNINGS: {first_bat_name}**")
    team1_innings = simulate_innings_detailed(first_bat_name, first_bat_squad, second_bat_squad, pitch, weather)
    
    # Show over-by-over for first innings (every 3rd over to avoid spam)
    for over_data in team1_innings['over_by_over'][::3]:
        over_msg = f"**{over_data['summary']}**"
        if over_data['commentary']:
            over_msg += "\n" + "\n".join(over_data['commentary'][:2])
        await ctx.send(over_msg)
        await asyncio.sleep(1)
    
    innings_summary = f"\n**📊 {first_bat_name} Innings Summary**\n"
    innings_summary += f"**Score: {team1_innings['total']}/{team1_innings['wickets']} ({team1_innings['overs']} overs)**"
    await ctx.send(innings_summary)
    
    # Top scorer
    team1_batsmen = [(p, s) for p, s in team1_innings['batsmen'].items() if s['balls'] > 0]
    if team1_batsmen:
        top_bat = max(team1_batsmen, key=lambda x: x[1]['runs'])
        await ctx.send(f"⭐ Top Scorer: **{top_bat[0]}** - {top_bat[1]['runs']}({top_bat[1]['balls']})")
    
    await asyncio.sleep(2)
    
    # Second Innings
    target = team1_innings['total']
    await ctx.send(f"\n**🎯 TARGET: {target + 1} runs**")
    await ctx.send(f"**🏏 SECOND INNINGS: {second_bat_name}**")
    
    team2_innings = simulate_innings_detailed(second_bat_name, second_bat_squad, first_bat_squad, pitch, weather, target)
    
    # Show over-by-over with win probability
    for over_data in team2_innings['over_by_over'][::3]:
        overs_remaining = 20 - over_data['over']
        win_prob = calculate_win_probability(
            target, 0,
            over_data['total'], over_data['wickets'],
            overs_remaining
        )
        
        over_msg = f"**{over_data['summary']}**\n"
        over_msg += f"📊 Win Probability: **{win_prob:.1f}%**"
        
        if over_data['commentary']:
            over_msg += "\n" + "\n".join(over_data['commentary'][:2])
        
        await ctx.send(over_msg)
        await asyncio.sleep(1)
    
    # Determine winner
    if first_bat_name == team1_name:
        final_team1 = team1_innings
        final_team2 = team2_innings
    else:
        final_team1 = team2_innings
        final_team2 = team1_innings
    
    # Update team records
    if final_team1['total'] > final_team2['total']:
        winner = team1_name
        teams_data[team1_name]['wins'] = teams_data[team1_name].get('wins', 0) + 1
    elif final_team2['total'] > final_team1['total']:
        winner = team2_name
        teams_data[team2_name]['wins'] = teams_data[team2_name].get('wins', 0) + 1
    else:
        winner = team1_name if team1_overall > team2_overall else team2_name
    
    teams_data[team1_name]['matches_played'] = teams_data[team1_name].get('matches_played', 0) + 1
    teams_data[team2_name]['matches_played'] = teams_data[team2_name].get('matches_played', 0) + 1
    
    save_data(TEAMS_FILE, teams_data)
    
    # Final scorecard
    embed = discord.Embed(title="📋 FINAL SCORECARD", color=0xffd700)
    
    if final_team1['total'] > final_team2['total']:
        result = f"🏆 **{team1_name}** won by **{final_team1['total'] - final_team2['total']} runs**"
    elif final_team2['total'] > final_team1['total']:
        wickets_rem = 10 - final_team2['wickets']
        result = f"🏆 **{team2_name}** won by **{wickets_rem} wickets**"
    else:
        result = f"🏆 **{winner}** won (tie-breaker)"
    
    embed.add_field(name="Result", value=result, inline=False)
    
    embed.add_field(
        name=f"{final_team1['team']} 🏏",
        value=f"**{final_team1['total']}/{final_team1['wickets']}** ({final_team1['overs']} overs)",
        inline=True
    )
    embed.add_field(
        name=f"{final_team2['team']} 🏏",
        value=f"**{final_team2['total']}/{final_team2['wickets']}** ({final_team2['overs']} overs)",
        inline=True
    )
    
    # Top performers
    team1_batsmen = [(p, s) for p, s in final_team1['batsmen'].items() if s['balls'] > 0]
    team2_batsmen = [(p, s) for p, s in final_team2['batsmen'].items() if s['balls'] > 0]
    
    if team1_batsmen:
        top_bat1 = max(team1_batsmen, key=lambda x: x[1]['runs'])
        embed.add_field(
            name=f"⭐ Top Scorer - {final_team1['team']}",
            value=f"**{top_bat1[0]}** - {top_bat1[1]['runs']}({top_bat1[1]['balls']}) | SR: {top_bat1[1]['strike_rate']:.1f}",
            inline=False
        )
    
    if team2_batsmen:
        top_bat2 = max(team2_batsmen, key=lambda x: x[1]['runs'])
        embed.add_field(
            name=f"⭐ Top Scorer - {final_team2['team']}",
            value=f"**{top_bat2[0]}** - {top_bat2[1]['runs']}({top_bat2[1]['balls']}) | SR: {top_bat2[1]['strike_rate']:.1f}",
            inline=False
        )
    
    embed.add_field(name="Conditions", value=f"🌱 {pitch_name} | 🌤 {weather_name}", inline=False)
    embed.set_footer(text=f"Match completed at {datetime.now().strftime('%H:%M')}")
    
    await ctx.send(embed=embed)

@bot.command(name='players')
async def list_players(ctx):
    """List all players"""
    embed = discord.Embed(
        title="🏏 Available Players",
        description=f"Total: {len(PLAYER_DATABASE)} players",
        color=0x00ff00
    )
    
    roles = {}
    for player, data in PLAYER_DATABASE.items():
        role = data['role']
        if role not in roles:
            roles[role] = []
        roles[role].append(player)
    
    for role, players_list in roles.items():
        player_names = ", ".join(players_list[:10])
        if len(players_list) > 10:
            player_names += f" ... (+{len(players_list)-10} more)"
        embed.add_field(
            name=f"{role.replace('_', ' ').title()} ({len(players_list)})",
            value=player_names,
            inline=False
        )
    
    await ctx.send(embed=embed)

@bot.command(name='player')
async def player_profile(ctx, *, player_name: str):
    """Show player profile"""
    if player_name not in PLAYER_DATABASE:
        similar = find_similar_player(player_name)
        if similar:
            await ctx.send(f"❓ Did you mean: **{', '.join(similar)}**?")
        else:
            await ctx.send(f"❌ Player '{player_name}' not found!")
        return
    
    player_data = PLAYER_DATABASE[player_name]
    
    embed = discord.Embed(title=f"🏏 {player_name}", color=0x3498db)
    embed.add_field(name="📊 Batting", value=f"**{player_data['batting']}**/100", inline=True)
    embed.add_field(name="⚾ Bowling", value=f"**{player_data['bowling']}**/100", inline=True)
    embed.add_field(name="🧤 Fielding", value=f"**{player_data['fielding']}**/100", inline=True)
    embed.add_field(name="🎭 Role", value=player_data['role'].replace('_', ' ').title(), inline=True)
    
    overall = (player_data['batting'] + player_data['bowling'] + player_data['fielding']) / 3
    embed.add_field(name="⭐ Overall", value=f"**{overall:.1f}**/100", inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name='teamdelete')
async def team_delete(ctx, *, team_name: str):
    """Delete a team"""
    if team_name not in teams_data:
        await ctx.send(f"❌ Team '{team_name}' not found!")
        return
    
    del teams_data[team_name]
    save_data(TEAMS_FILE, teams_data)
    await ctx.send(f"✅ Team **{team_name}** deleted.")

# Run Bot
if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN")
    if not TOKEN:
        TOKEN = os.getenv("TOKEN")
    if not TOKEN:
        print("❌ Error: DISCORD_TOKEN not set!")
    else:
        print("🚀 Starting Cricket Bot...")
        bot.run(TOKEN)
