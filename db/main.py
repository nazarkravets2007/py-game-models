import json
from db.models import Race, Skill, Guild, Player
from django.db import transaction


def main():
    with open('players.json', 'r', encoding='utf-8') as f:
        players_data = json.load(f)

    for player_data in players_data:
        # Race
        race_name = player_data['race']['name']
        race_description = player_data['race'].get('description', '')
        race, _ = Race.objects.get_or_create(name=race_name, defaults={'description': race_description})

        # Skills
        skills_data = player_data['race'].get('skills', [])
        for skill_data in skills_data:
            Skill.objects.get_or_create(
                name=skill_data['name'],
                defaults={
                    'bonus': skill_data['bonus'],
                    'race': race
                }
            )

        # Guild
        guild_data = player_data.get('guild')
        if guild_data:
            guild_name = guild_data['name']
            guild_description = guild_data.get('description')
            guild, _ = Guild.objects.get_or_create(name=guild_name, defaults={'description': guild_description})
        else:
            guild = None

        # Player
        Player.objects.get_or_create(
            nickname=player_data['nickname'],
            defaults={
                'email': player_data['email'],
                'bio': player_data['bio'],
                'race': race,
                'guild': guild
            }
        )
