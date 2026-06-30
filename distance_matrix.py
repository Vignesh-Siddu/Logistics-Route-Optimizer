"""
distance_matrix.py

Generates a distance matrix for all delivery locations.
Current implementation uses the Haversine formula.
Can later be replaced with OpenRouteService road distances.
"""

import math
from data_loader import LocationLoader


class DistanceMatrixGenerator:

    def __init__(self, locations):
        self.locations = locations
        self.distance_matrix = []

    @staticmethod
    def haversine_distance(lat1, lon1, lat2, lon2):
        """
        Calculate great-circle distance between two coordinates.
        Returns distance in kilometers.
        """

        R = 6371.0

        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1)
            * math.cos(lat2)
            * math.sin(dlon / 2) ** 2
        )

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return round(R * c, 2)

    def build_distance_matrix(self):

        matrix = []

        for source in self.locations:

            row = []

            for destination in self.locations:

                distance = self.haversine_distance(
                    source["latitude"],
                    source["longitude"],
                    destination["latitude"],
                    destination["longitude"],
                )

                row.append(distance)

            matrix.append(row)

        self.distance_matrix = matrix

        return matrix

    def print_distance_matrix(self):

        names = [loc["name"] for loc in self.locations]

        print("\nDistance Matrix (km)\n")

        print(f"{'':15}", end="")

        for name in names:
            print(f"{name[:10]:>12}", end="")

        print()

        for i, row in enumerate(self.distance_matrix):

            print(f"{names[i]:15}", end="")

            for distance in row:
                print(f"{distance:12.2f}", end="")

            print()


if __name__ == "__main__":

    loader = LocationLoader("data/locations.csv")

    locations = loader.load_locations()

    generator = DistanceMatrixGenerator(locations)

    generator.build_distance_matrix()

    generator.print_distance_matrix()