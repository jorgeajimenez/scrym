"""
Gemini Assistant Coach Service
Uses Google's Gemini 1.5 Pro to synthesize analytics into natural language coaching advice.
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv
from data_loader import NFLDataLoader

# Configure API
load_dotenv()
API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

class GeminiCoach:
    def __init__(self):
        self.data_loader = NFLDataLoader()
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest') if API_KEY else None

    def analyze_situation(self, state, analytics_recommendation, team_abbr="KC"):
        """
        Generates a text summary of the decision.
        """
        if not self.model:
            return "Gemini API Key not configured. Please set GEMINI_API_KEY environment variable."

        # 1. Get Context
        starters = self.data_loader.get_team_starters(team_abbr)
        qb_name = starters.get('QB', ['the QB'])[0]
        rb_name = starters.get('RB', ['the RB'])[0]
        
        # 2. Construct Prompt
        prompt = f"""
        You are an elite NFL Offensive Coordinator assisting the Head Coach.
        
        **Current Situation:**
        - Down: {state.down} & {state.ydstogo}
        - Field Position: Opponent {state.yardline_100} yard line
        - Score: {state.score_differential} (We are {'leading' if state.score_differential > 0 else 'trailing'})
        - Time Remaining: {state.game_seconds_remaining} seconds
        - Quarter: {state.qtr}
        
        **Team Context:**
        - QB: {qb_name}
        - RB: {rb_name}
        
        **Analytics Model Recommendation:**
        - The Math says: {analytics_recommendation}
        
        **Your Task:**
        1. Review the analytics recommendation. Is it sound?
        2. Provide a 2-sentence "Coach's Summary" explaining WHY we should do this, citing specific situational details.
        3. Mention the key players ({qb_name}/{rb_name}) if relevant to the play type.
        
        Keep it punchy, professional, and decisive.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating analysis: {str(e)}"

# Singleton for reuse
coach_ai = GeminiCoach()
