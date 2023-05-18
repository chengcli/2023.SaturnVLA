## How to generate Figures
- Figure 1: 
```
./plot_data_contribution_atm.py
```

- Figure 2:
```
# unskip job plot-vla-images-scxukq
./write_workflow.py -i vla_processing.yml
./vla_processing.sh

# unskip job stack-vla-images
./write_workflow.py -i vla_processing.yml
./vla_processing.sh
```

- Figure 3:
```
./plot_saturn_latitude_v2.py
```

- Figure 4:
```
./write_workflow.py -i vla_processing.yml
./vla_processing.sh
```

- Figure S7:
```
./plot_fit_quality.py
```
