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
    "RichardNgarava": {"batting": 24, "bowling": 73, "fielding": 69, "role": "bowler", "style": "fast"},
    
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
FIXTURES_FILE = 'fixtures.json'
RESULT_CHANNEL_FILE = 'result_channel.json'

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
fixtures_data = load_data(FIXTURES_FILE)
result_channels = load_data(RESULT_CHANNEL_FILE)

# Initialize fixtures structure
if 'fixtures' not in fixtures_data:
    fixtures_data['fixtures'] = []
if 'completed' not in fixtures_data:
    fixtures_data['completed'] = []

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

# ADD THIS CLASS HERE (before @bot.event)

class ScorecardView(discord.ui.View):
    def __init__(self, team1_innings, team2_innings, winner, pitch_name, weather_name, timeout=180):
        super().__init__(timeout=timeout)
        self.team1_innings = team1_innings
        self.team2_innings = team2_innings
        self.winner = winner
        self.pitch_name = pitch_name
        self.weather_name = weather_name
    
    @discord.ui.button(label=f"📊 Summary", style=discord.ButtonStyle.primary, custom_id="summary")
    async def summary_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = create_match_summary(
            self.team1_innings, self.team2_innings, 
            self.winner, self.pitch_name, self.weather_name
        )
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="🏏 Team 1 Batting", style=discord.ButtonStyle.success, custom_id="team1_bat")
    async def team1_batting_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = create_batting_scorecard(self.team1_innings)
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="⚾ Team 1 Bowling", style=discord.ButtonStyle.danger, custom_id="team1_bowl")
    async def team1_bowling_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = create_bowling_scorecard(self.team2_innings)  # Team1 bowled against Team2
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="🏏 Team 2 Batting", style=discord.ButtonStyle.success, custom_id="team2_bat")
    async def team2_batting_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = create_batting_scorecard(self.team2_innings)
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="⚾ Team 2 Bowling", style=discord.ButtonStyle.danger, custom_id="team2_bowl")
    async def team2_bowling_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = create_bowling_scorecard(self.team1_innings)  # Team2 bowled against Team1
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def on_timeout(self):
        # Disable all buttons when view times out
        for item in self.children:
            item.disabled = True
