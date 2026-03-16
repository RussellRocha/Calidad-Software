import numpy as np

def expected_range(df):

    vol = df["close"].pct_change().std()

    last = df["close"].iloc[-1]

    return {
        "min": last * (1 - vol * 2),
        "max": last * (1 + vol * 2)
    }
