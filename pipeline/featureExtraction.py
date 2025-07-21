def extract_features(df):

    df.drop(columns=df.columns[0], axis=1, inplace=True)
    metaData_cols = df.iloc[:, 0:9]
    df.drop(columns=df.columns[0:9], axis=1, inplace=True)

    return df, metaData_cols