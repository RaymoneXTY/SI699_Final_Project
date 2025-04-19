import pandas as pd
import numpy as np
import random
import heapq
from enum import Enum

class State(Enum):
    IDLE = 0
    ATTACK = 1
    DODGE = 2
    DEAD = 3

def calculate_damage_multiplier(r):
    if r < 0.125:
        return 0.10
    elif 0.125 <= r <= 1:
        return 0.10 + ((r - 0.125) ** 2) / 2.552
    elif 1 < r <= 2.5:
        return 0.70 - ((2.5 - r) ** 2) / 7.5
    elif 2.5 < r <= 8:
        return 0.90 - ((8 - r) ** 2) / 151.25
    else:
        return 0.90

class Character:
    def __init__(self, name, hp, attack, attack_speed, defense, dodge_frequency):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.attack_speed = attack_speed
        self.defense = defense
        self.dodge_frequency = dodge_frequency
        self.state = State.IDLE

    def is_alive(self):
        return self.hp > 0

    def attempt_dodge(self):
        return random.random() < self.dodge_frequency

    def attack_target(self, target):
        if target.attempt_dodge():
            return
        r = self.attack / target.defense
        damage = self.attack * calculate_damage_multiplier(r)
        target.hp = max(0, target.hp - damage)

def get_fixed_dodge_frequencies():
    base_freqs = np.clip(np.random.normal(loc=0.4, scale=0.2, size=18), 0, 0.8)
    combined = np.unique(np.round(np.append(base_freqs, [0.0, 0.8]), 2))
    while len(combined) < 20:
        extra = np.clip(np.random.normal(loc=0.4, scale=0.2, size=1), 0, 0.8)
        combined = np.unique(np.round(np.append(combined, extra), 2))
    return np.sort(combined)

def run_simulation(weapons_file, enemies_file, output_file="agent_simulation_results.csv", simulation_rounds=1):
    enemies_df = pd.read_csv(enemies_file)
    weapons_df = pd.read_csv(weapons_file)

    weapon_data = {
        row['weapon']: {
            'attack': row['attack_Phy'],
            'attack_speed': row['hits_per_minute'],
            'defense': row['defence_Phy']
        } for _, row in weapons_df.iterrows()
    }

    dodge_freqs = get_fixed_dodge_frequencies()
    records = []

    for weapon, stats in weapon_data.items():
        for dodge in dodge_freqs:
            for _, enemy in enemies_df.iterrows():
                for round_num in range(simulation_rounds):
                    player = Character("Player", 500, stats['attack'], stats['attack_speed'], stats['defense'], dodge)
                    enemy_char = Character("Enemy", enemy['hp'], enemy['attack'], enemy['attack_speed'], enemy['defense'], enemy['dodge_frequency'])

                    queue = []
                    heapq.heappush(queue, (60 / player.attack_speed, 'player'))
                    heapq.heappush(queue, (60 / enemy_char.attack_speed, 'enemy'))

                    player_attacks = 0

                    while player.is_alive() and enemy_char.is_alive():
                        time, attacker = heapq.heappop(queue)
                        if attacker == 'player' and player.is_alive():
                            player.attack_target(enemy_char)
                            player_attacks += 1
                            heapq.heappush(queue, (time + 60 / player.attack_speed, 'player'))
                        elif attacker == 'enemy' and enemy_char.is_alive():
                            enemy_char.attack_target(player)
                            heapq.heappush(queue, (time + 60 / enemy_char.attack_speed, 'enemy'))

                    records.append({
                        'weapon': weapon,
                        'dodge_frequency': dodge,
                        'enemy_id': enemy['id'],
                        'enemy_defense_multiplier': enemy['defense_multiplier'],
                        'round': round_num + 1,
                        'result': 'win' if player.is_alive() else 'lose',
                        'attacks_spent': player_attacks,
                        'player_hp_left': round(player.hp, 1)
                    })

    df = pd.DataFrame(records)
    df.to_csv(output_file, index=False)
    print(f"Simulation complete. Results saved to: {output_file}")


# if __name__ == "__main__":
#     run_simulation("data/physical_weapons.csv", "data/generated_enemies.csv", "agent_simulation_results.csv", simulation_rounds=5)
