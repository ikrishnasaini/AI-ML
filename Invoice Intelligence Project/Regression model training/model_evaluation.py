from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def train_linear_regression(x_train, y_train):
    model = LinearRegression()
    model.fit(x_train, y_train)
    return model


def train_decision_tree(x_train, y_train, max_depth=5):
    model = DecisionTreeRegressor(max_depth=max_depth,random_state=42)
    model.fit(x_train, y_train)
    return model


def train_random_forest(x_train, y_train, n_estimators=100, max_depth=5):
    model = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
    model.fit(x_train, y_train)
    return model

def evaluate_model(model, x_test, y_test,model_name:str)-> dict:
    '''
    Evaluate the model and return metrics.
    '''
    preds = model.predict(x_test)
    mae = mean_absolute_error(y_test, preds)
    mse = mean_squared_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    print(f"{model_name} - Mean Absolute Error: {mae}, Mean Squared Error: {mse}, R^2 Score: {r2}")
    return {"model": model_name, "mae": mae, "mse": mse, "r2": r2}