from pathlib import Path as path
import pickle
import pandas as pd

base_path=path.cwd()
file_path=base_path/"model"/"model.pkl"
print(base_path)
print(file_path)

def load_model():
    with open(file_path,"rb") as f:
        data=pickle.load(f)

    return data

def predict_output(user_input:dict):

    model=load_model()
    df=pd.DataFrame([user_input])
    predict_class=model.predict(df)[0]

    return predict_class

