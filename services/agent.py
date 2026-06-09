import os
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
from extract_resume_data import extract_text_from_resume

# Load environment variables from .env file
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("API_KEY")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")
MODEL = os.getenv("MODEL")

# Create Crew and add agents
class ResumeReviewCrew:
    def __init__(self):
        # Initialize agents
        self.feedback_agent = Agent(
            role="Professional Resume Advisor",
            goal="Give feedback on the resume to make it stand out in the job market.",
            model=MODEL,
            verbose=True,
            backstory="With a strategic mind and an eye for detail, you excel at providing feedback on resumes to highlight the most relevant skills and experiences."
        )
        
        self.improvement_agent = Agent(
            role="Professional Resume Writer",
            goal="Based on the feedback received from Resume Advisor, make changes to the resume to make it stand out in the job market.",
            model=MODEL,
            verbose=True,
            backstory="With a strategic mind and an eye for detail, you excel at refining resumes based on the feedback to highlight the most relevant skills and experiences."
        )
        
        self.serper_tool = SerperDevTool()
        self.research_agent = Agent(
            role="Senior Recruitment Consultant",
            goal="Find the 5 most relevant, recently posted jobs based on the improved resume received from resume advisor and the location preference",
            tools=[self.serper_tool],
            model=MODEL,
            verbose=True,
            backstory="""As a senior recruitment consultant your prowess in finding the most relevant jobs based on the resume and location preference is unmatched. 
            You can scan the resume efficiently, identify the most suitable job roles and search for the best suited recently posted open job positions at the preferred location."""
        )
        
        # Define tasks
        self.resume_feedback_task = Task(
            description=(
                """Give feedback on the resume to make it stand out for recruiters. 
                Review every section, including the summary, work experience, skills, and education. Suggest to add relevant sections if they are missing.  
                Also give an overall score to the resume out of 10. This is the resume: {resume}"""
            ),
            expected_output="The overall score of the resume followed by the feedback in bullet points.",
            agent=self.feedback_agent
        )
        
        self.resume_improvement_task = Task(
            description=(
                """Rewrite the resume based on the feedback to make it stand out for recruiters. You can adjust and enhance the resume but don't make up facts. 
                Review and update every section, including the summary, work experience, skills, and education to better reflect the candidate's abilities. This is the resume: {resume}"""
            ),
            expected_output="Resume in markdown format that effectively highlights the candidate's qualifications and experiences",
            agent=self.improvement_agent,
            context=[self.resume_feedback_task]
        )
        
        self.search_task = Task(
            description="""Find the 5 most relevant recent job postings based on the resume received from resume advisor and location preference. This is the preferred location: {location}. 
                Use the tools to gather relevant content and shortlist the 5 most relevant, recent, job openings""",
            expected_output="A bullet point list of the 5 job openings, with the appropriate links and detailed description about each job, in markdown format",
            agent=self.research_agent
        )
        
        # Create crew with agents and tasks
        self.crew = Crew(
            agents=[self.feedback_agent, self.improvement_agent, self.research_agent],
            tasks=[self.resume_feedback_task, self.resume_improvement_task, self.search_task],
            verbose=True
        )
    
    def kickoff(self, inputs):
        """Run the crew with the provided inputs"""
        return self.crew.kickoff(inputs=inputs)
    

if __name__ == "__main__":
    resume_text = extract_text_from_resume("file_path_to_resume")
    crew = ResumeReviewCrew()
    result = crew.kickoff(inputs={
        "resume": resume_text,
        "location": "Pune"
    })
    print("Final Output:")
    print(result.output.raw if hasattr(result.output, 'raw') else str(result.output))
