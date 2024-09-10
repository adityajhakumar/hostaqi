import streamlit as st
import requests
import matplotlib.pyplot as plt

# Chat-based system introduction
st.title("🌱 Welcome to TERVIVE! 🌱")
st.write("Earn green credits by buying eco-friendly plants and improving air quality.")

# WAQI Demo Token (replace with your token if you have one)
TOKEN = 'demo'

# Thresholds for pollutant levels
pollutant_thresholds = {
    'aqi': [50, 100, 150, 200],
    'pm25': [12, 35, 55, 150],
    'pm10': [50, 150, 250, 350],
    'co': [1, 4, 9, 30],
    'no2': [53, 100, 360, 649],
    'o3': [60, 120, 180, 240],
    'so2': [75, 185, 304, 604]
}

# Plant database with 10 plants per pollutant, both indoor and outdoor plants of Indian origin
plant_database = {
    'co': {
        'Spider Plant': {'description': 'Absorbs CO (Indoor).', 'link': 'https://www.amazon.in/s?k=spider+plant'},
        'Aloe Vera': {'description': 'Absorbs CO and CO2 (Indoor).', 'link': 'https://www.amazon.in/s?k=aloe+vera+plant'},
        'Areca Palm': {'description': 'Filters carbon monoxide (Indoor).', 'link': 'https://www.amazon.in/s?k=areca+palm+plant'},
        'Money Plant': {'description': 'Reduces CO levels (Indoor).', 'link': 'https://www.amazon.in/s?k=money+plant'},
        'Snake Plant': {'description': 'Absorbs CO and produces oxygen at night (Indoor).', 'link': 'https://www.amazon.in/s?k=snake+plant'},
        'Gerbera Daisy': {'description': 'Removes CO from the air (Outdoor).', 'link': 'https://www.amazon.in/s?k=gerbera+daisy'},
        'Chrysanthemum': {'description': 'Effective against airborne toxins, including CO (Outdoor).', 'link': 'https://www.amazon.in/s?k=chrysanthemum+plant'},
        'Rubber Plant': {'description': 'Absorbs airborne toxins including CO (Indoor).', 'link': 'https://www.amazon.in/s?k=rubber+plant'},
        'Bamboo Palm': {'description': 'Filters out CO (Indoor).', 'link': 'https://www.amazon.in/s?k=bamboo+palm'},
        'Ficus': {'description': 'Absorbs CO and other pollutants (Indoor).', 'link': 'https://www.amazon.in/s?k=ficus+plant'}
    },
    'pm25': {
        'Rubber Plant': {'description': 'Filters PM2.5 (Indoor).', 'link': 'https://www.amazon.in/s?k=rubber+plant'},
        'Ficus': {'description': 'Removes dust particles (Indoor).', 'link': 'https://www.amazon.in/s?k=ficus+plant'},
        'Tulsi': {'description': 'Reduces airborne particles (Outdoor).', 'link': 'https://www.amazon.in/s?k=tulsi+plant'},
        'Neem': {'description': 'Absorbs particulate matter from the air (Outdoor).', 'link': 'https://www.amazon.in/s?k=neem+plant'},
        'Peace Lily': {'description': 'Filters fine particulate matter (Indoor).', 'link': 'https://www.amazon.in/s?k=peace+lily+plant'},
        'Boston Fern': {'description': 'Absorbs PM2.5 and improves air quality (Indoor).', 'link': 'https://www.amazon.in/s?k=boston+fern+plant'},
        'Aloe Vera': {'description': 'Absorbs fine particulate matter (Indoor).', 'link': 'https://www.amazon.in/s?k=aloe+vera+plant'},
        'Areca Palm': {'description': 'Removes dust particles and pollutants (Indoor).', 'link': 'https://www.amazon.in/s?k=areca+palm+plant'},
        'Golden Pothos': {'description': 'Effective for PM2.5 reduction (Indoor).', 'link': 'https://www.amazon.in/s?k=golden+pothos+plant'},
        'Spider Plant': {'description': 'Filters fine particles from the air (Indoor).', 'link': 'https://www.amazon.in/s?k=spider+plant'}
    },
    'pm10': {
        'Tulsi': {'description': 'Filters particulate matter (Outdoor).', 'link': 'https://www.amazon.in/s?k=tulsi+plant'},
        'Neem': {'description': 'Purifies the air and reduces PM10 (Outdoor).', 'link': 'https://www.amazon.in/s?k=neem+plant'},
        'Areca Palm': {'description': 'Removes dust particles (Indoor).', 'link': 'https://www.amazon.in/s?k=areca+palm+plant'},
        'Rubber Plant': {'description': 'Filters large dust particles (Indoor).', 'link': 'https://www.amazon.in/s?k=rubber+plant'},
        'Ficus': {'description': 'Absorbs large airborne particles (Indoor).', 'link': 'https://www.amazon.in/s?k=ficus+plant'},
        'Boston Fern': {'description': 'Absorbs PM10 from the air (Indoor).', 'link': 'https://www.amazon.in/s?k=boston+fern+plant'},
        'Peace Lily': {'description': 'Removes PM10 particles (Indoor).', 'link': 'https://www.amazon.in/s?k=peace+lily+plant'},
        'Snake Plant': {'description': 'Removes particulate matter from indoor air (Indoor).', 'link': 'https://www.amazon.in/s?k=snake+plant'},
        'Aloe Vera': {'description': 'Filters PM10 particles (Indoor).', 'link': 'https://www.amazon.in/s?k=aloe+vera+plant'},
        'Bamboo Palm': {'description': 'Reduces particulate matter (Indoor).', 'link': 'https://www.amazon.in/s?k=bamboo+palm'}
    },
    'no2': {
        'Peace Lily': {'description': 'Absorbs NO2 and improves indoor air (Indoor).', 'link': 'https://www.amazon.in/s?k=peace+lily+plant'},
        'Boston Fern': {'description': 'Removes NO2 from the air (Indoor).', 'link': 'https://www.amazon.in/s?k=boston+fern+plant'},
        'Spider Plant': {'description': 'Effective in absorbing nitrogen dioxide (Indoor).', 'link': 'https://www.amazon.in/s?k=spider+plant'},
        'Aloe Vera': {'description': 'Reduces nitrogen dioxide and other pollutants (Indoor).', 'link': 'https://www.amazon.in/s?k=aloe+vera+plant'},
        'Areca Palm': {'description': 'Filters nitrogen dioxide (Indoor).', 'link': 'https://www.amazon.in/s?k=areca+palm+plant'},
        'Chrysanthemum': {'description': 'Absorbs NO2 and other harmful gases (Outdoor).', 'link': 'https://www.amazon.in/s?k=chrysanthemum+plant'},
        'Snake Plant': {'description': 'Removes nitrogen dioxide from indoor air (Indoor).', 'link': 'https://www.amazon.in/s?k=snake+plant'},
        'Tulsi': {'description': 'Reduces nitrogen dioxide levels (Outdoor).', 'link': 'https://www.amazon.in/s?k=tulsi+plant'},
        'Neem': {'description': 'Purifies air by absorbing nitrogen dioxide (Outdoor).', 'link': 'https://www.amazon.in/s?k=neem+plant'},
        'Rubber Plant': {'description': 'Absorbs nitrogen dioxide and other pollutants (Indoor).', 'link': 'https://www.amazon.in/s?k=rubber+plant'}
    },
    'o3': {
        'Snake Plant': {'description': 'Removes ozone from the air (Indoor).', 'link': 'https://www.amazon.in/s?k=snake+plant'},
        'English Ivy': {'description': 'Reduces ozone levels indoors (Indoor).', 'link': 'https://www.amazon.in/s?k=english+ivy+plant'},
        'Aloe Vera': {'description': 'Absorbs ozone from the air (Indoor).', 'link': 'https://www.amazon.in/s?k=aloe+vera+plant'},
        'Spider Plant': {'description': 'Reduces ozone levels indoors (Indoor).', 'link': 'https://www.amazon.in/s?k=spider+plant'},
        'Peace Lily': {'description': 'Filters ozone from indoor air (Indoor).', 'link': 'https://www.amazon.in/s?k=peace+lily+plant'},
        'Chrysanthemum': {'description': 'Absorbs ozone and other toxins (Outdoor).', 'link': 'https://www.amazon.in/s?k=chrysanthemum+plant'},
        'Tulsi': {'description': 'Reduces ozone in outdoor air (Outdoor).', 'link': 'https://www.amazon.in/s?k=tulsi+plant'},
        'Neem': {'description': 'Absorbs harmful gases including ozone (Outdoor).', 'link': 'https://www.amazon.in/s?k=neem+plant'},
        'Areca Palm': {'description': 'Filters indoor ozone (Indoor).', 'link': 'https://www.amazon.in/s?k=areca+palm+plant'},
        'Ficus': {'description': 'Absorbs ozone and other air pollutants (Indoor).', 'link': 'https://www.amazon.in/s?k=ficus+plant'}
    },
    'so2': {
        'Neem': {'description': 'Removes SO2 from the air (Outdoor).', 'link': 'https://www.amazon.in/s?k=neem+plant'},
        'Tulsi': {'description': 'Absorbs SO2 and improves air quality (Outdoor).', 'link': 'https://www.amazon.in/s?k=tulsi+plant'},
        'Aloe Vera': {'description': 'Filters sulfur dioxide from indoor air (Indoor).', 'link': 'https://www.amazon.in/s?k=aloe+vera+plant'},
        'Spider Plant': {'description': 'Absorbs sulfur dioxide (Indoor).', 'link': 'https://www.amazon.in/s?k=spider+plant'},
        'Peace Lily': {'description': 'Removes SO2 from the air (Indoor).', 'link': 'https://www.amazon.in/s?k=peace+lily+plant'},
        'Rubber Plant': {'description': 'Absorbs sulfur dioxide (Indoor).', 'link': 'https://www.amazon.in/s?k=rubber+plant'},
        'Ficus': {'description': 'Filters SO2 and other pollutants (Indoor).', 'link': 'https://www.amazon.in/s?k=ficus+plant'},
        'Boston Fern': {'description': 'Absorbs sulfur dioxide from indoor air (Indoor).', 'link': 'https://www.amazon.in/s?k=boston+fern+plant'},
        'Areca Palm': {'description': 'Removes sulfur dioxide (Indoor).', 'link': 'https://www.amazon.in/s?k=areca+palm+plant'},
        'Chrysanthemum': {'description': 'Filters out harmful gases including SO2 (Outdoor).', 'link': 'https://www.amazon.in/s?k=chrysanthemum+plant'}
    }
}

