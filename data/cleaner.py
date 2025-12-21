import pandas as pd
import os
import numpy as np


def load_data(filepath):
    """
    Load a CSV dataset and print a detailed summary.

    Parameters
    ----------
    filepath : str
        Path to the CSV file to load.

    Returns
    -------
    pandas.DataFrame
        Loaded dataset with no modifications.

    Notes
    -----
    Prints dataset shape, data types, missing value counts,
    and unique value counts for each column.
    """
    print("=" * 60)
    print("STEP 1: LOADING DATA")
    print("=" * 60)

    df = pd.read_csv(filepath)

    print(f"Loaded dataset with {df.shape[0]} rows and {df.shape[1]} columns.\n")

    print("Column Summary:")
    print(f"{'Column':<20} {'Type':<10} {'Missing':<10} {'Unique':<10}")
    print("-" * 60)

    for col in df.columns:
        missing = df[col].isna().sum()
        missing_pct = (missing / len(df)) * 100
        unique = df[col].nunique()

        print(f"{col:<20} {str(df[col].dtype):<10} "
              f"{missing} ({missing_pct:.1f}%) {unique}")

    return df


def handle_missing(df, missing_threshold=0.5, fill_method="median"):
    """
    Handle missing values by dropping sparse columns and imputing others.

    Parameters
    ----------
    df : pandas.DataFrame
        Input dataset.
    missing_threshold : float, default=0.5
        Proportion of missing values above which a column is dropped.
        Example: 0.5 means "drop columns with >50% missing".
    fill_method : {"median", "mean"}, default="median"
        Method to fill numeric missing values.

    Returns
    -------
    pandas.DataFrame
        Dataset with missing values handled.

    Notes
    -----
    - Non-numeric columns are filled with their mode.
    - Columns exceeding the missing threshold are removed.
    """
    print("\n" + "=" * 60)
    print("STEP 2: HANDLING MISSING VALUES")
    print("=" * 60)

    missing_counts = df.isna().sum()

    to_drop = missing_counts[missing_counts / len(df) > missing_threshold].index

    if len(to_drop) > 0:
        print("Dropping columns with too many missing values:")
        for col in to_drop:
            print("  -", col)
        df = df.drop(columns=to_drop)
    else:
        print("No columns exceed missing threshold.")

    for col in df.columns:
        if df[col].isna().sum() > 0:
            if pd.api.types.is_numeric_dtype(df[col]):
                value = df[col].median() if fill_method == "median" else df[col].mean()
                df[col] = df[col].fillna(value)
                print(f"Filled numeric column {col} with {fill_method}.")
            else:
                mode_value = df[col].mode()[0]
                df[col] = df[col].fillna(mode_value)
                print(f"Filled text column {col} with mode.")

    return df


def remove_duplicates(df):
    """
    Remove duplicate rows from the dataset.

    Parameters
    ----------
    df : pandas.DataFrame
        Input dataset.

    Returns
    -------
    pandas.DataFrame
        Dataset with duplicates removed.

    Notes
    -----
    Prints the number of duplicates detected before removal.
    """
    print("\n" + "=" * 60)
    print("STEP 3: REMOVING DUPLICATES")
    print("=" * 60)

    dup_count = df.duplicated().sum()
    print(f"Found {dup_count} duplicates.")

    df = df.drop_duplicates()
    print("Duplicates removed.")

    return df


def fix_types(df):
    """
    Convert specific columns to appropriate numeric types.

    Parameters
    ----------
    df : pandas.DataFrame
        Input dataset.

    Returns
    -------
    pandas.DataFrame
        Dataset with corrected data types.

    Notes
    -----
    Attempts conversion of columns such as:
    - Year → Int64
    - Latitude/Longitude → Float64
    - Temperature/Precipitation → Float64
    """
    print("\n" + "=" * 60)
    print("STEP 4: FIXING DATA TYPES")
    print("=" * 60)

    type_map = {
        "Year": "Int64",
        "Population": "Int64",
        "Latitude": "Float64",
        "Longitude": "Float64",
        "Temperature": "Float64",
        "Precipitation": "Float64",
        "Shift_km": "Float64"
    }


    for col, dtype in type_map.items():
        if col in df.columns:
            try:
                df[col] = df[col].astype(dtype)
                print(f"Converted {col} -> {dtype}")
            except:
                print(f"Could not convert {col}.")

    return df


def validate_ranges(df, year_range=(1970, 2025)):
    """
    Validate numeric ranges and filter out invalid values.

    Parameters
    ----------
    df : pandas.DataFrame
        Input dataset.
    year_range : tuple(int, int), default=(1980, 2010)
        Valid inclusive range for the "Year" column.

    Returns
    -------
    pandas.DataFrame
        Dataset filtered based on valid ranges.

    Notes
    -----
    Removes rows where Year is outside the specified range.
    """
    print("\n" + "=" * 60)
    print("STEP 6: VALIDATING RANGES")
    print("=" * 60)

    yr_min, yr_max = year_range

    if "Year" in df.columns:
        before_len = len(df)
        df = df[(df["Year"] >= yr_min) & (df["Year"] <= yr_max)]
        print(f"Removed {before_len - len(df)} rows with invalid years.")

    return df


