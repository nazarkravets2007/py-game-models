import json
from db.models import Race, Skill, Guild, Player
from django.db import transaction


def main():
    with open('players.json', 'r', encoding='utf-8') as f:
        players_data = json.load(f)

    with transaction.atomic():
        for player_data in players_data:
            # SAFE access to race
            race_data = player_data.get('race')
            if race_data:
                race_name = race_data.get('name')
                race_description = race_data.get('description', '')
                race, _ = Race.objects.get_or_create(
                    name=race_name,
                    defaults={'description': race_description}
                )

                # SAFE access to skills
                skills_data = race_data.get('skills', [])
                for skill_data in skills_data:
                    skill_name = skill_data.get('name')
                    skill_bonus = skill_data.get('bonus', '')
                    if skill_name:
                        Skill.objects.get_or_create(
                            name=skill_name,
                            defaults={'bonus': skill_bonus, 'race': race}
                        )
            else:
                race = None

            # SAFE access to guild
            guild_data = player_data.get('guild')
            if guild_data:
                guild_name = guild_data.get('name')
                guild_description = guild_data.get('description')
                if guild_name:
                    guild, _ = Guild.objects.get_or_create(
                        name=guild_name,
                        defaults={'description': guild_description}
                    )
                else:
                    guild = None
            else:
                guild = None

            # Create player
            nickname = player_data.get('nickname')
            email = player_data.get('email', '')
            bio = player_data.get('bio', '')

            if nickname:  # must have nickname
                Player.objects.get_or_create(
                    nickname=nickname,
                    defaults={
                        'email': email,
                        'bio': bio,
                        'race': race,
                        'guild': guild
                    }
                )
