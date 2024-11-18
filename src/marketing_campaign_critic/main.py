#!/usr/bin/env python
import sys
from marketing_campaign_critic.crew import MarketingCampaignCriticCrew

def run(inputs, image_path=None, pdf_path=None):
    """
    Run the crew with marketing campaign details and custom demographics.
    :param inputs: A dictionary containing campaign details.
    :param image_path: Optional path to the uploaded campaign image.
    :param pdf_path: Optional path to the uploaded campaign PDF.
    """
    if not isinstance(inputs, dict):
        raise ValueError("Expected a dictionary for 'inputs', but got {type(inputs)}")
    
    
    # Initialize the crew with paths and inputs
    crew_instance = MarketingCampaignCriticCrew(image_path=image_path, pdf_path=pdf_path, inputs=inputs)
    crew_instance.crew().kickoff()
    

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        MarketingCampaignCriticCrew().crew().train(
            n_iterations=int(sys.argv[1]),
            filename=sys.argv[2],
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        MarketingCampaignCriticCrew().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and return the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        MarketingCampaignCriticCrew().crew().test(
            n_iterations=int(sys.argv[1]),
            openai_model_name=sys.argv[2],
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


if __name__ == "__main__":
    # Mapping CLI commands to functions
    command_map = {
        "run": run,
        "train": train,
        "replay": replay,
        "test": test,
    }

    if len(sys.argv) < 2 or sys.argv[1] not in command_map:
        print("Usage: main.py [run|train|replay|test] [arguments...]")
        sys.exit(1)

    # Execute the selected command
    command = sys.argv[1]
    command_map[command]()
