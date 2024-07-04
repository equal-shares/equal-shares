from src.algorithm.public import AlgorithmInput, ProjectItem, VouterItem, run_algorithm


def test_run_algorithm_passed() -> None:
    algorithm_input = AlgorithmInput(
        projects=[
            ProjectItem(project_id=11, min_cost=100, max_cost=100),
            ProjectItem(project_id=12, min_cost=100, max_cost=100),
        ],
        voutes=[
            VouterItem(vouter_id=1, voutes={11: 200}),
            VouterItem(vouter_id=2, voutes={12: 200}),
        ],
        budget=300,
    )

    run_algorithm(algorithm_input)

    # TODO: implement assertions
