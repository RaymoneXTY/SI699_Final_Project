import argparse
from BattleSimulation import run_simulation

# Argument parsing
parser = argparse.ArgumentParser(description="Run FSM battle simulation with weapon and enemy data.")
parser.add_argument("--weapons", default="physical_weapons.csv", help="Path to weapons CSV file")
parser.add_argument("--enemies", default="generated_enemies.csv", help="Path to enemies CSV file")
parser.add_argument("--output", default="agent_simulation_results.csv", help="Output CSV file")
parser.add_argument("--rounds", type=int, default=10, help="Number of rounds to simulate per match-up")
parser.add_argument('--variant', type=int, default=0)

args = parser.parse_args()

# Run the simulation
run_simulation(args.weapons, args.enemies, args.output, simulation_rounds=args.rounds)
