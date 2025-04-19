This is the repo for SI699 project: 
RPG Game Balance Principles and Methodologies: Case Study of Elden Ring

Here are the instructions of the scripts:
- data_exploration.ipynb: used to explore and analyse the game's data, such as weapon stats and player progression curve.
- BattleSimulation.py: turn-based simulation model for the project, which includes a run_simulation function to be passed to the HPC.
- EnemyGenerator.py: used to generate 1000 enemies with normal distribution of the attributes' stats.
- run_simulation.slurm: slurm project to be passed to the Great Lakes cluster to achieve large-scale simulations.
- driver.py: used to convert the file paths to relative for the HPC.
- simulation_result.ipynb: used to interpret and visualize the simulations results.
  
The simulation results are too large to upload to the repo, they can be downloaded through this google drive link: https://drive.google.com/drive/folders/1RnnIjZlymCDaMQ__TapyrfLtGKgQDU4h?usp=sharing

In the simulation, each player fights each enemy for 100 rounds by running the simulation 10 times. As a result, 42,000,000 battles are simulated with the help of the high-performance computing cluster.

The pdf file concludes the final analysis and results.
