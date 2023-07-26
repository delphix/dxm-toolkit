def pytest_addoption(parser):
    parser.addoption(
        "--engine",
        action="append",
        default=[]
    )


def pytest_generate_tests(metafunc):
    if "engine" in metafunc.fixturenames:
        metafunc.parametrize("engine", metafunc.config.getoption("engine"))