import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
# all function use was guided by the package library
# cited in report

# get the final dataframe
df = pd.read_csv("../data/processed/FINAL_DATA.csv")

########## Part 1: General Info Graph ##########
def plot_EV_rate_info():
    """
    This function will plot an interactive choropleth map of EV adoption rates 
    for each state.
    choropleth map visualizes state-level EV adoption rates using a color scale,
    which could explore geographic patterns in EV usage
    additional ranking metrics are displayed when hovering over each state
    """
    # using plotly express to create an interactive choropleth map
    # function use was guided by plotly library and 
    # refering https://towardsdatascience.com/simplest-way-of-creating-a-choropleth-map-by-u-s-states-in-python-f359ada7735e/
    fig = px.choropleth(
        # dataframe for the figure
        df,
        # set up the map graphic
        locations="Abbr",
        locationmode="USA-states",
        scope="usa",
        # color refers to EV adoption rate
        color="EV_rate",
        # color was selected on plotly library
        color_continuous_scale="Blues",
        # set up interactive use
        # when hover over each state following data will be shown
        hover_name="State",
        hover_data=["EV_rate_rank", "Station_rank",
                    "gas_price_rank", "Income_rank"],
        # figure title
        title="EV Adoption Rate by State"
    )
    # save the figure as html for interaction
    fig.write_html("../results/plots/EV_adoption_rate_info.html")
    # save the figure as PNG for github use
    fig.write_image("../results/plots/EV_adoption_rate_info.png")

########## Part 2: Linear Regression graphs ##########
def plot_non_age_factor():
    """
    This function will plot with 4 subplots
    each subplot is representing a non-age factor linear regression with
    EV adoption rate. The four factors are: EV charging station counts, income,
    gas price and higher education level rate
    """
    # set whole figure basics
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # upper left: EV vs Stations
    sns.regplot(data=df, x="Stations", y="EV_rate", ax=axes[0, 0])
    # set the subplot's location in figure and subplot title
    axes[0, 0].set_title("EV vs Stations")

    # upper right: EV vs Income
    sns.regplot(data=df, x="Median_Income", y="EV_rate", ax=axes[0, 1])
    # set the subplot's location in figure and subplot title
    axes[0, 1].set_title("EV vs Income")

    # bottom left: EV vs Gas Price
    sns.regplot(data=df, x="gas_price", y="EV_rate", ax=axes[1, 0])
    # set the subplot's location in figure and subplot title
    axes[1, 0].set_title("EV vs Gas Price")

    # bottom right: EV vs Higher Education Level
    sns.regplot(data=df, x="High_Edu_Level_Percent", y="EV_rate", ax=axes[1, 1])
    # set the subplot's location in figure and subplot title
    axes[1, 1].set_title("EV vs Higher Education Level")

    # set the title for whole figure
    fig.suptitle("EV Adoption Rate VS Non-age Factors")
    # save the subplots into results
    plt.savefig("../results/plots/Non-age_factors.png")
    plt.close()

def plot_age_factor():
    """
    This function will plot with 4 subplots
    each subplot is representing an age factor linear regression with
    EV adoption rate. The four factors are: teen_rate, young_rate,
    middle_rate, and elderly rate
    """
    # set whole figure basics
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # upper left: EV vs Teen Percent in Population
    sns.regplot(data=df, x="Teen_Percent", y="EV_rate", ax=axes[0, 0])
    # set the subplot's location in figure and subplot title
    axes[0, 0].set_title("EV vs Teen Percent in Population")

    # bottom left: EV vs Young Percent in Population
    sns.regplot(data=df, x="Young_Percent", y="EV_rate", ax=axes[0, 1])
    # set the subplot's location in figure and subplot title
    axes[0, 1].set_title("EV vs Young Percent in Population")

    # upper right: EV vs Middle Percent in Population
    sns.regplot(data=df, x="Middle_Percent", y="EV_rate", ax=axes[1, 0])
    axes[1, 0].set_title("EV vs Middle Percent in Population")

    # bottom right: EV vs Elderly Percent in Population
    sns.regplot(data=df, x="Elderly_Percent", y="EV_rate", ax=axes[1, 1])
    # set the subplot's location in figure and subplot title
    axes[1, 1].set_title("EV vs Elderly Percent in Population")

    # set the title for whole figure
    fig.suptitle("EV Adoption Rate VS Age Factors")
    # save the subplots into results
    plt.savefig("../results/plots/Age_factors.png")
    plt.close()

########## Part 3: Distribution Graph ##########
def plot_distribution():
    """
    This function will plot a distribution histogram plot of EV adoption rate
    distribution is used to shows which EV adoption levels do states have
    """
    # set figure size
    plt.figure(figsize=(12,6))
    # plot a histogram, refering sns.histplot library
    # set bins number for more detailed graph
    # add a kernel density estimate to smooth the histogram
    sns.histplot(df["EV_rate"], bins=15, kde=True)
    # plot title
    plt.title("Distribution of EV Adoption Rate")
    # x-label
    plt.xlabel("EV Adoption Rate")
    # save the histogram into results
    plt.savefig("../results/plots/EV_rate_distribution.png")
    plt.close()

########## Part 4: Statistical Results Table ##########
def stats_table_df():
    """
    This function will return the dataframe for stats table
    By using stats.pearsonr to calculate the r and p value
    calculator each factor's r-value and p-value
    """
    # store all the factor col name that will be used
    factors = ["Stations", "Median_Income", "gas_price",
        "High_Edu_Level_Percent", "Teen_Percent",
        "Young_Percent", "Middle_Percent", "Elderly_Percent"]

    # create an empty list to store the final calculation result
    results = []
    # go through factor list that calculate the corresponding r and p
    for col in factors:
        # use the stats function from scipy to make a calcultation
        r_value, p_value = stats.pearsonr(df[col], df["EV_rate"])
        # append the result list with calculated results
        # name of column is the factors
        results.append({"Factor": col,
            # r_value is the correlation calculated, and round in 3 decimals
            "Correlation (r-value)": round(r_value, 3),
            # p-value, since some p-value is relative small, no rounding is used
            "p-value": p_value})
    # convert the list into datarame
    stats_df = pd.DataFrame(results)
    return stats_df

def plot_stats_table():
    """
    This function will plot a table that have all factor's
    r-value and p-value for comparasion by using plotly.graph_objects
    refering plotly library
    """
    # save the dataframe for ploting
    stats_df = stats_table_df()

    # plot the table
    fig = go.Figure(data=[go.Table(
        # header row is the columns's name of the table_df
        header=dict(values=list(stats_df.columns)),
        # table content is each row of the table_df
        cells=dict(values=[stats_df[col] for col in stats_df.columns])
        )])
    # save the plotly figure
    fig.write_image("../results/plots/stats_table.png")

########## Part 5: Function Calling ##########
# geo-graphic plot
plot_EV_rate_info()

# linear regressions
plot_non_age_factor()
plot_age_factor()

# disribution
plot_distribution()

# stats table
plot_stats_table()