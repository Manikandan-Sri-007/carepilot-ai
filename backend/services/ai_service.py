def analyze_symptoms(symptoms: str):

    symptoms = symptoms.lower()

    if "fever" in symptoms and "cough" in symptoms:
        return {
            "possible_disease": "Flu or Viral Infection",
            "recommendation": "Drink plenty of fluids and consult a doctor if symptoms worsen."
        }

    elif "headache" in symptoms:
        return {
            "possible_disease": "Migraine or Stress",
            "recommendation": "Take adequate rest and stay hydrated."
        }

    elif "stomach pain" in symptoms:
        return {
            "possible_disease": "Gastric Problem",
            "recommendation": "Avoid oily foods and seek medical advice if pain continues."
        }

    return {
        "possible_disease": "Unknown",
        "recommendation": "Please consult a healthcare professional."
    }