# Fetch AQI data
def fetch_aqi_data(city):
    url = f"http://api.waqi.info/feed/{city}/?token={TOKEN}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "ok":
            return data['data']['iaqi'], data['data']['aqi']
        else:
            return None, None
    return None, None

# Classify pollutant levels
def classify_pollutants(pollutants):
    classified = {}
    for pollutant, value in pollutants.items():
        if pollutant in pollutant_thresholds:
            thresholds = pollutant_thresholds[pollutant]
            if value['v'] <= thresholds[0]:
                classified[pollutant] = 'Safe'
            elif value['v'] <= thresholds[1]:
                classified[pollutant] = 'Moderate'
            elif value['v'] <= thresholds[2]:
                classified[pollutant] = 'Risky'
            else:
                classified[pollutant] = 'Very Risky'
    return classified

# Identify the most risky pollutant
def most_risky_pollutant(classified_pollutants):
    risk_levels = {'Safe': 1, 'Moderate': 2, 'Risky': 3, 'Very Risky': 4}
    max_risk = 'Safe'
    max_pollutant = None
    
    for pollutant, level in classified_pollutants.items():
        if risk_levels[level] > risk_levels[max_risk]:
            max_risk = level
            max_pollutant = pollutant
    
    return max_pollutant, max_risk

