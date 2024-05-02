import streamlit as st
import requests
import google.generativeai as genai

# Set your Gemini API key
gemini_api_key = 'AIzaSyAaHXTSLHIQi0l0lEbhITSCIYzSQGeFP-I'

# Set up the Generative AI model
genai.configure(api_key="AIzaSyAaHXTSLHIQi0l0lEbhITSCIYzSQGeFP-I")
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]
model = genai.GenerativeModel(model_name="gemini-1.0-pro", generation_config=generation_config, safety_settings=safety_settings)

# Sample fitness prompts
fitness_prompts = {
    ('sedentary', 'fitness'): "Generate a fitness workout routine for a sedentary lifestyle.",
    ('sedentary', 'weight_loss'): "Generate a weight loss workout routine for a sedentary lifestyle.",
    ('sedentary', 'muscle_gain'): "Generate a muscle gain workout routine for a sedentary lifestyle.",
    ('active', 'fitness'): "Generate a fitness workout routine for an active lifestyle.",
    ('active', 'weight_loss'): "Generate a weight loss workout routine for an active lifestyle.",
    ('active', 'muscle_gain'): "Generate a muscle gain workout routine for an active lifestyle."
}

# Sample workout data (replace with actual workout data)
workouts = {
    'fitness': ['Cardio', 'Strength Training', 'Yoga', 'Pilates'],
    'weight_loss': ['HIIT', 'Circuit Training', 'Running', 'Swimming'],
    'muscle_gain': ['Bodybuilding', 'Powerlifting', 'Weight Training', 'CrossFit']
}

def generate_workout_prompt(lifestyle, fitness_goal, equipment_choice, current_weight, target_weight):
    prompt_key = (lifestyle, fitness_goal)
    if prompt_key in fitness_prompts:
        prompt = fitness_prompts[prompt_key]
        prompt += f" Current weight: {current_weight} kg. Target weight: {target_weight} kg."
        return prompt
    else:
        return ""

def generate_workout(prompt):
    # Use Generative AI model to generate workout
    convo = model.start_chat(history=[])
    convo.send_message(prompt)
    return convo.last.text

def main():
    # Add background image and change text color to black
    st.markdown(
        """
        <style>
        body {
            color: black;
            background-image: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcStfl41D7VQFr1WwBq3_nAQppO5jkoKxGKmIpavQI58hrYfK3-gibsfLi1sg991931NUo4&usqp=CAU");
            background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title('Workout Generator')
    lifestyle = st.selectbox('Select Lifestyle', ('sedentary', 'active'))
    fitness_goal = st.selectbox('Select Fitness Goal', ('fitness', 'weight_loss', 'muscle_gain'))
    equipment_choice = st.selectbox('Select Equipment Choice', ('gym equipment', 'home workout tools', 'no equipment'))
    current_weight = st.number_input('Enter Your Current Weight (kg)')
    target_weight = st.number_input('Enter Your Target Weight (kg)')
    if st.button('Generate Workout'):
        prompt = generate_workout_prompt(lifestyle, fitness_goal, equipment_choice, current_weight, target_weight)
        if prompt:
            workout = generate_workout(prompt)
            st.success('Workout Generated:')
            st.write(workout)
        else:
            st.error('Invalid fitness goal.')

if __name__ == '__main__':
    main()
