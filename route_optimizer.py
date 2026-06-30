"""
route_optimizer.py

Uses Google OR-Tools to solve the Vehicle Routing Problem (VRP)
using a distance matrix.
"""

from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

from data_loader import LocationLoader
from distance_matrix import DistanceMatrixGenerator


class RouteOptimizer:

    def __init__(self, distance_matrix):

        self.distance_matrix = distance_matrix

        self.manager = None
        self.routing = None
        self.solution = None

    def create_data_model(self):

        return {
            "distance_matrix": self.distance_matrix,
            "num_vehicles": 1,
            "depot": 0
        }

    def solve(self):

        data = self.create_data_model()

        self.manager = pywrapcp.RoutingIndexManager(
            len(data["distance_matrix"]),
            data["num_vehicles"],
            data["depot"]
        )

        self.routing = pywrapcp.RoutingModel(self.manager)

        def distance_callback(from_index, to_index):

            from_node = self.manager.IndexToNode(from_index)
            to_node = self.manager.IndexToNode(to_index)

            return int(
                data["distance_matrix"][from_node][to_node] * 1000
            )

        transit_callback_index = self.routing.RegisterTransitCallback(
            distance_callback
        )

        self.routing.SetArcCostEvaluatorOfAllVehicles(
            transit_callback_index
        )

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()

        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )

        self.solution = self.routing.SolveWithParameters(
            search_parameters
        )

        return self.solution

    def print_solution(self, location_names):

        if self.solution is None:
            print("No solution found.")
            return

        print("\nOptimized Delivery Route\n")
        print("-" * 45)

        index = self.routing.Start(0)

        total_distance = 0

        while not self.routing.IsEnd(index):

            node = self.manager.IndexToNode(index)

            print(location_names[node])

            previous_index = index

            index = self.solution.Value(
                self.routing.NextVar(index)
            )

            total_distance += self.routing.GetArcCostForVehicle(
                previous_index,
                index,
                0
            )

        print(location_names[0])

        print("\nTotal Distance : {:.2f} km".format(
            total_distance / 1000
        ))


if __name__ == "__main__":

    loader = LocationLoader("data/locations.csv")

    locations = loader.load_locations()

    matrix_generator = DistanceMatrixGenerator(locations)

    matrix = matrix_generator.build_distance_matrix()

    optimizer = RouteOptimizer(matrix)

    optimizer.solve()

    names = [loc["name"] for loc in locations]

    optimizer.print_solution(names)