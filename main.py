import os
from flask import Flask, jsonify
from flask_cors import CORS
from openai import OpenAI
import re
import random

app = Flask(__name__)
CORS(app, resources={r"/generate-weapon": {"origins": "http://127.0.0.1:5500"}})

class MessageGenerator:
    def __init__(self, model="gpt-4", temperature=0.7):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.temperature = temperature

    def generate_message(self, user_message, system_instructions):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_instructions},
                    {"role": "user", "content": user_message}
                ],
                temperature=self.temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"Error generating message: {str(e)}")
import re

def extract_weapon_info(response):
    weapon_info = {}

    # Regex patterns for extracting all weapon details
    patterns = {
        'name': r'\[([^\]]+)\]',  # Extracts weapon name inside [ ]
        'type': r'Type:\s*([^\n]+)',  # Extracts weapon type
        'element': r'Element:\s*([^\n]*)',  # Extracts weapon element (optional)
        'rarity': r'Rarity:\s*([^\n]+)',  # Extracts weapon rarity
        
        # Stats patterns
        'attack_power': r'Attack Power:\s*(\d+)',  # Extract attack power
        'defense_power': r'Defense Power:\s*(\d+)?',  # Optional defense power
        'weight': r'Weight:\s*([^\n]+)',  # Extract weight
        'crit_chance': r'Critical Hit Chance:\s*([^\n]+)?',  # Optional crit chance

        # Special ability section
        'special_ability': r'Special Ability:\s*([^\n]*)',  # Optional special ability
        'ability_effect': r'Effect:\s*([^\n]*)',  # Optional ability effect
        'cooldown': r'Cooldown:\s*([^\n]*)',  # Optional cooldown

        # Passive effect section
        'passive_effect': r'Passive Effect:\s*([^\n]*)',  # Optional passive effect
        'passive_effect_description': r'Effect:\s*([^\n]*)',  # Optional passive effect description
        'trigger_condition': r'Trigger Condition:\s*([^\n]*)',  # Optional trigger condition
    }

    # Extract basic details from the response text
    for key, pattern in patterns.items():
        match = re.search(pattern, response)
        if match:
            weapon_info[key] = match.group(1).strip()  # Trim any extra spaces

    # Group stats into a dictionary
    weapon_info['stats'] = {
        'attack_power': weapon_info.pop('attack_power', None),
        'defense_power': weapon_info.pop('defense_power', None),
        'weight': weapon_info.pop('weight', None),
        'crit_chance': weapon_info.pop('crit_chance', None)
    }

    return weapon_info


def extract_stats(stats_section):
    stats = {}
    stat_patterns = {
        'attack_power': r'Attack Power:\s*(\d+)',
        'defense_power': r'Defense Power:\s*(\d+)',
        'durability': r'Durability:\s*(\d+)',
        'weight': r'Weight:\s*(\d+)',
        'crit_chance': r'Critical Hit Chance:\s*(\d+%)',
        'attack_speed': r'Attack Speed:\s*(\S+)'
    }

    for key, pattern in stat_patterns.items():
        match = re.search(pattern, stats_section)
        if match:
            stats[key] = match.group(1)

    return stats

def extract_crafting_materials(materials_section):
    return re.findall(r'(\w+\s\w+:\s\d+)', materials_section)

def generate_rarity():
    rarity_chances = [
        ("Common", 90),
        ("Uncommon", 6),
        ("Rare", 2),
        ("Epic", 1),
        ("Legendary", 0.2),
        ("Mythic", 0.05)
    ]
    total = sum(chance for _, chance in rarity_chances)
    roll = random.uniform(0, total)
    current = 0
    for rarity, chance in rarity_chances:
        current += chance
        if roll <= current:
            return rarity
    return "Common"  # Fallback

@app.route('/generate-weapon', methods=['GET'])
def generate_weapon():
    system_prompt = """
        Generate a random weapon with the following minimal details:

        [Weapon Name] <- This is important
        Type: [Weapon Type]
        Element: [Weapon Element] (optional)
        Rarity: [Weapon Rarity: Common, Rare, Epic, Legendary]
        Stats:
        - Attack Power: [integer]
        - Defense Power: [integer] (optional)
        - Weight: [value]
        - Critical Hit Chance: [percentage] (optional)

        Special Ability: [Ability Name] (optional)
        Effect: [What the ability does] (optional)
        Cooldown: [Cooldown time] (optional)

        Passive Effect: [Passive Effect Name] (optional)
        Effect: [What the passive effect does] (optional)
        Trigger Condition: [When the passive effect is triggered] (optional)
        """


    generator = MessageGenerator("gpt-4")
    user_prompt = "Generate a random weapon. Stats are required"

    try:
        generated_message = generator.generate_message(user_prompt, system_prompt)
        weapon_info = extract_weapon_info(generated_message)
        print(weapon_info)
        return jsonify(weapon_info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)