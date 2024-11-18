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

    def __init__(self, image_path=None, pdf_path=None, agents_config=None, inputs = {}):
        super().__init__()
        self.image_path = image_path
        self.pdf_path = pdf_path
        self.agents_config = agents_config or {}
        self.inputs = inputs

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
                "description": f"""
                You are tasked with generating a comprehensive and detailed summary review of the marketing campaign. Your task includes:

                1. **Inputs Summary**: Provide a clear summary of the details provided for the campaign. This includes the campaign name, company name, product details, target audience, and additional information like the image and PDF if available. 
                    - If an image is provided, describe its content and how it aligns with the campaign.
                    - If a PDF is provided, summarize the main points covered in the document.
                
                2. **Agent Feedback Aggregation**: Collect and aggregate the reviews provided by all other agents. This includes:
                    - Listing the scores given by each agent and calculating the average score.
                    - Highlighting key strengths, weaknesses, and recommendations mentioned by the agents.

                3. **Independent Evaluation**: If no other agents have provided reviews, generate an independent evaluation of the campaign based on the provided inputs. Use the same structure as an individual agent review.

                4. **Comprehensive Summary**: Provide your final, unbiased review of the campaign. This should:
                    - Synthesize the agent reviews (if available).
                    - Highlight the campaign's overall strengths and weaknesses.
                    - Provide actionable recommendations for improving the campaign.

                Please format the report as a structured markdown document using the following format:

                ```
                # Master Reviewer Summary

                ## Inputs Summary
                - **Campaign Name**: {self.inputs['campaign_name']}
                - **Company Name**: {self.inputs['company_name']}
                - ** Campaign Description**: {self.inputs['campaign_description']}
                - **Product Name**: {self.inputs['product_name']}
                - **Product Description**: {self.inputs['product_description']}
                - **Target Audience**:
                    - Age Group: {self.inputs['age_group']}
                    - Location: {self.inputs['location']}
                    - Interests: {self.inputs['interests']}
                    - Income Bracket: {self.inputs['income_bracket']}
                - **Image Description**: [Brief description of the provided image or 'No image provided']
                - **PDF Summary**: [Brief summary of the PDF content or 'No PDF provided']

                ## Agent Feedback
                - **Scores**:
                    - Agent 1: [Score]
                    - Agent 2: [Score]
                    - ...
                - **Average Score**: [Calculated Average]
                - **Key Strengths**: 
                    - [Key strength 1]
                    - [Key strength 2]
                - **Key Weaknesses**:
                    - [Key weakness 1]
                    - [Key weakness 2]
                - **Recommendations**:
                    - [Recommendation 1]
                    - [Recommendation 2]

                ## Independent Evaluation (if applicable)
                - **Score**: [Score out of 10]
                - **Strengths**: [Strengths based on provided inputs]
                - **Weaknesses**: [Weaknesses based on provided inputs]
                - **Recommendations**: [Suggestions for improvement]

                ## Final Summary
                - **Overall Strengths**: [Summary of strengths]
                - **Overall Weaknesses**: [Summary of weaknesses]
                - **Actionable Recommendations**: [Final suggestions for improvement]
                ```
                """,
                "expected_output": """
                A detailed markdown report including:
                - Summary of campaign inputs (details, image, PDF).
                - Aggregated scores and insights from all agents.
                - Independent evaluation if no agent reviews are available.
                - Final comprehensive summary including strengths, weaknesses, and actionable recommendations.
                """
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
    
    
