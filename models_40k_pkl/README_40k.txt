Fake Review Detection Models - 40K Dataset
============================================================

Training Date: 2025-10-26 21:38:24
Total Records: 40,431
Training Set: 32,344
Test Set: 8,087

Model Performance:
------------------------------------------------------------
                    accuracy  precision  recall  f1_score  training_time
LogisticRegression    0.9269     0.9194  0.9360    0.9276           6.09
LinearSVC             0.9267     0.9247  0.9290    0.9269           7.12
RandomForest          0.9001     0.8812  0.9248    0.9025          22.80
MultinomialNB         0.8831     0.8778  0.8902    0.8840           6.00
ComplementNB          0.8831     0.8778  0.8902    0.8840           5.90
BernoulliNB           0.8589     0.8787  0.8328    0.8551           5.09
GradientBoosting      0.8394     0.8230  0.8647    0.8434          93.25
AdaBoost              0.8081     0.7937  0.8326    0.8127          47.71
DecisionTree          0.7616     0.7299  0.8306    0.7770          17.38
KNeighbors            0.5023     0.7317  0.0074    0.0147           5.98

============================================================
Best Model: LogisticRegression (Accuracy: 0.9269)
