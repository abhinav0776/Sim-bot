"""
DISCORD CRICKET SIMULATION BOT
===============================
Complete cricket simulation bot with IPL-style scorecards and World Cup mode

FEATURES:
- Match Simulation with realistic scoring
- IPL-style scorecard images with top performers
- Team Management (add/remove teams and squads)
- Stats Tracking (runs, wickets, averages)
- Leaderboards (Orange Cap, Purple Cap, Best Average)
- World Cup Mode (league stage, semi-finals, final)
- Player Profiles
- Match History

COMMANDS:
!sim TeamA vs TeamB - Simulate a match
!teamadd TeamName Player1, Player2... - Add team
!teamremove TeamName - Remove team
!addstats - Add stats from last match (reply to scorecard)
!removestats - Remove stats (reply to scorecard)
!lb - Show leaderboards
!player PlayerName - Show player stats
!wcstart Team1, Team2, Team3... - Start World Cup
!wcmatch TeamA vs TeamB - World Cup match
!wcstandings - Show World Cup table
!wcsemis - Generate semi-final matchups
!wcfinal TeamA vs TeamB - World Cup final
!history - Show recent matches
"""

import discord
from discord.ext import commands
from discord import app_commands
import random
from PIL import Image, ImageDraw, ImageFont
import io
import json
import os
from datetime import datetime

# ============================================================================
# BOT SETUP
# ============================================================================

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# ============================================================================
# DATA FILES
# ============================================================================

TEAMS_FILE = 'teams.json'
STATS_FILE = 'stats.json'
WORLDCUP_FILE = 'worldcup.json'
HISTORY_FILE = 'history.json'

# ============================================================================
# DATA LOADING AND SAVING
# ============================================================================

def load_data(filename):
    """Load data from JSON file"""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {}

