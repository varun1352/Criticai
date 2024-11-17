from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import os
from crewai_tools import VisionTool, PDFSearchTool
import logging
import yaml
import os
import glob

llm = LLM(
    model="cerebras/llama3.1-8b",
    base_url="https://api.cerebras.ai/v1",
    api_key=os.getenv("CEREBRAS_API_KEY")
)

@CrewBase
class MarketingCampaignCriticCrew:
    """Crew for critiquing a marketing campaign with demographic-specific agents and a Master Agent."""

    def __init__(self, image_path=None, pdf_path=None, agents_config=None):
        super().__init__()
        self.image_path = image_path
        self.pdf_path = pdf_path
        self.agents_config = agents_config or {}

        # Load tasks.yaml
        with open('src/marketing_campaign_critic/config/tasks.yaml', 'r') as task_file:
            self.task_data = yaml.safe_load(task_file)

        # Validate agent configs
        for agent_name, config in self.agents_config.items():
            if not all(k in config for k in ["role", "goal", "backstory"]):
                raise ValueError(f"Agent '{agent_name}' is missing required fields: {config}")
            logging.debug(f"Validated Agent Config for '{agent_name}': {config}")

    @agent
    def master_reviewer(self) -> Agent:
        tools = []
        if self.image_path:
            tools.append(VisionTool(image_path_url=self.image_path))
        if self.pdf_path:
            tools.append(PDFSearchTool(pdf=self.pdf_path))
        return Agent(
            config={
                "role": "Generalist Marketing Reviewer",
                "goal": """Provide an unbiased, concise summary of the marketing campaign's effectiveness based on personal review and the review provided by the other reviewers, and at the same time list the scores 
                        provided by every single reviewer, and in the case of no reviewers, provide a score based on personal perspective .""",
                "backstory": "An experienced marketing expert with a neutral perspective."
            },
            verbose=True,
            llm=llm,
            tools=tools
        )

    def clear_output_directory(self):
        files = glob.glob('output/*.md')
        for f in files:
            os.remove(f)

    def user_agents(self) -> list[Agent]:
        """Dynamically creates agents based on user-defined configurations."""
        agents = []
        agents_config = self.agents_config['agents']
        for agent_name, config in agents_config.items():
            tools = []
            if self.image_path:
                tools.append(VisionTool(image_path_url=self.image_path))
            if self.pdf_path:
                tools.append(PDFSearchTool(pdf=self.pdf_path))
            agents.append(Agent(
                config={
                    "role": config["role"],
                    "goal": config["goal"],
                    "backstory": config["backstory"]
                },
                verbose=True,
                llm=llm,
                tools=tools
            ))
        return agents

    @task
    def master_review_task(self) -> Task:
        """Task for the Master Agent to summarize the overall review."""
        return Task(
            config={
                "description": """Generate a comprehensive summary review of the reviews given by each of the other agents and if there are no other agents provide an independent evaluation.""",
                "expected_output": "An unbiased markdown report on the campaign's strengths and weaknesses."
            },
            agent=self.master_reviewer(),
            output_file='output/master_feedback.md'
        )

    def user_agent_tasks(self) -> list[Task]:
        """Creates tasks for each user-defined agent."""
        tasks = []
        for agent in self.user_agents():  # Make sure to call the method
            if agent.role != 'Generalist Marketing Reviewer':
                task_config = self.task_data['tasks']['campaign_review']
                tasks.append(Task(
                    config=task_config,
                    agent=agent,
                    output_file=f"output/{agent.role}_feedback.md"
                ))
        return tasks

    @crew
    def crew(self) -> Crew:
        """Creates the MarketingCampaignCritic crew."""
        all_agents = self.user_agents()  # List of user agents
        all_agents.append(self.master_reviewer())  # Add the master reviewer at the end of the list

        all_tasks = [self.master_review_task()] + self.user_agent_tasks()  # Include all tasks
        self.clear_output_directory()
        return Crew(
            agents=all_agents,  # Ensure agents is a valid list
            tasks=all_tasks,
            process=Process.sequential,
            verbose=True
        )
    
    
