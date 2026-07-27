import ipywidgets as widgets
from IPython.display import display, clear_output, HTML
import numpy as np

# Create input fields with better descriptions
age_in = widgets.IntSlider(
    value=30, min=10, max=80, description='Age:', 
    style={'description_width': '100px'}
)
gender_in = widgets.Dropdown(
    options=[('Male', 1), ('Female', 0)], 
    description='Gender:',
    style={'description_width': '100px'}
)
rem_in = widgets.FloatSlider(
    value=20, min=0, max=100, description='REM %:', 
    style={'description_width': '100px'}
)
deep_in = widgets.FloatSlider(
    value=50, min=0, max=100, description='Deep %:', 
    style={'description_width': '100px'}
)
light_in = widgets.FloatSlider(
    value=30, min=0, max=100, description='Light %:', 
    style={'description_width': '100px'}
)
awake_in = widgets.IntSlider(
    value=1, min=0, max=10, description='Awakenings:', 
    style={'description_width': '100px'}
)
smoke_in = widgets.Dropdown(
    options=[('Yes', 1), ('No', 0)], 
    description='Smoker:',
    style={'description_width': '100px'}
)
caff_in = widgets.FloatSlider(
    value=0, min=0, max=500, description='Caffeine (mg):', 
    style={'description_width': '100px'}
)
alc_in = widgets.FloatSlider(
    value=0, min=0, max=10, description='Alcohol (oz):', 
    style={'description_width': '100px'}
)
exe_in = widgets.IntSlider(
    value=3, min=0, max=7, description='Exercise/wk:', 
    style={'description_width': '100px'}
)

button = widgets.Button(
    description="Predict Sleep Efficiency", 
    button_style='success',
    tooltip='Click to predict your sleep efficiency'
)
reset_button = widgets.Button(
    description="Reset to Defaults",
    button_style='info'
)
output = widgets.Output()

def on_button_clicked(b):
    with output:
        clear_output()
        
        try:
            # Validate sleep percentages sum to reasonable value
            total_sleep_pct = rem_in.value + deep_in.value + light_in.value
            if total_sleep_pct > 105 or total_sleep_pct < 95:
                print("⚠️ Warning: Sleep stage percentages should sum to ~100%")
                print(f"   Current total: {total_sleep_pct:.1f}%\n")
            
            # Arrange inputs for the model (must match training feature order)
            user_data = np.array([[
                age_in.value, 
                gender_in.value, 
                rem_in.value, 
                deep_in.value,
                light_in.value, 
                awake_in.value, 
                smoke_in.value,
                caff_in.value, 
                alc_in.value, 
                exe_in.value
            ]])
            
            # Scale the input
            user_scaled = scaler.transform(user_data)
            
            # Predict
            prediction = final_model.predict(user_scaled)[0]
            
            # Display results with styling
            print("=" * 50)
            print("🛏️  SLEEP EFFICIENCY PREDICTION")
            print("=" * 50)
            print(f"\n✨ Estimated Sleep Efficiency: {prediction:.1%}\n")
            
            # Provide personalized feedback
            if prediction > 0.85:
                status = "Excellent Sleep Quality! 🌙"
                color = "green"
                advice = "Keep up your current sleep habits!"
            elif prediction > 0.75:
                status = "Good Sleep Quality. 👍"
                color = "blue"
                advice = "Your sleep is healthy. Minor improvements possible."
            elif prediction > 0.65:
                status = "Fair Sleep Quality. 😴"
                color = "orange"
                advice = "Consider adjusting some habits for better sleep."
            else:
                status = "Poor Sleep Quality. ⚠️"
                color = "red"
                advice = "Significant improvements recommended."
            
            print(f"Status: {status}")
            print(f"Recommendation: {advice}")
            
            # Provide specific suggestions
            print("\n" + "=" * 50)
            print("💡 PERSONALIZED SUGGESTIONS:")
            print("=" * 50)
            
            suggestions = []
            if deep_in.value < 15:
                suggestions.append("• Increase deep sleep % (more exercise, cooler room)")
            if rem_in.value < 20:
                suggestions.append("• Increase REM sleep % (better sleep hygiene)")
            if awake_in.value > 2:
                suggestions.append("• Reduce awakenings (limit caffeine, check sleep environment)")
            if caff_in.value > 200:
                suggestions.append("• Reduce caffeine intake (especially after 2 PM)")
            if alc_in.value > 3:
                suggestions.append("• Reduce alcohol consumption (disrupts sleep quality)")
            if exe_in.value < 3:
                suggestions.append("• Increase exercise frequency (at least 3x/week)")
            
            if suggestions:
                for suggestion in suggestions:
                    print(suggestion)
            else:
                print("• Your habits look great! Maintain your current routine.")
            
            print("=" * 50)
            
        except Exception as e:
            print(f"❌ Error making prediction: {str(e)}")
            print("Please ensure the model and scaler are properly loaded.")

def on_reset_clicked(b):
    age_in.value = 30
    gender_in.value = 1
    rem_in.value = 20
    deep_in.value = 50
    light_in.value = 30
    awake_in.value = 1
    smoke_in.value = 0
    caff_in.value = 0
    alc_in.value = 0
    exe_in.value = 3
    with output:
        clear_output()

button.on_click(on_button_clicked)
reset_button.on_click(on_reset_clicked)

# Create organized layout
input_section = widgets.VBox([
    widgets.HTML("<h3>📊 Sleep Metrics Input</h3>"),
    widgets.HBox([age_in, gender_in]),
    widgets.HTML("<h4>Sleep Stages (should sum to ~100%)</h4>"),
    widgets.HBox([rem_in, deep_in, light_in]),
    widgets.HBox([awake_in]),
    widgets.HTML("<h4>Lifestyle Factors</h4>"),
    widgets.HBox([smoke_in, caff_in, alc_in, exe_in]),
])

button_section = widgets.HBox([button, reset_button])

ui = widgets.VBox([
    input_section,
    button_section,
    output
], layout=widgets.Layout(padding='20px', border='1px solid #ddd'))

display(ui)