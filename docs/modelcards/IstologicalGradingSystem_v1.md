
# Istological Grading System - v1

## Description
Istological Grading System is designed to tackle a medical classification task with the goal of diagnosing breast cancer. This model uses a set of features extracted from medical images and clinical data, such as the size and shape of the tumor mass, to determine whether a tumor is malignant or benign.

The classification is based on a series of quantitative measurements, which are processed by the model to accurately predict the nature of the tumor. The features analyzed include parameters such as the mass size, its shape, density, and other relevant morphological properties.

## General Information 
- Developed by: donatooooooo
- Model Type: RandomForestClassifier
- sklearn version: 1.5.2
- Python version: 3.12.7

## How to use
```
trainer = model_name(target value, [drop column], dataset)
trainer.findBestParams()
print(trainer.getParams())
trainer.run()
print(trainer.getMetrics())
```

## Training Details
- Dataset: Breast_Cancer_Wisconsin.csv
- Parameters: 
    - `criterion` entropy
    - `max_depth` None
    - `min_samples_leaf` 2
    - `min_samples_split` 5
    - `n_estimators` 50
    
- Training started at: 18:27:42 2024-11-21
- Training ended at: 18:31:48 2024-11-21

## Evaluation
- `Accuracy` 0.9649122807017544
- `Precision` 0.9649122807017544
- `Recall` 0.9649122807017544
- `F1_micro score` 0.9649122807017544
- `F1_macro score` 0.9623015873015872

## Limitations
1. **Dependence on Data Quality**: The accuracy of the IGS model heavily relies on the quality of the medical images and clinical data. Any inaccuracies or missing data in the input features (such as tumor size, shape, or density) can lead to incorrect predictions.
2. **Limited Generalization to rare cases**: The model may not generalize well rare cases that differ significantly from the training dataset. This can affect its performance in diagnosing atypical tumor types or unusual clinical presentations.
3. **Potential Overfitting to Specific Features**: The model may overfit to certain features that are highly represented in the training data, such as common tumor characteristics. This could result in reduced accuracy when encountering tumors with different or less common attributes.
