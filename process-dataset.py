import pandas as pd

crop = 'Banana'

train_dataset = pd.DataFrame(columns=['State', 'District', 'Year', 'Season', 'Produce', 'Temperature', 'Rainfall'])
test_dataset = pd.DataFrame(columns=['State', 'District', 'Year', 'Season', 'Produce', 'Temperature', 'Rainfall'])

df = pd.read_csv('dataset.csv')
temperature_df = pd.read_csv('temperature.csv', skiprows=1)
rainfall_df = pd.read_csv('rainfall-processed.csv')

# get unique states and years
state_list = sorted(df['State_Name'].unique())
year_list = sorted(df['Crop_Year'].unique())

df['State_Name'] = df['State_Name'].str.strip()
df['Season'] = df['Season'].str.strip()
df['Crop'] = df['Crop'].str.strip()
df['District_Name'] = df['District_Name'].str.strip()

# print("Rainfall Years: %", sorted(rainfall_df['YEAR'].unique()))

# print("Rainfall districts: ", sorted(rainfall_df["DISTRICTS_NAME"].unique()))
# print("Crop districts: ", sorted(df["District_Name"].unique()))

# print("Rainfall states: ", sorted(rainfall_df["INDIAN_STATES_NAME"].unique()))
# print("Crop states: ", sorted(df["State_Name"].unique()))

# print("Rainfall districts Length: ", len(rainfall_df["DISTRICTS_NAME"].unique()))
# print("Crop districts Length: ", len(df["District_Name"].unique()))

season_list = ["Kharif", "Rabi", "Whole Year", "Summer", "Winter"]
year_list = [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015]
district_list = df["District_Name"].unique()

# ignore states because temperature not found
ignore_state_list = ["Jammu and Kashmir", "Telangana"]

# print(state_list)
# print(sorted(rainfall_df["SUBDIVISION"].unique()))

# temperature_df = temperature_df[
# temperature_df.columns.drop(list(temperature_df.filter(regex='Administrative unit not ava*')))]

crop_ss = df[df["Crop"] == crop]
last_year = sorted(crop_ss['Crop_Year'].unique())[-1]

for district in district_list:
    district_subset = df[df["District_Name"] == district]
    for year in year_list:
        year_subset = district_subset[district_subset["Crop_Year"] == year]
        if not year_subset.empty:
            for season in season_list:
                season_subset = year_subset[year_subset["Season"] == season]
                if not season_subset.empty:
                    crop_subset = season_subset[season_subset["Crop"] == crop]
                    if not crop_subset.empty:
                        total_production = crop_subset["Production"].sum()
                        total_area = crop_subset["Area"].sum()
                        produce = (total_production / total_area)

                        rainfall_district_df = rainfall_df[
                            rainfall_df["DISTRICTS_NAME"].str.contains(district, case=False)]
                        if rainfall_district_df.empty:
                            continue

                        rainfall_year_df = rainfall_district_df[rainfall_district_df["YEAR"] == year]
                        if rainfall_year_df.empty:
                            continue

                        if season == "Kharif" or season == "Summer":
                            rainfall_kharif = rainfall_year_df[rainfall_year_df['MONTH'].isin([6, 7, 8, 9])]
                            if not rainfall_kharif.empty:
                                rainfall = rainfall_kharif['VALUE'].sum()
                                combined_season = "Kharif"
                            else:
                                continue

                        if season == "Whole Year":
                            if not rainfall_year_df.empty:
                                rainfall = rainfall_year_df['VALUE'].sum()
                                combined_season = "Whole Year"
                            else:
                                continue

                        if season == "Rabi" or season == "Winter":
                            rainfall_rabi = rainfall_year_df[rainfall_year_df['MONTH'].isin([10, 11, 12, 1, 2, 3])]
                            if not rainfall_rabi.empty:
                                rainfall = rainfall_rabi['VALUE'].sum()
                                combined_season = "Rabi"
                            else:
                                continue

                        state = rainfall_district_df['INDIAN_STATES_NAME'].iloc[0]
                        if any(state in ignore_state for ignore_state in ignore_state_list):
                            continue

                        temp_year_df = temperature_df[temperature_df["Year"] == year]
                        temp_state_df = temp_year_df[state]

                        if not rainfall_year_df.empty and not temp_state_df.empty and (not pd.isna(produce)):
                            if year != last_year:
                                train_dataset = train_dataset.append(
                                    {'State': state, 'District': district, 'Year': year, 'Season': combined_season,
                                     'Produce': produce,
                                     'Temperature': temp_state_df.iloc[0],
                                     'Rainfall': rainfall},
                                    ignore_index=True)
                            if year == last_year:
                                test_dataset = test_dataset.append(
                                    {'State': state, 'District': district, 'Year': year, 'Season': combined_season,
                                     'Produce': produce,
                                     'Temperature': temp_state_df.iloc[0],
                                     'Rainfall': rainfall},
                                    ignore_index=True)

train_dataset.to_csv("train_" + crop + ".csv", index=False)
test_dataset.to_csv("test_" + crop + ".csv", index=False)
print("Saving " + crop + " datasets.")