def clean_text(df):
    """
    Clean and standardize text columns.

    Parameters
    ----------
    df : pandas.DataFrame
        Input dataset.

    Returns
    -------
    pandas.DataFrame
        Dataset with cleaned text formatting.

    Notes
    -----
    Applies stripping and title-case formatting to:
    - Bird_Species
    - Country
    """
    print("\n" + "=" * 60)
    print("STEP 7: CLEANING TEXT COLUMNS")
    print("=" * 60)

    text_cols = ["Bird_Species", "Country"]

    for col in text_cols:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.title()
            )
            print(f"Cleaned text column {col}.")

    return df

def lowercase_columns(df):
    """
    Convert DataFrame column names to lowercase.
    """
    df.columns = df.columns.str.lower()
    return df



def clean_bird_data(input_file, output_file="cleaned_bird_data.csv"):
    """
    Run a complete cleaning pipeline on raw bird occurrence and climate data.

    Parameters
    ----------
    input_file : str
        Path to the input raw CSV file.
    output_file : str, default="cleaned_bird_data.csv"
        Path where the cleaned dataset will be saved.

    Returns
    -------
    pandas.DataFrame
        Fully cleaned dataset.

    Workflow
    --------
    1. Load data
    2. Handle missing values
    3. Remove duplicates
    4. Fix data types
    5. Validate numeric ranges
    6. Clean text fields
    7. Column names to lowercase
    Saves the cleaned CSV to `output_file`.
    """
    df = load_data(input_file)
    df = handle_missing(df)
    df = remove_duplicates(df)
    df = fix_types(df)
    df = validate_ranges(df)
    df = clean_text(df)
    df = lowercase_columns(df)

    save_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(save_dir, exist_ok=True)
    output_path = os.path.join(save_dir, output_file)
    df.to_csv(output_path, index=False)
    print(f"\nCleaned dataset saved as {output_path}")
    return df


def model_data_spyros(df: pd.DataFrame) -> pd.DataFrame:
    # Aggregate population per species per year
    df_yearly = df.groupby(["bird_species", "year"])["population"].sum().reset_index()

    # Pivot population table
    df_pivot = (
        df_yearly.pivot(
            index="year",
            columns="bird_species",
            values="population"
        ).reset_index()
    )

    # Compute average temperature, precipitation, traffic per year
    df_avg = (
        df.groupby("year")[["temperature", "precipitation", "traffic"]]
        .mean()
        .reset_index()
    )

    # Merge population pivot with environmental variables
    df_merged = (
        pd.merge(
            df_pivot,
            df_avg,
            on="year",
            how="inner"
        )
    )

    return df_merged


def get_bird_shift_climate_and_land_usage_data(df):
    """
    Extracts climate and land usage related statistics for bird species by country and year.
    For each combination of country, bird species, and year, this function:
    - Filters the dataset to matching records
    - Identifies the row with the maximum geographic shift (shift_km)
    - Collects the population and temperature values associated with that maximum shift

    The result is a summary DataFrame showing how bird species’ maximum
    range shifts relate to population and temperature over time.

    :param df: Input DataFrame containing bird climate data.
    
               Required columns: country, bird_species, year,
               shift_km, population, temperature
    :return: Summary DataFrame with maximum shift statistics per year
    """
    # Standardize column names for consistency and ease of access
    #df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    # Get unique countries,bird species and years in the dataset
    countries=set(df["country"])
    bird_species_set=set(df["bird_species"])
    years=set(df["year"])

    # Get sorted list, since sets are unordered
    country_list = sorted(list(countries))
    bird_species_list = sorted((bird_species_set))
    year_list = sorted(list(years))

    # Initialize a list to store summary statistics for each year
    stats_by_year = []

    # Loop through each country
    for country in country_list:

        # Loop through each bird species
        for bird_species in bird_species_list:

            # Filter the DataFrame for the current country and species
            """ The dataset is first filtered by country and species, and
              then further filtered by year to extract annual movement statistics."""
            country_species_df = df[
                (df["country"] == country) &
                (df["bird_species"] == bird_species)
            ]
            # Skip if no data exists for this country–species combination
            if country_species_df.empty:
                continue

            # Loop through each year
            for year in year_list:

                """annual_data contains records for this species in this country for the given year"""
                # Filter data for the current year
                annual_data = country_species_df[country_species_df["year"] == year]

                # Skip if no data exists for this year
                if annual_data.empty:
                    continue

                # Identify the row with the maximum shift distance
                max_row = annual_data.loc[annual_data["shift_km"].idxmax()]

                """ A list of dictionaries is used to store year-specific summary records 
                    that can be efficiently transformed into a DataFrame"""
                
                # Store the extracted statistics
                stats_by_year.append({
                    "country": country,
                    "bird_species": bird_species,
                    "year": year,
                    "max_shift_km": max_row["shift_km"],
                    "population_at_max_shift": max_row["population"],
                    "temperature_at_max_shift": max_row["temperature"]
                })

    # Convert collected statistics into a DataFrame and sort by year
    bird_shift_climate_and_land_usage_data = pd.DataFrame(stats_by_year).sort_values(by="year")

    # Return the final summarized DataFrame
    return bird_shift_climate_and_land_usage_data


if __name__ == "__main__":
    cleaned = clean_bird_data("./Occurance_and_climatedata_of_birds.csv")
    print("\nCleaning complete!")

