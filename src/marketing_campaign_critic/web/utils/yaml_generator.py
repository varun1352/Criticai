import yaml
import os

def get_project_root():
    """Get the absolute path to the project root directory"""
    current_dir = os.path.dirname(os.path.abspath(__file__))  # utils directory
    web_dir = os.path.dirname(current_dir)  # web directory
    project_dir = os.path.dirname(web_dir)  # marketing_campaign_critic directory
    return project_dir

def ensure_config_directory():
    """Ensure the config directory exists"""
    config_dir = os.path.join(get_project_root(), "config")
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    return config_dir

def validate_data(data, required_keys):
    """Validate that all required keys are present in the given data dictionary."""
    missing_keys = [key for key in required_keys if key not in data]
    if missing_keys:
        raise ValueError(f"Missing required keys: {', '.join(missing_keys)}")

def generate_yaml_files(agent_data, task_data):
    """
    Validate and generate agents.yaml and tasks.yaml files.

    Parameters:
        agent_data (dict): A dictionary containing agent configurations.
        task_data (dict): A dictionary containing task configurations.

    Returns:
        tuple: Paths to the generated agents.yaml and tasks.yaml files

    Raises:
        ValueError: If required keys are missing in agent or task data.
        OSError: If there are issues creating directories or writing files.
    """
    # Validate agent data
    for agent_name, agent_details in agent_data.items():
        try:
            validate_data(agent_details, ["role", "goal", "backstory"])
        except ValueError as e:
            raise ValueError(f"Error in agent '{agent_name}': {e}")

    # Validate task data
    for task_name, task_details in task_data.items():
        try:
            validate_data(task_details, ["description", "expected_output"])
        except ValueError as e:
            raise ValueError(f"Error in task '{task_name}': {e}")

    # Ensure config directory exists
    config_dir = ensure_config_directory()

    # Generate agents.yaml
    agents_path = os.path.join(config_dir, "agents.yaml")
    with open(agents_path, "w") as agent_file:
        yaml.dump({"agents": agent_data}, agent_file, default_flow_style=False)

    # Generate tasks.yaml
    tasks_path = os.path.join(config_dir, "tasks.yaml")
    with open(tasks_path, "w") as task_file:
        yaml.dump({"tasks": task_data}, task_file, default_flow_style=False)

    return agents_path, tasks_path