class LiveMatchView(discord.ui.View):
    def __init__(self, ctx, first_bat_name, first_bat_squad, second_bat_name, second_bat_squad, 
                 pitch, weather, pitch_name, weather_name, team1_name, team2_name):
        super().__init__(timeout=300)  # 5 minutes timeout
        self.ctx = ctx
        self.first_bat_name = first_bat_name
        self.first_bat_squad = first_bat_squad
        self.second_bat_name = second_bat_name
        self.second_bat_squad = second_bat_squad
        self.pitch = pitch
        self.weather = weather
        self.pitch_name = pitch_name
        self.weather_name = weather_name
        self.team1_name = team1_name
        self.team2_name = team2_name
        
        # Match state
        self.innings = 1
        self.current_over = 0
        self.team1_innings = None
        self.team2_innings = None
        self.message = None
        
    async def start_match(self):
        """Initialize and start the match"""
        embed = discord.Embed(
            title=f"🏏 {self.first_bat_name} vs {self.second_bat_name}",
            description=f"**First Innings: {self.first_bat_name}**\nPress 'Next Over' to start!",
            color=0x00ff00
        )
        embed.add_field(name="🌱 Pitch", value=self.pitch_name, inline=True)
        embed.add_field(name="🌤 Weather", value=self.weather_name, inline=True)
        embed.add_field(name="Score", value="0/0 (0.0 overs)", inline=False)
        
        self.message = await self.ctx.send(embed=embed, view=self)
    
    @discord.ui.button(label="⏭️ Next Over", style=discord.ButtonStyle.primary)
    async def next_over_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        
        if self.innings == 1:
            await self.simulate_first_innings_over()
        else:
            await self.simulate_second_innings_over()
    
    @discord.ui.button(label="⏩ Simulate All", style=discord.ButtonStyle.secondary)
    async def simulate_all_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        
        if self.innings == 1:
            # Finish first innings
            while self.current_over < 20 and (not self.team1_innings or self.team1_innings['wickets'] < 10):
                await self.simulate_first_innings_over()
                await asyncio.sleep(0.5)
        else:
            # Finish second innings
            target = self.team1_innings['total']
            while (self.current_over < 20 and self.team2_innings['wickets'] < 10 
                   and self.team2_innings['total'] <= target):
                await self.simulate_second_innings_over()
                await asyncio.sleep(0.5)
    
    @discord.ui.button(label="📊 Scorecard", style=discord.ButtonStyle.success)
    async def scorecard_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.innings == 1 and self.team1_innings:
            embed = self.create_mini_scorecard(self.team1_innings, "First Innings")
        elif self.innings == 2 and self.team2_innings:
            embed = self.create_mini_scorecard(self.team2_innings, "Second Innings", 
                                               self.team1_innings['total'])
        else:
            embed = discord.Embed(title="No data yet", color=0xff0000)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    async def simulate_first_innings_over(self):
        """Simulate one over of first innings"""
        if self.current_over == 0:
            # Initialize innings
            self.team1_innings = self.init_innings(self.first_bat_name, self.first_bat_squad)
        
        if self.current_over >= 20 or self.team1_innings['wickets'] >= 10:
            await self.end_first_innings()
            return
        
        # Simulate the over
        over_data = self.simulate_one_over(
            self.team1_innings, 
            self.first_bat_squad,
            self.second_bat_squad
        )
        
        self.current_over += 1
        
        # Update display
        embed = self.create_over_embed(over_data, self.team1_innings, 1)
        await self.message.edit(embed=embed, view=self)
        
        # Check if innings ended
        if self.current_over >= 20 or self.team1_innings['wickets'] >= 10:
            await asyncio.sleep(2)
            await self.end_first_innings()
    
    async def simulate_second_innings_over(self):
        """Simulate one over of second innings"""
        if self.current_over == 0:
            # Initialize second innings
            self.team2_innings = self.init_innings(self.second_bat_name, self.second_bat_squad)
        
        target = self.team1_innings['total']
        
        if (self.current_over >= 20 or self.team2_innings['wickets'] >= 10 
            or self.team2_innings['total'] > target):
            await self.end_match()
            return
        
        # Simulate the over
        over_data = self.simulate_one_over(
            self.team2_innings,
            self.second_bat_squad,
            self.first_bat_squad,
            target
        )
        
        self.current_over += 1
        
        # Update display
        embed = self.create_over_embed(over_data, self.team2_innings, 2, target)
        await self.message.edit(embed=embed, view=self)
        
        # Check if innings/match ended
        if (self.current_over >= 20 or self.team2_innings['wickets'] >= 10 
            or self.team2_innings['total'] > target):
            await asyncio.sleep(2)
            await self.end_match()
    
    def init_innings(self, team_name, squad):
        """Initialize innings data structure"""
        batting_order = squad[:11]
        batsman_scores = {}
        for batsman in batting_order:
            batsman_scores[batsman] = {
                'runs': 0, 'balls': 0, 'fours': 0, 'sixes': 0, 
                'out': False, 'strike_rate': 0.0
            }
        
        return {
            'team': team_name,
            'total': 0,
            'wickets': 0,
            'overs': 0,
            'batsmen': batsman_scores,
            'current_batsmen': [batting_order[0], batting_order[1]],
            'next_batsman_index': 2,
            'batting_order': batting_order
        }
    
    def simulate_one_over(self, innings, batting_squad, bowling_squad, target=None):
        """Simulate one complete over"""
        bowlers = get_bowlers(bowling_squad)
        current_bowler = bowlers[self.current_over % len(bowlers)]
        
        over_runs = 0
        over_events = []
        balls_in_over = 0
        
        while balls_in_over < 6 and innings['wickets'] < 10:
            if target and innings['total'] > target:
                break
            
            striker = innings['current_batsmen'][0]
            outcome = simulate_ball(striker, current_bowler, self.pitch, self.weather)
            
            if outcome == 'W':
                innings['wickets'] += 1
                innings['batsmen'][striker]['out'] = True
                over_events.append(f"🔴 WICKET! {striker} OUT")
                
                # New batsman
                if innings['next_batsman_index'] < len(innings['batting_order']):
                    new_batsman = innings['batting_order'][innings['next_batsman_index']]
                    innings['current_batsmen'][0] = new_batsman
                    innings['next_batsman_index'] += 1
                    over_events.append(f"▶️ {new_batsman} comes to bat")
            else:
                runs = int(outcome)
                innings['total'] += runs
                over_runs += runs
                innings['batsmen'][striker]['runs'] += runs
                innings['batsmen'][striker]['balls'] += 1
                
                if runs == 4:
                    innings['batsmen'][striker]['fours'] += 1
                    over_events.append(f"🔵 FOUR by {striker}")
                elif runs == 6:
                    innings['batsmen'][striker]['sixes'] += 1
                    over_events.append(f"🟢 SIX by {striker}!")
                elif runs > 0:
                    over_events.append(f"{runs} run(s)")
                
                # Rotate strike on odd runs
                if runs % 2 == 1:
                    innings['current_batsmen'][0], innings['current_batsmen'][1] = \
                        innings['current_batsmen'][1], innings['current_batsmen'][0]
            
            balls_in_over += 1
        
        innings['overs'] = self.current_over + 1
        
        # Rotate strike at end of over
        innings['current_batsmen'][0], innings['current_batsmen'][1] = \
            innings['current_batsmen'][1], innings['current_batsmen'][0]
        
        # Update strike rates
        for batsman, stats in innings['batsmen'].items():
            if stats['balls'] > 0:
                stats['strike_rate'] = (stats['runs'] / stats['balls']) * 100
        
        return {
            'over_number': self.current_over + 1,
            'runs': over_runs,
            'bowler': current_bowler,
            'events': over_events
        }
    
    def create_over_embed(self, over_data, innings, innings_num, target=None):
        """Create embed for over summary"""
        if innings_num == 1:
            title = f"🏏 First Innings - {innings['team']}"
            color = 0x00ff00
        else:
            title = f"🏏 Second Innings - {innings['team']}"
            color = 0x00aaff
        
        embed = discord.Embed(title=title, color=color)
        
        # Over summary
        over_summary = f"**Over {over_data['over_number']}: {over_data['runs']} runs**\n"
        over_summary += f"Bowler: {over_data['bowler']}\n\n"
        
        # Events (max 4 lines)
        if over_data['events']:
            over_summary += "**Events:**\n"
            for event in over_data['events'][:4]:
                over_summary += f"• {event}\n"
        
        embed.description = over_summary
        
        # Current score
        score_text = f"**{innings['total']}/{innings['wickets']}** ({innings['overs']} overs)"
        embed.add_field(name="📊 Score", value=score_text, inline=True)
        
        # Target info for second innings
        if target is not None:
            runs_needed = target - innings['total'] + 1
            balls_left = (20 - innings['overs']) * 6
            
            if runs_needed > 0:
                rrr = (runs_needed / ((20 - innings['overs']) if innings['overs'] < 20 else 1)) if innings['overs'] < 20 else 0
                target_text = f"Need **{runs_needed}** from **{balls_left}** balls\nRRR: {rrr:.2f}"
            else:
                target_text = f"🏆 **TARGET ACHIEVED!**"
            
            embed.add_field(name="🎯 Target", value=target_text, inline=True)
        
        # Current batsmen
        batsmen_text = ""
        for i, batsman in enumerate(innings['current_batsmen'][:2]):
            if batsman in innings['batsmen']:
                stats = innings['batsmen'][batsman]
                if not stats['out']:
                    striker = "*" if i == 0 else ""
                    batsmen_text += f"{striker}{batsman}: **{stats['runs']}({stats['balls']})**\n"
        
        if batsmen_text:
            embed.add_field(name="🏏 At Crease", value=batsmen_text, inline=False)
        
        return embed
    
    def create_mini_scorecard(self, innings, title, target=None):
        """Create mini scorecard embed"""
        embed = discord.Embed(title=f"📊 {title} - {innings['team']}", color=0xffd700)
        
        # Top 5 batsmen
        batsmen_list = [(p, s) for p, s in innings['batsmen'].items() if s['balls'] > 0]
        batsmen_list.sort(key=lambda x: x[1]['runs'], reverse=True)
        
        bat_text = "```\n"
        bat_text += f"{'Player':<15} {'R(B)':<10} {'SR':<6}\n"
        bat_text += "-" * 35 + "\n"
        
        for player, stats in batsmen_list[:5]:
            out = "*" if stats['out'] else ""
            bat_text += f"{player[:14]:<15} {stats['runs']}({stats['balls']}) {out:<10} {stats['strike_rate']:.0f}\n"
        
        bat_text += "```"
        embed.add_field(name="Batting", value=bat_text, inline=False)
        
        score = f"**{innings['total']}/{innings['wickets']}** ({innings['overs']} overs)"
        if target:
            score += f"\nTarget: {target + 1}"
        embed.add_field(name="Score", value=score, inline=False)
        
        return embed
    
    async def end_first_innings(self):
        """End first innings and start second"""
        embed = discord.Embed(
            title=f"📊 End of First Innings",
            description=f"**{self.first_bat_name}: {self.team1_innings['total']}/{self.team1_innings['wickets']}** ({self.team1_innings['overs']} overs)",
            color=0xffd700
        )
        
        # Top scorer
        batsmen_list = [(p, s) for p, s in self.team1_innings['batsmen'].items() if s['balls'] > 0]
        if batsmen_list:
            top_bat = max(batsmen_list, key=lambda x: x[1]['runs'])
            embed.add_field(
                name="⭐ Top Scorer",
                value=f"**{top_bat[0]}** - {top_bat[1]['runs']}({top_bat[1]['balls']})",
                inline=False
            )
        
        target = self.team1_innings['total']
        embed.add_field(
            name="🎯 Target",
            value=f"**{self.second_bat_name}** needs **{target + 1}** runs to win",
            inline=False
        )
        
        await self.message.edit(embed=embed, view=self)
        
        # Reset for second innings
        self.innings = 2
        self.current_over = 0
        
        await asyncio.sleep(3)
        
        # Start second innings display
        embed = discord.Embed(
            title=f"🏏 Second Innings - {self.second_bat_name}",
            description=f"**Target: {target + 1} runs**\nPress 'Next Over' to continue!",
            color=0x00aaff
        )
        embed.add_field(name="Score", value="0/0 (0.0 overs)", inline=False)
        
        await self.message.edit(embed=embed, view=self)
    
    async def end_match(self):
        """End match and show final result"""
        # Disable all buttons
        for item in self.children:
            item.disabled = True
        
        # Determine winner
        if self.team1_innings['total'] > self.team2_innings['total']:
            winner = self.team1_name
            margin = self.team1_innings['total'] - self.team2_innings['total']
            result = f"🏆 **{winner}** won by **{margin} runs**"
        elif self.team2_innings['total'] > self.team1_innings['total']:
            winner = self.team2_name
            wickets_rem = 10 - self.team2_innings['wickets']
            result = f"🏆 **{winner}** won by **{wickets_rem} wickets**"
        else:
            winner = self.team1_name
            result = f"🏆 **Match Tied! {winner}** wins on boundary count"
        
        # Update team stats
        teams_data[self.team1_name]['matches_played'] = teams_data[self.team1_name].get('matches_played', 0) + 1
        teams_data[self.team2_name]['matches_played'] = teams_data[self.team2_name].get('matches_played', 0) + 1
        
        if winner == self.team1_name:
            teams_data[self.team1_name]['wins'] = teams_data[self.team1_name].get('wins', 0) + 1
        else:
            teams_data[self.team2_name]['wins'] = teams_data[self.team2_name].get('wins', 0) + 1
        
        save_data(TEAMS_FILE, teams_data)
        await self.message.edit(view=self)
        
        # Show final scorecard with buttons
        if self.first_bat_name == self.team1_name:
            final_team1 = self.team1_innings
            final_team2 = self.team2_innings
        else:
            final_team1 = self.team2_innings
            final_team2 = self.team1_innings
        
        summary_embed = create_match_summary(
            final_team1, final_team2, winner, self.pitch_name, self.weather_name
        )
        
        view = ScorecardView(
            final_team1, final_team2, winner, self.pitch_name, self.weather_name
        )
        
        view.children[1].label = f"🏏 {final_team1['team']} Batting"
        view.children[2].label = f"⚾ {final_team1['team']} Bowling"
        view.children[3].label = f"🏏 {final_team2['team']} Batting"
        view.children[4].label = f"⚾ {final_team2['team']} Bowling"
        
        await self.ctx.send(
            "**🏏 Match Complete! Use buttons below to view detailed scorecards:**",
            embed=summary_embed,
            view=view
        )
        
        # Send raw stats
        raw_stats = create_raw_stats(
            final_team1, final_team2, winner, self.pitch_name, self.weather_name
        )
        await self.ctx.send(
            f"```jsonn{json.dumps(raw_stats, indent=2)}n```n*Reply to this message with `!addstats` to add to leaderboard*"
        )

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
        value=(
            "**!teamadd <name> <p1> ... <p11>** - Create team\n"
            "**!teams** - Show all teams\n"
            "**!teamdelete <name>** - Delete team"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🎮 Match Simulation",
        value=(
            "**!sim <team1> <team2>** - Quick simulation\n"
            "**!simlive <team1> <team2>** - Interactive over-by-over\n"
            "**!quicksim <team1> <team2>** - Instant result"
        ),
        inline=False
    )
    
    embed.add_field(
        name="📊 Statistics & Leaderboards",
        value=(
            "**!addstats** - Add match stats (reply to stats msg)\n"
            "**!standings** - Team rankings\n"
            "**!lb [category]** - Player leaderboards\n"
            "   Categories: `PURPLE_CAP`, `ORANGE_CAP`, `DUCK`, `ALL`"
        ),
        inline=False
    )
    
    embed.add_field(
        name="📅 Fixtures & Results",
        value=(
            "**!fixtures add <t1> <t2> <date>** - Add fixture\n"
            "**!fixtures list** - Show fixtures\n"
            "**!fixtures remove <id>** - Remove fixture\n"
            "**!result #channel** - Set result channel"
        ),
        inline=False
    )
    
    embed.add_field(
        name="👤 Player Info",
        value=(
            "**!player <name>** - View player profile\n"
            "**!players** - List all players"
        ),
        inline=False
    )
    
    embed.add_field(
        name="ℹ️ Other",
        value=(
            "**!updates** - View bot updates\n"
            "**!resetstats** - Reset all stats (Admin only)"
        ),
        inline=False
    )
    
    embed.set_footer(text="Use !updates to see latest features!")
    
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

