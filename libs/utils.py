import os


class EnvironmentException(Exception):
    pass


def get_env_variable(variable_name: str):
    """Safely load environment variable from system environment."""
    variable = os.environ.get(variable_name, None)
    if variable is None:
        raise EnvironmentException(
            "Cannot find variable. Run 'printenv' in terminal to check if variable exists."
        )
    return variable
