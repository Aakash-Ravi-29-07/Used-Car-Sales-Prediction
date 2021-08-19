import pickle
import Sales_Prediction
import numpy as np

model = None
brands = None
columns = None
df = Sales_Prediction.final_df
columns = df.columns
brands = list(columns[:-4])
brands.append("Maruti")
seats = list(df["seats"].unique())
year = list(df["year"].unique())

with open('used_car_sales_prediction_model.pickle', 'rb') as f:
    model = pickle.load(f)


def predictSalesPrice(brand, year, engine, seats):
    index = -1
    if brand in brands:
        index = brands.index(brand)
    input = np.zeros(len(columns)-1)
    input[-3] = year
    input[-2] = engine
    input[-1] = seats
    if(index >= 0):
        input[index] = 1
    # input = scaleData(input)
    return model.predict([input])[0]