# ADD THE THREE HELPER FUNCTIONS HERE:

def create_batting_scorecard(innings_data):
    """Create batting scorecard embed"""
    embed = discord.Embed(
        title=f"🏏 {innings_data['team']} - Batting Scorecard",
        color=0x00ff00
    )
    
    # Sort batsmen by batting order (runs scored)
    batsmen_list = [(player, stats) for player, stats in innings_data['batsmen'].items() 
                    if stats['balls'] > 0 or stats['out']]
    
    scorecard_text = "```\n"
    scorecard_text += f"{'Player':<20} {'R':<5} {'B':<5} {'4s':<4} {'6s':<4} {'SR':<6}\n"
    scorecard_text += "-" * 50 + "\n"
    
    for player, stats in batsmen_list:
        out_symbol = "*" if stats['out'] else ""
        scorecard_text += f"{player:<20} {stats['runs']:<5} {stats['balls']:<5} "
        scorecard_text += f"{stats['fours']:<4} {stats['sixes']:<4} {stats['strike_rate']:<6.1f}{out_symbol}\n"
    
    scorecard_text += "```"
    embed.description = scorecard_text
    
    embed.add_field(
        name="Total",
        value=f"**{innings_data['total']}/{innings_data['wickets']}** ({innings_data['overs']} overs)",
        inline=False
    )
    
    return embed

