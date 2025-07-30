def extract_features(df):

    metaData_cols = df.iloc[:, 0:9]
    df.drop(columns=df.columns[0:9], axis=1, inplace=True)

    return df, metaData_cols