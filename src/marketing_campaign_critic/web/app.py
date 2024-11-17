from flask import Flask, render_template, request, redirect, url_for
import os, sys
import logging
from marketing_campaign_critic.main import run
from marketing_campaign_critic.web.utils.yaml_generator import generate_yaml_files
from marketing_campaign_critic.web.utils.agent_templates import AGENT_TEMPLATES
import markdown


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)

app = Flask(__name__,
            static_folder=os.path.join(current_dir, "static"),
            template_folder=os.path.join(current_dir, "templates"))


print("Flask working directory:", os.getcwd())

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)


def render_markdown(file_path):
    with open(file_path, 'r') as md_file:
        text = md_file.read()
        return markdown.markdown(text)
    
@app.route('/')
def landing():
    return render_template('landing.html', title="Home")

@app.route('/about')
def about():
    return render_template('about.html', title="About")

@app.route('/campaign-form')
def index():
    return render_template('index.html', title="Campaigns")

@app.route('/run-crew', methods=['POST'])
def run_crew():
    # Basic campaign information
    campaign_name = request.form.get('campaign_name')
    company_name = request.form.get('company_name')
    campaign_description = request.form.get('campaign_description')
    product_name = request.form.get('product_name')
    product_description = request.form.get('product_description')
    age_group = request.form.get('age_group')
    location = request.form.get('location')
    interests = request.form.get('interests')
    income_bracket = request.form.get('income_bracket')
    image_file = request.files.get('image_file')

    # Capture base agents selected for customization
    selected_base_agents = request.form.getlist('base_agent[]')

    # Capture custom/new agents
    agent_names = request.form.getlist('agent_name[]')
    agent_roles = request.form.getlist('agent_role[]')
    agent_goals = request.form.getlist('agent_goal[]')
    agent_backstories = request.form.getlist('agent_backstory[]')

    # Save the image if provided
    image_path = None
    if image_file:
        image_path = os.path.join("output", "campaign_image.jpg")
        image_file.save(image_path)

    # Construct agent data (flat dictionary structure)
    agent_data = {}

    # Process selected base agents with optional modifications
    for base_agent_name in selected_base_agents:
        base_template = AGENT_TEMPLATES[base_agent_name]
        if not base_template:
            raise ValueError(f"Base agent '{base_agent_name}' not found in templates.")
        agent_data[base_agent_name] = {
            "role": base_template["role"],
            "goal": base_template["goal"],
            "backstory": base_template["backstory"]
        }

    agent_data['master_reviewer'] = {
        "role": "Generalist Marketing Reviewer",
        "goal": """Provide an unbiased, concise summary of the marketing campaign's effectiveness, and at the same time list the scores 
                provided by every single reviewer, and in the case of no reviewers, provide a score based on personal perspective .""",
        "backstory": "An experienced marketing expert with a neutral perspective."
    }

    # Process additional or customized agents
    for i in range(len(agent_names)):
        agent_name = agent_names[i]
        role = agent_roles[i] or "Default role"
        goal = agent_goals[i] or "Default goal"
        backstory = agent_backstories[i] or "Default backstory"

        agent_data[agent_name] = {
            "role": role,
            "goal": goal,
            "backstory": backstory
        }

    # Log agent data for debugging
    logging.debug(f"Constructed Agent Data: {agent_data}")

    inputs = {
        "campaign_name": campaign_name,
        "company_name": company_name,
        "campaign_description": campaign_description,
        "product_name": product_name,
        "product_description": product_description,
        "age_group": age_group,
        "location": location,
        "interests": interests,
        "income_bracket": income_bracket,
    }
    logging.debug(f"Inputs: {inputs}")

    # Define a single task for all agents to perform the campaign review
    task_data = {
        "campaign_review": {
            "description": f"""
            Analyze the marketing campaign '{campaign_name}' by {company_name} for their product '{product_name}'.
            The campaign is targeted at {age_group} audiences in {location} with interests in {interests}.
            
            As an agent with your backstory, your review should reflect your unique perspective. 
            Please make sure to evaluate the campaign from the angle of your backstory and role without introducing general assumptions.
            
            **Campaign Overview:**
            - **Campaign Name**: {campaign_name}
            - **Company**: {company_name}
            - **Campaign Description**: {campaign_description}
            
            **Product Details:**
            - **Product Name**: {product_name}
            - **Product Description**: {product_description}
            
            **Target Audience:**
            - **Age Group**: {age_group}
            - **Location**: {location}
            - **Interests**: {interests}
            - **Income Bracket**: {income_bracket}
            
            Your role requires you to assess this campaign based on how it resonates with the target audience from your unique perspective. 
            Please analyze this campaign's strengths, weaknesses, appeal, and engagement through the lens of your personal backstory and role.
            """,
            "expected_output": """
            Provide a structured markdown report following this format(please dont change the format of the report that your produce and follow this):

            - **Score**: Provide a score (out of 10) based on the campaign’s effectiveness and alignment with the target audience.
            - **Campaign Strengths**: Identify aspects of the campaign that align well with your perspective and the target audience.
            - **Campaign Weaknesses**: Highlight any gaps or shortcomings that are apparent from your expertise and experience.
            - **Appeal and Engagement**: Evaluate how engaging the campaign is, considering the target audience's interests and your viewpoint.
            - **Recommendations for Improvement**: Offer actionable suggestions for enhancing the campaign, drawing from your own professional background.
            
            Please use only the provided campaign details and any images (if available) to guide your review. Your analysis should be thoughtful, concise, and based on your specific perspective.
            """
        }
    }

    # Generate YAML files
    generate_yaml_files(agent_data, task_data)

    # Run the crew
    
    run(inputs=inputs, image_path=image_path)  # This should now pass the inputs correctly
    # except Exception as e:
    #     logging.error(f"An error occurred: {e}")
    #     print(f"An error occurred: {e}")
    
    return redirect(url_for('results'))

@app.route('/results')
def results():
    feedback_reports = []

    # Load the master feedback
    master_feedback = render_markdown("output/master_feedback.md")
    feedback_reports.append({"name": "master_feedback.md", "content": master_feedback})

    # Load agent-specific feedback
    for feedback_file in os.listdir("output"):
        if feedback_file.endswith(".md") and feedback_file != "master_feedback.md":
            agent_feedback = render_markdown(f"output/{feedback_file}")
            feedback_reports.append({"name": feedback_file, "content": agent_feedback})

    return render_template('results.html', feedback_reports=feedback_reports)

@app.route('/output/<filename>')
def serve_markdown(filename):
    # Check if the file exists in the 'output' directory
    file_path = os.path.join('output', filename)
    if os.path.exists(file_path) and filename.endswith('.md'):
        with open(file_path, 'r') as md_file:
            return markdown.markdown(md_file.read())
    else:
        return "File not found", 404

@app.context_processor
def inject_current_year():
    from datetime import datetime
    return {'current_year': datetime.now().year}

if __name__ == '__main__':
    app.run(debug=True)


