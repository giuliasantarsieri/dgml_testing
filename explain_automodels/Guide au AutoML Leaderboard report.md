# Guide au AutoML Leaderboard report

Cette page a pour but de vous aider à mieux comprendre les résultats du AutoML Leaderboard report qui est fourni pour chaque dataset.

Cliquez ici pour voir le guide officiel de la librairie `mljar-supervised` à l'aide de laquelle nous avons généré ces rapport: https://supervised.mljar.com/

## Page principale

Dans la page principale du report, un tableau récapitule les modèles entraînés sur le dataset avec les métriques associées, ainsi qu'un graphique :

(mettre image de la première page)




Les algorithmes sont entraînés en partageant le dataset en base d'apprentissage et de test avec une proportion de 75% / 25%.

### A quoi correspondent ces algorithmes?

1. `Baseline`: correspond au [`DummyClassifier` de scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyClassifier.html) pour la classification et au [`DummyRegressor` de scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyRegressor.html) pour la régression
2. `DecisionTree`: utilise le [`DecisionTreeClassifier`](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html) pour la Classification et le [`DecisionTreeRegressor`](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeRegressor.html) pour la regression
3. `Linear`: [`LogisticRegression` de scikit-learn](https://scikit-learn.org/0.16/modules/generated/sklearn.linear_model.LogisticRegression.html) pour la Classification et  [`LinearRegression` de scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html) pour la Régression
4. `Random Forest`
5. `Extra Trees`
6. `Xgboost`
7. `NeuralNetwork`
8. `Ensemble`

