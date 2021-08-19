import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.svm import SVR
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
import pickle


def processData(data):
    df = data[data["year"] > 2010]

    kms = df.km_driven
    new_kms = []
    for km in kms:
        temp = km.split(' ')
        temp = temp[0].split(',')
        s = ''
        for t in temp:
            s += t
        new_kms.append(int(s))
    df.km_driven = new_kms

    most_used_cars = df[df["km_driven"] >= 120000]

    df1 = df[df["km_driven"] < 120000]

    car_names = df1["full_name"]
    brands = []
    for car in car_names:
        brands.append(car.split(' ')[0])
    df1["brands"] = brands

    df2 = df1.dropna(how="any")

    seats = df2.seats
    new_seats = []
    for seat in seats:
        temp = seat.split('s')
        new_seats.append(int(temp[1]))
    df2.seats = new_seats

    engines = df2.engine
    new_engines = []
    for engine in engines:
        temp = engine.split('e')
        temp = temp[1].split(' ')
        new_engines.append(int(temp[0]))
    df2.engine = new_engines

    mileage = df2.mileage
    new_mileage = []
    for mil in mileage:
        temp = mil.split('e')
        temp = temp[2].split(' ')
        new_mileage.append(float(temp[0]))
    df2.mileage = new_mileage

    df3 = df2[df2["km_driven"] > 10000]

    prices = df3.selling_price
    new_prices = []
    for price in prices:
        temp = price.split(' ')
        temp = temp[0].split(',')
        if (len(temp) > 1):
            new_prices.append(float(temp[0]) * 0.01)
        else:
            new_prices.append(float(temp[0]))
    df3.selling_price = new_prices

    df4 = df3[(df3["selling_price"] >= 1)]
    df5 = df4[df4["selling_price"] <= 80]

    dummies = pd.get_dummies(df5["brands"])
    df5 = pd.concat([dummies, df5.drop("brands", axis=1)], axis=1)

    final_df = df5.drop(
        ["full_name", "seller_type", "owner_type", "fuel_type", "transmission_type", "mileage", "max_power", "Maruti", "km_driven"],
        axis=1)

    return final_df


def scaleData(final_df):
    scaler = MinMaxScaler()
    X = final_df.drop(["selling_price"], axis = 1)
    y = final_df["selling_price"]
    X = scaler.fit_transform(X)
    return X, y


def getBestModel(X, y, models):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
    model_details = []
    for model_name, config in models.items():
        gs = GridSearchCV(config["model"], config["params"], cv = 5, return_train_score=False)
        gs.fit(X, y)
        model_details.append({
            'name' : model_name,
            'best score': gs.best_score_,
            'best_params': gs.best_params_
        })

    print(model_details)



def getModels():
    models = {
        'linear_regression' : {
            'model' : LinearRegression(),
            'params' : {
                'normalize' : [True, False]
            }
        },
        'lasso': {
            'model': Lasso(),
            'params': {
                'alpha': [1,2]
            }
        },
        'Ridge': {
            'model': Ridge(),
            'params': {
                'alpha': [1.2]
            }
        },
        'Random_forest': {
            'model': RandomForestRegressor(),
            'params': {
                'n_estimators': [100,200,300],
                'max_depth': [10,20,30]
            }
        }
    }

    return models;


def createModel(X, y):
    model = RandomForestRegressor(max_depth=20, n_estimators=300)
    model.fit(X, y);
    return model

def exportModel(model):
    with open('used_car_sales_prediction_model.pickle', 'wb') as f:
        pickle.dump(model, f)

data = pd.read_csv("cardekho_updated.csv")
full_price = data.new_price
data.drop("new_price", axis=1, inplace=True)

final_df = processData(data)
# X, y = scaleData(final_df)
# models = getModels()
X = final_df.drop("selling_price", axis = 1)
y = final_df["selling_price"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
final_model = createModel(X_train, y_train)
exportModel(final_model)



