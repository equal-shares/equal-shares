import random
import sys

sys.path.append("../..")

import pytest

from src.server.algorithms import (
    calculate_totals,
    convert_structure,
    generalized_median_algorithm,
    median_algorithm,
    unite_votes,
    update_dict_ids,
)
from src.server.counter import Counter


class TestMedianAlgorithm:
    def test_median_algorithm_with_two_users(self) -> None:
        # Test case 1: Testing the output of the function with two users.
        votes = {
            "user1": {
                "Department of Defense": {"Army": 40, "Police": 30, "total": 70},
                "Department of Education": {
                    "Schools": 20,
                    "Higher education": 10,
                    "total": 30,
                },
                "total": 100,
            },
            "user2": {
                "Department of Defense": {"Army": 10, "Police": 10, "total": 20},
                "Department of Education": {
                    "Schools": 30,
                    "Higher education": 50,
                    "total": 80,
                },
                "total": 100,
            },
        }

        budget_data = median_algorithm(votes)

        assert budget_data == {
            "Department of Defense": {"Army": 25, "Police": 20, "total": 45},
            "Department of Education": {
                "Schools": 25,
                "Higher education": 30,
                "total": 55,
            },
            "total": 100,
        }

    def test_median_algorithm_with_empty_dictionary(self) -> None:
        # Test case 2: Testing the function with an empty dictionary.
        votes = {}

        budget_data = median_algorithm(votes)

        assert budget_data == {}

    def test_median_algorithm_with_same_votes(self) -> None:
        # Test case 3: Testing the function with the same vote for each department.
        votes = {
            "user1": {
                "Department of Defense": {"Army": 1, "Police": 1, "total": 2},
                "Department of Education": {
                    "Schools": 1,
                    "Higher education": 1,
                    "total": 2,
                },
                "total": 4,
            },
            "user2": {
                "Department of Defense": {"Army": 1, "Police": 1, "total": 2},
                "Department of Education": {
                    "Schools": 1,
                    "Higher education": 1,
                    "total": 2,
                },
                "total": 4,
            },
        }

        budget_data = median_algorithm(votes)

        assert budget_data == {
            "Department of Defense": {"Army": 1, "Police": 1, "total": 2},
            "Department of Education": {
                "Schools": 1,
                "Higher education": 1,
                "total": 2,
            },
            "total": 4,
        }

    def test_median_algorithm_one_user(self) -> None:
        # Test case 4: Testing the function with only one user.
        votes = {
            "user1": {
                "Department of Defense": {"Army": 1, "Police": 1, "total": 2},
                "Department of Education": {
                    "Schools": 1,
                    "Higher education": 1,
                    "total": 2,
                },
                "total": 4,
            }
        }

        budget_data = median_algorithm(votes)

        assert budget_data == {
            "Department of Defense": {"Army": 1, "Police": 1, "total": 2},
            "Department of Education": {
                "Schools": 1,
                "Higher education": 1,
                "total": 2,
            },
            "total": 4,
        }

    def test_median_algorithm_wrong_answer(self) -> None:
        # Test case 5: Testing the function for wrong answer.
        votes = {
            "user1": {
                "Department of Defense": {"Army": 1, "Police": 1, "total": 2},
                "Department of Education": {
                    "Schools": 1,
                    "Higher education": 1,
                    "total": 2,
                },
                "total": 4,
            }
        }

        budget_data = median_algorithm(votes)

        assert budget_data != {
            "Department of Defense": {"Army": 2, "Police": 1, "total": 3},
            "Department of Education": {
                "Schools": 4,
                "Higher education": 1,
                "total": 5,
            },
            "total": 8,
        }

    def test_median_algorithm_three_users(self) -> None:
        # Test case 6: Testing the output of the function with three users.
        votes = {
            "user1": {
                "Department of Defense": {"Army": 6, "total": 6},
                "Department of Education": {"Schools": 0, "total": 0},
                "Department of Interior": {"immigration": 0, "total": 0},
                "total": 6,
            },
            "user2": {
                "Department of Defense": {"Army": 0, "total": 0},
                "Department of Education": {"Schools": 3, "total": 3},
                "Department of Interior": {"immigration": 3, "total": 3},
                "total": 6,
            },
            "user3": {
                "Department of Defense": {"Army": 3, "total": 3},
                "Department of Education": {"Schools": 3, "total": 3},
                "Department of Interior": {"immigration": 0, "total": 0},
                "total": 6,
            },
        }

        expected_result = {
            "Department of Defense": {"Army": 3, "total": 3},
            "Department of Education": {"Schools": 3, "total": 3},
            "Department of Interior": {"immigration": 0, "total": 0},
            "total": 6,
        }

        assert median_algorithm(votes) == expected_result


