from src.algorithm.computation import min_max_equal_shares

if __name__ == "__main__":
    import time

    # T.0 Testing of multiple projects
    print("T.0 Testing of multiple projects")
    voters = [1, 2, 3, 4, 5]  # Voters
    cost_min_max = [
        {1: (100, 200)},
        {2: (150, 250)},
        {3: (200, 300)},
        {4: (250, 350)},
        {5: (300, 400)},
        {6: (350, 450)},
        {7: (400, 500)},
        {8: (450, 550)},
        {9: (500, 600)},
        {10: (550, 650)},
    ]
    bids = {
        1: {1: 100, 2: 130, 3: 0, 4: 150},
        2: {2: 160, 5: 190},
        3: {1: 200, 5: 240},
        4: {
            3: 270,
            4: 280,
        },
        5: {2: 310, 3: 320, 5: 340},
        6: {2: 360, 5: 390},
        7: {
            1: 400,
            4: 430,
        },
        8: {2: 460, 5: 490},
        9: {1: 500, 3: 520, 5: 540},
        10: {
            2: 560,
            3: 570,
        },
    }
    budget = 1000  # Total budget

    start_time = time.time()
    winners_allocations, candidates_payments_per_voter = min_max_equal_shares(voters, cost_min_max, budget, bids)
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time
    print(" T.0 result: ", winners_allocations)
    print(candidates_payments_per_voter)
    print(f"Function executed in {elapsed_time:.4f} seconds")
    # Iterate over each entry in the bids dictionary
    total_sum = 0
    for bid in winners_allocations.values():
        total_sum += bid  # Add the value where the key is 1
    # Output the result
    print("The sum of all Projects:", total_sum, ", budget - total = ", budget - total_sum)  # Record the end time
    print("----------------------------------------------------------------------------------")

    # T.1 Testing of multiple projects - prime experiment
    print("T.1 Testing of multiple projects - prime experiment")
    voters = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    cost_min_max = [
        {1: (11000, 70000)},
        {2: (1000, 40000)},
        {3: (20000, 400000)},
        {4: (2000, 10000)},
        {5: (2000, 30000)},
        {6: (35000, 85000)},
        {7: (160000, 350000)},
        {8: (500, 3000)},
        {9: (500000, 1500000)},
        {10: (30000, 90000)},
        {11: (200000, 500000)},
        {12: (30000, 80000)},
        {13: (30000, 100000)},
        {14: (2000, 10000)},
        {15: (2000, 10000)},
        {16: (1000, 60000)},
        {17: (1000, 60000)},
        {18: (15000, 50000)},
        {19: (3000, 85000)},
        {20: (4000, 10000)},
        {21: (5000, 15000)},
        {22: (1000, 15000)},
        {23: (15000, 70000)},
        {24: (20000, 100000)},
        {25: (40000, 150000)},
        {26: (5000, 50000)},
        {27: (10000, 100000)},
        {28: (6000, 60000)},
        {29: (15000, 70000)},
        {30: (100000, 200000)},
        {31: (70000, 150000)},
    ]

    total = 0
    # Iterate over each dictionary in the list
    for item in cost_min_max:
        # For each dictionary, access the tuple and add the second value (max) to the total
        for key, value in item.items():
            total += value[1]
    print("all :", total)

    bids = {
        1: {1: 70000, 2: 0, 3: 44000, 4: 0, 5: 28000, 6: 11000, 7: 0, 8: 11000, 9: 20000},
        2: {1: 26000, 2: 0, 3: 25000, 4: 0, 5: 18000, 6: 40000, 7: 14000, 8: 5000, 9: 23000},
        3: {1: 200000, 2: 0, 3: 400000, 4: 0, 5: 169000, 6: 340000, 7: 400000, 8: 60000, 9: 107000},
        4: {1: 10000, 2: 0, 3: 10000, 4: 0, 5: 10000, 6: 6000, 7: 7000, 8: 10000, 9: 10000},
        5: {1: 30000, 2: 0, 3: 30000, 4: 0, 5: 30000, 6: 30000, 7: 30000, 8: 10000, 9: 20000},
        6: {1: 85000, 2: 0, 3: 62000, 4: 0, 5: 61000, 6: 35000, 7: 69000, 8: 35000, 9: 55000},
        7: {1: 160000, 2: 0, 3: 300000, 4: 0, 5: 217000, 6: 350000, 7: 266000, 8: 201000, 9: 292000},
        8: {1: 3000, 2: 0, 3: 3000, 4: 0, 5: 3000, 6: 3000, 7: 3000, 8: 500, 9: 500},
        9: {1: 1120000, 2: 0, 3: 1500000, 4: 682000, 5: 1174000, 6: 1245000, 7: 1238000, 8: 500000, 9: 1150000},
        10: {1: 65000, 2: 0, 3: 70000, 4: 0, 5: 53000, 6: 90000, 7: 68000, 8: 30000, 9: 40000},
        11: {1: 400000, 2: 0, 3: 0, 4: 0, 5: 262000, 6: 0, 7: 0, 8: 0, 9: 296000},
        12: {1: 45000, 2: 0, 3: 30000, 4: 0, 5: 45000, 6: 30000, 7: 0, 8: 0, 9: 37000},
        13: {1: 35000, 2: 30000, 3: 30000, 4: 69000, 5: 59000, 6: 100000, 7: 0, 8: 0, 9: 95000},
        14: {1: 10000, 2: 10000, 3: 7000, 4: 0, 5: 7000, 6: 10000, 7: 10000, 8: 2000, 9: 10000},
        15: {1: 10000, 2: 10000, 3: 10000, 4: 9000, 5: 8000, 6: 8000, 7: 3000, 8: 2000, 9: 8000},
        16: {1: 15000, 2: 1000, 3: 60000, 4: 0, 5: 0, 6: 49000, 7: 60000, 8: 8000, 9: 60000},
        17: {1: 15000, 2: 60000, 3: 60000, 4: 33000, 5: 47000, 6: 37000, 7: 0, 8: 0, 9: 19000},
        18: {1: 30000, 2: 50000, 3: 0, 4: 0, 5: 29000, 6: 41000, 7: 0, 8: 20000, 9: 20000},
        19: {1: 65000, 2: 3000, 3: 85000, 4: 0, 5: 78000, 6: 85000, 7: 0, 8: 85000, 9: 63000},
        20: {1: 10000, 2: 10000, 3: 8000, 4: 0, 5: 0, 6: 7000, 7: 0, 8: 0, 9: 9000},
        21: {1: 15000, 2: 0, 3: 12000, 4: 0, 5: 13000, 6: 13000, 7: 0, 8: 0, 9: 10000},
        22: {1: 10000, 2: 15000, 3: 15000, 4: 13000, 5: 13000, 6: 12000, 7: 15000, 8: 3000, 9: 15000},
        23: {1: 40000, 2: 34000, 3: 0, 4: 0, 5: 0, 6: 15000, 7: 0, 8: 15000, 9: 28000},
        24: {1: 55000, 2: 0, 3: 0, 4: 0, 5: 0, 6: 20000, 7: 0, 8: 0, 9: 71000},
        25: {1: 40000, 2: 0, 3: 0, 4: 0, 5: 150000, 6: 0, 7: 0, 8: 40000, 9: 86000},
        26: {1: 50000, 2: 0, 3: 36000, 4: 0, 5: 50000, 6: 37000, 7: 0, 8: 0, 9: 35000},
        27: {1: 30000, 2: 10000, 3: 12000, 4: 0, 5: 100000, 6: 10000, 7: 100000, 8: 0, 9: 100000},
        28: {1: 25000, 2: 60000, 3: 6000, 4: 0, 5: 60000, 6: 36000, 7: 60000, 8: 21000, 9: 60000},
        29: {1: 70000, 2: 70000, 3: 15000, 4: 0, 5: 0, 6: 70000, 7: 70000, 8: 15000, 9: 70000},
        30: {1: 180000, 2: 0, 3: 100000, 4: 154000, 5: 190000, 6: 200000, 7: 0, 8: 100000, 9: 110000},
        31: {1: 81000, 2: 111000, 3: 70000, 4: 0, 5: 126000, 6: 70000, 7: 150000, 8: 96000, 9: 80000},
    }
    budget = 3000000

    start_time = time.time()
    winners_allocations, candidates_payments_per_voter = min_max_equal_shares(voters, cost_min_max, budget, bids)
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time
    print(" T.1 result: ", winners_allocations)
    print(candidates_payments_per_voter)
    print(f"Function executed in {elapsed_time:.4f} seconds")
    # Iterate over each entry in the bids dictionary
    total_sum = 0
    for bid in winners_allocations.values():
        total_sum += bid  # Add the value where the key is 1
    # Output the result
    print("The sum of all Projects:", total_sum, ", budget - total = ", budget - total_sum)  #
    print("----------------------------------------------------------------------------------")

    # T.2 Three projects with different prices
    print("T.2 Three projects with different prices")
    voters = [1, 2]  # voter
    cost_min_max = [{1: (200, 700)}, {2: (300, 900)}, {3: (100, 100)}]
    bids = {1: {1: 500, 2: 200}, 2: {1: 300, 2: 300}, 3: {2: 100}}
    budget = 900  # Budget

    start_time = time.time()
    winners_allocations, candidates_payments_per_voter = min_max_equal_shares(voters, cost_min_max, budget, bids)
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time
    print(" T.2 result: ", winners_allocations)
    print(candidates_payments_per_voter)
    print(f"Function executed in {elapsed_time:.4f} seconds")
    # Iterate over each entry in the bids dictionary
    total_sum = 0
    for bid in winners_allocations.values():
        total_sum += bid  # Add the value where the key is 1
    # Output the result
    print("The sum of all Projects:", total_sum, ", budget - total = ", budget - total_sum)
    print("----------------------------------------------------------------------------------")

    # T.3 Two projects with the same amount of voters and the price difference between them is 1
    print("T.3 Two projects with the same amount of voters and the price difference between them is 1")
    voters = [1, 2]  # voter
    cost_min_max = [{1: (99, 200)}, {2: (98, 200)}]
    bids = {1: {2: 99}, 2: {1: 98}}
    budget = 100  # Budget

    start_time = time.time()
    winners_allocations, candidates_payments_per_voter = min_max_equal_shares(voters, cost_min_max, budget, bids)
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time
    print(" T.3 result: ", winners_allocations)
    print(candidates_payments_per_voter)
    print(f"Function executed in {elapsed_time:.4f} seconds")
    # Iterate over each entry in the bids dictionary
    total_sum = 0
    for bid in winners_allocations.values():
        total_sum += bid  # Add the value where the key is 1
    # Output the result
    print("The sum of all Projects:", total_sum, ", budget - total = ", budget - total_sum)
    print("----------------------------------------------------------------------------------")

    # T.4 For 4 projects with same cost and same voters,
    # while the budget suffices for all the 1 ( take the first index) .
    print("T.4 Check break_ties Function For 4 projects with same cost and same voters, ")
    print("while the budget suffices for all the 1 ( take the first index)")
    voters = [1, 2, 3, 4]  # voter
    cost_min_max = [{1: (500, 600)}, {2: (500, 600)}, {3: (500, 600)}, {4: (500, 600)}]
    bids = {
        1: {1: 500, 2: 500, 3: 500, 4: 500},
        2: {1: 500, 2: 500, 3: 500, 4: 500},
        3: {1: 500, 2: 500, 3: 500, 4: 500},
        4: {1: 500, 2: 500, 3: 500, 4: 500},
    }  # for each project
    budget = 500  # Budget

    start_time = time.time()
    winners_allocations, candidates_payments_per_voter = min_max_equal_shares(voters, cost_min_max, budget, bids)
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time
    print(" T.4 result: ", winners_allocations)
    print(candidates_payments_per_voter)
    print(f"Function executed in {elapsed_time:.4f} seconds")
    # Iterate over each entry in the bids dictionary
    total_sum = 0
    for bid in winners_allocations.values():
        total_sum += bid  # Add the value where the key is 1
    # Output the result
    print("The sum of all Projects:", total_sum, ", budget - total = ", budget - total_sum)
    print("----------------------------------------------------------------------------------")

    # T.5 For one projects with one voter. the budget > project cost.
    print("T.5 For one projects with one voter. the budget > project cost")
    voters = [1]
    cost_min_max = [{1: (500, 600)}]  # Cost for each project
    bids = {1: {1: 600}}
    budget = 1000  # Budget

    start_time = time.time()
    winners_allocations, candidates_payments_per_voter = min_max_equal_shares(voters, cost_min_max, budget, bids)
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time
    print(" T.5 result: ", winners_allocations)
    print(candidates_payments_per_voter)
    print(f"Function executed in {elapsed_time:.4f} seconds")
    # Iterate over each entry in the bids dictionary
    total_sum = 0
    for bid in winners_allocations.values():
        total_sum += bid  # Add the value where the key is 1
    # Output the result
    print("The sum of all Projects:", total_sum, ", budget - total = ", budget - total_sum)
    print("----------------------------------------------------------------------------------")

    # T.6 For one projects with one voter. the budget <= project min cost.
    print("T.6 For one projects with one voter. the budget <= project min cost")
    voters = [1]
    cost_min_max = [{1: (500, 600)}]  # Cost for each project
    bids = {1: {1: 600}}
    budget = 500  # Budget

    start_time = time.time()
    winners_allocations, candidates_payments_per_voter = min_max_equal_shares(voters, cost_min_max, budget, bids)
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time
    print(" T.6 result: ", winners_allocations)
    print(candidates_payments_per_voter)
    print(f"Function executed in {elapsed_time:.4f} seconds")
    # Iterate over each entry in the bids dictionary
    total_sum = 0
    for bid in winners_allocations.values():
        total_sum += bid  # Add the value where the key is 1
    # Output the result
    print("The sum of all Projects:", total_sum, ", budget - total = ", budget - total_sum)
    print("----------------------------------------------------------------------------------")

    # T.7 For one projects with one voter. the budget < project min  cost.
    print("T.7 For one projects with one voter. the budget < project min  cost")
    voters = [1]
    cost_min_max = [{1: (600, 600)}]  # Cost for each project
    bids = {1: {1: 600}}
    budget = 500  # Budget

    start_time = time.time()
    winners_allocations, candidates_payments_per_voter = min_max_equal_shares(voters, cost_min_max, budget, bids)
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time
    print(" T.7 result: ", winners_allocations)
    print(candidates_payments_per_voter)
    print(f"Function executed in {elapsed_time:.4f} seconds")
    # Iterate over each entry in the bids dictionary
    total_sum = 0
    for bid in winners_allocations.values():
        total_sum += bid  # Add the value where the key is 1
    # Output the result
    print("The sum of all Projects:", total_sum, ", budget - total = ", budget - total_sum)
    print("----------------------------------------------------------------------------------")

    # T.8 For 3 projects with same cost and same voters, while the budget suffices for all the 3.
    print("T.8 For 3 projects with same cost and same voters, while the budget suffices for all the 3")
    voters = [1, 2, 3]
    cost_min_max = [{1: (500, 600)}, {2: (500, 600)}, {3: (500, 600)}]
    bids = {1: {1: 500, 2: 500, 3: 500}, 2: {1: 500, 2: 500, 3: 500}, 3: {1: 500, 2: 500, 3: 500}}
    budget = 1500  # Budget

    start_time = time.time()
    winners_allocations, candidates_payments_per_voter = min_max_equal_shares(voters, cost_min_max, budget, bids)
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time
    print(" T.8 result: ", winners_allocations)
    print(candidates_payments_per_voter)
    print(f"Function executed in {elapsed_time:.4f} seconds")
    # Iterate over each entry in the bids dictionary
    total_sum = 0
    for bid in winners_allocations.values():
        total_sum += bid  # Add the value where the key is 1
    # Output the result
    print("The sum of all Projects:", total_sum, ", budget - total = ", budget - total_sum)
    print("----------------------------------------------------------------------------------")

    # T.9 the projects order not continuous [the result same to 8 test].
    print("T.9  the projects order not continuous [the result same to 8 test]")
    voters = [1, 5, 3]
    cost_min_max = [{15: (500, 600)}, {7: (500, 600)}, {9: (500, 600)}]
    bids = {15: {1: 500, 5: 500, 3: 500}, 7: {1: 500, 5: 500, 3: 500}, 9: {1: 500, 5: 500, 3: 500}}
    budget = 1500  # Budget

    start_time = time.time()

    winners_allocations, candidates_payments_per_voter = min_max_equal_shares(voters, cost_min_max, budget, bids)
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time
    print(" T.9 result: ", winners_allocations)
    print(candidates_payments_per_voter)
    print(f"Function executed in {elapsed_time:.4f} seconds")
    # Iterate over each entry in the bids dictionary
    total_sum = 0
    for bid in winners_allocations.values():
        total_sum += bid  # Add the value where the key is 1
    # Output the result
    print("The sum of all Projects:", total_sum, ", budget - total = ", budget - total_sum)
    print("----------------------------------------------------------------------------------")