def save_data(filename, data):
    """Save data to JSON file"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Load all data
teams_data = load_data(TEAMS_FILE)
player_stats = load_data(STATS_FILE)
worldcup_data = load_data(WORLDCUP_FILE)
match_history = load_data(HISTORY_FILE)

if 'matches' not in match_history:
    match_history['matches'] = []

# ============================================================================
# CRICKET SIMULATION ENGINE
# ============================================================================

def simulate_innings(team_name, squad, target=None):
    """
    Simulate a cricket innings
    
    Args:
        team_name: Name of the batting team
        squad: List of players in the squad
        target: Target score to chase (None if batting first)
    
    Returns:
        Dictionary with innings data including runs, wickets, overs, and batsman scores
    """
    # Create default squad if not provided
    if not squad or len(squad) < 5:
        squad = [f"Player{i+1}" for i in range(11)]
    
    batting_order = squad[:11]
    total_runs = 0
    wickets = 0
    overs = 0
    max_overs = 20
    
    # Initialize batsman statistics
    batsman_scores = {}
    for batsman in batting_order:
        batsman_scores[batsman] = {
            'runs': 0,
            'balls': 0,
            'fours': 0,
            'sixes': 0,
            'out': False,
            'strike_rate': 0.0
        }
    
    # Current batsmen on crease
    current_batsmen = [batting_order[0], batting_order[1]]
    batsman_index = 2
    
    # Bowling statistics
    bowler_stats = {}
    
    # Ball-by-ball simulation
    while overs < max_overs and wickets < 10:
        # Check if target is reached
        if target and total_runs > target:
            break
        
        balls_in_over = 0
        while balls_in_over < 6 and wickets < 10:
            if target and total_runs > target:
                break
            
            # Generate random outcome with realistic probabilities
            outcome = random.choices(
                ['0', '1', '2', '3', '4', '6', 'W', 'wd', 'nb'],
                weights=[25, 30, 15, 8, 10, 5, 7, 3, 2]
            )[0]
            
            striker = current_batsmen[0]
            
            if outcome == 'W':
                # Wicket falls
                batsman_scores[striker]['out'] = True
                wickets += 1
                balls_in_over += 1
                
                # Next batsman comes in
                if batsman_index < len(batting_order):
                    current_batsmen[0] = batting_order[batsman_index]
                    batsman_index += 1
                    
            elif outcome == 'wd' or outcome == 'nb':
                # Wide or no-ball - extra run but no ball counted
                total_runs += 1
                
            else:
                # Normal scoring shot
                runs = int(outcome)
                total_runs += runs
                batsman_scores[striker]['runs'] += runs
                batsman_scores[striker]['balls'] += 1
                balls_in_over += 1
                
                # Update boundaries
                if runs == 4:
                    batsman_scores[striker]['fours'] += 1
                elif runs == 6:
                    batsman_scores[striker]['sixes'] += 1
                
                # Strike rotation
                if runs % 2 == 1:
                    current_batsmen[0], current_batsmen[1] = current_batsmen[1], current_batsmen[0]
        
        overs += 1
        # End of over - rotate strike
        current_batsmen[0], current_batsmen[1] = current_batsmen[1], current_batsmen[0]
    
    # Calculate strike rates
    for batsman, stats in batsman_scores.items():
        if stats['balls'] > 0:
            stats['strike_rate'] = (stats['runs'] / stats['balls']) * 100
    
    return {
        'team': team_name,
        'total': total_runs,
        'wickets': wickets,
        'overs': overs,
        'batsmen': batsman_scores
    }

def determine_winner(team1_data, team2_data):
    """Determine match winner and format result message"""
    if team1_data['total'] > team2_data['total']:
        margin = team1_data['total'] - team2_data['total']
        return {
            'winner': team1_data['team'],
            'result': f"{team1_data['team']} won by {margin} runs",
            'winner_team': team1_data
        }
    elif team2_data['total'] > team1_data['total']:
        wickets_left = 10 - team2_data['wickets']
        return {
            'winner': team2_data['team'],
            'result': f"{team2_data['team']} won by {wickets_left} wickets",
            'winner_team': team2_data
        }
    else:
        return {
            'winner': 'tie',
            'result': "Match Tied!",
            'winner_team': team1_data
        }

# ============================================================================
# SCORECARD IMAGE GENERATOR (IPL STYLE)
# ============================================================================

def create_scorecard_image(team1_data, team2_data):
    """
    Create IPL-style match summary image
    Shows match result, top performers, and player of the match
    """
    width, height = 900, 650
    img = Image.new('RGB', (width, height), color='#1a1a2e')
    draw = ImageDraw.Draw(img)
    
    # Load fonts with fallback
    try:
        font_title = ImageFont.truetype("arial.ttf", 32)
        font_large = ImageFont.truetype("arial.ttf", 24)
        font_medium = ImageFont.truetype("arial.ttf", 18)
        font_small = ImageFont.truetype("arial.ttf", 14)
    except:
        font_title = ImageFont.load_default()
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Header with gradient effect
    draw.rectangle([(0, 0), (width, 80)], fill='#ff6b35')
    draw.text((width//2, 40), "MATCH SUMMARY", fill='#ffffff', font=font_title, anchor='mm')
    
    # Team scores section
    y = 110
    team1_score = f"{team1_data['team']}: {team1_data['total']}/{team1_data['wickets']} ({team1_data['overs']} ov)"
    team2_score = f"{team2_data['team']}: {team2_data['total']}/{team2_data['wickets']} ({team2_data['overs']} ov)"
    
    draw.text((50, y), team1_score, fill='#00ff88', font=font_large)
    draw.text((50, y + 40), team2_score, fill='#00ff88', font=font_large)
    
    # Winner section
    y += 100
    match_result = determine_winner(team1_data, team2_data)
    result_text = match_result['result']
    winner_team = match_result['winner_team']
    
    draw.rectangle([(30, y), (width-30, y+55)], fill='#ffd700')
    draw.text((width//2, y+27), result_text, fill='#000000', font=font_large, anchor='mm')
    
    # Top performers section
    y += 80
    draw.text((50, y), "TOP PERFORMERS", fill='#ffd700', font=font_medium)
    
    # Top scorer
    y += 40
    all_batsmen = list(team1_data['batsmen'].items()) + list(team2_data['batsmen'].items())
    all_batsmen = [(p, s) for p, s in all_batsmen if s['balls'] > 0]
    
    if all_batsmen:
        top_scorer = max(all_batsmen, key=lambda x: x[1]['runs'])
        draw.text((50, y), "⭐ Top Scorer:", fill='#ffffff', font=font_small)
        scorer_text = f"{top_scorer[0]} - {top_scorer[1]['runs']}({top_scorer[1]['balls']}) [{top_scorer[1]['fours']}x4, {top_scorer[1]['sixes']}x6]"
        draw.text((50, y+22), scorer_text, fill='#00d9ff', font=font_medium)
        
        # Best strike rate (min 10 balls)
        y += 65
        eligible_batsmen = [(p, s) for p, s in all_batsmen if s['balls'] >= 10]
        if eligible_batsmen:
            best_sr = max(eligible_batsmen, key=lambda x: x[1]['strike_rate'])
            draw.text((50, y), "🔥 Best Strike Rate:", fill='#ffffff', font=font_small)
            sr_text = f"{best_sr[0]} - SR: {best_sr[1]['strike_rate']:.1f}"
            draw.text((50, y+22), sr_text, fill='#ff6b6b', font=font_medium)
    
    # Player of the match
    y += 65
    winner_batsmen = [(p, s) for p, s in winner_team['batsmen'].items() if s['balls'] > 0]
    if winner_batsmen:
        potm = max(winner_batsmen, key=lambda x: x[1]['runs'])
        draw.text((50, y), "🏅 Player of the Match:", fill='#ffffff', font=font_small)
        potm_text = f"{potm[0]} - {potm[1]['runs']}({potm[1]['balls']})"
        draw.text((50, y+22), potm_text, fill='#ff6b35', font=font_medium)
    
    # Footer
    draw.rectangle([(0, height-45), (width, height)], fill='#0f0f1e')
    draw.text((width//2, height-22), "Powered by Cricket Sim Bot | Use → to see full scorecard", fill='#888888', font=font_small, anchor='mm')
    
    # Save to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    return img_bytes

# ============================================================================
# DISCORD UI VIEWS (BUTTONS AND NAVIGATION)
# ============================================================================

class ScorecardView(discord.ui.View):
    """Interactive scorecard with navigation buttons"""
    
    def __init__(self, team1_data, team2_data):
        super().__init__(timeout=300)
        self.team1_data = team1_data
        self.team2_data = team2_data
        self.current_page = 0
    
    @discord.ui.button(label='→ Next', style=discord.ButtonStyle.primary)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Navigate to next page"""
        self.current_page = (self.current_page + 1) % 3
        embed = self.get_embed()
        await interaction.response.edit_message(embed=embed)
    
    def get_embed(self):
        """Get current page embed"""
        if self.current_page == 0:
            return self.get_summary_embed()
        elif self.current_page == 1:
            return self.get_team_embed(self.team1_data)
        else:
            return self.get_team_embed(self.team2_data)
    
    def get_summary_embed(self):
        """Match summary page"""
        embed = discord.Embed(title="📊 Match Summary", color=0x00ff88)
        embed.add_field(
            name=f"{self.team1_data['team']} 🏏",
            value=f"**{self.team1_data['total']}/{self.team1_data['wickets']}** ({self.team1_data['overs']} overs)",
            inline=False
        )
        embed.add_field(
            name=f"{self.team2_data['team']} 🏏",
            value=f"**{self.team2_data['total']}/{self.team2_data['wickets']}** ({self.team2_data['overs']} overs)",
            inline=False
        )
        
        result = determine_winner(self.team1_data, self.team2_data)
        embed.add_field(name="🏆 Result", value=result['result'], inline=False)
        embed.set_footer(text="Click → to see full scorecards")
        return embed
    
    def get_team_embed(self, team_data):
        """Full team scorecard page"""
        embed = discord.Embed(title=f"📋 {team_data['team']} Scorecard", color=0x3498db)
        embed.add_field(
            name="Total Score",
            value=f"**{team_data['total']}/{team_data['wickets']}** ({team_data['overs']} overs)",
            inline=False
        )
        
        # Batting scorecard
        batting_text = "```\n"
        batting_text += "Batsman            Runs  Balls  4s  6s   SR\n"
        batting_text += "─" * 50 + "\n"
        
        for batsman, stats in team_data['batsmen'].items():
            if stats['balls'] > 0 or stats['out']:
                status = "*" if stats['out'] else " "
                sr = f"{stats['strike_rate']:.1f}" if stats['balls'] > 0 else "0.0"
                batting_text += f"{batsman[:17]:<17}{status} {stats['runs']:>4}  {stats['balls']:>5}  {stats['fours']:>2}  {stats['sixes']:>2} {sr:>6}\n"
        
        batting_text += "```"
        embed.add_field(name="🏏 Batting Performance", value=batting_text, inline=False)
        
        # Extras and run rate
        run_rate = (team_data['total'] / team_data['overs']) if team_data['overs'] > 0 else 0
        embed.add_field(name="Run Rate", value=f"{run_rate:.2f}", inline=True)
        
        return embed

