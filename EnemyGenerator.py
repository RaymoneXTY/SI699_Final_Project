import numpy as np
import pandas as pd

# Total enemies and target stat ranges
TOTAL_ENEMIES = 1000
STAT_RANGES = {
    'defense': (10, 1000),
    'attack': (20, 200),
    'hp': (250, 1000),
    'attack_speed': (30, 120),
    'dodge_frequency': (0, 0.3)
}

# Function to generate enemies using normal distributions across full range
def generate_enemies_full_range_normal(total_count):
    np.random.seed(42)  # for reproducibility

    # Calculate mean and std for each stat to span the entire range with clipping
    def generate_stat(mean, std, count, low, high):
        return np.clip(np.random.normal(loc=mean, scale=std, size=count), low, high)

    # Calculate parameters
    def_mean = np.mean(STAT_RANGES['defense'])
    atk_mean = np.mean(STAT_RANGES['attack'])
    hp_mean = np.mean(STAT_RANGES['hp'])
    spd_mean = np.mean(STAT_RANGES['attack_speed'])
    dodge_mean = np.mean(STAT_RANGES['dodge_frequency'])

    # Generate values
    defense = generate_stat(def_mean, 300, total_count, *STAT_RANGES['defense'])
    attack = generate_stat(atk_mean, 60, total_count, *STAT_RANGES['attack'])
    hp = generate_stat(hp_mean, 400, total_count, *STAT_RANGES['hp'])
    attack_speed = generate_stat(spd_mean, 20, total_count, *STAT_RANGES['attack_speed'])
    dodge_frequency = generate_stat(dodge_mean, 0.15, total_count, *STAT_RANGES['dodge_frequency'])

    # Assemble DataFrame
    return pd.DataFrame({
        'defense': np.round(defense, 1),
        'attack': np.round(attack, 1),
        'hp': np.round(hp, 1),
        'attack_speed': np.round(attack_speed, 1),
        'dodge_frequency': np.round(dodge_frequency, 2)
    })

# Function to assign defense multiplier based on defense thresholds
def assign_defense_multiplier(defense):
    if defense > 956:
        return "Very Low"      # r < 0.125
    elif defense > 120:
        return "Low"           # 0.125 ≤ r ≤ 1
    elif defense > 48:
        return "Median"        # 1 < r ≤ 2.5
    elif defense > 15:
        return "High"          # 2.5 < r ≤ 8
    else:
        return "Very High"     # r > 8

# Generate and format the full dataset
def create_enemy_dataset():
    df = generate_enemies_full_range_normal(TOTAL_ENEMIES)
    df['defense_multiplier'] = df['defense'].apply(assign_defense_multiplier)
    df.insert(0, 'id', range(1, len(df) + 1))

    # Reorder columns
    return df[['id', 'defense_multiplier', 'hp', 'attack', 'attack_speed', 'defense', 'dodge_frequency']]

# Create and preview the dataset
final_enemies = create_enemy_dataset()
print(final_enemies.head())

# save to CSV
final_enemies.to_csv("data/generated_enemies.csv", index=False)
