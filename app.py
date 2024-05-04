import streamlit as st
import google.generativeai as genai
import pandas as pd

# Set up the Generative AI model
genai.configure(api_key="AIzaSyAaHXTSLHIQi0l0lEbhITSCIYzSQGeFP-I")
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

# Sample fitness prompts
fitness_prompts = {
    ("sedentary", "fitness"): "Generate an in-depth table for workout plan and an in-depth table for a diet plan for a sedentary lifestyle.",
    ("sedentary", "weight_loss"): "Generate an in-depth table for workout plan and an in-depth table for a diet plan for weight loss in a sedentary lifestyle.",
    ("sedentary", "muscle_gain"): "Generate an in-depth table for workout plan and an in-depth table for a diet plan for muscle gain in a sedentary lifestyle.",
    ("active", "fitness"): "Generate an in-depth table for workout plan and an in-depth table for a diet plan for an active lifestyle.",
    ("active", "weight_loss"): "Generate an in-depth table for workout plan and an in-depth table for a diet plan for weight loss in an active lifestyle.",
    ("active", "muscle_gain"): "Generate an in-depth table for workout plan and an in-depth table for a diet plan for muscle gain in an active lifestyle.",
}


def generate_workout_prompt(lifestyle, fitness_goal, equipment_choice, current_weight, target_weight, age, height,
                            food_choice, health_problems):
    prompt_key = (lifestyle, fitness_goal)
    if prompt_key in fitness_prompts:
        prompt = fitness_prompts[prompt_key]
        prompt += f"\n\nPersonal Details:\nAge: {age} years\nHeight: {height} cm\nFood Choice: {food_choice}\nHealth Problems: {health_problems}\n\nCurrent Weight: {current_weight} kg. Target Weight: {target_weight} kg."
        return prompt
    else:
        return ""


def generate_workout(prompt):
    convo = model.start_chat(history=[])
    convo.send_message(prompt)
    return convo.last.text


def main():
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

    st.title('Personalized Fitness Coach')
    lifestyle = st.selectbox('Select Lifestyle', ('sedentary', 'active'))
    fitness_goal = st.selectbox('Select Fitness Goal', ('fitness', 'weight_loss', 'muscle_gain'))
    equipment_choice = st.selectbox('Select Equipment Choice', ('gym equipment', 'home workout tools', 'no equipment'))
    current_weight = st.number_input('Enter Your Current Weight (kg)')
    target_weight = st.number_input('Enter Your Target Weight (kg)')
    age = st.number_input('Enter Your Age')
    height = st.number_input('Enter Your Height (cm)')
    food_choice = st.selectbox('Choose Food Preference', ('Vegetarian', 'Non-Vegetarian'))
    health_problems = st.text_input('Any Health Problems?')

    # Display summary of entered details
    st.subheader('Summary of Entered Details:')
    details_summary = {'Age': age, 'Height': height, 'Current Weight': current_weight, 'Target Weight': target_weight,
                       'Food Choice': food_choice, 'Health Problems': health_problems}
    details_df = pd.DataFrame.from_dict(details_summary, orient='index', columns=['Value'])
    st.table(details_df)

    if st.button('Generate Personalized Plan'):
        prompt = generate_workout_prompt(lifestyle, fitness_goal, equipment_choice, current_weight, target_weight, age,
                                         height, food_choice, health_problems)
        response = generate_workout(prompt)

        st.success('Personalized Plan Generated:')
        st.subheader('Generated Plan:')
        st.write(response)

if __name__ == '__main__':
    main()
