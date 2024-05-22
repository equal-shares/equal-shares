from src.algorithm.only_example import example_add


def test_only_example() -> None:
    assert example_add(1, 2) == 3
    assert example_add(3, 4) == 7
    assert example_add(5, 6) == 11
