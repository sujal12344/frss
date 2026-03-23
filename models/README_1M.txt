Fake Review Detection Models - 1M Dataset
=============================================================================================

Training Date: 2026-01-28 11:33:25
Total Records: 999,996
Training Set: 799,996
Test Set: 200,000

Model Performance:
--------------------------------------------------------------------------------------------
                              accuracy    precision   recall     f1_score      training_time
LogisticRegression             0.9285       0.9291    0.9294      0.9292           190.83
RidgeClassifier                0.9283       0.9281    0.9301      0.9291           175.41
LinearSVC                      0.9282       0.9288    0.9290      0.9289           230.01
PassiveAggressiveClassifier    0.9181       0.9174    0.9205      0.9190           159.13
Perceptron                     0.9017       0.9040    0.9010      0.9025           153.12
RandomForest                   0.9001       0.8812    0.9248      0.9025           122.80
MultinomialNB                  0.8911       0.8961    0.8871      0.8916           128.19
ComplementNB                   0.8910       0.8979    0.8846      0.8912           161.63
SGDClassifier                  0.8871       0.8896    0.8863      0.8879           158.65
BernoulliNB                    0.8802       0.8736    0.8916      0.8825           154.82

=============================================================================================
Best Model: LogisticRegression (Accuracy: 0.9285)

Memory Usage:
Final: 5759.02 MB
