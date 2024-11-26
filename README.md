# Machine Learning Model Cards Generator
The following repository contains a project designed to automate the cration of Model Cards, a type of documentation for Machine Learning models. With standardized experiment tracking, the software automates documentation creation by adopting CI practices to get Model Cards up-to-date throughout the model lifecycle. Through the use of MLFlow and GitHub Actions, the system can document models automatically, keeping track of crucial information to ensure transparency, reliability and explainability.

# Project Organization
```

    ├── LICENSE
    ├── Makefile                                        <- Makefile with commands like `make data` or `make train`
    ├── README.md                                       <- The top-level README for developers using this project.
    ├── data                                            <- Data used in this project.
    ├── docs                                            <- Main software for automated model card creation.
    |   ├───ModelCards                                  <- Model Cards generated.
    |   ├───setup                                       <- Files to setup the Model Cards generation.
    |   |       config.yml                              <- File used for setup of generation. 
    |   └───src                      
    |       |   generator.py                            <- Methods for creation of Model Cards.
    |       |   main.py                                 <- Script to start generation.
    |       ├───Templates
    |       |       evaluation_template.md              <- Evaluation template.
    |       |       generalinformation_template.md      <- Information template.
    |       |       modelCard_template.md               <- Model Card deault template.
    |       |       title_template.md                   <- Title template.
    |       |       trainingdetails_template.md         <- Training template.
    |       |       _part.md                            <- read from file template.
    |       └───Utils
    |               exceptions.py                       <- Custom exceptions.
    |               logger.py                           <- Manages the output of the Model Card creation program.
    |               parser.py                           <- Parse config.yml configuration file.
    |               utility.py                          <- Contains support functions for Model Card creation.
    ├── models                                          <- Trained and serialized models, model predictions, or model summaries
    ├── notebooks                                       <- Jupyter notebooks.
    ├── references                                      <- Data dictionaries, manuals, and all other explanatory materials.
    ├── reports                                         <- Generated analysis as HTML, PDF, LaTeX, etc.
    ├── requirements.txt                                <- The requirements file for reproducing the analysis environment.
    ├── setup.py                                        <- makes project pip installable so src can be imported.
    ├── src                                             <- Source code for use in this project.
    │   ├── __init__.py                                 <- Makes src a Python module.
    │   ├── data                                        <- Scripts to download or generate data.
    │   │   └── make_dataset.py
    │   ├── features                                    <- Scripts to turn raw data into features for modeling.
    │   │   └── build_features.py
    │   ├── models                                      <- Scripts to train models and then use trained models to make predictions.
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   └── visualization                               <- Scripts to create exploratory and results oriented visualizations.
    │       └── visualize.py
    └── tox.ini                                         <- tox file with settings for running tox.
```
# User Guide


# Model Card structure
If no configuration is provided, a basic model card template is used. In the absence of certain details, the structure of the model card is adjusted to ensure that all essential sections are included, even if some information is missing.

---
### Model Name - version  
#### General Information  
- Developed by: indicates who developed the model  
- Model Type: specifies the model used  
- Library used for learning: indicates the name and version  
- Python Version: indicates the Python version used  

#### Training Details  
- Dataset: specifies the dataset used  
- Parameters: indicates the parameters used for learning  
   - `List of parameters`  
- Training started at: specifies when the training started  
- Training ended at: specifies when the training ended  

#### Evaluation  
   - `List of metrics`: list of all metrics used to evaluate the model  
---