# Visualize pollutants using a pie chart
def visualize_pollutants(pollutants):
    labels = list(pollutants.keys())
    sizes = [pollutant['v'] for pollutant in pollutants.values()]
    
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    plt.axis('equal')
    plt.title('Pollutant Levels Distribution')
    st.pyplot(plt)

# Input for city
city = st.text_input("Please provide your city to get started:")

if city:
    st.write(f"Fetching air quality data for **{city}**...")
    
    pollutants, aqi = fetch_aqi_data(city)
    
    if pollutants:
        st.write(f"Air Quality Index (AQI) for {city}: **{aqi}**")
        
        # Pollutant classification
        classified = classify_pollutants(pollutants)
        st.write("Here is the breakdown of pollutants:")
        for pollutant, value in pollutants.items():
            st.write(f"- {pollutant.upper()}: {value['v']} ({classified.get(pollutant, 'N/A')})")
        
        # Most risky pollutant
        risky_pollutant, risk_level = most_risky_pollutant(classified)
        if risky_pollutant:
            st.write(f"The most risky pollutant is **{risky_pollutant.upper()}** ({risk_level}).")
        
        # Visualize pollutants
        visualize_pollutants(pollutants)
        
        # Ask if the user wants to proceed with plant recommendations
        proceed = st.radio("Do you want to proceed with plant recommendations?", ("Yes", "No"))
        
        if proceed == "Yes":
            st.write("🌿 Great! Let's look at some plant recommendations. 🌿")
            
            # Plant recommendations with accordions
            for pollutant in pollutants:
                if pollutant in plant_database:
                    with st.expander(f"Recommendations for {pollutant.upper()}:"):
                        for plant, info in plant_database[pollutant].items():
                            st.write(f"- [{plant}]({info['link']}): {info['description']}")
            
            # Highlight the best plant for the most risky pollutant
            if risky_pollutant:
                st.write(f"For **{risky_pollutant.upper()}**, the most suitable plant for you is:")
                for plant, info in plant_database[risky_pollutant].items():
                    st.write(f"- [{plant}]({info['link']}): {info['description']}")
            
            # Award green credits
            st.write("🌿 You've earned **10 Green Credits**! 🌿")

            # Link to website
            st.markdown("[For more queries, visit our website!](https://tervive.vercel.app/)")
    else:
        st.error(f"Unable to fetch data for {city}.")
