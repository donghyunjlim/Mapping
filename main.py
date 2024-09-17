import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd


def load_in_data(shp_file_name, csv_file_name):
    """
    Takes two parameters(census dataset and food access
    dataset) and return a merged dataset of the parameters
    which is a GeoDataFrame.
    """
    shp_file = gpd.read_file(shp_file_name)
    csv_file = pd.read_csv(csv_file_name)
    merged_dataset = shp_file.merge(
        csv_file, left_on="CTIDFP00", right_on="CensusTract", how="left")
    return merged_dataset


def percentage_food_data(state_data):
    """
    Takes the merged dataset and returns the percentage of census tracts
    in Washington.
    """
    return float(
        state_data[
            "CensusTract"].count() / state_data["CTIDFP00"].count()) * 100


def plot_map(state_data):
    """
    Takes the merged dataset and plots the shape of all census tracts
    in Washington.
    """
    state_data.plot()
    plt.title("Washington State")
    plt.savefig("map.png")


def plot_population_map(state_data):
    """
    Takes the merged dataset and plots the shapes of all the census
    tracts in Washington where each census tract is colored according
    to population.
    """
    fig, ax = plt.subplots(1)
    state_data.plot(color="#EEEEEE", ax=ax)
    state_data.plot(column="POP2010", legend=True, ax=ax)
    plt.title("Washington Census Tract Populations")
    plt.savefig("population_map.png")


def plot_population_county_map(state_data):
    """
    Takes the merged dataset and plots the shape of all the
    census tracts in Washington where each county is colored
    according to population.
    """
    county = state_data[["POP2010", "County", "geometry"]]
    county = state_data.dissolve(by="County", aggfunc="sum")
    fig, ax = plt.subplots(1)
    state_data.plot(color="#EEEEEE", ax=ax)
    county.plot(ax=ax, column="POP2010", legend=True)
    plt.title("Washington County Populations")
    plt.savefig("county_population_map.png")


def plot_food_access_by_county(state_data):
    """
    Takes the merged dataset and create 4 plots on the same figure showing
    information about food access across different income level.
    """
    ratio_data = state_data[
        ["County", "geometry", "POP2010", "lapophalf", "lapop10",
            "lalowihalf", "lalowi10"]]
    ratio_data = ratio_data.dissolve(by="County", aggfunc="sum")
    # computing the ratio of people in each category
    ratio_data[
        "lapophalf_ratio"] = ratio_data["lapophalf"] / ratio_data["POP2010"]
    ratio_data[
        "lapop10_ratio"] = ratio_data["lapop10"] / ratio_data["POP2010"]
    ratio_data[
        "lalowihalf_ratio"] = ratio_data["lalowihalf"] / ratio_data["POP2010"]
    ratio_data[
        "lalowi10_ratio"] = ratio_data["lalowi10"] / ratio_data["POP2010"]

    fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(2, 2, figsize=(20, 10))
    state_data.plot(color="#EEEEEE", ax=ax1)
    ratio_data.plot(
        column="lapophalf_ratio", legend=True, ax=ax1, vmin=0, vmax=1)
    ax1.set_title("Low Access: Half")
    state_data.plot(color="#EEEEEE", ax=ax3)
    ratio_data.plot(
        column="lapop10_ratio", legend=True, ax=ax3, vmin=0, vmax=1)
    ax2.set_title("Low Access + Low Income: Half")
    state_data.plot(color="#EEEEEE", ax=ax2)
    ratio_data.plot(
        column="lalowihalf_ratio", legend=True, ax=ax2, vmin=0, vmax=1)
    ax3.set_title("Low Access: 10")
    state_data.plot(color="#EEEEEE", ax=ax4)
    ratio_data.plot(
        column="lalowi10_ratio", legend=True, ax=ax4, vmin=0, vmax=1)
    ax4.set_title("Low Access + Low Income: 10")
    plt.savefig("county_food_access.png")


def plot_low_access_tracts(state_data):
    """
    Takes the merged dataset and plots all census tracts that are considered
    "low access". The classification of low access differs depending on the
    location of the census tract (rural or urban), therefore a computation
    of measuring "low access" is included in this function.
    """
    urban_area = (state_data["Urban"] == 1) & (
        (state_data["lapophalf"] >= 500) | (
            state_data["lapophalf"] / state_data["POP2010"] >= 0.33))
    rural_area = (state_data["Rural"] == 1) & (
        (state_data["lapop10"] >= 500) | (
            state_data["lapop10"] / state_data["POP2010"] >= 0.33))
    # column that contains a null if the row satisfies both conditions
    state_data["low_access"] = urban_area | rural_area
    # dropping NA values
    food_access = state_data[state_data["POP2010"].notnull()]
    low_access = food_access[food_access["low_access"]]

    fig, ax = plt.subplots(1)
    state_data.plot(color="#EEEEEE", ax=ax)
    food_access.plot(color="#AAAAAA", ax=ax)
    low_access.plot(ax=ax)
    plt.title("Low Access Census Tracts")
    plt.savefig("low_access.png")


def main():
    state_data = load_in_data(
        '/course/food_access/tl_2010_53_tract00/tl_2010_53_tract00.shp',
        '/course/food_access/food_access.csv'
    )
    print(percentage_food_data(state_data))
    plot_map(state_data)
    plot_population_map(state_data)
    plot_population_county_map(state_data)
    plot_food_access_by_county(state_data)
    plot_low_access_tracts(state_data)


if __name__ == '__main__':
    main()