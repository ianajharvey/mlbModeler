def extract_features(df):

    df.drop(columns=df.columns[0], axis=1, inplace=True)
    metaData_cols = df.columns[0:9]
    df.drop(columns=metaData_cols, axis=1, inplace=True)

    return df