"""
ADVANCED DISCORD CRICKET SIMULATION BOT
========================================
- Real player database with batting/bowling/fielding stats
- Pitch conditions (Green, Dry, Dusty, Flat)
- Weather effects (Sunny, Cloudy, Overcast, Rain)
- Over-by-over simulation with live updates
- Win probability calculator
- Realistic simulation based on player ratings
- Player name fuzzy matching
- Leaderboards and statistics
- World Cup tournament mode
"""

import discord
from discord.ext import commands
import random
import json
import os
from datetime import datetime
import asyncio
from difflib import get_close_matches

# ============================================================================
# BOT SETUP
# ============================================================================

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# ============================================================================
# REAL PLAYER DATABASE
# ============================================================================

PLAYER_DATABASE = {
    # Indian Players
    "Virat Kohli": {"batting": 95, "bowling": 20, "fielding": 92, "role": "batsman", "style": "right_hand"},
    "Rohit Sharma": {"batting": 94, "bowling": 25, "fielding": 85, "role": "batsman", "style": "right_hand"},
    "Jasprit Bumrah": {"batting": 35, "bowling": 98, "fielding": 80, "role": "bowler", "style": "fast"},
    "Hardik Pandya": {"batting": 82, "bowling": 78, "fielding": 88, "role": "all_rounder", "style": "right_hand"},
    "KL Rahul": {"batting": 88, "bowling": 15, "fielding": 90, "role": "batsman", "style": "right_hand"},
    "Ravindra Jadeja": {"batting": 75, "bowling": 88, "fielding": 95, "role": "all_rounder", "style": "spin"},
    "Mohammed Shami": {"batting": 30, "bowling": 92, "fielding": 75, "role": "bowler", "style": "fast"},
    "Rishabh Pant": {"batting": 85, "bowling": 10, "fielding": 82, "role": "wicket_keeper", "style": "left_hand"},
    "Suryakumar Yadav": {"batting": 90, "bowling": 20, "fielding": 87, "role": "batsman", "style": "right_hand"},
    "Yuzvendra Chahal": {"batting": 25, "bowling": 86, "fielding": 70, "role": "bowler", "style": "spin"},
    "Ravichandran Ashwin": {"batting": 55, "bowling": 90, "fielding": 78, "role": "all_rounder", "style": "spin"},
    
    # Australian Players
    "Steve Smith": {"batting": 93, "bowling": 30, "fielding": 88, "role": "batsman", "style": "right_hand"},
    "David Warner": {"batting": 91, "bowling": 15, "fielding": 84, "role": "batsman", "style": "left_hand"},
    "Pat Cummins": {"batting": 40, "bowling": 95, "fielding": 82, "role": "bowler", "style": "fast"},
    "Glenn Maxwell": {"batting": 84, "bowling": 75, "fielding": 90, "role": "all_rounder", "style": "right_hand"},
    "Mitchell Starc": {"batting": 35, "bowling": 94, "fielding": 78, "role": "bowler", "style": "fast"},
    "Josh Hazlewood": {"batting": 28, "bowling": 91, "fielding": 76, "role": "bowler", "style": "fast"},
    "Adam Zampa": {"batting": 22, "bowling": 84, "fielding": 72, "role": "bowler", "style": "spin"},
    "Travis Head": {"batting": 86, "bowling": 35, "fielding": 83, "role": "batsman", "style": "left_hand"},
    "Marcus Stoinis": {"batting": 80, "bowling": 72, "fielding": 85, "role": "all_rounder", "style": "right_hand"},
    "Alex Carey": {"batting": 78, "bowling": 10, "fielding": 88, "role": "wicket_keeper", "style": "left_hand"},
    "Mitchell Marsh": {"batting": 79, "bowling": 74, "fielding": 84, "role": "all_rounder", "style": "right_hand"},
    
    # English Players
    "Joe Root": {"batting": 94, "bowling": 35, "fielding": 86, "role": "batsman", "style": "right_hand"},
    "Ben Stokes": {"batting": 87, "bowling": 82, "fielding": 91, "role": "all_rounder", "style": "left_hand"},
    "Jos Buttler": {"batting": 89, "bowling": 10, "fielding": 85, "role": "wicket_keeper", "style": "right_hand"},
    "Jofra Archer": {"batting": 32, "bowling": 93, "fielding": 80, "role": "bowler", "style": "fast"},
    "Mark Wood": {"batting": 28, "bowling": 89, "fielding": 75, "role": "bowler", "style": "fast"},
    "Adil Rashid": {"batting": 30, "bowling": 85, "fielding": 74, "role": "bowler", "style": "spin"},
    "Jonny Bairstow": {"batting": 86, "bowling": 15, "fielding": 83, "role": "batsman", "style": "right_hand"},
    "Sam Curran": {"batting": 68, "bowling": 79, "fielding": 82, "role": "all_rounder", "style": "left_hand"},
    "Moeen Ali": {"batting": 76, "bowling": 78, "fielding": 80, "role": "all_rounder", "style": "left_hand"},
    "Chris Woakes": {"batting": 55, "bowling": 86, "fielding": 81, "role": "all_rounder", "style": "right_hand"},
    
    # Pakistani Players
    "Babar Azam": {"batting": 96, "bowling": 20, "fielding": 89, "role": "batsman", "style": "right_hand"},
    "Shaheen Afridi": {"batting": 30, "bowling": 94, "fielding": 77, "role": "bowler", "style": "fast"},
    "Mohammad Rizwan": {"batting": 87, "bowling": 10, "fielding": 90, "role": "wicket_keeper", "style": "right_hand"},
    "Shadab Khan": {"batting": 65, "bowling": 81, "fielding": 88, "role": "all_rounder", "style": "spin"},
    "Haris Rauf": {"batting": 25, "bowling": 88, "fielding": 73, "role": "bowler", "style": "fast"},
    "Fakhar Zaman": {"batting": 84, "bowling": 15, "fielding": 79, "role": "batsman", "style": "left_hand"},
    "Mohammad Nawaz": {"batting": 58, "bowling": 76, "fielding": 80, "role": "all_rounder", "style": "spin"},
    "Naseem Shah": {"batting": 28, "bowling": 85, "fielding": 74, "role": "bowler", "style": "fast"},
    "Iftikhar Ahmed": {"batting": 72, "bowling": 60, "fielding": 77, "role": "all_rounder", "style": "right_hand"},
    "Hasan Ali": {"batting": 32, "bowling": 83, "fielding": 76, "role": "bowler", "style": "fast"},
    
    # South African Players
    "Quinton de Kock": {"batting": 90, "bowling": 10, "fielding": 86, "role": "wicket_keeper", "style": "left_hand"},
    "Kagiso Rabada": {"batting": 35, "bowling": 96, "fielding": 79, "role": "bowler", "style": "fast"},
    "Aiden Markram": {"batting": 85, "bowling": 45, "fielding": 84, "role": "batsman", "style": "right_hand"},
    "Anrich Nortje": {"batting": 28, "bowling": 92, "fielding": 76, "role": "bowler", "style": "fast"},
    "David Miller": {"batting": 83, "bowling": 15, "fielding": 87, "role": "batsman", "style": "left_hand"},
    "Keshav Maharaj": {"batting": 40, "bowling": 84, "fielding": 75, "role": "bowler", "style": "spin"},
    "Tabraiz Shamsi": {"batting": 25, "bowling": 86, "fielding": 72, "role": "bowler", "style": "spin"},
    "Rassie van der Dussen": {"batting": 82, "bowling": 35, "fielding": 83, "role": "batsman", "style": "right_hand"},
    "Heinrich Klaasen": {"batting": 81, "bowling": 10, "fielding": 85, "role": "wicket_keeper", "style": "right_hand"},
    "Marco Jansen": {"batting": 48, "bowling": 80, "fielding": 78, "role": "all_rounder", "style": "fast"},
    
    # New Zealand Players
    "Kane Williamson": {"batting": 93, "bowling": 30, "fielding": 88, "role": "batsman", "style": "right_hand"},
    "Trent Boult": {"batting": 30, "bowling": 93, "fielding": 77, "role": "bowler", "style": "fast"},
    "Devon Conway": {"batting": 84, "bowling": 10, "fielding": 82, "role": "batsman", "style": "left_hand"},
    "Daryl Mitchell": {"batting": 80, "bowling": 55, "fielding": 85, "role": "all_rounder", "style": "right_hand"},
    "Tim Southee": {"batting": 35, "bowling": 88, "fielding": 74, "role": "bowler", "style": "fast"},
    "Mitchell Santner": {"batting": 58, "bowling": 79, "fielding": 86, "role": "all_rounder", "style": "spin"},
    "Glenn Phillips": {"batting": 78, "bowling": 45, "fielding": 89, "role": "batsman", "style": "right_hand"},
    "Lockie Ferguson": {"batting": 25, "bowling": 87, "fielding": 76, "role": "bowler", "style": "fast"},
    "Tom Latham": {"batting": 82, "bowling": 10, "fielding": 87, "role": "wicket_keeper", "style": "left_hand"},
    "Ish Sodhi": {"batting": 22, "bowling": 80, "fielding": 71, "role": "bowler", "style": "spin"},
    
    # West Indies Players
    "Nicholas Pooran": {"batting": 85, "bowling": 10, "fielding": 84, "role": "wicket_keeper", "style": "left_hand"},
    "Andre Russell": {"batting": 82, "bowling": 76, "fielding": 80, "role": "all_rounder", "style": "right_hand"},
    "Shimron Hetmyer": {"batting": 80, "bowling": 15, "fielding": 78, "role": "batsman", "style": "left_hand"},
    "Jason Holder": {"batting": 65, "bowling": 84, "fielding": 86, "role": "all_rounder", "style": "fast"},
    "Alzarri Joseph": {"batting": 25, "bowling": 85, "fielding": 73, "role": "bowler", "style": "fast"},
    "Akeal Hosein": {"batting": 28, "bowling": 78, "fielding": 75, "role": "bowler", "style": "spin"},
    "Kyle Mayers": {"batting": 76, "bowling": 68, "fielding": 79, "role": "all_rounder", "style": "left_hand"},
    "Shai Hope": {"batting": 81, "bowling": 10, "fielding": 83, "role": "batsman", "style": "right_hand"},
    "Romario Shepherd": {"batting": 55, "bowling": 72, "fielding": 77, "role": "all_rounder", "style": "right_hand"},
    "Obed McCoy": {"batting": 20, "bowling": 76, "fielding": 70, "role": "bowler", "style": "fast"},
    
    # Sri Lankan Players
    "Wanindu Hasaranga": {"batting": 60, "bowling": 88, "fielding": 82, "role": "all_rounder", "style": "spin"},
    "Pathum Nissanka": {"batting": 83, "bowling": 15, "fielding": 80, "role": "batsman", "style": "right_hand"},
    "Dasun Shanaka": {"batting": 68, "bowling": 70, "fielding": 81, "role": "all_rounder", "style": "right_hand"},
    "Maheesh Theekshana": {"batting": 25, "bowling": 82, "fielding": 76, "role": "bowler", "style": "spin"},
    "Dushmantha Chameera": {"batting": 22, "bowling": 84, "fielding": 72, "role": "bowler", "style": "fast"},
    "Charith Asalanka": {"batting": 75, "bowling": 50, "fielding": 79, "role": "batsman", "style": "left_hand"},
    "Kusal Mendis": {"batting": 80, "bowling": 10, "fielding": 82, "role": "wicket_keeper", "style": "right_hand"},
    "Dilshan Madushanka": {"batting": 20, "bowling": 79, "fielding": 71, "role": "bowler", "style": "fast"},
    "Dhananjaya de Silva": {"batting": 72, "bowling": 74, "fielding": 78, "role": "all_rounder", "style": "spin"},
    "Lahiru Kumara": {"batting": 18, "bowling": 81, "fielding": 69, "role": "bowler", "style": "fast"},
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def find_similar_player(name, threshold=0.6):
    """Find similar player names using fuzzy matching"""
    all_players = list(PLAYER_DATABASE.keys())
    matches = get_close_matches(name, all_players, n=3, cutoff=threshold)
    return matches

def calculate_team_overall(squad):
    """Calculate team overall rating"""
    if not squad:
        return 0
    
    total_rating = 0
    for player in squad:
        if player in PLAYER_DATABASE:
            stats = PLAYER_DATABASE[player]
            # Overall = average of batting, bowling, fielding
            overall = (stats['batting'] + stats['bowling'] + stats['fielding']) / 3
            total_rating += overall
        else:
            total_rating += 50  # Default for unknown players
    
    return total_rating / len(squad)

def validate_squad(squad):
    """Validate squad composition"""
    if len(squad) != 11:
        return False, "Squad must have exactly 11 players"
    
    roles = {'batsman': 0, 'bowler': 0, 'all_rounder': 0, 'wicket_keeper': 0}
    
    for player in squad:
        if player in PLAYER_DATABASE:
            role = PLAYER_DATABASE[player]['role']
            roles[role] += 1
    
    # Check minimum requirements
    if roles['wicket_keeper'] < 1:
        return False, "Squad must have at least 1 wicket keeper"
    
    if roles['bowler'] + roles['all_rounder'] < 4:
        return False, "Squad must have at least 4 bowlers/all-rounders"
    
    if roles['batsman'] + roles['all_rounder'] < 5:
        return False, "Squad must have at least 5 batsmen/all-rounders"
    
    return True, "Valid squad"

# ============================================================================
# DATA FILES
# ============================================================================

TEAMS_FILE = 'teams.json'
STATS_FILE = 'stats.json'
WORLDCUP_FILE = 'worldcup.json'
HISTORY_FILE = 'history.json'

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
worldcup_data = load_data(WORLDCUP_FILE)
match_history = load_data(HISTORY_FILE)

if 'matches' not in match_history:
    match_history['matches'] = []

# ============================================================================
# PITCH AND WEATHER CONDITIONS
# ============================================================================

PITCH_CONDITIONS = {
    "Green Pitch": {
        "pace_bonus": 15,
        "spin_bonus": -10,
        "batting_difficulty": 10,
        "description": "Helps fast bowlers with movement"
    },
    "Dry Pitch": {
        "pace_bonus": -5,
        "spin_bonus": 15,
        "batting_difficulty": 5,
        "description": "Assists spinners, cracks develop"
    },
    "Dusty Pitch": {
        "pace_bonus": -10,
        "spin_bonus": 20,
        "batting_difficulty": 8,
        "description": "Spin-friendly, turning track"
    },
    "Flat Pitch": {
        "pace_bonus": 0,
        "spin_bonus": 0,
        "batting_difficulty": -10,
        "description": "Batsman-friendly, high scores"
    }
}

WEATHER_CONDITIONS = {
    "Sunny": {
        "swing_factor": 0,
        "visibility": 100,
        "description": "Clear skies, good for batting"
    },
    "Cloudy": {
        "swing_factor": 10,
        "visibility": 90,
        "description": "Helps swing bowling"
    },
    "Overcast": {
        "swing_factor": 20,
        "visibility": 80,
        "description": "Significant swing, tough batting"
    }
}

# ============================================================================
# SIMULATION ENGINE
# ============================================================================

def calculate_batting_probability(batsman, bowler, pitch, weather):
    """Calculate probability of scoring runs"""
    bat_rating = PLAYER_DATABASE.get(batsman, {}).get("batting", 50)
    bowl_rating = PLAYER_DATABASE.get(bowler, {}).get("bowling", 50)
    
    pitch_diff = pitch["batting_difficulty"]
    
    bowler_style = PLAYER_DATABASE.get(bowler, {}).get("style", "fast")
    if bowler_style == "fast":
        bowl_rating += pitch["pace_bonus"]
    elif bowler_style == "spin":
        bowl_rating += pitch["spin_bonus"]
    
    if bowler_style == "fast":
        bowl_rating += weather["swing_factor"] // 2
    
    net_rating = bat_rating - bowl_rating - pitch_diff
    probability = 50 + (net_rating / 4)
    
    return max(10, min(90, probability))

def simulate_ball(batsman, bowler, pitch, weather):
    """Simulate a single ball"""
    bat_prob = calculate_batting_probability(batsman, bowler, pitch, weather)
    
    if bat_prob > 70:
        weights = [15, 25, 18, 10, 15, 12, 5, 0, 0]
    elif bat_prob > 50:
        weights = [25, 30, 15, 8, 10, 5, 7, 0, 0]
    else:
        weights = [30, 25, 12, 5, 8, 3, 15, 1, 1]
    
    outcomes = ['0', '1', '2', '3', '4', '6', 'W', 'wd', 'nb']
    return random.choices(outcomes, weights=weights)[0]

def get_bowlers(squad):
    """Get bowling lineup"""
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
        # Add best bowlers from remaining players
        remaining = [p for p in squad if p not in bowling_lineup]
        remaining.sort(key=lambda x: PLAYER_DATABASE.get(x, {}).get('bowling', 0), reverse=True)
        bowling_lineup.extend(remaining[:5-len(bowling_lineup)])
    
    return bowling_lineup[:5]

def simulate_innings_realistic(team_name, squad, opp_squad, pitch, weather, target=None):
    """Simulate innings with realistic outcomes"""
    if not squad or len(squad) < 11:
        squad = [f"Player{i+1}" for i in range(11)]
    
    batting_order = squad[:11]
    total_runs = 0
    wickets = 0
    overs = 0
    max_overs = 20
    
    batsman_scores = {}
    for batsman in batting_order:
        batsman_scores[batsman] = {
            'runs': 0, 'balls': 0, 'fours': 0, 'sixes': 0,
            'out': False, 'strike_rate': 0.0
        }
    
    bowlers = get_bowlers(opp_squad)
    current_bowler_idx = 0
    
    bowler_stats = {}
    for bowler in bowlers:
        bowler_stats[bowler] = {
            'overs': 0, 'runs': 0, 'wickets': 0, 'maidens': 0, 'economy': 0.0
        }
    
    current_batsmen = [batting_order[0], batting_order[1]]
    batsman_index = 2
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
                    
            elif outcome in ['wd', 'nb']:
                total_runs += 1
                over_runs += 1
                bowler_stats[current_bowler]['runs'] += 1
                over_commentary.append(f"Extra: {outcome}")
                
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

def update_player_stats(innings_data):
    """Update player statistics"""
    for player, stats in innings_data['batsmen'].items():
        if player not in player_stats:
            player_stats[player] = {
                'matches': 0, 'runs': 0, 'balls': 0, 'wickets': 0,
                'fours': 0, 'sixes': 0, 'high_score': 0
            }
        
        if stats['balls'] > 0:
            player_stats[player]['matches'] += 1
            player_stats[player]['runs'] += stats['runs']
            player_stats[player]['balls'] += stats['balls']
            player_stats[player]['fours'] += stats['fours']
            player_stats[player]['sixes'] += stats['sixes']
            
            if stats['runs'] > player_stats[player]['high_score']:
                player_stats[player]['high_score'] = stats['runs']
    
    for bowler, stats in innings_data['bowlers'].items():
        if bowler not in player_stats:
            player_stats[bowler] = {
                'matches': 0, 'runs': 0, 'balls': 0, 'wickets': 0,
                'fours': 0, 'sixes': 0, 'high_score': 0, 'overs': 0,
                'runs_conceded': 0, 'best_bowling': 0
            }
        
        if stats['overs'] > 0:
            if 'overs' not in player_stats[bowler]:
                player_stats[bowler]['overs'] = 0
            if 'runs_conceded' not in player_stats[bowler]:
                player_stats[bowler]['runs_conceded'] = 0
            if 'best_bowling' not in player_stats[bowler]:
                player_stats[bowler]['best_bowling'] = 0
            
            player_stats[bowler]['overs'] += stats['overs']
            player_stats[bowler]['runs_conceded'] += stats['runs']
            player_stats[bowler]['wickets'] += stats['wickets']
            
            if stats['wickets'] > player_stats[bowler]['best_bowling']:
                player_stats[bowler]['best_bowling'] = stats['wickets']
    
    save_data(STATS_FILE, player_stats)

# ============================================================================
# DISCORD COMMANDS
# ============================================================================

@bot.event
async def on_ready():
    print(f'{bot.user} is online!')
    print(f'Connected to {len(bot.guilds)} servers')

@bot.command(name='help_cricket')
async def help_cricket(ctx):
    """Show all cricket commands"""
    embed = discord.Embed(
        title="🏏 Cricket Simulation Bot Commands",
        description="Complete command list for cricket simulation",
        color=0x00ff00
    )
    
    embed.add_field(
        name="📋 Team Management",
        value=(
            "**!teamadd <name> <player1> <player2> ... <player11>**\n"
            "Create a new team with 11 players\n\n"
            "**!teams**\n"
            "Show all registered teams\n\n"
            "**!teamdelete <name>**\n"
            "Delete a team"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🎮 Match Simulation",
        value=(
            "**!sim <team1> <team2>**\n"
            "Simulate a match between two teams\n\n"
            "**!quicksim <team1> <team2>**\n"
            "Quick simulation without over-by-over updates"
        ),
        inline=False
    )
    
    embed.add_field(
    name="🎮 Match Simulation",
    value=(
        "**!sim <team1> <team2>**\n"
        "Simulate a match between two teams\n\n"
        "**!quicksim <team1> <team2>**\n"
        "Quick simulation without over-by-over updates"
    ),
    inline=False
)

embed.add_field(
    name="👤 Player Info",
    value=(
        "**!player <name>**\n"
        "View player profile and stats\n\n"
        "**!players [search]**\n"
        "List all available players or search by name"
    ),
    inline=False
)

embed.add_field(
    name="📊 Statistics & History",
)

embed.add_field(
    name="🏆 World Cup Mode",
    value=(
        "**!wcsetup**\n"
        "Setup World Cup tournament\n\n"
        "**!wcmatch <team1> <team2>**\n"
        "Play a World Cup match\n\n"
        "**!wcstandings**\n"
        "View points table\n\n"
        "**!wcfinal**\n"
        "Play World Cup final"
    ),
    inline=False
)

embed.set_footer(text="Use !help <command> for detailed info on any command")

await ctx.send(embed=embed)
@bot.command(name='teamadd')
async def teamadd(ctx, team_name: str, *players):
    """Add a new team with player validation"""
    if len(players) != 11:
    await ctx.send(f"❌ Error: You must provide exactly 11 players. You provided {len(players)}.")
    return
# Validate and match player names
validated_players = []
suggestions = []
invalid_players = []

for player in players:
    if player in PLAYER_DATABASE:
        validated_players.append(player)
    else:
        # Find similar names
        similar = find_similar_player(player, threshold=0.6)
        if similar:
            suggestions.append(f"❓ **{player}** not found. Did you mean: **{', '.join(similar)}**?")
            invalid_players.append(player)
        else:
            invalid_players.append(player)
            suggestions.append(f"❌ **{player}** not found in database and no similar names found.")

if invalid_players:
    error_msg = f"⚠️ **Team Registration Failed**\n\n"
    error_msg += "\n".join(suggestions)
    error_msg += f"\n\n💡 Use `!players` to see all available players."
    await ctx.send(error_msg)
    return

# Validate squad composition
is_valid, message = validate_squad(validated_players)
if not is_valid:
    await ctx.send(f"❌ Invalid squad composition: {message}")
    return

# Calculate team overall
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

# Show squad by role
roles_display = {'batsman': [], 'bowler': [], 'all_rounder': [], 'wicket_keeper': []}
for player in validated_players:
    role = PLAYER_DATABASE[player]['role']
    roles_display[role].append(player)

if roles_display['batsman']:
    embed.add_field(name="🏏 Batsmen", value="\n".join(roles_display['batsman']), inline=True)
if roles_display['bowler']:
    embed.add_field(name="⚾ Bowlers", value="\n".join(roles_display['bowler']), inline=True)
if roles_display['all_rounder']:
    embed.add_field(name="⭐ All-Rounders", value="\n".join(roles_display['all_rounder']), inline=True)
if roles_display['wicket_keeper']:
    embed.add_field(name="🧤 Wicket Keeper", value="\n".join(roles_display['wicket_keeper']), inline=True)

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

for team_name, team_info in sorted(teams_data.items(), key=lambda x: x[1].get('overall', 0), reverse=True):
    overall = team_info.get('overall', 0)
    matches = team_info.get('matches_played', 0)
    wins = team_info.get('wins', 0)
    losses = team_info.get('losses', 0)
    
    win_rate = (wins / matches * 100) if matches > 0 else 0
    
    value = f"📊 Overall: **{overall:.1f}**\n"
    value += f"🎮 Matches: {matches} | W: {wins} | L: {losses}\n"
    value += f"📈 Win Rate: **{win_rate:.1f}%**"
    
    embed.add_field(name=f"🔵 {team_name}", value=value, inline=True)

await ctx.send(embed=embed)
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

# Stronger team more likely to bat first
if teams_data[toss_winner]['overall'] > 75:
    choice = 'bat' if random.random() > 0.4 else 'bowl'
else:
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
team1_innings = simulate_innings_realistic(first_bat_name, first_bat_squad, second_bat_squad, pitch, weather)

# Show over-by-over for first innings
for over_data in team1_innings['over_by_over'][::2]:  # Show every 2nd over to avoid spam
    over_msg = f"**{over_data['summary']}**"
    if over_data['commentary']:
        over_msg += "\n" + "\n".join(over_data['commentary'][:2])
    await ctx.send(over_msg)
    await asyncio.sleep(1)

innings_summary = f"\n**📊 {first_bat_name} Innings Summary**\n"
innings_summary += f"**Score: {team1_innings['total']}/{team1_innings['wickets']} ({team1_innings['overs']} overs)**"
await ctx.send(innings_summary)

await asyncio.sleep(2)

# Second Innings
target = team1_innings['total']
await ctx.send(f"\n**🎯 TARGET: {target + 1} runs**")
await ctx.send(f"**🏏 SECOND INNINGS: {second_bat_name}**")

team2_innings = simulate_innings_realistic(second_bat_name, second_bat_squad, first_bat_squad, pitch, weather, target)

# Show over-by-over with win probability
for over_data in team2_innings['over_by_over'][::2]:
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

# Determine winner based on team overall if scores are close
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
    teams_data[team2_name]['losses'] = teams_data[team2_name].get('losses', 0) + 1
elif final_team2['total'] > final_team1['total']:
    winner = team2_name
    teams_data[team2_name]['wins'] = teams_data[team2_name].get('wins', 0) + 1
    teams_data[team1_name]['losses'] = teams_data[team1_name].get('losses', 0) + 1
else:
    # Tie-breaker based on team overall
    winner = team1_name if team1_overall > team2_overall else team2_name

teams_data[team1_name]['matches_played'] = teams_data[team1_name].get('matches_played', 0) + 1
teams_data[team2_name]['matches_played'] = teams_data[team2_name].get('matches_played', 0) + 1

save_data(TEAMS_FILE, teams_data)

# Update stats
update_player_stats(final_team1)
update_player_stats(final_team2)

# Save match history
match_record = {
    'date': datetime.now().isoformat(),
    'team1': team1_name,
    'team2': team2_name,
    'team1_score': f"{final_team1['total']}/{final_team1['wickets']}",
    'team2_score': f"{final_team2['total']}/{final_team2['wickets']}",
    'winner': winner,
    'pitch': pitch_name,
    'weather': weather_name
}

match_history['matches'].insert(0, match_record)
match_history['matches'] = match_history['matches'][:50]  # Keep last 50 matches
save_data(HISTORY_FILE, match_history)

# Final scorecard
await show_final_scorecard(ctx, final_team1, final_team2, pitch_name, weather_name, winner)
async def show_final_scorecard(ctx, team1_data, team2_data, pitch, weather, winner):
"""Show final match scorecard"""
embed = discord.Embed(title="📋 FINAL SCORECARD", color=0xffd700)
# Match result
if team1_data['total'] > team2_data['total']:
    result = f"🏆 **{team1_data['team']}** won by **{team1_data['total'] - team2_data['total']} runs**"
elif team2_data['total'] > team1_data['total']:
    wickets_rem = 10 - team2_data['wickets']
    result = f"🏆 **{team2_data['team']}** won by **{wickets_rem} wickets**"
else:
    result = f"🏆 **{winner}** won (tie-breaker)"

embed.add_field(name="Result", value=result, inline=False)

# Team scores
embed.add_field(
    name=f"{team1_data['team']} 🏏",
    value=f"**{team1_data['total']}/{team1_data['wickets']}** ({team1_data['overs']} overs)",
    inline=True
)
embed.add_field(
    name=f"{team2_data['team']} 🏏",
    value=f"**{team2_data['total']}/{team2_data['wickets']}** ({team2_data['overs']} overs)",
    inline=True
)

# Top performers
team1_batsmen = [(p, s) for p, s in team1_data['batsmen'].items() if s['balls'] > 0]
team2_batsmen = [(p, s) for p, s in team2_data['batsmen'].items() if s['balls'] > 0]

if team1_batsmen:
    top_bat1 = max(team1_batsmen, key=lambda x: x[1]['runs'])
    embed.add_field(
        name=f"⭐ Top Scorer - {team1_data['team']}",
        value=f"**{top_bat1[0]}** - {top_bat1[1]['runs']}({top_bat1[1]['balls']}) | SR: {top_bat1[1]['strike_rate']:.1f}",
        inline=False
    )

if team2_batsmen:
    top_bat2 = max(team2_batsmen, key=lambda x: x[1]['runs'])
    embed.add_field(
        name=f"⭐ Top Scorer - {team2_data['team']}",
        value=f"**{top_bat2[0]}** - {top_bat2[1]['runs']}({top_bat2[1]['balls']}) | SR: {top_bat2[1]['strike_rate']:.1f}",
        inline=False
    )

# Best bowler
team1_bowlers = [(b, s) for b, s in team1_data['bowlers'].items() if s['overs'] > 0]
team2_bowlers = [(b, s) for b, s in team2_data['bowlers'].items() if s['overs'] > 0]

if team1_bowlers:
    best_bowl1 = max(team1_bowlers, key=lambda x: x[1]['wickets'])
    if best_bowl1[1]['wickets'] > 0:
        embed.add_field(
            name=f"🎯 Best Bowler - {team1_data['team']}",
            value=f"**{best_bowl1[0]}** - {best_bowl1[1]['wickets']}/{best_bowl1[1]['runs']} | Econ: {best_bowl1[1]['economy']:.2f}",
            inline=False
        )

if team2_bowlers:
    best_bowl2 = max(team2_bowlers, key=lambda x: x[1]['wickets'])
    if best_bowl2[1]['wickets'] > 0:
        embed.add_field(
            name=f"🎯 Best Bowler - {team2_data['team']}",
            value=f"**{best_bowl2[0]}** - {best_bowl2[1]['wickets']}/{best_bowl2[1]['runs']} | Econ: {best_bowl2[1]['economy']:.2f}",
            inline=False
        )

embed.add_field(name="Conditions", value=f"🌱 {pitch} | 🌤 {weather}", inline=False)
embed.set_footer(text=f"Match completed at {datetime.now().strftime('%H:%M')}")

await ctx.send(embed=embed)
@bot.command(name='player')
async def player_profile(ctx, *, player_name: str):
    """Show player profile and stats"""
    # Try exact match first
    if player_name not in PLAYER_DATABASE:
    # Try fuzzy match
    similar = find_similar_player(player_name, threshold=0.6)
    if similar:
    player_name = similar[0]
    await ctx.send(f"📝 Showing stats for {player_name} (closest match)")
    else:
    await ctx.send(f"❌ Player '{player_name}' not found! Use !players to see all players.")
    return
player_data = PLAYER_DATABASE[player_name]
stats = player_stats.get(player_name, {})

embed = discord.Embed(
    title=f"🏏 {player_name}",
    color=0x3498db
)

# Player ratings
embed.add_field(name="📊 Batting", value=f"**{player_data['batting']}**/100", inline=True)
embed.add_field(name="⚾ Bowling", value=f"**{player_data['bowling']}**/100", inline=True)
embed.add_field(name="🧤 Fielding", value=f"**{player_data['fielding']}**/100", inline=True)

# Role and style
embed.add_field(name="🎭 Role", value=player_data['role'].replace('_', ' ').title(), inline=True)
embed.add_field(name="✋ Style", value=player_data['style'].replace('_', ' ').title(), inline=True)

# Career stats
if stats:
    matches = stats.get('matches', 0)
    runs = stats.get('runs', 0)
    balls = stats.get('balls', 0)
    wickets = stats.get('wickets', 0)
    high_score = stats.get('high_score', 0)
    
    if matches > 0:
        avg = runs / matches if matches > 0 else 0
        sr = (runs / balls * 100) if balls > 0 else 0
        
        career_stats = f"**Matches:** {matches}\n"
        career_stats += f"**Runs:** {runs} | **Avg:** {avg:.2f}\n"
        career_stats += f"**Strike Rate:** {sr:.2f}\n"
        career_stats += f"**High Score:** {high_score}\n"
        
        if wickets > 0:
            career_stats += f"**Wickets:** {wickets}"
        
        embed.add_field(name="📈 Career Stats", value=career_stats, inline=False)
else:
    embed.add_field(name="📈 Career Stats", value="No matches played yet", inline=False)

# Overall rating
overall = (player_data['batting'] + player_data['bowling'] + player_data['fielding']) / 3
embed.add_field(name="⭐ Overall Rating", value=f"**{overall:.1f}**/100", inline=False)

await ctx.send(embed=embed)
@bot.command(name='players')
async def list_players(ctx, *, search: str = None):
    """List all players or search by name"""
    if search:
    # Search for players
    matching_players = [p for p in PLAYER_DATABASE.keys() if search.lower() in p.lower()]
    if not matching_players:
    await ctx.send(f"❌ No players found matching '{search}'")
    return
    
    embed = discord.Embed(
        title=f"🔍 Search Results for '{search}'",
        description=f"Found {len(matching_players)} players",
        color=0x3498db
    )
    
    for player in matching_players[:25]:  # Limit to 25
        data = PLAYER_DATABASE[player]
        overall = (data['batting'] + data['bowling'] + data['fielding']) / 3
        embed.add_field(
            name=player,
            value=f"{data['role'].title()} | Overall: {overall:.1f}",
            inline=True
        )
else:
    # List all players by country/role
    embed = discord.Embed(
        title="🏏 Available Players",
        description=f"Total: {len(PLAYER_DATABASE)} players\nUse `!players <name>` to search",
        color=0x00ff00
    )
    
    # Group by role
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
@bot.command(name='lb')
    async def leaderboard(ctx, category: str = "runs"):
    """Show leaderboards"""
    if not player_stats:
    await ctx.send("❌ No statistics available yet! Play some matches first.")
    return
category = category.lower()

if category == "runs":
    sorted_players = sorted(
        [(p, s) for p, s in player_stats.items() if s.get('runs', 0) > 0],
        key=lambda x: x[1]['runs'],
        reverse=True
    )[:10]
    
    embed = discord.Embed(title="🏆 Top Run Scorers", color=0xffd700)
    
    for i, (player, stats) in enumerate(sorted_players, 1):
        matches = stats.get('matches', 0)
        runs = stats['runs']
        avg = runs / matches if matches > 0 else 0
        
        embed.add_field(
            name=f"{i}. {player}",
            value=f"Runs: **{runs}** | Avg: {avg:.2f} | HS: {stats.get('high_score', 0)}",
            inline=False
        )

elif category == "wickets":
    sorted_players = sorted(
        [(p, s) for p, s in player_stats.items() if s.get('wickets', 0) > 0],
        key=lambda x: x[1]['wickets'],
        reverse=True
    )[:10]
    
    embed = discord.Embed(title="🎯 Top Wicket Takers", color=0xff6b6b)
    
    for i, (player, stats) in enumerate(sorted_players, 1):
        wickets = stats['wickets']
        overs = stats.get('overs', 0)
        runs_conceded = stats.get('runs_conceded', 0)
        economy = (runs_conceded / overs) if overs > 0 else 0
        
        embed.add_field(
            name=f"{i}. {player}",
            value=f"Wickets: **{wickets}** | Econ: {economy:.2f} | Best: {stats.get('best_bowling', 0)}",
            inline=False
        )

elif category == "average":
    sorted_players = sorted(
        [(p, s) for p, s in player_stats.items() if s.get('runs', 0) > 0 and s.get('matches', 0) >= 3],
        key=lambda x: x[1]['runs'] / x[1]['matches'],
        reverse=True
    )[:10]
    
    embed = discord.Embed(title="📊 Best Batting Average (min 3 matches)", color=0x4ecdc4)
    
    for i, (player, stats) in enumerate(sorted_players, 1):
        matches = stats['matches']
        runs = stats['runs']
        avg = runs / matches
        
        embed.add_field(
            name=f"{i}. {player}",
            value=f"Average: **{avg:.2f}** | Runs: {runs} | Matches: {matches}",
            inline=False
        )

else:
    await ctx.send(f"❌ Invalid category! Use: `runs`, `wickets`, or `average`")
    return

await ctx.send(embed=embed)
@bot.command(name='history')
async def match_history_cmd(ctx, limit: int = 10):
    """Show recent match history"""
    if not match_history.get('matches'):
    await ctx.send("❌ No match history available yet!")
    return
limit = min(limit, 20)  # Max 20 matches
matches = match_history['matches'][:limit]

embed = discord.Embed(
    title=f"📜 Recent Match History (Last {len(matches)} matches)",
    color=0x9b59b6
)

for i, match in enumerate(matches, 1):
    result = f"**{match['team1']}** {match['team1_score']} vs {match['team2_score']} **{match['team2']}**\n"
    result += f"🏆 Winner: **{match['winner']}**\n"
    result += f"Conditions: {match['pitch']} | {match['weather']}"
    
    match_date = datetime.fromisoformat(match['date']).strftime('%b %d, %Y')
    
    embed.add_field(
        name=f"{i}. {match_date}",
        value=result,
        inline=False
    )

await ctx.send(embed=embed)
@bot.command(name='teamstats')
async def team_stats(ctx, *, team_name: str):
    """View team statistics"""
    if team_name not in teams_data:
    await ctx.send(f"❌ Team '{team_name}' not found! Use !teams to see all teams.")
    return
team = teams_data[team_name]

embed = discord.Embed(
    title=f"📊 {team_name} Statistics",
    color=0x3498db
)

# Overall stats
overall = team.get('overall', 0)
matches = team.get('matches_played', 0)
wins = team.get('wins', 0)
losses = team.get('losses', 0)
win_rate = (wins / matches * 100) if matches > 0 else 0

embed.add_field(name="⭐ Overall Rating", value=f"**{overall:.1f}**/100", inline=True)
embed.add_field(name="🎮 Matches Played", value=str(matches), inline=True)
embed.add_field(name="📈 Win Rate", value=f"**{win_rate:.1f}%**", inline=True)

embed.add_field(name="✅ Wins", value=str(wins), inline=True)
embed.add_field(name="❌ Losses", value=str(losses), inline=True)

# Squad analysis
squad = team['squad']
roles = {'batsman': 0, 'bowler': 0, 'all_rounder': 0, 'wicket_keeper': 0}

total_bat = 0
total_bowl = 0
total_field = 0

for player in squad:
    if player in PLAYER_DATABASE:
        data = PLAYER_DATABASE[player]
        roles[data['role']] += 1
        total_bat += data['batting']
        total_bowl += data['bowling']
        total_field += data['fielding']

avg_bat = total_bat / len(squad)
avg_bowl = total_bowl / len(squad)
avg_field = total_field / len(squad)

squad_composition = f"Batsmen: {roles['batsman']} | Bowlers: {roles['bowler']}\n"
squad_composition += f"All-Rounders: {roles['all_rounder']} | WK: {roles['wicket_keeper']}"

embed.add_field(name="👥 Squad Composition", value=squad_composition, inline=False)

embed.add_field(name="📊 Avg Batting", value
=f"{avg_bat:.1f}", inline=True)
embed.add_field(name="⚾ Avg Bowling", value=f"{avg_bowl:.1f}", inline=True)
embed.add_field(name="🧤 Avg Fielding", value=f"{avg_field:.1f}", inline=True)
# Top 3 players
top_players = sorted(squad, key=lambda x: (
    PLAYER_DATABASE.get(x, {}).get('batting', 0) +
    PLAYER_DATABASE.get(x, {}).get('bowling', 0) +
    PLAYER_DATABASE.get(x, {}).get('fielding', 0)
) / 3, reverse=True)[:3]

top_text = "\n".join([f"⭐ {p}" for p in top_players])
embed.add_field(name="🌟 Star Players", value=top_text, inline=False)

created_date = datetime.fromisoformat(team['created_at']).strftime('%b %d, %Y')
embed.set_footer(text=f"Created by {team['created_by']} on {created_date}")

await ctx.send(embed=embed)
@bot.command(name='wcsetup')
async def worldcup_setup(ctx):
    """Setup World Cup tournament"""
    if len(teams_data) < 4:
    await ctx.send("❌ Need at least 4 teams for World Cup! Create more teams first.")
    return
# Initialize World Cup
participating_teams = list(teams_data.keys())[:8]  # Max 8 teams

worldcup_data['teams'] = {}
for team in participating_teams:
    worldcup_data['teams'][team] = {
        'matches': 0,
        'wins': 0,
        'losses': 0,
        'points': 0,
        'nrr': 0.0
    }

worldcup_data['status'] = 'league'
worldcup_data['matches_played'] = []

save_data(WORLDCUP_FILE, worldcup_data)

embed = discord.Embed(
    title="🏆 World Cup Tournament Initialized!",
    description=f"**{len(participating_teams)} teams** will compete",
    color=0xffd700
)

teams_list = "\n".join([f"{i+1}. {team}" for i, team in enumerate(participating_teams)])
embed.add_field(name="Participating Teams", value=teams_list, inline=False)

embed.add_field(
    name="📋 Format",
    value="• League matches: Each team plays every other team\n• Top 4 advance to semi-finals\n• Winners play in the final",
    inline=False
)

embed.set_footer(text="Use !wcmatch <team1> <team2> to play league matches")

await ctx.send(embed=embed)
@bot.command(name='wcmatch')
async def worldcup_match(ctx, team1_name: str, team2_name: str):
    """Play a World Cup match"""
    if 'teams' not in worldcup_data or not worldcup_data.get('teams'):
    await ctx.send("❌ World Cup not setup! Use !wcsetup first.")
    return
    if team1_name not in worldcup_data['teams'] or team2_name not in worldcup_data['teams']:
    await ctx.send("❌ One or both teams not in World Cup!")
    return

# Check if match already played
match_id = tuple(sorted([team1_name, team2_name]))
if match_id in worldcup_data.get('matches_played', []):
    await ctx.send("❌ This match has already been played!")
    return

await ctx.send(f"🏆 **WORLD CUP MATCH**\n{team1_name} vs {team2_name}")

# Simulate match (reuse sim logic)
# ... (similar to regular sim but update WC standings)

await ctx.send("⚠️ World Cup match simulation coming soon! Use `!sim` for now.")
@bot.command(name='wcstandings')
async def worldcup_standings(ctx):
"""Show World Cup standings"""
if 'teams' not in worldcup_data or not worldcup_data.get('teams'):
await ctx.send("❌ World Cup not setup! Use !wcsetup first.")
return
teams = worldcup_data['teams']
sorted_teams = sorted(teams.items(), key=lambda x: (x[1]['points'], x[1]['nrr']), reverse=True)

embed = discord.Embed(
    title="🏆 World Cup Standings",
    color=0xffd700
)

standings_text = "```\n"
standings_text += f"{'Pos':<4} {'Team':<20} {'M':<3} {'W':<3} {'L':<3} {'Pts':<4} {'NRR':<6}\n"
standings_text += "-" * 55 + "\n"

for i, (team, stats) in enumerate(sorted_teams, 1):
    standings_text += f"{i:<4} {team:<20} {stats['matches']:<3} {stats['wins']:<3} {stats['losses']:<3} {stats['points']:<4} {stats['nrr']:<6.2f}\n"

standings_text += "```"

embed.description = standings_text
embed.set_footer(text="Top 4 teams qualify for semi-finals")

await ctx.send(embed=embed)
@bot.command(name='wcfinal')
async def worldcup_final(ctx):
"""Play World Cup final"""
if 'teams' not in worldcup_data or not worldcup_data.get('teams'):
await ctx.send("❌ World Cup not setup!")
return
teams = worldcup_data['teams']
sorted_teams = sorted(teams.items(), key=lambda x: (x[1]['points'], x[1]['nrr']), reverse=True)

if len(sorted_teams) < 2:
    await ctx.send("❌ Not enough teams have played!")
    return

finalist1 = sorted_teams[0][0]
finalist2 = sorted_teams[1][0]

await ctx.send(f"🏆 **WORLD CUP FINAL**\n{finalist1} vs {finalist2}\n\nUse `!sim {finalist1} {finalist2}` to play the final!")
@bot.command(name='quicksim')
async def quick_sim(ctx, team1_name: str, team2_name: str):
    """Quick simulation without over-by-over updates"""
    if team1_name not in teams_data or team2_name not in teams_data:
    await ctx.send(f"❌ One or both teams not found!")
    return
    await ctx.send(f"⚡ **Quick Match: {team1_name} vs {team2_name}**")

# Simulate quickly
pitch_name = random.choice(list(PITCH_CONDITIONS.keys()))
weather_name = random.choice(list(WEATHER_CONDITIONS.keys()))
pitch = PITCH_CONDITIONS[pitch_name]
weather = WEATHER_CONDITIONS[weather_name]

team1_squad = teams_data[team1_name]['squad']
team2_squad = teams_data[team2_name]['squad']

team1_innings = simulate_innings_realistic(team1_name, team1_squad, team2_squad, pitch, weather)
target = team1_innings['total']
team2_innings = simulate_innings_realistic(team2_name, team2_squad, team1_squad, pitch, weather, target)

# Determine winner
if team1_innings['total'] > team2_innings['total']:
    winner = team1_name
    margin = f"{team1_innings['total'] - team2_innings['total']} runs"
elif team2_innings['total'] > team1_innings['total']:
    winner = team2_name
    margin = f"{10 - team2_innings['wickets']} wickets"
else:
    team1_overall = teams_data[team1_name]['overall']
    team2_overall = teams_data[team2_name]['overall']
    winner = team1_name if team1_overall > team2_overall else team2_name
    margin = "tie (super over)"

# Update records
teams_data[team1_name]['matches_played'] = teams_data[team1_name].get('matches_played', 0) + 1
teams_data[team2_name]['matches_played'] = teams_data[team2_name].get('matches_played', 0) + 1

if winner == team1_name:
    teams_data[team1_name]['wins'] = teams_data[team1_name].get('wins', 0) + 1
    teams_data[team2_name]['losses'] = teams_data[team2_name].get('losses', 0) + 1
else:
    teams_data[team2_name]['wins'] = teams_data[team2_name].get('wins', 0) + 1
    teams_data[team1_name]['losses'] = teams_data[team1_name].get('losses', 0) + 1

save_data(TEAMS_FILE, teams_data)
update_player_stats(team1_innings)
update_player_stats(team2_innings)

# Show result
await show_final_scorecard(ctx, team1_innings, team2_innings, pitch_name, weather_name, winner)
@bot.command(name='teamdelete')
async def team_delete(ctx, *, team_name: str):
    """Delete a team"""
    if team_name not in teams_data:
    await ctx.send(f"❌ Team '{team_name}' not found!")
    return
    # Check if user created the team or is admin
    team = teams_data[team_name]
    if str(ctx.author) != team['created_by'] and not ctx.author.guild_permissions.administrator:
    await ctx.send("❌ You can only delete teams you created!")
    return

del teams_data[team_name]
save_data(TEAMS_FILE, teams_data)

await ctx.send(f"✅ Team **{team_name}** has been deleted.")
============================================================================
RUN BOT
============================================================================       

if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN")
    if not TOKEN:
        print("❌ Error: DISCORD_TOKEN environment variable not set!")
    else:
        bot.run(TOKEN)
