def choose_chart(dataframe):

    cols = dataframe.columns

    if len(cols) < 2:
        return "table"

    if "date" in cols[0].lower():
        return "line"

    if dataframe.shape[0] <= 6:
        return "pie"

    return "bar"