def create_bowling_scorecard(innings_data):
    """Create bowling scorecard embed"""
    embed = discord.Embed(
        title=f"⚾ Bowling Against {innings_data['team']}",
        color=0xff6b6b
    )
    
    bowlers_list = [(bowler, stats) for bowler, stats in innings_data['bowlers'].items() 
                    if stats['overs'] > 0]
    
    scorecard_text = "```\n"
    scorecard_text += f"{'Bowler':<20} {'O':<4} {'R':<5} {'W':<4} {'Eco':<6}\n"
    scorecard_text += "-" * 45 + "\n"
    
    for bowler, stats in bowlers_list:
        scorecard_text += f"{bowler:<20} {stats['overs']:<4} {stats['runs']:<5} "
        scorecard_text += f"{stats['wickets']:<4} {stats['economy']:<6.2f}\n"
    
    scorecard_text += "```"
    embed.description = scorecard_text
    
    return embed

def create_match_summary(team1_innings, team2_innings, winner, pitch_name, weather_name):
    embed = discord.Embed(title="📊 Match Summary", color=0xffd700)
    if team1_innings['total'] > team2_innings['total']:
        margin = team1_innings['total'] - team2_innings['total']
        result = f"🏆 **{winner}** won by **{margin} runs**"
    else:
        wickets_rem = 10 - team2_innings['wickets']
        result = f"🏆 **{winner}** won by **{wickets_rem} wickets**"
    embed.add_field(name="Result", value=result, inline=False)
    embed.add_field(name=f"{team1_innings['team']}", value=f"**{team1_innings['total']}/{team1_innings['wickets']}** ({team1_innings['overs']})", inline=True)
    embed.add_field(name=f"{team2_innings['team']}", value=f"**{team2_innings['total']}/{team2_innings['wickets']}** ({team2_innings['overs']})", inline=True)
    team1_batsmen = [(p, s) for p, s in team1_innings['batsmen'].items() if s['balls'] > 0]
    team2_batsmen = [(p, s) for p, s in team2_innings['batsmen'].items() if s['balls'] > 0]
    performers_text = ""
    if team1_batsmen:
        top_bat1 = max(team1_batsmen, key=lambda x: x[1]['runs'])
        performers_text += f"⭐ **{top_bat1[0]}** - {top_bat1[1]['runs']}({top_bat1[1]['balls']})n"
    if team2_batsmen:
        top_bat2 = max(team2_batsmen, key=lambda x: x[1]['runs'])
        performers_text += f"⭐ **{top_bat2[0]}** - {top_bat2[1]['runs']}({top_bat2[1]['balls']})\n"
    all_bowlers = []
    for bowler, stats in team1_innings['bowlers'].items():
        if stats['wickets'] > 0:
            all_bowlers.append((bowler, stats))
    for bowler, stats in team2_innings['bowlers'].items():
        if stats['wickets'] > 0:
            all_bowlers.append((bowler, stats))
    if all_bowlers:
        best_bowler = max(all_bowlers, key=lambda x: x[1]['wickets'])
        performers_text += f"🎯 **{best_bowler[0]}** - {best_bowler[1]['wickets']}/{best_bowler[1]['runs']}"
    embed.add_field(name="Top Performers", value=performers_text, inline=False)
    embed.add_field(name="Conditions", value=f"🌱 {pitch_name} | 🌤 {weather_name}", inline=False)
    return embed


