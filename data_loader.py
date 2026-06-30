"""
data_loader.py

Loads delivery locations from a CSV file and performs
basic validation.
"""

import pandas as pd


class LocationLoader:

    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.locations = []

    def load_locations(self):

        try:
            df = pd.read_csv(self.csv_file)

        except FileNotFoundError:
            raise FileNotFoundError(
                f"Could not find {self.csv_file}"
            )

        required_columns = [
            "Name",
            "Latitude",
            "Longitude"
        ]

        for column in required_columns:

            if column not in df.columns:

                raise ValueError(
                    f"Missing required column: {column}"
                )

        self.locations = []

        for _, row in df.iterrows():

            location = {
                "name": row["Name"],
                "latitude": float(row["Latitude"]),
                "longitude": float(row["Longitude"])
            }

            self.locations.append(location)

        return self.locations

    def display_locations(self):

        print("\nDelivery Locations")
        print("-" * 40)

        for i, location in enumerate(self.locations):

            print(
                f"{i}. "
                f"{location['name']} "
                f"({location['latitude']}, "
                f"{location['longitude']})"
            )


if __name__ == "__main__":

    loader = LocationLoader("data/locations.csv")

    locations = loader.load_locations()

    loader.display_locations()