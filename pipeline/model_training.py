from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from xgboost import XGBClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import VotingClassifier


def train_models(df):

    results = df["home_team_wins"]
    df.drop(columns=df.columns[44], axis=1, inplace=True)

    # Assume X and y already defined
    X_train, X_test, y_train, y_test = train_test_split(df, results, stratify=results, random_state=3)

    # Logistic Regression + PCA pipeline
    pipe = Pipeline([
        ('scaler', StandardScaler()),
        ('pca', PCA(n_components=30)),
        ('logreg', LogisticRegression(max_iter=1000))
    ])

    # Define parameters to search
    param_grid = {
        'pca__n_components': [10, 20,30,40],
        'logreg__C': [0.01, 0.1, 1, 10],  # Inverse of regularization strength
        'logreg__penalty': ['l2'],        # 'l1' requires solver='liblinear'
    }

    grid = GridSearchCV(pipe, param_grid, cv=5, scoring='accuracy')
    grid.fit(X_train, y_train)
    log_reg_model = grid.best_estimator_



    xgb_model = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=3)

    param_dist_xgb = {
        'n_estimators': [100, 200, 300],
        'max_depth': [3, 4, 5, 6],
        'learning_rate': [0.01, 0.05, 0.1, 0.2],
        'subsample': [0.7, 0.8, 0.9, 1],
        'colsample_bytree': [0.7, 0.8, 0.9, 1]
    }

    xgb_search = RandomizedSearchCV(
        xgb_model,
        param_distributions=param_dist_xgb,
        n_iter=50,
        scoring='accuracy',
        cv=5,
        random_state=3,
        n_jobs=-1
    )

    xgb_search.fit(X_train, y_train)
    xgb_model = xgb_search.best_estimator_


    # Define the base model
    rf_model = RandomForestClassifier(random_state=3)

    # Hyperparameter grid
    param_dist_rf = {
        'n_estimators': [100, 200, 300],
        'max_depth': [4, 6, 8, None],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'max_features': ['sqrt', 'log2', None],
        'bootstrap': [True, False]
    }

    # Randomized search
    rf_search = RandomizedSearchCV(
        rf_model,
        param_distributions=param_dist_rf,
        n_iter=30,
        cv=5,
        scoring='accuracy',
        random_state=42,
        n_jobs=-1
    )

    # Fit the model
    rf_search.fit(X_train, y_train)
    rf_model = rf_search.best_estimator_


    voting_clf = VotingClassifier(
        estimators=[
            ('logreg', grid.best_estimator_),
            ('xgb', xgb_search.best_estimator_),
            ('rf', rf_search.best_estimator_)
        ],
        voting='soft'
    )

    param_grid = {
        'weights': [
            [1, 1, 1],
            [2, 1, 1],
            [3, 1, 1],
            [1, 2, 1],
            [1, 3, 1],
            [1, 1, 2],
            [1, 1, 3],
            [2, 2, 1],
            [1, 3, 1],
        ]
    }

    grid_voting = GridSearchCV(
        voting_clf,
        param_grid,
        scoring='accuracy',
        cv=5,
        n_jobs=-1
    )

    grid_voting.fit(X_train, y_train)
    ensemble_model = grid_voting.best_estimator_

    return log_reg_model, xgb_model, rf_model, ensemble_model