# Script to aggregate the features and save them ina  new csv

import pandas as pd

df = pd.read_csv("movies_with_feats.csv", index_col=0)

df["FK_read_level_mean_char"] = (df["FK_read_level_char_1"] + df["FK_read_level_char_2"] + 
                                 df["FK_read_level_char_3"] + df["FK_read_level_char_4"] + 
                                 df["FK_read_level_char_5"])/5
del df["FK_read_level_char_1"], df["FK_read_level_char_2"], df["FK_read_level_char_3"]
del df["FK_read_level_char_4"], df["FK_read_level_char_5"]


def get_stdvs_above_mean(feat_general_name):
    n_all = df[feat_general_name + "1"]
    for i in range(2, 6):
        n_all += df[feat_general_name + str(i)]
        del df[feat_general_name + str(i)]
    n_all_mean = n_all.mean()
    n_all_std = n_all.std()
    df["stdvs_" + feat_general_name[:-5] + "above_mean"] = (n_all - n_all_mean)/n_all_std
    del df[feat_general_name + "1"]


get_stdvs_above_mean("n_stop_words_char_")
get_stdvs_above_mean("n_curse_words_char_")
get_stdvs_above_mean("n_mentions_others_char_")

df.to_csv("movies_with_agg_feats.csv")