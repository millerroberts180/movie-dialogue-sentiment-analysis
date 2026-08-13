# Guidance if a predictive model is added

The current project is descriptive and includes no predictive model. If classification or prediction is introduced, the unit of independence is the film, not the scene.

Use `movie_id` as the group in a grouped split:

```python
from sklearn.model_selection import GroupShuffleSplit

splitter = GroupShuffleSplit(n_splits=1, test_size=0.20, random_state=112)
train_idx, test_idx = next(splitter.split(X, y, groups=df["movie_id"]))

X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
```

Fit all learned preprocessing—including TF-IDF vocabulary, feature selection, scaling, imputation, and class balancing—on the training films only. Prefer a scikit-learn `Pipeline`. For cross-validation, use `GroupKFold` or `StratifiedGroupKFold` when class balance permits. Assert that the train and test film-ID sets are disjoint before fitting.
