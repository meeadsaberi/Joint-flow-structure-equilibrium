# Joint Flow–Structure Equilibrium under Ecological Ceilings and Social Floors

This repository contains the reproducibility code accompanying the working paper:

> **Urban Transportation Economics Under Planetary Boundaries**  
> Meead Saberi  
> Working paper, UNSW Sydney, 2026.

The paper develops a transportation network framework that distinguishes three related questions:

1. **Structural feasibility**: Whether at least one allocation can satisfy an ecological ceiling and social floors at a given structural state.
2. **Equilibrium admissibility**: Whether the unregulated network equilibrium itself satisfies those boundaries.
3. **Endogenous structural adjustment**: Where a slower-moving structural state, such as fleet electrification, settles when it responds to network outcomes.

The Sioux Falls application is an illustrative computational example used to reproduce the numerical results in the paper. The ecological ceiling is represented by a system tailpipe emissions limit and the social floor by minimum accessibility requirements. They provide a simplified transport system representation of the safe and just extension of the planetary boundaries framework, with an upper ecological ceiling and a lower social floor.

## Repository contents

- `SiouxFalls_implementation_of_the_joint_flow_structure_equilibrium_problem_v2.ipynb` — self-contained reproducibility notebook for the revised Sioux Falls application.
- `LICENSE` — MIT License.
- `CITATION.cff` — citation metadata for the repository.
- `requirements.txt` — Python dependencies.

The notebook writes the verified model implementation to temporary local Python modules during execution so that the repository can remain compact while the numerical workflow stays readable.

## What the revised notebook implements

The current implementation matches the revised paper and includes:

- the standard Sioux Falls network with 24 nodes, 76 directed links, 528 OD pairs, and 360,600 baseline trips;
- BPR congestion functions;
- pseudo-lengths constructed from free-flow travel times to maintain consistency between time, speed, operating cost, and emissions;
- two origin-based user groups, peripheral and central;
- four commodities defined by user class and vehicle technology, ICE and EV;
- heterogeneous values of time and vehicle operating costs;
- fixed and elastic OD demand;
- speed-dependent ICE tailpipe emissions;
- group-specific accessibility floors;
- an endogenous EV-share structural response;
- equilibrium-admissibility thresholds `s_E`;
- stationary structural states `s_star`;
- use-stage emissions pricing with fixed and endogenous structure;
- robustness and sensitivity calculations used in the paper.

The network assignment is solved using a potential-based Frank–Wolfe formulation where applicable, with direct equilibrium checks for priced cases. Scalar thresholds and stationary structural states are located using one-dimensional root searches.

## Reproducing the paper results

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the notebook

Open `SiouxFalls_implementation_of_the_joint_flow_structure_equilibrium_problem_v2.ipynb` in JupyterLab, Jupyter Notebook, VS Code, or Google Colab and run all cells from top to bottom.

The notebook automatically downloads the standard Sioux Falls network, trips, and node files from the Transportation Networks repository maintained by Hillel Bar-Gera and collaborators.

### 3. Outputs

The notebook reproduces the main numerical objects reported in Section 6 of the paper, including:

- fixed- versus elastic-demand equilibrium-admissibility thresholds and stationary EV shares;
- the response of `s_E` and `s_star` to tighter emissions ceilings;
- emissions and accessibility along the structural axis;
- the reduced structural residual `R(s)`;
- pricing results with fixed structure;
- pricing results when the same use-stage price also affects vehicle choice;
- robustness calculations for demand elasticity and structural-response assumptions.

Generated tables and figures are written to the local `results/` directory when the notebook is run.

The notebook also contains numerical assertions against the manuscript values. These checks are intentionally tolerant only to small numerical and rounding differences so that implementation drift is visible.

## Interpretation of the example

The Sioux Falls application is a transparent benchmark illustration rather than an empirical model of Sioux Falls. In particular, the benchmark `length` field does not provide independent geographical link lengths, so pseudo-lengths are constructed from free-flow travel times. Results should therefore be interpreted as network-level computational illustrations of the framework rather than calibrated forecasts.

The emissions ceiling and accessibility floors are illustrative transport-system bounds. The paper uses the planetary-boundaries framework as an organizing principle for ecological limits together with its safe-and-just extension incorporating social foundations; the numerical thresholds are not presented as formally downscaled planetary boundaries.

## Data

The Sioux Falls data are obtained from the Transportation Networks repository:

https://github.com/bstabler/TransportationNetworks

The notebook downloads the required files directly when they are not already available locally.

## Citation

If you use this code or the framework, please cite the accompanying working paper:

> Saberi, M. (2026). *Urban Transportation Economics Under Planetary Boundaries*. Working paper, UNSW Sydney.

BibTeX:

```bibtex
@unpublished{Saberi2026PlanetaryBoundaries,
  author = {Saberi, Meead},
  title  = {Urban Transportation Economics Under Planetary Boundaries},
  year   = {2026},
  note   = {Working paper, UNSW Sydney}
}
```

## Status

This repository corresponds to the revised working-paper version of the model and supersedes the earlier Sioux Falls implementation previously hosted here.

## License

MIT License. See `LICENSE`.

## Acknowledgement

This research is supported by an Australian Research Council Future Fellowship (FT250100584).

## Contact

Meead Saberi  
University of New South Wales (UNSW Sydney)  
meead.saberi@unsw.edu.au
