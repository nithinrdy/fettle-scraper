# %%
import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L12-v2")


# %%
def encodeSymptomVectors(symptoms):
    return model.encode(str(symptoms)).tolist()


def encodeRarityScore(rarity):
    if rarity is not np.NaN:
        rarityMap = {
            "Very common": 0,
            "Common": 1,
            "Rare": 2,
            "Very rare": 3,
            "Extremely rare": 4,
        }
        return rarityMap[rarity]


encoded_diseases = pd.read_csv("diseases_complete.csv").reset_index()
encoded_diseases["symptomVectors"] = encoded_diseases["symptoms"].apply(encodeSymptomVectors)
encoded_diseases["rarityScore"] = encoded_diseases["rarity"].apply(encodeRarityScore)


# %%
encoded_diseases.dropna(subset=["disease", "primary_description"], inplace=True)

# %%
encoded_diseases.to_csv("diseases__encoded.csv", index=False, )