def create_raw_stats(team1_innings, team2_innings, winner, pitch_name, weather_name):
    match_id = f"match_{int(datetime.now().timestamp())}"
    team1_batsmen = [(p, s) for p, s in team1_innings['batsmen'].items() if s['balls'] > 0]
    team2_batsmen = [(p, s) for p, s in team2_innings['batsmen'].items() if s['balls'] > 0]
    top_bat_team1 = max(team1_batsmen, key=lambda x: x[1]['runs']) if team1_batsmen else (None, {'runs': 0})
    top_bat_team2 = max(team2_batsmen, key=lambda x: x[1]['runs']) if team2_batsmen else (None, {'runs': 0})
    team1_bowlers = [(b, s) for b, s in team1_innings['bowlers'].items() if s['overs'] > 0]
    team2_bowlers = [(b, s) for b, s in team2_innings['bowlers'].items() if s['overs'] > 0]
    best_bowl_team1 = max(team1_bowlers, key=lambda x: x[1]['wickets']) if team1_bowlers else (None, {'wickets': 0})
    best_bowl_team2 = max(team2_bowlers, key=lambda x: x[1]['wickets']) if team2_bowlers else (None, {'wickets': 0})
    return {
        'match_id': match_id,
        'date': datetime.now().isoformat(),
        'teams': {
            team1_innings['team']: {
                'score': f"{team1_innings['total']}/{team1_innings['wickets']}",
                'overs': team1_innings['overs'],
                'batsmen': team1_innings['batsmen'],
                'bowlers': team2_innings['bowlers']
            },
            team2_innings['team']: {
                'score': f"{team2_innings['total']}/{team2_innings['wickets']}",
                'overs': team2_innings['overs'],
                'batsmen': team2_innings['batsmen'],
                'bowlers': team1_innings['bowlers']
            }
        },
        'winner': winner,
        'conditions': {'pitch': pitch_name, 'weather': weather_name},
        'top_performers': {
            'highest_score': top_bat_team1[0] if top_bat_team1[1]['runs'] > top_bat_team2[1]['runs'] else top_bat_team2[0],
            'highest_score_runs': max(top_bat_team1[1]['runs'], top_bat_team2[1]['runs']),
            'best_bowling': best_bowl_team1[0] if best_bowl_team1[1]['wickets'] > best_bowl_team2[1]['wickets'] else best_bowl_team2[0],
            'best_bowling_wickets': max(best_bowl_team1[1]['wickets'], best_bowl_team2[1]['wickets'])
        }
    }


def update_player_stats(raw_stats):
    for team_name, team_data in raw_stats['teams'].items():
        for player, bat_stats in team_data['batsmen'].items():
            if bat_stats['balls'] > 0:
                if player not in player_stats:
                    player_stats[player] = {'matches': 0, 'runs': 0, 'balls': 0, 'highest_score': 0, 'fifties': 0, 'hundreds': 0, 'fours': 0, 'sixes': 0, 'ducks': 0, 'wickets': 0, 'overs_bowled': 0, 'runs_conceded': 0, 'best_bowling': '0/0'}
                player_stats[player]['matches'] += 1
                player_stats[playeatsmen].items()
            if bat_stats['balls'] > 0:
                if player not in player_stats:
                    player_stats[player] = {
                        'matches': 0,
                        'runs': 0,
                        'balls': 0,
                        'highest_score': 0,
                        'fifties': 0,
                        'hundreds': 0,
                        'fours': 0,
                        'sixes': 0,
                        'ducks': 0,
                        'wickets': 0,
                        'overs_bowled': 0,
                        'runs_conceded': 0,
                        'best_bowling': '0/0'
                    }
                
                player_stats[player]['matches'] += 1
                player_stats[player]['runs'] += bat_stats['runs']
                player_stats[player]['balls'] += bat_stats['balls']
                player_stats[player]['fours'] += bat_stats['fours']
                player_stats[player]['sixes'] += bat_stats['sixes']
                
                if bat_stats['runs'] > player_stats[player]['highest_score']:
                    player_stats[player]['highest_score'] = bat_stats['runs']
                
                if bat_stats['runs'] >= 100:
                    player_stats[player]['hundreds'] += 1
                elif bat_stats['runs'] >= 50:
                    player_stats[player]['fifties'] += 1
                
                if bat_stats['runs'] == 0 and bat_stats['out']:
                    player_stats[player]['ducks'] += 1
        
        # Update bowling stats
        for bowler, bowl_stats in team_data['bowlers'].items():
            if bowl_stats['overs'] > 0:
                if bowler not in player_stats:
                    player_stats[bowler] = {
                        'matches': 0,
                        'runs': 0,
                        'balls': 0,
                        'highest_score': 0,
                        'fifties': 0,
                        'hundreds': 0,
                        'fours': 0,
                        'sixes': 0,
                        'ducks': 0,
                        'wickets': 0,
                        'overs_bowled': 0,
                        'runs_conceded': 0,
                        'best_bowling': '0/0'
                    }
                
                player_stats[bowler]['wickets'] += bowl_stats['wickets']
                player_stats[bowler]['overs_bowled'] += bowl_stats['overs']
                player_stats[bowler]['runs_conceded'] += bowl_stats['runs']
                
                # Update best bowling
                current_best = player_stats[bowler]['best_bowling'].split('/')
                if bowl_stats['wickets'] > int(current_best[0]):
                    player_stats[bowler]['best_bowling'] = f"{bowl_stats['wickets']}/{bowl_stats['runs']}"
                elif bowl_stats['wickets'] == int(current_best[0]) and bowl_stats['runs'] < int(current_best[1]):
                    player_stats[bowler]['best_bowling'] = f"{bowl_stats['wickets']}/{bowl_stats['runs']}"
    
    save_data(STATS_FILE, player_stats)
    return embed
@bot.command(name='removestats')
async def remove_stats(ctx):
    """Remove stats from a match result (reply to raw stats message)"""
    if not ctx.message.reference:
        await ctx.send("❌ Please reply to a raw stats message to remove stats!")
        return
    
    await ctx.send("⚠️ **Warning:** Removing stats is complex and may cause inconsistencies. Consider resetting all stats instead with `!resetstats`.")