class LeaderboardView(discord.ui.View):
    """Interactive leaderboard with cap selection"""
    
    def __init__(self):
        super().__init__(timeout=300)
        self.current_cap = 'orange'
    
    @discord.ui.button(label='🟠 Orange Cap', style=discord.ButtonStyle.danger)
    async def orange_cap(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show top run scorers"""
        self.current_cap = 'orange'
        embed = self.get_leaderboard_embed()
        await interaction.response.edit_message(embed=embed)
    
    @discord.ui.button(label='🟣 Purple Cap', style=discord.ButtonStyle.blurple)
    async def purple_cap(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show top wicket takers"""
        self.current_cap = 'purple'
        embed = self.get_leaderboard_embed()
        await interaction.response.edit_message(embed=embed)
    
    @discord.ui.button(label='🟢 Best Average', style=discord.ButtonStyle.green)
    async def avg_cap(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show best batting averages"""
        self.current_cap = 'average'
        embed = self.get_leaderboard_embed()
        await interaction.response.edit_message(embed=embed)
    
    @discord.ui.button(label='⚡ Best Strike Rate', style=discord.ButtonStyle.secondary)
    async def sr_cap(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show best strike rates"""
        self.current_cap = 'strike_rate'
        embed = self.get_leaderboard_embed()
        await interaction.response.edit_message(embed=embed)
    
    def get_leaderboard_embed(self):
        """Generate leaderboard embed based on current selection"""
        if self.current_cap == 'orange':
            # Orange Cap - Top Run Scorers
            sorted_players = sorted(
                player_stats.items(),
                key=lambda x: x[1].get('runs', 0),
                reverse=True
            )[:10]
            
            embed = discord.Embed(title="🟠 Orange Cap - Top Run Scorers", color=0xff6600)
            
            leaderboard = "```\n"
            leaderboard += "Rank  Player              Runs   Avg    SR   Inns\n"
            leaderboard += "─" * 52 + "\n"
            
            for i, (player, stats) in enumerate(sorted_players, 1):
                runs = stats.get('runs', 0)
                innings = stats.get('innings', 1)
                balls = stats.get('balls', 1)
                avg = runs / innings if innings > 0 else 0
                sr = (runs / balls * 100) if balls > 0 else 0
                leaderboard += f"{i:<5} {player[:18]:<18} {runs:>5} {avg:>6.1f} {sr:>5.1f} {innings:>4}\n"
            
            leaderboard += "```"
            embed.description = leaderboard
            
        elif self.current_cap == 'purple':
            # Purple Cap - Top Wicket Takers
            sorted_players = sorted(
                player_stats.items(),
                key=lambda x: x[1].get('wickets', 0),
                reverse=True
            )[:10]
            
            embed = discord.Embed(title="🟣 Purple Cap - Top Wicket Takers", color=0x9b59b6)
            
            leaderboard = "```\n"
            leaderboard += "Rank  Player              Wkts  Avg   Econ  Inns\n"
            leaderboard += "─" * 50 + "\n"
            
            for i, (player, stats) in enumerate(sorted_players, 1):
                wickets = stats.get('wickets', 0)
                runs_given = stats.get('runs_given', 0)
                overs = stats.get('overs', 1)
                innings = stats.get('bowling_innings', 0)
                avg = runs_given / wickets if wickets > 0 else 0
                econ = runs_given / overs if overs > 0 else 0
                leaderboard += f"{i:<5} {player[:18]:<18} {wickets:>4} {avg:>6.1f} {econ:>5.2f} {innings:>4}\n"
            
            leaderboard += "```"
            embed.description = leaderboard
            
        elif self.current_cap == 'average':
            # Best Batting Average (min 3 innings)
            sorted_players = sorted(
                [(p, s) for p, s in player_stats.items() if s.get('innings', 0) >= 3],
                key=lambda x: x[1].get('runs', 0) / x[1].get('innings', 1),
                reverse=True
            )[:10]
            
            embed = discord.Embed(title="🟢 Best Batting Average (Min 3 Innings)", color=0x2ecc71)
            
            leaderboard = "```\n"
            leaderboard += "Rank  Player              Avg    Runs  Inns  50s\n"
            leaderboard += "─" * 50 + "\n"
            
            for i, (player, stats) in enumerate(sorted_players, 1):
                runs = stats.get('runs', 0)
                innings = stats.get('innings', 1)
                fifties = stats.get('fifties', 0)
                avg = runs / innings
                leaderboard += f"{i:<5} {player[:18]:<18} {avg:>6.1f} {runs:>5} {innings:>4} {fifties:>4}\n"
            
            leaderboard += "```"
            embed.description = leaderboard
            
        else:
            # Best Strike Rate (min 50 balls)
            sorted_players = sorted(
                [(p, s) for p, s in player_stats.items() if s.get('balls', 0) >= 50],
                key=lambda x: (x[1].get('runs', 0) / x[1].get('balls', 1)) * 100,
                reverse=True
            )[:10]
            
            embed = discord.Embed(title="⚡ Best Strike Rate (Min 50 Balls)", color=0xf1c40f)
            
            leaderboard = "```\n"
            leaderboard += "Rank  Player                SR   Runs  Balls 6s\n"
            leaderboard += "─" * 50 + "\n"
            
            for i, (player, stats) in enumerate(sorted_players, 1):
                runs = stats.get('runs', 0)
                balls = stats.get('balls', 1)
                sixes = stats.get('sixes', 0)
                sr = (runs / balls) * 100
                leaderboard += f"{i:<5} {player[:18]:<18} {sr:>6.1f} {runs:>5} {balls:>5} {sixes:>3}\n"
            
            leaderboard += "```"
            embed.description = leaderboard
        
        embed.set_footer(text="Click buttons to switch between leaderboards")
        return embed

# ============================================================================
# BOT COMMANDS - MATCH SIMULATION
# ============================================================================

@bot.command()
async def sim(ctx, *, teams_input: str):
    """
    Simulate a cricket match
    Usage: !sim Team1 vs Team2
    """
    try:
        # Parse team names
        team_names = teams_input.split(' vs ')
        if len(team_names) != 2:
            await ctx.send("❌ Invalid format! Use: `!sim Team1 vs Team2`")
            return
        
        team1_name = team_names[0].strip()
        team2_name = team_names[1].strip()
        
        # Get squads
        team1_squad = teams_data.get(team1_name, [])
        team2_squad = teams_data.get(team2_name, [])
        
        # Send simulation message
        sim_msg = await ctx.send(f"🏏 **Simulating Match**\n{team1_name} vs {team2_name}\n\n⏳ Toss happening...")
        
        # Simulate toss
        await asyncio.sleep(1)
        toss_winner = random.choice([team1_name, team2_name])
        choice = random.choice(['bat', 'bowl'])
        await sim_msg.edit(content=f"🏏 **Simulating Match**\n{team1_name} vs {team2_name}\n\n🪙 {toss_winner} won the toss and chose to {choice}\n⏳ Match in progress...")
        
        # Simulate both innings
        if (toss_winner == team1_name and choice == 'bat') or (toss_winner == team2_name and choice == 'bowl'):
            team1_innings = simulate_innings(team1_name, team1_squad)
            team2_innings = simulate_innings(team2_name, team2_squad, target=team1_innings['total'])
        else:
            team2_innings = simulate_innings(team2_name, team2_squad)
            team1_innings = simulate_innings(team1_name, team1_squad, target=team2_innings['total'])
        
        # Create scorecard image
        img_bytes = create_scorecard_image(team1_innings, team2_innings)
        
        # Create view with navigation
        view = ScorecardView(team1_innings, team2_innings)
        
        # Send final result
        file = discord.File(img_bytes, filename='scorecard.png')
        embed = view.get_summary_embed()
        embed.set_image(url='attachment://scorecard.png')
        embed.set_footer(text=f"Toss: {toss_winner} chose to {choice}")
        
        message = await ctx.send(file=file, embed=embed, view=view)
        
        # Store match data
        bot.last_match = {
            'message_id': message.id,
            'team1': team1_innings,
            'team2': team2_innings,
            'timestamp': datetime.now().isoformat()
        }
        
        # Add to history
        match_history['matches'].insert(0, {
            'team1': team1_name,
            'team2': team2_name,
            'score1': f"{team1_innings['total']}/{team1_innings['wickets']}",
            'score2': f"{team2_innings['total']}/{team2_innings['wickets']}",
            'result': determine_winner(team1_innings, team2_innings)['result'],
            'date': datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        
        # Keep only last 20 matches
        match_history['matches'] = match_history['matches'][:20]
        save_data(HISTORY_FILE, match_history)
        
        # Delete simulation message
        await sim_msg.delete()
        
    except Exception as e:
        await ctx.send(f"❌ Error simulating match: {str(e)}")

# ============================================================================
# BOT COMMANDS - TEAM MANAGEMENT
# ============================================================================

@bot.command()
@commands.has_permissions(administrator=True)
async def teamadd(ctx, team_name: str, *, players: str):
    """
    Add a team with squad
    Usage: !teamadd TeamName Player1, Player2, Player3...
    """
    player_list = [p.strip() for p in players.split(',')]
    
    if len(player_list) < 11:
        await ctx.send(f"⚠️ Warning: Only {len(player_list)} players added. Minimum 11 recommended.")
    
    teams_data[team_name] = player_list
    save_data(TEAMS_FILE, teams_data)
    
    embed = discord.Embed(title=f"✅ Team Added: {team_name}", color=0x2ecc71)
    embed.add_field(name=f"Squad ({len(player_list)} players)", value=", ".join(player_list), inline=False)
    embed.set_footer(text=f"Added by {ctx.author.name}")
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def teamremove(ctx, team_name: str):
    """
    Remove a team
    Usage: !teamremove TeamName
    """
    if team_name in teams_data:
        del teams_data[team_name]
        save_data(TEAMS_FILE, teams_data)
        await ctx.send(f"✅ Team **{team_name}** has been removed!")
    else:
        await ctx.send(f"❌ Team **{team_name}** not found!")

@bot.command()
async def teams(ctx):
    """Show all registered teams"""
    if not teams:
        await ctx.send("❌ No teams registered yet! Use `!teamadd` to add teams.")
        return
    
    embed = discord.Embed(title="📋 Registered Teams", color=0x3498db)
    
    for team_name, squad in teams.items():
        embed.add_field(
            name=f"{team_name} ({len(squad)} players)",
            value=", ".join(squad[:5]) + ("..." if len(squad) > 5 else ""),
            inline=False
        )
    
    embed.set_footer(text=f"Total teams: {len(teams)}")
    await ctx.send(embed=embed)

# ============================================================================
# BOT COMMANDS - STATS MANAGEMENT
# ============================================================================

@bot.command()
@commands.has_permissions(administrator=True)
async def addstats(ctx):
    """
    Add stats from last match
    Usage: Reply to a scorecard message with !addstats
    """
    if not ctx.message.reference:
        await ctx.send("❌ Please reply to a scorecard message!")
        return
    
    if not hasattr(bot, 'last_match'):
        await ctx.send("❌ No recent match data found!")
        return
    
    team1 = bot.last_match['team1']
    team2 = bot.last_match['team2']
    
    stats_added = 0
    
    # Add batting stats for both teams
    for batsman, stats in team1['batsmen'].items():
        if batsman not in player_stats:
            player_stats[batsman] = {
                'runs': 0, 'balls': 0, 'innings': 0, 'fours': 0,
                'sixes': 0, 'fifties': 0, 'hundreds': 0, 'wickets': 0
            }
        
        if stats['balls'] > 0:
            player_stats[batsman]['runs'] += stats['runs']
            player_stats[batsman]['balls'] += stats['balls']
            player_stats[batsman]['innings'] += 1
            player_stats[batsman]['fours'] += stats['fours']
            player_stats[batsman]['sixes'] += stats['sixes']
            
            # Check for milestones
            if stats['runs'] >= 100:
                player_stats[batsman]['hundreds'] = player_stats[batsman].get('hundreds', 0) + 1
            elif stats['runs'] >= 50:
                player_stats[batsman]['fifties'] = player_stats[batsman].get('fifties', 0) + 1
            
            stats_added += 1
    
    for batsman, stats in team2['batsmen'].items():
        if batsman not in player_stats:
            player_stats[batsman] = {
                'runs': 0, 'balls': 0, 'innings': 0, 'fours': 0,
                'sixes': 0, 'fifties': 0, 'hundreds': 0, 'wickets': 0
            }
        
        if stats['balls'] > 0:
            player_stats[batsman]['runs'] += stats['runs']
            player_stats[batsman]['balls'] += stats['balls']
            player_stats[batsman]['innings'] += 1
            player_stats[batsman]['fours'] += stats['fours']
            player_stats[batsman]['sixes'] += stats['sixes']
            
            if stats['runs'] >= 100:
                player_stats[batsman]['hundreds'] = player_stats[batsman].get('hundreds', 0) + 1
            elif stats['runs'] >= 50:
                player_stats[batsman]['fifties'] = player_stats[batsman].get('fifties', 0) + 1
            
            stats_added += 1
    
    save_data(STATS_FILE, player_stats)
    
    embed = discord.Embed(title="✅ Stats Added Successfully!", color=0x2ecc71)
    embed.add_field(name="Players Updated", value=str(stats_added), inline=True)
    embed.add_field(name="Match", value=f"{team1['team']} vs {team2['team']}", inline=True)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def removestats(ctx):
    """
    Remove stats from last match
    Usage: Reply to a scorecard message with !removestats
    """
    if not ctx.message.reference:
        await ctx.send("❌ Please reply to a scorecard message!")
        return
    
    if not hasattr(bot, 'last_match'):
        await ctx.send("❌ No recent match data found!")
        return
    
    team1 = bot.last_match['team1']
    team2 = bot.last_match['team2']
    
    # Remove batting stats
    for batsman, stats in team1['batsmen'].items():
        if batsman in player_stats and stats['balls'] > 0:
            player_stats[batsman]['runs'] -= stats['runs']
            player_stats[batsman]['balls'] -= stats['balls']
            player_stats[batsman]['innings'] -= 1
            player_stats[batsman]['fours'] -= stats['fours']
            player_stats[batsman]['sixes'] -= stats['sixes']
    
    for batsman, stats in team2['batsmen'].items():
        if batsman in player_stats and stats['balls'] > 0:
            player_stats[batsman]['runs'] -= stats['runs']
            player_stats[batsman]['balls'] -= stats['balls']
            player_stats[batsman]['innings'] -= 1
            player_stats[batsman]['fours'] -= stats['fours']
            player_stats[batsman]['sixes'] -= stats['sixes']
    
    save_data(STATS_FILE, player_stats)
    await ctx.send("✅ Stats removed successfully!")

# ============================================================================
# BOT COMMANDS - LEADERBOARDS AND PLAYER INFO
# ============================================================================

@bot.command()
async def lb(ctx):
    """
    Show leaderboards
    Usage: !lb
    """
    if not player_stats:
        await ctx.send("❌ No player stats available yet!")
        return
    
    view = LeaderboardView()
    embed = view.get_leaderboard_embed()
    await ctx.send(embed=embed, view=view)

@bot.command()
async def player(ctx, *, player_name: str):
    """
    Show player profile and stats
    Usage: !player PlayerName
    """
    if player_name not in player_stats:
        await ctx.send(f"❌ Player **{player_name}** not found in stats!")
        return
    
    stats = player_stats[player_name]
    
    embed = discord.Embed(title=f"👤 {player_name}", color=0x3498db)
    
    # Batting stats
    runs = stats.get('runs', 0)
    balls = stats.get('balls', 1)
    innings = stats.get('innings', 0)
    avg = runs / innings if innings > 0 else 0
    sr = (runs / balls * 100) if balls > 0 else 0
    
    batting = f"```\n"
    batting += f"Runs:      {runs}\n"
    batting += f"Innings:   {innings}\n"
    batting += f"Average:   {avg:.2f}\n"
    batting += f"Strike Rate: {sr:.2f}\n"
    batting += f"Balls Faced: {balls}\n"
    batting += f"Fours:     {stats.get('fours', 0)}\n"
    batting += f"Sixes:     {stats.get('sixes', 0)}\n"
    batting += f"Fifties:   {stats.get('fifties', 0)}\n"
    batting += f"Hundreds:  {stats.get('hundreds', 0)}\n"
    batting += "```"
    
    embed.add_field(name="🏏 Batting Stats", value=batting, inline=False)
    
    # Bowling stats (if any)
    wickets = stats.get('wickets', 0)
    if wickets > 0:
        bowling = f"```\n"
        bowling += f"Wickets: {wickets}\n"
        bowling += "```"
        embed.add_field(name="⚾ Bowling Stats", value=bowling, inline=False)
    
    await ctx.send(embed=embed)

@bot.command()
async def history(ctx):
    """Show recent match history"""
    if not match_history.get('matches'):
        await ctx.send("❌ No match history available!")
        return
    
    embed = discord.Embed(title="📜 Recent Match History", color=0x9b59b6)
    
    for i, match in enumerate(match_history['matches'][:10], 1):
        match_info = f"{match['team1']} {match['score1']} vs {match['team2']} {match['score2']}\n"
        match_info += f"**{match['result']}**\n"
        match_info += f"_{match['date']}_"
        embed.add_field(name=f"Match {i}", value=match_info, inline=False)
    
    await ctx.send(embed=embed)

# ============================================================================
# BOT COMMANDS - WORLD CUP MODE
# ============================================================================

@bot.command()
@commands.has_permissions(administrator=True)
async def wcstart(ctx, *, team_names: str):
    """
    Start World Cup tournament
    Usage: !wcstart Team1, Team2, Team3, Team4...
    """
    wc_teams = [t.strip() for t in team_names.split(',')]
    
    if len(wc_teams) < 4:
        await ctx.send("❌ Need at least 4 teams for World Cup!")
        return
    
    # Initialize World Cup data
    worldcup_data['teams'] = wc_teams
    worldcup_data['standings'] = {}
    
    for team in wc_teams:
        worldcup_data['standings'][team] = {
            'played': 0,
            'won': 0,
            'lost': 0,
            'tied': 0,
            'points': 0,
            'nrr': 0.0,
            'for': 0,
            'against': 0
        }
    
    worldcup_data['stage'] = 'league'
    worldcup_data['matches_played'] = []
    save_data(WORLDCUP_FILE, worldcup_data)
    
    embed = discord.Embed(title="🏆 WORLD CUP STARTED!", color=0xffd700)
    embed.add_field(name="🌍 Participating Teams", value=", ".join(wc_teams), inline=False)
    embed.add_field(name="📋 Format", value="League Stage → Semi Finals → Final", inline=False)
    embed.add_field(name="📊 Points System", value="Win: 2 points | Tie: 1 point | Loss: 0 points", inline=False)
    embed.set_footer(text="Use !wcmatch to play matches | !wcstandings to view table")
    
    await ctx.send(embed=embed)

@bot.command()
async def wcmatch(ctx, *, teams_input: str):
    """
    Play World Cup match
    Usage: !wcmatch Team1 vs Team2
    """
    if 'teams' not in worldcup_data:
        await ctx.send("❌ No World Cup in progress! Use `!wcstart` to start one.")
        return
    
    try:
        team_names = teams_input.split(' vs ')
        if len(team_names) != 2:
            await ctx.send("❌ Invalid format! Use: `!wcmatch Team1 vs Team2`")
            return
        
        team1_name = team_names[0].strip()
        team2_name = team_names[1].strip()
        
        if team1_name not in worldcup_data['teams'] or team2_name not in worldcup_data['teams']:
            await ctx.send("❌ Both teams must be in the World Cup!")
            return
        
        # Get squads
        team1_squad = teams_data.get(team1_name, [])
        team2_squad = teams_data.get(team2_name, [])
        
        await ctx.send(f"🏆 **WORLD CUP MATCH**\n🏏 {team1_name} vs {team2_name}\n\n⏳ Simulating...")
        
        # Simulate match
        team1_innings = simulate_innings(team1_name, team1_squad)
        team2_innings = simulate_innings(team2_name, team2_squad, target=team1_innings['total'])
        
        # Update standings
        worldcup_data['standings'][team1_name]['played'] += 1
        worldcup_data['standings'][team2_name]['played'] += 1
        worldcup_data['standings'][team1_name]['for'] += team1_innings['total']
        worldcup_data['standings'][team1_name]['against'] += team2_innings['total']
        worldcup_data['standings'][team2_name]['for'] += team2_innings['total']
        worldcup_data['standings'][team2_name]['against'] += team1_innings['total']
        
        if team1_innings['total'] > team2_innings['total']:
            worldcup_data['standings'][team1_name]['won'] += 1
            worldcup_data['standings'][team1_name]['points'] += 2
            worldcup_data['standings'][team2_name]['lost'] += 1
        elif team2_innings['total'] > team1_innings['total']:
            worldcup_data['standings'][team2_name]['won'] += 1
            worldcup_data['standings'][team2_name]['points'] += 2
            worldcup_data['standings'][team1_name]['lost'] += 1
        else:
            worldcup_data['standings'][team1_name]['tied'] += 1
            worldcup_data['standings'][team2_name]['tied'] += 1
            worldcup_data['standings'][team1_name]['points'] += 1
            worldcup_data['standings'][team2_name]['points'] += 1
        
        save_data(WORLDCUP_FILE, worldcup_data)
        
        # Create scorecard
        img_bytes = create_scorecard_image(team1_innings, team2_innings)
        view = ScorecardView(team1_innings, team2_innings)
        
        file = discord.File(img_bytes, filename='scorecard.png')
        embed = view.get_summary_embed()
        embed.set_image(url='attachment://scorecard.png')
        embed.set_footer(text="🏆 World Cup Match | Use !wcstandings to see table")
        embed.color = 0xffd700
        
        await ctx.send(file=file, embed=embed, view=view)
        
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command()
async def wcstandings(ctx):
    """Show World Cup points table"""
    if 'standings' not in worldcup_data:
        await ctx.send("❌ No World Cup in progress!")
        return
    
    sorted_teams = sorted(
        worldcup_data['standings'].items(),
        key=lambda x: (x[1]['points'], x[1]['won'], x[1]['for'] - x[1]['against']),
        reverse=True
    )
    
    embed = discord.Embed(title="🏆 WORLD CUP STANDINGS", color=0xffd700)
    
    table = "```\n"
    table += "Pos Team            P   W   L   T  Pts  NRR\n"
    table += "─" * 48 + "\n"
    
    for i, (team, stats) in enumerate(sorted_teams, 1):
        nrr = (stats['for'] - stats['against']) / stats['played'] if stats['played'] > 0 else 0
        qualifier = "🟢" if i <= 4 else ""
        table += f"{i:<3} {team[:14]:<14}{qualifier} {stats['played']:>2}  {stats['won']:>2}  {stats['lost']:>2}  {stats['tied']:>2}  {stats['points']:>3} {nrr:>5.2f}\n"
    
    table += "\n🟢 = Qualified for Semi-Finals (Top 4)"
    table += "```"
    
    embed.description = table
    embed.set_footer(text=f"Stage: {worldcup_data.get('stage', 'league').upper()}")
    
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def wcsemis(ctx):
    """Generate semi-final matchups"""
    if 'standings' not in worldcup_data:
        await ctx.send("❌ No World Cup in progress!")
        return
    
    sorted_teams = sorted(
        worldcup_data['standings'].items(),
        key=lambda x: (x[1]['points'], x[1]['won']),
        reverse=True
    )
    
    if len(sorted_teams) < 4:
        await ctx.send("❌ Not enough teams for semi-finals!")
        return
    
    worldcup_data['stage'] = 'semifinals'
    save_data(WORLDCUP_FILE, worldcup_data)
    
    embed = discord.Embed(title="🏆 WORLD CUP SEMI-FINALS", color=0xff6b35)
    embed.add_field(
        name="🥇 Semi-Final 1",
        value=f"**{sorted_teams_data[0][0]}** vs **{sorted_teams_data[3][0]}**\n_(1st vs 4th)_",
        inline=False
    )
    embed.add_field(
        name="🥈 Semi-Final 2",
        value=f"**{sorted_teams_data[1][0]}** vs **{sorted_teams_data[2][0]}**\n_(2nd vs 3rd)_",
        inline=False
    )
    embed.set_footer(text="Use !wcmatch to play semi-final matches")
    
    await ctx.send(embed=embed)

@bot.command()
async def wcfinal(ctx, *, teams_input: str):
    """
    Play World Cup final
    Usage: !wcfinal Team1 vs Team2
    """
    try:
        team_names = teams_input.split(' vs ')
        team1_name = team_names[0].strip()
        team2_name = team_names[1].strip()
        
        team1_squad = teams_data.get(team1_name, [])
        team2_squad = teams_data.get(team2_name, [])
        
        await ctx.send(f"🏆 **WORLD CUP FINAL**\n🏏 {team1_name} vs {team2_name}\n\n⏳ The biggest match is being simulated...")
        
        team1_innings = simulate_innings(team1_name, team1_squad)
        team2_innings = simulate_innings(team2_name, team2_squad, target=team1_innings['total'])
        
        img_bytes = create_scorecard_image(team1_innings, team2_innings)
        view = ScorecardView(team1_innings, team2_innings)
        
        file = discord.File(img_bytes, filename='final.png')
        embed = view.get_summary_embed()
        embed.title = "🏆 WORLD CUP FINAL RESULT"
        embed.set_image(url='attachment://final.png')
        embed.color = 0xffd700
        
        winner = determine_winner(team1_innings, team2_innings)['winner']
        embed.add_field(
            name="🎉 WORLD CUP CHAMPIONS",
            value=f"**{winner}** 🏆",
            inline=False
        )
        
        await ctx.send(file=file, embed=embed, view=view)
        
        worldcup_data['champion'] = winner
        worldcup_data['stage'] = 'completed'
        save_data(WORLDCUP_FILE, worldcup_data)
        
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

# ============================================================================
# BOT EVENTS
# ============================================================================

@bot.event
async def on_ready():
    """Called when bot is ready"""
    print(f'✅ {bot.user} is now online!')
    print(f'📊 {len(teams)} teams loaded')
    print(f'👥 {len(player_stats)} players in database')
    print('🏏 Cricket Simulation Bot is ready!')
    
    # Set bot status
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="cricket matches | !sim"
        )
    )

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to use this command!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing argument: {error.param.name}")
    else:
        await ctx.send(f"❌ Error: {str(error)}")

# ============================================================================
# HELP COMMAND
# ============================================================================

@bot.command()
async def help_cricket(ctx):
    """Show all commands"""
    embed = discord.Embed(title="🏏 Cricket Sim Bot - Commands", color=0x00ff88)
    
    embed.add_field(
        name="⚾ Match Commands",
        value="```\n!sim Team1 vs Team2 - Simulate match\n!history - Recent matches```",
        inline=False
    )
    
    embed.add_field(
        name="👥 Team Commands",
        value="```\n!teamadd Name Player1,Player2... - Add team\n!teamremove Name - Remove team\n!teams - List all teams```",
        inline=False
    )
    
    embed.add_field(
        name="📊 Stats Commands",
        value="```\n!addstats - Add match stats\n!removestats - Remove stats\n!lb - Leaderboards\n!player Name - Player profile```",
        inline=False
    )
    
    embed.add_field(
        name="🏆 World Cup Commands",
        value="```\n!wcstart Team1,Team2... - Start WC\n!wcmatch Team1 vs Team2 - WC match\n!wcstandings - Points table\n!wcsemis - Generate semis\n!wcfinal Team1 vs Team2 - Final```",
        inline=False
    )
    
    await ctx.send(embed=embed)

# ============================================================================
# RUN BOT
# ============================================================================

# Import asyncio for delays
import asyncio

import os

TOKEN = os.getenv("TOKEN")  # get the token from Railway variable

bot.run(TOKEN)
