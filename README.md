# Critic.ai

## Overview
Critic.ai is a sophisticated marketing campaign analysis tool designed to simulate and critique marketing campaigns using AI-driven insights. The application leverages advanced AI models to provide demographic-specific feedback, making it an invaluable asset for small-scale agencies and individual marketers seeking to optimize their marketing strategies and enhance campaign effectiveness.

## Features
- **Demographic-Specific Analysis**: Tailors feedback based on different demographic profiles to provide targeted insights into the potential reception of marketing campaigns.
- **Comprehensive Feedback**: Combines the capabilities of various AI agents to critique different aspects of a campaign, from visual appeal to content relevance.
- **Intuitive User Interface**: Features a user-friendly interface that makes it easy for users to input campaign details and receive structured feedback.
- **Scalable Architecture**: Built to handle multiple users and sessions simultaneously, ensuring a responsive experience across various devices.

## Technology Stack
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask (Python)
- **AI Models**: Integrated with CrewAI for advanced data processing and analysis.
- **Database**: (Optional - describe any database used like MySQL, PostgreSQL, etc.)
- **Deployment**: Docker, (and any cloud platforms used, like AWS, GCP, etc.)

## Getting Started

### Prerequisites
- Python 3.11 or higher
- Flask
- crewai


### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/varun1352/Critic.ai.git
   cd Critic.ai
   pip install flask
   pip install crewai
   ```

2. **Set up a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Environment Variables**:
   Set up the necessary environment variables or use a `.env` file to load them.

4. **Run the application**:
   ```bash
   flask run
   ```

## Usage
After starting the application, navigate to `http://localhost:5000` in your web browser to start using Critic.ai. Follow the on-screen instructions to input your marketing campaign details and receive feedback.

## Contributing
Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
Distributed under the MIT License. See `LICENSE` for more information.

## Contact
Varun Deliwala - [your-email@example.com](mailto:varundeliwala@gmail.com) - email address

Project Link: [https://github.com/varun1352/Critic.ai](https://github.com/varun1352/Critic.ai)

## Acknowledgements
- CrewAI
- Flask
- Contributors who participated in this project.
```

This README template includes basic instructions and descriptions. Adjust the content to include any specific installation steps, external service configurations, or environmental variables that might be necessary for your application.
