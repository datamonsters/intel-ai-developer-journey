import os
import shutil
import zipfile
import numpy as np


def prepare_data(data_path="../data", valid_size=0.2, seed=21, FORCED_DATA_REWRITE=False):

    train_path = os.path.join(data_path, "train")
    valid_path = os.path.join(data_path, "valid")

    if FORCED_DATA_REWRITE:
        if os.path.exists(data_path):
            shutil.rmtree(data_path)

    if not os.path.exists(data_path):
        
        if not os.path.exists("Dataset 50-50.zip"):
            os.system("wget https://www.dropbox.com/s/gweehtotah778py/Dataset%2050-50.zip")
        
        zip_ref = zipfile.ZipFile("Dataset 50-50.zip", "r")
        zip_ref.extractall("data_temp")
        zip_ref.close()
        
        os.rename("data_temp/dataset 50:50", data_path)
        shutil.rmtree("data_temp")
        
        os.mkdir(train_path)
        os.mkdir(valid_path)

        for category in ["Negative", "Positive"]:
            train_emo_path = os.path.join(train_path, category)
            valid_emo_path = os.path.join(valid_path, category)
            os.mkdir(train_emo_path)
            os.mkdir(valid_emo_path)

            categoty_list = np.array(os.listdir(os.path.join(data_path, category)))
            np.random.seed(seed)
            np.random.shuffle(categoty_list)
            
            train_list = categoty_list[int(len(categoty_list) * valid_size):]
            valid_list = categoty_list[:int(len(categoty_list) * valid_size)]
            
            for filename in train_list:
                os.rename(os.path.join(data_path, category, filename), 
                          os.path.join(train_emo_path, filename.replace(" ", "")))
                
            for filename in valid_list:
                os.rename(os.path.join(data_path, category, filename), 
                          os.path.join(valid_emo_path, filename.replace(" ", "")))
                
            shutil.rmtree(os.path.join(data_path, category))

    return train_path, valid_path
