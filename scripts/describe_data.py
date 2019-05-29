# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from scripts.timeit import timeit

@timeit
def describe_data(df):
    # description of the data set
    print("---------------5 first lines--------------")
    print(df.head())
    print("---------------info--------------")
    print(df.info())
    print("---------------Statistics--------------")
    print(df.describe())
    print("---------------Graph--------------")
    ax= df.ask_AUD.plot(legend=True,color='b')
    df.ask_NZD.plot(ax=ax, legend=True,color='r')
    df.bid_AUD.plot(ax=ax, legend=True,color='g')
    df.bid_NZD.plot(ax=ax, legend=True,color='k')
    plt.legend(['AUD ask','NZD ask', 'AUD bid', 'NZD bid'])
    plt.ylabel('(USD)')
    plt.xlabel('Time')
    plt.title('The evolution of the closing price of AUD & NZD vs USD')
    plt.show()