class TestGeneralizedMedianAlgorithm:
    EPSILON = 0.01  # a threshold value

    def test_generalized_median_algorithm_with_three_users(self) -> None:
        # Test case 1: Testing the output of the function with three users.
        votes = {
            "user1": {
                "Department of Defense": {"Army": 6, "total": 6},
                "Department of Education": {"Schools": 0, "total": 0},
                "Department of Interior": {"immigration": 0, "total": 0},
                "total": 6,
            },
            "user2": {
                "Department of Defense": {"Army": 0, "total": 0},
                "Department of Education": {"Schools": 3, "total": 3},
                "Department of Interior": {"immigration": 3, "total": 3},
                "total": 6,
            },
            "user3": {
                "Department of Defense": {"Army": 3, "total": 3},
                "Department of Education": {"Schools": 3, "total": 3},
                "Department of Interior": {"immigration": 0, "total": 0},
                "total": 6,
            },
        }

        expected_result = {
            "Department of Defense": {"Army": 2.4, "total": 2.4},
            "Department of Education": {"Schools": 2.4, "total": 2.4},
            "Department of Interior": {"immigration": 1.2, "total": 1.2},
            "total": 6,
        }

        assert generalized_median_algorithm(votes) == expected_result

    def test_generalized_median_algorithm_with_empty_dictionary(self) -> None:
        # Test case 2: Testing the function with an empty dictionary.
        votes = {}

        budget_data = generalized_median_algorithm(votes)

        assert budget_data == {}

    def test_generalized_median_algorithm_with_same_votes(self) -> None:
        # Test case 3: Testing the function with the same vote for each department.
        votes = {
            "user1": {
                "Department of Defense": {"Army": 1, "Police": 1, "total": 2},
                "Department of Education": {
                    "Schools": 1,
                    "Higher education": 1,
                    "total": 2,
                },
                "total": 4,
            },
            "user2": {
                "Department of Defense": {"Army": 1, "Police": 1, "total": 2},
                "Department of Education": {
                    "Schools": 1,
                    "Higher education": 1,
                    "total": 2,
                },
                "total": 4,
            },
        }

        budget_data = generalized_median_algorithm(votes)

        assert budget_data == {
            "Department of Defense": {"Army": 1, "Police": 1, "total": 2},
            "Department of Education": {
                "Schools": 1,
                "Higher education": 1,
                "total": 2,
            },
            "total": 4,
        }

    def test_generalized_median_algorithm_one_user(self) -> None:
        # Test case 4: Testing the function with only one user.
        votes = {
            "user1": {
                "Department of Defense": {"Army": 1, "Police": 1, "total": 2},
                "Department of Education": {
                    "Schools": 1,
                    "Higher education": 1,
                    "total": 2,
                },
                "total": 4,
            }
        }

        budget_data = generalized_median_algorithm(votes)

        assert budget_data == {
            "Department of Defense": {"Army": 1, "Police": 1, "total": 2},
            "Department of Education": {
                "Schools": 1,
                "Higher education": 1,
                "total": 2,
            },
            "total": 4,
        }

    def test_generalized_median_algorithm_wrong_answer(self) -> None:
        # Test case 5: Testing the function for wrong answer.
        votes = {
            "user1": {
                "Department of Defense": {"Army": 1, "Police": 1, "total": 2},
                "Department of Education": {
                    "Schools": 1,
                    "Higher education": 1,
                    "total": 2,
                },
                "total": 4,
            }
        }

        budget_data = generalized_median_algorithm(votes)

        assert budget_data != {
            "Department of Defense": {"Army": 2, "Police": 1, "total": 3},
            "Department of Education": {
                "Schools": 4,
                "Higher education": 1,
                "total": 5,
            },
            "total": 8,
        }

    def test_generalized_median_algorithm_random_votes(self) -> None:
        # Test the function by generating random votes and ensuring that the total budget remains the same.

        # set up the initial budget and departments
        initial_budget = 100
        departments = [
            "Department of Defense",
            "Department of Education",
            "Department of Interior",
        ]

        # generate random votes for 10 users
        num_users = 10
        votes = {}
        for i in range(num_users):
            while True:
                user_votes = {}
                for dept in departments:
                    dept_votes = {}
                    for j in range(2):
                        dept_votes[f"Option{j+1}"] = random.randint(0, initial_budget)
                    dept_votes["total"] = sum(dept_votes.values())
                    user_votes[dept] = dept_votes
                user_votes["total"] = sum([v["total"] for v in user_votes.values()])
                if user_votes["total"] == initial_budget:
                    break
            votes[f"user{i+1}"] = user_votes

        # compute the budget data using the algorithm
        budget_data = generalized_median_algorithm(votes)

        # check that the total budget remains the same
        new_total_budget = budget_data["total"]
        assert (
            abs(new_total_budget - initial_budget) <= self.EPSILON
        ), f"Total budget does not match original budget. Original: {initial_budget}, New: {new_total_budget}"

    class TestUtilityFunctions:
        def test_calculate_totals_integers(self) -> None:
            vote = {
                "id": 0,
                "name": "root",
                "description": "I am root",
                "parent": None,
                "allocated_budget_amount": "",
                "children": [
                    {
                        "id": 1,
                        "name": "Security and public order",
                        "description": "I am Security and public order",
                        "parent": 0,
                        "allocated_budget_amount": "",
                        "children": [
                            {
                                "id": 2,
                                "name": "Security",
                                "description": "I am Security",
                                "parent": 1,
                                "allocated_budget_amount": "",
                                "children": [
                                    {
                                        "id": 3,
                                        "name": "Ministry of Defense",
                                        "description": "I am Ministry of Defense",
                                        "parent": 2,
                                        "allocated_budget_amount": "",
                                        "children": [
                                            {
                                                "id": 4,
                                                "name": "HR",
                                                "description": "I am HR",
                                                "parent": 3,
                                                "allocated_budget_amount": "",
                                                "children": [
                                                    {
                                                        "id": 6,
                                                        "name": "Current salary of permanent soldiers",
                                                        "description": "I am Current salary of permanent soldiers",
                                                        "parent": 4,
                                                        "allocated_budget_amount": 11171083,
                                                        "children": [],
                                                    },
                                                    {
                                                        "id": 7,
                                                        "name": "Current salary of Ministry of Defense employees",
                                                        "description": "I am Current salary of Ministry of Defense employees",
                                                        "parent": 4,
                                                        "allocated_budget_amount": 1265398,
                                                        "children": [],
                                                    },
                                                ],
                                            },
                                            {
                                                "id": 5,
                                                "name": "Pensions",
                                                "description": "I am Pensions",
                                                "parent": 3,
                                                "allocated_budget_amount": "",
                                                "children": [
                                                    {
                                                        "id": 8,
                                                        "name": "Permanent soldiers pensions",
                                                        "description": "I am Permanent soldiers' pensions",
                                                        "parent": 5,
                                                        "allocated_budget_amount": 7780739,
                                                        "children": [],
                                                    },
                                                    {
                                                        "id": 9,
                                                        "name": "Retirement grants for permanent soldiers",
                                                        "description": "I am Retirement grants for permanent soldiers",
                                                        "parent": 5,
                                                        "allocated_budget_amount": 374853,
                                                        "children": [],
                                                    },
                                                ],
                                            },
                                        ],
                                    }
                                ],
                            }
                        ],
                    }
                ],
            }

            expected_result = {
                "id": 0,
                "name": "root",
                "description": "I am root",
                "parent": None,
                "allocated_budget_amount": 20592073,
                "children": [
                    {
                        "id": 1,
                        "name": "Security and public order",
                        "description": "I am Security and public order",
                        "parent": 0,
                        "allocated_budget_amount": 20592073,
                        "children": [
                            {
                                "id": 2,
                                "name": "Security",
                                "description": "I am Security",
                                "parent": 1,
                                "allocated_budget_amount": 20592073,
                                "children": [
                                    {
                                        "id": 3,
                                        "name": "Ministry of Defense",
                                        "description": "I am Ministry of Defense",
                                        "parent": 2,
                                        "allocated_budget_amount": 20592073,
                                        "children": [
                                            {
                                                "id": 4,
                                                "name": "HR",
                                                "description": "I am HR",
                                                "parent": 3,
                                                "allocated_budget_amount": 12436481,
                                                "children": [
                                                    {
                                                        "id": 6,
                                                        "name": "Current salary of permanent soldiers",
                                                        "description": "I am Current salary of permanent soldiers",
                                                        "parent": 4,
                                                        "allocated_budget_amount": 11171083,
                                                        "children": [],
                                                    },
                                                    {
                                                        "id": 7,
                                                        "name": "Current salary of Ministry of Defense employees",
                                                        "description": "I am Current salary of Ministry of Defense employees",
                                                        "parent": 4,
                                                        "allocated_budget_amount": 1265398,
                                                        "children": [],
                                                    },
                                                ],
                                            },
                                            {
                                                "id": 5,
                                                "name": "Pensions",
                                                "description": "I am Pensions",
                                                "parent": 3,
                                                "allocated_budget_amount": 8155592,
                                                "children": [
                                                    {
                                                        "id": 8,
                                                        "name": "Permanent soldiers pensions",
                                                        "description": "I am Permanent soldiers' pensions",
                                                        "parent": 5,
                                                        "allocated_budget_amount": 7780739,
                                                        "children": [],
                                                    },
                                                    {
                                                        "id": 9,
                                                        "name": "Retirement grants for permanent soldiers",
                                                        "description": "I am Retirement grants for permanent soldiers",
                                                        "parent": 5,
                                                        "allocated_budget_amount": 374853,
                                                        "children": [],
                                                    },
                                                ],
                                            },
                                        ],
                                    }
                                ],
                            }
                        ],
                    }
                ],
            }

            calculate_totals(vote)
            assert vote == expected_result

        def test_calculate_totals_floats(self) -> None:
            vote = {
                "id": 0,
                "name": "root",
                "description": "I am root",
                "parent": None,
                "allocated_budget_amount": "",
                "children": [
                    {
                        "id": 1,
                        "name": "Security and public order",
                        "description": "I am Security and public order",
                        "parent": 0,
                        "allocated_budget_amount": "",
                        "children": [
                            {
                                "id": 2,
                                "name": "Security",
                                "description": "I am Security",
                                "parent": 1,
                                "allocated_budget_amount": "",
                                "children": [
                                    {
                                        "id": 3,
                                        "name": "Ministry of Defense",
                                        "description": "I am Ministry of Defense",
                                        "parent": 2,
                                        "allocated_budget_amount": "",
                                        "children": [
                                            {
                                                "id": 4,
                                                "name": "HR",
                                                "description": "I am HR",
                                                "parent": 3,
                                                "allocated_budget_amount": "",
                                                "children": [
                                                    {
                                                        "id": 6,
                                                        "name": "Current salary of permanent soldiers",
                                                        "description": "I am Current salary of permanent soldiers",
                                                        "parent": 4,
                                                        "allocated_budget_amount": 11171083.0,
                                                        "children": [],
                                                    },
                                                    {
                                                        "id": 7,
                                                        "name": "Current salary of Ministry of Defense employees",
                                                        "description": "I am Current salary of Ministry of Defense employees",
                                                        "parent": 4,
                                                        "allocated_budget_amount": 1265398.0,
                                                        "children": [],
                                                    },
                                                ],
                                            },
                                            {
                                                "id": 5,
                                                "name": "Pensions",
                                                "description": "I am Pensions",
                                                "parent": 3,
                                                "allocated_budget_amount": "",
                                                "children": [
                                                    {
                                                        "id": 8,
                                                        "name": "Permanent soldiers pensions",
                                                        "description": "I am Permanent soldiers' pensions",
                                                        "parent": 5,
                                                        "allocated_budget_amount": 7780739.0,
                                                        "children": [],
                                                    },
                                                    {
                                                        "id": 9,
                                                        "name": "Retirement grants for permanent soldiers",
                                                        "description": "I am Retirement grants for permanent soldiers",
                                                        "parent": 5,
                                                        "allocated_budget_amount": 374853.0,
                                                        "children": [],
                                                    },
                                                ],
                                            },
                                        ],
                                    }
                                ],
                            }
                        ],
                    }
                ],
            }

            expected_result = {
                "id": 0,
                "name": "root",
                "description": "I am root",
                "parent": None,
                "allocated_budget_amount": 20592073.0,
                "children": [
                    {
                        "id": 1,
                        "name": "Security and public order",
                        "description": "I am Security and public order",
                        "parent": 0,
                        "allocated_budget_amount": 20592073.0,
                        "children": [
                            {
                                "id": 2,
                                "name": "Security",
                                "description": "I am Security",
                                "parent": 1,
                                "allocated_budget_amount": 20592073.0,
                                "children": [
                                    {
                                        "id": 3,
                                        "name": "Ministry of Defense",
                                        "description": "I am Ministry of Defense",
                                        "parent": 2,
                                        "allocated_budget_amount": 20592073.0,
                                        "children": [
                                            {
                                                "id": 4,
                                                "name": "HR",
                                                "description": "I am HR",
                                                "parent": 3,
                                                "allocated_budget_amount": 12436481.0,
                                                "children": [
                                                    {
                                                        "id": 6,
                                                        "name": "Current salary of permanent soldiers",
                                                        "description": "I am Current salary of permanent soldiers",
                                                        "parent": 4,
                                                        "allocated_budget_amount": 11171083.0,
                                                        "children": [],
                                                    },
                                                    {
                                                        "id": 7,
                                                        "name": "Current salary of Ministry of Defense employees",
                                                        "description": "I am Current salary of Ministry of Defense employees",
                                                        "parent": 4,
                                                        "allocated_budget_amount": 1265398.0,
                                                        "children": [],
                                                    },
                                                ],
                                            },
                                            {
                                                "id": 5,
                                                "name": "Pensions",
                                                "description": "I am Pensions",
                                                "parent": 3,
                                                "allocated_budget_amount": 8155592.0,
                                                "children": [
                                                    {
                                                        "id": 8,
                                                        "name": "Permanent soldiers pensions",
                                                        "description": "I am Permanent soldiers' pensions",
                                                        "parent": 5,
                                                        "allocated_budget_amount": 7780739.0,
                                                        "children": [],
                                                    },
                                                    {
                                                        "id": 9,
                                                        "name": "Retirement grants for permanent soldiers",
                                                        "description": "I am Retirement grants for permanent soldiers",
                                                        "parent": 5,
                                                        "allocated_budget_amount": 374853.0,
                                                        "children": [],
                                                    },
                                                ],
                                            },
                                        ],
                                    }
                                ],
                            }
                        ],
                    }
                ],
            }

            calculate_totals(vote)
            assert vote == expected_result

        def check_duplicate_ids(self, tree: dict) -> bool:
            unique_ids = set()
            error = False

            # check for duplicates in the root node
            if tree["id"] in unique_ids:
                print(f"Error: Duplicate id '{tree['id']}' found in the tree")
                error = True
            else:
                unique_ids.add(tree["id"])

            # iterate through children nodes
            for node in tree.get("children", []):
                if node["id"] in unique_ids:
                    print(f"Error: Duplicate id '{node['id']}' found in the tree")
                    error = True
                else:
                    unique_ids.add(node["id"])
                if node.get("children"):
                    error_in_child = self.check_duplicate_ids(node)
                    if error_in_child:
                        error = True

            return error

        def test_update_dict_ids(self) -> None:
            tree = {
                "id": 13,
                "name": "root",
                "description": "I am root",
                "parent": None,
                "allocated_budget_amount": 20592073,
                "children": [
                    {
                        "id": 300,
                        "name": "Security and public order",
                        "description": "I am Security and public order",
                        "parent": 13,
                        "allocated_budget_amount": 20592073,
                        "children": [
                            {
                                "id": 300,
                                "name": "Security",
                                "description": "I am Security",
                                "parent": 1,
                                "allocated_budget_amount": 20592073,
                                "children": [
                                    {
                                        "id": 200,
                                        "name": "Ministry of Defense",
                                        "description": "I am Ministry of Defense",
                                        "parent": 300,
                                        "allocated_budget_amount": 20592073,
                                        "children": [
                                            {
                                                "id": 400,
                                                "name": "HR",
                                                "description": "I am HR",
                                                "parent": 200,
                                                "allocated_budget_amount": 12436481,
                                                "children": [
                                                    {
                                                        "id": 60,
                                                        "name": "Current salary of permanent soldiers",
                                                        "description": "I am Current salary of permanent soldiers",
                                                        "parent": 400,
                                                        "allocated_budget_amount": 11171083,
                                                        "children": [],
                                                    },
                                                    {
                                                        "id": 7,
                                                        "name": "Current salary of Ministry of Defense employees",
                                                        "description": "I am Current salary of Ministry of Defense employees",
                                                        "parent": 400,
                                                        "allocated_budget_amount": 1265398,
                                                        "children": [],
                                                    },
                                                ],
                                            },
                                            {
                                                "id": 5,
                                                "name": "Pensions",
                                                "description": "I am Pensions",
                                                "parent": 200,
                                                "allocated_budget_amount": 8155592,
                                                "children": [
                                                    {
                                                        "id": 80,
                                                        "name": "Permanent soldiers pensions",
                                                        "description": "I am Permanent soldiers' pensions",
                                                        "parent": 5,
                                                        "allocated_budget_amount": 7780739,
                                                        "children": [],
                                                    },
                                                    {
                                                        "id": 1,
                                                        "name": "Retirement grants for permanent soldiers",
                                                        "description": "I am Retirement grants for permanent soldiers",
                                                        "parent": 5,
                                                        "allocated_budget_amount": 374853,
                                                        "children": [],
                                                    },
                                                ],
                                            },
                                        ],
                                    }
                                ],
                            }
                        ],
                    }
                ],
            }

            result_before = self.check_duplicate_ids(tree)
            assert result_before == True
            count = Counter()

            update_dict_ids(count, tree)
            result_after = self.check_duplicate_ids(tree)
            assert result_after == False

        def test_convert_structure(self) -> None:
            # Testing the converting of a JSON object from the server to the structre of the algorithms
            vote = {
                "id": 0,
                "name": "root",
                "description": "I am root",
                "parent": None,
                "allocated_budget_amount": 20592073,
                "children": [
                    {
                        "id": 1,
                        "name": "Security and public order",
                        "description": "I am Security and public order",
                        "parent": 0,
                        "allocated_budget_amount": 20592073,
                        "children": [
                            {
                                "id": 2,
                                "name": "Security",
                                "description": "I am Security",
                                "parent": 1,
                                "allocated_budget_amount": 20592073,
                                "children": [
                                    {
                                        "id": 3,
                                        "name": "Ministry of Defense",
                                        "description": "I am Ministry of Defense",
                                        "parent": 2,
                                        "allocated_budget_amount": 20592073,
                                        "children": [
                                            {
                                                "id": 4,
                                                "name": "HR",
                                                "description": "I am HR",
                                                "parent": 3,
                                                "allocated_budget_amount": 12436481,
                                                "children": [
                                                    {
                                                        "id": 5,
                                                        "name": "Current salary of permanent soldiers",
                                                        "description": "I am Current salary of permanent soldiers",
                                                        "parent": 4,
                                                        "allocated_budget_amount": 11171083,
                                                        "children": [],
                                                    },
                                                    {
                                                        "id": 6,
                                                        "name": "Current salary of Ministry of Defense employees",
                                                        "description": "I am Current salary of Ministry of Defense employees",
                                                        "parent": 4,
                                                        "allocated_budget_amount": 1265398,
                                                        "children": [],
                                                    },
                                                ],
                                            },
                                            {
                                                "id": 7,
                                                "name": "Pensions",
                                                "description": "I am Pensions",
                                                "parent": 3,
                                                "allocated_budget_amount": 8155592,
                                                "children": [
                                                    {
                                                        "id": 8,
                                                        "name": "Permanent soldiers pensions",
                                                        "description": "I am Permanent soldiers' pensions",
                                                        "parent": 7,
                                                        "allocated_budget_amount": 7780739,
                                                        "children": [],
                                                    },
                                                    {
                                                        "id": 9,
                                                        "name": "Retirement grants for permanent soldiers",
                                                        "description": "I am Retirement grants for permanent soldiers",
                                                        "parent": 7,
                                                        "allocated_budget_amount": 374853,
                                                        "children": [],
                                                    },
                                                ],
                                            },
                                        ],
                                    }
                                ],
                            }
                        ],
                    }
                ],
            }

            expected_result = {
                "Security and public order": {
                    "Security": {
                        "Ministry of Defense": {
                            "HR": {
                                "Current salary of permanent soldiers": 11171083,
                                "Current salary of Ministry of Defense employees": 1265398,
                                "total": 12436481,
                            },
                            "Pensions": {
                                "Permanent soldiers pensions": 7780739,
                                "Retirement grants for permanent soldiers": 374853,
                                "total": 8155592,
                            },
                            "total": 20592073,
                        },
                        "total": 20592073,
                    },
                    "total": 20592073,
                },
                "total": 20592073,
            }

            updated_vote = convert_structure(vote)
            assert updated_vote == expected_result

        def test_unite_votes(self) -> None:
            votes1 = {
                "id": 0,
                "name": "root",
                "description": "I am root",
                "parent": None,
                "allocated_budget_amount": 20592073,
                "children": [
                    {
                        "id": 1,
                        "name": "Security and public order",
                        "description": "I am Security and public order",
                        "parent": 0,
                        "allocated_budget_amount": 20592073,
                        "children": [
                            {
                                "id": 2,
                                "name": "Security",
                                "description": "I am Security",
                                "parent": 1,
                                "allocated_budget_amount": 20592073,
                                "children": [
                                    {
                                        "id": 3,
                                        "name": "Ministry of Defense",
                                        "description": "I am Ministry of Defense",
                                        "parent": 2,
                                        "allocated_budget_amount": 20592073,
                                        "children": [
                                            {
                                                "id": 4,
                                                "name": "HR",
                                                "description": "I am HR",
                                                "parent": 3,
                                                "allocated_budget_amount": 12436481,
                                                "children": [
                                                    {
                                                        "id": 5,
                                                        "name": "Current salary of permanent soldiers",
                                                        "description": "I am Current salary of permanent soldiers",
                                                        "parent": 4,
                                                        "allocated_budget_amount": 11171083,
                                                        "children": [],
                                                    },
                                                    {
                                                        "id": 6,
                                                        "name": "Current salary of Ministry of Defense employees",
                                                        "description": "I am Current salary of Ministry of Defense employees",
                                                        "parent": 4,
                                                        "allocated_budget_amount": 1265398,
                                                        "children": [],
                                                    },
                                                ],
                                            },
                                            {
                                                "id": 9,
                                                "name": "Pensions",
                                                "description": "I am Pensions",
                                                "parent": 3,
                                                "allocated_budget_amount": 8155592,
                                                "children": [
                                                    {
                                                        "id": 10,
                                                        "name": "Permanent soldiers pensions",
                                                        "description": "I am Permanent soldiers' pensions",
                                                        "parent": 9,
                                                        "allocated_budget_amount": 7780739,
                                                        "children": [],
                                                    },
                                                    {
                                                        "id": 11,
                                                        "name": "Retirement grants for permanent soldiers",
                                                        "description": "I am Retirement grants for permanent soldiers",
                                                        "parent": 9,
                                                        "allocated_budget_amount": 374853,
                                                        "children": [],
                                                    },
                                                ],
                                            },
                                        ],
                                    }
                                ],
                            }
                        ],
                    }
                ],
            }

            votes2 = {
                "id": 0,
                "name": "root",
                "description": "I am root",
                "parent": None,
                "allocated_budget_amount": 20592073,
                "children": [
                    {
                        "id": 1,
                        "name": "Security and public order",
                        "description": "I am Security and public order",
                        "parent": 0,
                        "allocated_budget_amount": 20592073,
                        "children": [
                            {
                                "id": 2,
                                "name": "Security",
                                "description": "I am Security",
                                "parent": 1,
                                "allocated_budget_amount": 20592073,
                                "children": [
                                    {
                                        "id": 3,
                                        "name": "Ministry of Defense",
                                        "description": "I am Ministry of Defense",
                                        "parent": 2,
                                        "allocated_budget_amount": 20592073,
                                        "children": [
                                            {
                                                "id": 4,
                                                "name": "HR",
                                                "description": "I am HR",
                                                "parent": 3,
                                                "allocated_budget_amount": 12436481,
                                                "children": [
                                                    {
                                                        "id": 5,
                                                        "name": "Current salary of permanent soldiers",
                                                        "description": "I am Current salary of permanent soldiers",
                                                        "parent": 4,
                                                        "allocated_budget_amount": 11171083,
                                                        "children": [],
                                                    },
                                                    {
                                                        "id": 6,
                                                        "name": "Current salary of Ministry of Defense employees",
                                                        "description": "I am Current salary of Ministry of Defense employees",
                                                        "parent": 4,
                                                        "allocated_budget_amount": 1265398,
                                                        "children": [],
                                                    },
                                                ],
                                            },
                                            {
                                                "id": 9,
                                                "name": "Pensions",
                                                "description": "I am Pensions",
                                                "parent": 3,
                                                "allocated_budget_amount": 8155592,
                                                "children": [
                                                    {
                                                        "id": 10,
                                                        "name": "Permanent soldiers pensions",
                                                        "description": "I am Permanent soldiers' pensions",
                                                        "parent": 9,
                                                        "allocated_budget_amount": 7780739,
                                                        "children": [],
                                                    },
                                                    {
                                                        "id": 11,
                                                        "name": "Retirement grants for permanent soldiers",
                                                        "description": "I am Retirement grants for permanent soldiers",
                                                        "parent": 9,
                                                        "allocated_budget_amount": 374853,
                                                        "children": [],
                                                    },
                                                ],
                                            },
                                        ],
                                    }
                                ],
                            }
                        ],
                    }
                ],
            }

            expected_votes = {
                "user1": {
                    "Security and public order": {
                        "Security": {
                            "Ministry of Defense": {
                                "HR": {
                                    "Current salary of permanent soldiers": 11171083,
                                    "Current salary of Ministry of Defense employees": 1265398,
                                    "total": 12436481,
                                },
                                "Pensions": {
                                    "Permanent soldiers pensions": 7780739,
                                    "Retirement grants for permanent soldiers": 374853,
                                    "total": 8155592,
                                },
                                "total": 20592073,
                            },
                            "total": 20592073,
                        },
                        "total": 20592073,
                    },
                    "total": 20592073,
                },
                "user2": {
                    "Security and public order": {
                        "Security": {
                            "Ministry of Defense": {
                                "HR": {
                                    "Current salary of permanent soldiers": 11171083,
                                    "Current salary of Ministry of Defense employees": 1265398,
                                    "total": 12436481,
                                },
                                "Pensions": {
                                    "Permanent soldiers pensions": 7780739,
                                    "Retirement grants for permanent soldiers": 374853,
                                    "total": 8155592,
                                },
                                "total": 20592073,
                            },
                            "total": 20592073,
                        },
                        "total": 20592073,
                    },
                    "total": 20592073,
                },
            }

            votes = [votes1, votes2]
            updated_votes = unite_votes(votes)
            assert updated_votes == expected_votes
