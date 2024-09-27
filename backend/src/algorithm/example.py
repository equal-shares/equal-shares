# import matplotlib.pyplot as plt
# import numpy as np


# def plot_bid_data(
#     bids: dict[int, dict[int, int]],
#     cost_min_max: list[dict[int, tuple[int, int]]],
#     average_bids: dict[int, int],
#     winners_allocations: dict[int, int],
# ) -> None:
#     # Extracting project IDs
#     project_ids = list(bids.keys())

#     # Flattening cost_min_max to work with the list of dictionaries
#     cost_min_values = []
#     cost_max_values = []
#     for project_id in project_ids:
#         for cost_dict in cost_min_max:
#             if project_id in cost_dict:
#                 cost_min, cost_max = cost_dict[project_id]
#                 cost_min_values.append(cost_min)
#                 cost_max_values.append(cost_max)
#                 break

#     # Extracting values for average_bids and winners_allocations
#     avg_bids_values = [average_bids[pid] for pid in project_ids]
#     winners_allocations_values = [winners_allocations[pid] for pid in project_ids]

#     # Bar width
#     bar_width = 0.5
#     x_pos = np.arange(len(project_ids))

#     # Small offset for equal values
#     small_offset = 0.001

#     # Create the plot
#     plt.figure(figsize=(10, 6))

#     # Sort the values (Average Bids, Winners Allocations, Cost Min, Cost Max) per project in ascending order
#     for i, project_id in enumerate(project_ids):
#         values = [
#             ("Average Bids", avg_bids_values[i], "blue"),
#             ("Winners Allocations", winners_allocations_values[i], "green"),
#             ("Cost Min", cost_min_values[i], "red"),
#             ("Cost Max", cost_max_values[i], "orange"),
#         ]

#         # Sort the values by the second element (the value itself)
#         values_sorted = sorted(values, key=lambda x: x[1])

#         # Plot the sorted bars, applying a small horizontal offset to distinguish equal values
#         cumulative_bottom = 0
#         last_value = None
#         for label, value, color in values_sorted:
#             if last_value is not None and value == last_value:
#                 # Add small horizontal offset for equal values
#                 value += small_offset
#             plt.bar(
#                 x_pos[i], value, width=bar_width, label=label if i == 0 else "", color=color, bottom=cumulative_bottom
#             )
#             cumulative_bottom += value
#             last_value = value

#     # Adding labels and title
#     plt.xlabel("Project ID")
#     plt.ylabel("Value")
#     plt.title("Bids, Winners Allocations, and Costs for Projects (Sorted and Offset for Equal Values)")
#     plt.xticks(x_pos, project_ids)
#     plt.legend()

#     # Display the plot
#     plt.tight_layout()
#     plt.show()


# # Example data to pass to the function
# bids = {15: {1: 500, 5: 500, 3: 500}, 7: {1: 500, 5: 500, 3: 500}, 9: {1: 500, 5: 500, 3: 500}}
# cost_min_max = [{15: (500, 600)}, {7: (500, 600)}, {9: (500, 600)}]
# average_bids = {15: 500.0, 7: 500.0, 9: 500.0}
# winners_allocations = {15: 500, 7: 500, 9: 500}
# # Call the function to plot
# plot_bid_data(bids, cost_min_max, average_bids, winners_allocations)
