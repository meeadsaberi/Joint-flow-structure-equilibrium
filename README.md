# Joint Flow–Structure Equilibrium Model with Environmental and Social Constraints

This repository contains the code accompanying the paper:

> *Urban Transportation Economics Under Planetary Boundaries*  
> *Meead Saberi*

The project implements a joint flow–structure equilibrium model on the Sioux Falls network, incorporating:
- congestion-dependent travel costs,
- endogenous technology adoption (EV share),
- emissions constraints (ecological ceiling),
- accessibility constraints (social floor).

## Overview

The model integrates:
- **User equilibrium traffic assignment** (two user classes)
- **Endogenous EV adoption dynamics**
- **Environmental feasibility** via emissions constraints
- **Distributional analysis** via accessibility floors

The equilibrium is computed as a fixed point between:
- network flows given EV share, and
- EV share given emissions.

## Requirements

- Python 3.9+
- numpy
- pandas
- matplotlib
- networkx
- scipy

## How to run

The code is organized sequentially following the paper.

### Step-by-step execution

1. **Load data and network**  
   Run Section 6.1
2. **Initialize behavioral + technological model**  
   Run Section 6.2
3. **Solve joint flow–structure equilibrium**  
   Run Section 6.3
4. **Analyze technological change and dynamics**  
   Run Section 6.4
5. **Evaluate accessibility and social floor**  
   Run Section 6.5
6. **Run pricing experiments**  
   Run Section 6.6

The code is designed to run in order (e.g., in a Jupyter notebook or Google Colab).

## Outputs

The model generates:

### CSV files
- sioux_falls_joint_equilibrium_summary.csv  
- sioux_falls_tech_scan.csv  
- sioux_falls_tech_dynamics.csv  
- sioux_falls_social_floor_scan_revised.csv  
- sioux_falls_pricing_social_floor_revised.csv  

### Figures
- Accessibility decay functions  
- Emissions vs speed (U-shaped relationship)  
- Adoption map  
- Congestion and cost functions  
- Network flow visualizations  

## Data

The Sioux Falls network is a standard benchmark dataset widely used in transportation research, obtained from https://github.com/bstabler/transportationnetworks

## Notes

- The model is numerical and does not enforce all theoretical convexity and monotonicity assumptions globally.  
- Results should be interpreted as a computational illustration of the theoretical framework.  

## License

MIT License

## Acknowledgements

This research was supported by an Australian Research Council Future Fellowship (FT250100584).

## Contact

Meead Saberi at the University of New South Wales
Email: meead.saberi@unsw.edu.au
