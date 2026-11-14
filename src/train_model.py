"""
Train baseline model and log to MLflow.

Comentários em português; nomes e API em inglês.
"""
from pathlib import Path
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score, accuracy_score
from joblib import dump, load


def train_baseline(train_csv: str, test_csv: str, experiment_name: str = 'baseline'):
    """Treina um modelo baseline e registra no MLflow localmente."""
    Path('models').mkdir(exist_ok=True)
    train = pd.read_csv(train_csv)
    test = pd.read_csv(test_csv)

    target = 'TARGET'
    features = [c for c in train.columns if c not in ['SK_ID_CURR', target]]

    X_train = train[features]
    y_train = train[target]
    X_test = test[features]
    y_test = test[target]

    # selecionar colunas numéricas e categóricas simples
    numeric_cols = X_train.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = [c for c in X_train.columns if c not in numeric_cols]

    numeric_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())])
    categorical_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='constant', fill_value='missing')), ('onehot', OneHotEncoder(handle_unknown='ignore'))])

    preprocessor = ColumnTransformer(transformers=[('num', numeric_transformer, numeric_cols), ('cat', categorical_transformer, categorical_cols)])

    clf = Pipeline(steps=[('preprocessor', preprocessor), ('model', XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42))])

    mlflow.set_experiment(experiment_name)
    with mlflow.start_run():
        clf.fit(X_train, y_train)
        preds = clf.predict_proba(X_test)[:, 1]
        auc = roc_auc_score(y_test, preds)
        acc = accuracy_score(y_test, (preds > 0.5).astype(int))

        mlflow.log_metric('roc_auc', float(auc))
        mlflow.log_metric('accuracy', float(acc))
        # Ao salvar modelos que referenciam tipos não-padrão (ex: xgboost),
        # informar `skops_trusted_types` para evitar erro de tipos não confiáveis.
        trusted = [
            "numpy.dtype",
            "xgboost.core.Booster",
            "xgboost.sklearn.XGBClassifier",
        ]
        mlflow.sklearn.log_model(clf, 'model', skops_trusted_types=trusted)

    # save a local copy for later scoring
    local_model_path = Path('models') / 'baseline.pkl'
    dump(clf, local_model_path)
    print(f'Local model saved to {local_model_path}')

    return {'roc_auc': auc, 'accuracy': acc}


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--train', default='data/train_reference.csv')
    parser.add_argument('--test', default='data/test_reference.csv')
    args = parser.parse_args()
    res = train_baseline(args.train, args.test)
    print('Training results:', res)