@bot.command(name='addstats')
async def add_stats(ctx):
    """Add stats from a match result (reply to raw stats message)"""
    if not ctx.message.reference:
        await ctx.send("❌ Please reply to a raw stats message to add stats!")
        return
    
    try:
        # Get the referenced message
        ref_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        
        # Extract JSON from code block
        content = ref_message.content
        if '```json' in content:
            json_str = content.split('```json')[1].split('```')[0].strip()
            raw_stats = json.loads(json_str)
            
            # Update player stats
            update_player_stats(raw_stats)
            
            await ctx.send(f"✅ Stats added successfully for match: {raw_stats['match_id']}")
        else:
            await ctx.send("❌ No valid stats found in the referenced message!")
    
    except Exception as e:
        await ctx.send(f"❌ Error adding stats: {str(e)}")
@bot.command(name='fixtures')
async def fixtures(ctx, action: str = "list", team1: str = None, team2: str = None, *, date: str = None):
    """Manage fixtures - Usage: !fixtures add <team1> <team2> <date> | !fixtures list | !fixtures remove <index>"""
    
    if action.lower() == "add":
        if not team1 or not team2:
            await ctx.send("❌ Usage: `!fixtures add <team1> <team2> <date>`")
            return
        
        if team1 not in teams_data or team2 not in teams_data:
            await ctx.send(f"❌ One or both teams not found!")
            return
        
        fixture = {
            'id': len(fixtures_data['fixtures']) + 1,
            'team1': team1,
            'team2': team2,
            'date': date or "TBD",
            'added_by': str(ctx.author),
            'added_at': datetime.now().isoformat()
        }
        
        fixtures_data['fixtures'].append(fixture)
        save_data(FIXTURES_FILE, fixtures_data)
        
        await ctx.send(f"✅ Fixture added: **{team1}** vs **{team2}** on {date or 'TBD'}")
    
    elif action.lower() == "list":
        if not fixtures_data['fixtures']:
            await ctx.send("❌ No upcoming fixtures!")
            return
        
        embed = discord.Embed(
            title="📅 UPCOMING FIXTURES",
            color=0x3498db
        )
        
        for fixture in fixtures_data['fixtures']:
            fixture_text = f"**{fixture['team1']}** vs **{fixture['team2']}**\n"
            fixture_text += f"📅 Date: {fixture['date']}\n"
            fixture_text += f"ID: {fixture['id']}"
            
            embed.add_field(
                name=f"Match #{fixture['id']}",
                value=fixture_text,
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    elif action.lower() == "remove":
        if not team1 or not team1.isdigit():
            await ctx.send("❌ Usage: `!fixtures remove <fixture_id>`")
            return
        
        fixture_id = int(team1)
        fixtures_data['fixtures'] = [f for f in fixtures_data['fixtures'] if f['id'] != fixture_id]
        save_data(FIXTURES_FILE, fixtures_data)
        
        await ctx.send(f"✅ Fixture #{fixture_id} removed!")
    
    else:
        await ctx.send("❌ Invalid action! Use: `add`, `list`, or `remove`")

@bot.command(name='result')
async def result(ctx, channel: discord.TextChannel = None):
    """Forward match result to a specific channel (reply to stats message)"""
    
    if channel:
        # Set result channel
        result_channels[str(ctx.guild.id)] = channel.id
        save_data(RESULT_CHANNEL_FILE, result_channels)
        await ctx.send(f"✅ Match results will now be forwarded to {channel.mention}")
        return
    
    if not ctx.message.reference:
        await ctx.send("❌ Please reply to a stats message or specify a channel: `!result #channel`")
        return
    
    try:
        # Get the referenced message
        ref_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        
        # Check if result channel is set
        guild_id = str(ctx.guild.id)
        if guild_id not in result_channels:
            await ctx.send("❌ No result channel set! Use `!result #channel` first.")
            return
        
        result_channel_id = result_channels[guild_id]
        result_channel = bot.get_channel(result_channel_id)
        
        if not result_channel:
            await ctx.send("❌ Result channel not found!")
            return
        
        # Forward the message
        await result_channel.send(f"**Match Result Posted by {ctx.author.mention}:**\n{ref_message.content}")
        await ctx.send(f"✅ Result forwarded to {result_channel.mention}")
    
    except Exception as e:
        await ctx.send(f"❌ Error forwarding result: {str(e)}")
@bot.command(name='standings')
async def standings(ctx):
    """Show team standings/leaderboard"""
    if not teams_data:
        await ctx.send("❌ No teams registered yet!")
                return
    
    # Sort teams by wins, then by overall rating
    sorted_teams = sorted(
        teams_data.items(),
        key=lambda x: (x[1].get('wins', 0), x[1].get('overall', 0)),
        reverse=True
    )
    
    embed = discord.Embed(
        title="🏆 TEAM STANDINGS",
        description="Rankings based on wins and team strength",
        color=0xffd700
    )
    
    standings_text = "```\n"
    standings_text += f"{'Rank':<6} {'Team':<20} {'P':<4} {'W':<4} {'L':<4} {'Rating':<8}\n"
    standings_text += "-" * 50 + "\n"
    
    for rank, (team_name, team_info) in enumerate(sorted_teams, 1):
        matches = team_info.get('matches_played', 0)
        wins = team_info.get('wins', 0)
        losses = matches - wins
        rating = team_info.get('overall', 0)
        
        medal = ""
        if rank == 1:
            medal = "🥇"
        elif rank == 2:
            medal = "🥈"
        elif rank == 3:
            medal = "🥉"
        
        standings_text += f"{medal}{rank:<5} {team_name[:19]:<20} {matches:<4} {wins:<4} {losses:<4} {rating:<8.1f}\n"
    
    standings_text += "```"
    
    embed.description = standings_text
    embed.set_footer(text="P=Played | W=Wins | L=Losses")
    
    await ctx.send(embed=embed)

@bot.command(name='lb')
async def leaderboard(ctx, category: str = "all"):
    """Show player leaderboards - Categories: PURPLE_CAP, ORANGE_CAP, DUCK, ALL"""
    if not player_stats:
        await ctx.send("❌ No player statistics available yet! Play some matches first.")
        return
    
    category = category.upper()
    
    if category == "PURPLE_CAP" or category == "PURPLE":
        # Most wickets
        sorted_players = sorted(
            player_stats.items(),
            key=lambda x: x[1].get('wickets', 0),
            reverse=True
        )[:10]
        
        embed = discord.Embed(
            title="🟣 PURPLE CAP - Most Wickets",
            color=0x800080
        )
        
        lb_text = "```\n"
        lb_text += f"{'Rank':<6} {'Player':<20} {'Wickets':<10} {'Overs':<8} {'Econ':<8}\n"
        lb_text += "-" * 55 + "\n"
        
        for rank, (player, stats) in enumerate(sorted_players, 1):
            wickets = stats.get('wickets', 0)
            overs = stats.get('overs_bowled', 0)
            runs = stats.get('runs_conceded', 0)
            econ = (runs / overs) if overs > 0 else 0
            
            lb_text += f"{rank:<6} {player[:19]:<20} {wickets:<10} {overs:<8} {econ:<8.2f}\n"
        
        lb_text += "```"
        embed.description = lb_text
    
    elif category == "ORANGE_CAP" or category == "ORANGE":
        # Most runs
        sorted_players = sorted(
            player_stats.items(),
            key=lambda x: x[1].get('runs', 0),
            reverse=True
        )[:10]
        
        embed = discord.Embed(
            title="🟠 ORANGE CAP - Most Runs",
            color=0xff8c00
        )
        
        lb_text = "```\n"
        lb_text += f"{'Rank':<6} {'Player':<20} {'Runs':<8} {'HS':<6} {'SR':<8}\n"
        lb_text += "-" * 50 + "\n"
        
        for rank, (player, stats) in enumerate(sorted_players, 1):
            runs = stats.get('runs', 0)
            hs = stats.get('highest_score', 0)
            balls = stats.get('balls', 1)
            sr = (runs / balls * 100) if balls > 0 else 0
            
            lb_text += f"{rank:<6} {player[:19]:<20} {runs:<8} {hs:<6} {sr:<8.1f}\n"
        
        lb_text += "```"
        embed.description = lb_text
    
    elif category == "DUCK" or category == "DUCKS":
        # Most ducks
        sorted_players = sorted(
            player_stats.items(),
            key=lambda x: x[1].get('ducks', 0),
            reverse=True
        )[:10]
        
        sorted_players = [p for p in sorted_players if p[1].get('ducks', 0) > 0]
        
        embed = discord.Embed(
            title="🦆 GOLDEN DUCK - Most Ducks",
            description="*Players who got out for 0 most times*",
            color=0xffff00
        )
        
        lb_text = "```\n"
        lb_text += f"{'Rank':<6} {'Player':<25} {'Ducks':<10} {'Matches':<10}\n"
        lb_text += "-" * 55 + "\n"
        
        for rank, (player, stats) in enumerate(sorted_players, 1):
            ducks = stats.get('ducks', 0)
            matches = stats.get('matches', 0)
            
            lb_text += f"{rank:<6} {player[:24]:<25} {ducks:<10} {matches:<10}\n"
        
        lb_text += "```"
        
        if not sorted_players:
            lb_text = "No ducks recorded yet! 🎉"
        
        embed.description = lb_text
    
    else:  # ALL
        embed = discord.Embed(
            title="📊 ALL LEADERBOARDS",
            color=0x00ff00
        )
        
        # Top 3 run scorers
        top_runs = sorted(player_stats.items(), key=lambda x: x[1].get('runs', 0), reverse=True)[:3]
        runs_text = ""
        for i, (player, stats) in enumerate(top_runs, 1):
            runs_text += f"{i}. **{player}** - {stats.get('runs', 0)} runs\n"
        embed.add_field(name="🟠 Top Run Scorers", value=runs_text or "No data", inline=True)
        
        # Top 3 wicket takers
        top_wickets = sorted(player_stats.items(), key=lambda x: x[1].get('wickets', 0), reverse=True)[:3]
        wickets_text = ""
        for i, (player, stats) in enumerate(top_wickets, 1):
            wickets_text += f"{i}. **{player}** - {stats.get('wickets', 0)} wickets\n"
        embed.add_field(name="🟣 Top Wicket Takers", value=wickets_text or "No data", inline=True)
        
        # Top 3 ducks
        top_ducks = sorted(player_stats.items(), key=lambda x: x[1].get('ducks', 0), reverse=True)[:3]
        top_ducks = [p for p in top_ducks if p[1].get('ducks', 0) > 0]
        ducks_text = ""
        for i, (player, stats) in enumerate(top_ducks, 1):
            ducks_text += f"{i}. **{player}** - {stats.get('ducks', 0)} ducks 🦆\n"
        embed.add_field(name="🦆 Most Ducks", value=ducks_text or "No ducks! 🎉", inline=False)
        
        embed.set_footer(text="Use !lb PURPLE_CAP, !lb ORANGE_CAP, or !lb DUCK for detailed leaderboards")
    
    await ctx.send(embed=embed)
@bot.command(name='resetstats')
async def reset_stats(ctx):
    """Reset all player statistics (Admin only)"""
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ Only administrators can reset stats!")
        return
    
    global player_stats
    player_stats = {}
    save_data(STATS_FILE, player_stats)
    await ctx.send("✅ All player statistics have been reset!")

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
    
    # Create interactive scorecard with buttons
    summary_embed = create_match_summary(
        final_team1, final_team2, winner, pitch_name, weather_name
    )
    
    view = ScorecardView(
        final_team1, final_team2, winner, pitch_name, weather_name
    )
    
    # Update button labels with actual team names
    view.children[1].label = f"🏏 {final_team1['team']} Batting"
    view.children[2].label = f"⚾ {final_team1['team']} Bowling"
    view.children[3].label = f"🏏 {final_team2['team']} Batting"
    view.children[4].label = f"⚾ {final_team2['team']} Bowling"
    
    await ctx.send(
        "**🏏 Match Complete! Use buttons below to view detailed scorecards:**",
        embed=summary_embed,
        view=view
    )
    
    # Send raw stats for adding to leaderboard
    raw_stats = create_raw_stats(final_team1, final_team2, winner, pitch_name, weather_name)
    stats_msg = await ctx.send(f"```json\n{json.dumps(raw_stats, indent=2)}\n```\n*Reply to this message with `!addstats` to add to leaderboard*")

@bot.command(name='simlive')
async def simulate_match_live(ctx, team1_name: str, team2_name: str):
    """Simulate a match with FULL over-by-over commentary"""
    if team1_name not in teams_data or team2_name not in teams_data:
        await ctx.send(f"❌ One or both teams not found!")
        return
    
    await ctx.send(f"🏏 **LIVE MATCH: {team1_name} vs {team2_name}**")
    await ctx.send("⚠️ This will show detailed over-by-over updates!")
    
    # Same setup as original sim
    pitch_name = random.choice(list(PITCH_CONDITIONS.keys()))
    weather_name = random.choice(list(WEATHER_CONDITIONS.keys()))
    pitch = PITCH_CONDITIONS[pitch_name]
    weather = WEATHER_CONDITIONS[weather_name]
    
    # Conditions
    conditions_embed = discord.Embed(title="🏏 Match Conditions", color=0x00ff88)
    conditions_embed.add_field(name="🌱 Pitch", value=f"{pitch_name}\n_{pitch['description']}_", inline=True)
    conditions_embed.add_field(name="🌤 Weather", value=f"{weather_name}\n_{weather['description']}_", inline=True)
    await ctx.send(embed=conditions_embed)
    await asyncio.sleep(2)
    
    # Toss
    toss_winner = random.choice([team1_name, team2_name])
    choice = random.choice(['bat', 'bowl'])
    await ctx.send(f"🪙 **{toss_winner}** won the toss and chose to **{choice}**")
    await asyncio.sleep(2)
    
    # Determine batting order
    if (toss_winner == team1_name and choice == 'bat') or (toss_winner == team2_name and choice == 'bowl'):
        first_bat_name, first_bat_squad = team1_name, teams_data[team1_name]['squad']
        second_bat_name, second_bat_squad = team2_name, teams_data[team2_name]['squad']
    else:
        first_bat_name, first_bat_squad = team2_name, teams_data[team2_name]['squad']
        second_bat_name, second_bat_squad = team1_name, teams_data[team1_name]['squad']
    
    # First Innings - DETAILED
    await ctx.send(f"\n**🏏 FIRST INNINGS: {first_bat_name}**")
    team1_innings = simulate_innings_detailed(first_bat_name, first_bat_squad, second_bat_squad, pitch, weather)
    
    # Show every 3rd over
    for over_data in team1_innings['over_by_over'][::3]:
        over_msg = f"**{over_data['summary']}**"
        if over_data['commentary']:
            over_msg += "\n" + "\n".join(over_data['commentary'][:2])
        await ctx.send(over_msg)
        await asyncio.sleep(1)
    
    innings_summary = f"\n**📊 {first_bat_name} Innings Summary**\n"
    innings_summary += f"**Score: {team1_innings['total']}/{team1_innings['wickets']} ({team1_innings['overs']} overs)**"
    await ctx.send(innings_summary)
    
    team1_batsmen = [(p, s) for p, s in team1_innings['batsmen'].items() if s['balls'] > 0]
    if team1_batsmen:
        top_bat = max(team1_batsmen, key=lambda x: x[1]['runs'])
        await ctx.send(f"⭐ Top Scorer: **{top_bat[0]}** - {top_bat[1]['runs']}({top_bat[1]['balls']})")
    
    await asyncio.sleep(2)
    
    # Second Innings - DETAILED
    target = team1_innings['total']
    await ctx.send(f"\n**🎯 TARGET: {target + 1} runs**")
    await ctx.send(f"**🏏 SECOND INNINGS: {second_bat_name}**")
    
    team2_innings = simulate_innings_detailed(second_bat_name, second_bat_squad, first_bat_squad, pitch, weather, target)
    
    # Show every 3rd over with win probability
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
    
    # Determine winner (rest of the code same as original)
    if first_bat_name == team1_name:
        final_team1 = team1_innings
        final_team2 = team2_innings
    else:
        final_team1 = team2_innings
        final_team2 = team1_innings
    
    if final_team1['total'] > final_team2['total']:
        winner = team1_name
        teams_data[team1_name]['wins'] = teams_data[team1_name].get('wins', 0) + 1
    elif final_team2['total'] > final_team1['total']:
        winner = team2_name
        teams_data[team2_name]['wins'] = teams_data[team2_name].get('wins', 0) + 1
    else:
        team1_overall = teams_data[team1_name]['overall']
        team2_overall = teams_data[team2_name]['overall']
        winner = team1_name if team1_overall > team2_overall else team2_name
    
    teams_data[team1_name]['matches_played'] = teams_data[team1_name].get('matches_played', 0) + 1
    teams_data[team2_name]['matches_played'] = teams_data[team2_name].get('matches_played', 0) + 1
    save_data(TEAMS_FILE, teams_data)
    
    # Final scorecard with buttons (same as before)
    summary_embed = create_match_summary(
        final_team1, final_team2, winner, pitch_name, weather_name
    )
    
    view = ScorecardView(
        final_team1, final_team2, winner, pitch_name, weather_name
    )
    
    view.children[1].label = f"🏏 {final_team1['team']} Batting"
    view.children[2].label = f"⚾ {final_team1['team']} Bowling"
    view.children[3].label = f"🏏 {final_team2['team']} Batting"
    view.children[4].label = f"⚾ {final_team2['team']} Bowling"
    
    await ctx.send(
        "**🏏 Match Complete! Use buttons below to view detailed scorecards:**",
        embed=summary_embed,
        view=view
    )
        
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
