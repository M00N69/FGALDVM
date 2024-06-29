import streamlit as st

questions = {
    "q1": "Le produit alimentaire est-il exempté de la DLC conformément au règlement (UE) n° 1169/2011 ou est-il couvert par d'autres dispositions de l'Union imposant d'autres types de marquage de la date ?",
    "q2": "Le produit alimentaire est-il congelé ?",
    "q3": "Le produit alimentaire subit-il un traitement assainissant valide éliminant toutes les spores des bactéries pathogènes ?",
    "q4": "Le produit alimentaire est-il soumis à un traitement assainissant valide éliminant toutes les cellules végétatives des bactéries pathogènes d'origine alimentaire ?",
    "q5a": "Existe-t-il un risque de recontamination du produit alimentaire avant l'emballage ?",
    "q5b": "Y a-t-il un risque de recontamination du produit alimentaire avant son emballage ?",
    "q6": "Le produit alimentaire subit-il un second traitement assainissant valide éliminant toutes les cellules végétatives des bactéries pathogènes d'origine ?",
    "q7": "Le traitement assainissant est-il appliqué à des produits emballés ou suivi d'un emballage aseptique ?",
    "q8": "Le produit alimentaire favorise-t-il la croissance de bactéries ?",
    "q9": "Le produit alimentaire favorise-t-il la germination, la croissance et la production de toxines ?",
    "q10": "L'opérateur est-il en mesure de démontrer (approche par étapes décrite à la section 3.4) que le produit alimentaire ne favorise pas la croissance et/ou la production de toxines de bactéries pathogènes dans des conditions de température raisonnablement prévisibles pendant la distribution ?",
    "finalQuestion": "Pas de croissance ni de production de toxines de bactéries pathogènes pendant la durée de conservation. Le produit alimentaire peut être conservé à température ambiante sauf si des raisons de qualité exigent une réfrigération."
}

def check_growth_factors(ph, aw):
    ph_value = float(ph)
    aw_value = float(aw)

    if ph_value <= 3.9 or aw_value <= 0.88:
        return 'NF'
    if (ph_value > 3.9 and ph_value <= 4.2) and (aw_value > 0.88 and aw_value <= 0.92):
        return 'NF'
    if (ph_value > 4.2 and ph_value <= 4.5) and (aw_value > 0.92 and aw_value <= 0.94):
        return 'NF'
    if (ph_value > 4.5 and ph_value <= 5.0) and aw_value > 0.94:
        return 'F'
    if ph_value > 5.0:
        return 'F'
    if aw_value <= 0.92:
        return 'NT'
    if (aw_value > 0.92 and aw_value <= 0.95) and ph_value <= 4.6:
        return 'NT'
    if aw_value > 0.95 and ph_value <= 5.2:
        return 'NT'
    return 'T'

def main():
    st.title("Arbre de décision EFSA : DLC ou DDM")
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = "q1"
        st.session_state.result = None
        st.session_state.ph = ""
        st.session_state.aw = ""
        st.session_state.growth_factor = None

    if st.session_state.result:
        st.success(f"Résultat final : {st.session_state.result}")
        if st.button("Recommencer"):
            st.session_state.current_question = "q1"
            st.session_state.result = None
            st.session_state.ph = ""
            st.session_state.aw = ""
            st.session_state.growth_factor = None
    else:
        st.write(questions[st.session_state.current_question])
        if st.session_state.current_question in ["q8", "q9"]:
            st.session_state.ph = st.number_input("pH:", step=0.1, format="%.1f")
            st.session_state.aw = st.number_input("Aw:", step=0.01, format="%.2f")
            if st.button("Vérifier"):
                st.session_state.growth_factor = check_growth_factors(st.session_state.ph, st.session_state.aw)
                st.write(f"Facteur de croissance: {st.session_state.growth_factor}")
                handle_answer(st.session_state.growth_factor)
        else:
            if st.button("Oui"):
                handle_answer("Oui")
            if st.button("Non"):
                handle_answer("Non")

def handle_answer(answer):
    current_question = st.session_state.current_question
    if current_question == "q1":
        if answer == "Oui":
            st.session_state.result = "Étiquetage selon réglementation en vigueur"
        else:
            st.session_state.current_question = "q2"
    elif current_question == "q2":
        if answer == "Oui":
            st.session_state.result = "DDM"
        else:
            st.session_state.current_question = "q3"
    elif current_question == "q3":
        if answer == "Oui":
            st.session_state.current_question = "q5a"
        else:
            st.session_state.current_question = "q4"
    elif current_question == "q4":
        if answer == "Oui":
            st.session_state.current_question = "q5b"
        else:
            st.session_state.result = "DLC"
    elif current_question in ["q5a", "q5b"]:
        if answer == "Oui":
            st.session_state.current_question = "q6"
        else:
            st.session_state.current_question = "q7"
    elif current_question == "q6":
        if answer == "Oui":
            st.session_state.current_question = "q7"
        else:
            st.session_state.result = "DLC"
    elif current_question == "q7":
        if answer == "Oui":
            st.session_state.current_question = "q8"
        else:
            st.session_state.result = "DLC"
    elif current_question == "q8":
        if answer == "F":
            st.session_state.result = "DLC"
        else:
            st.session_state.current_question = "q9"
    elif current_question == "q9":
        if answer in ["F", "T"]:
            st.session_state.current_question = "q10"
        else:
            st.session_state.current_question = "finalQuestion"
    elif current_question == "q10":
        if answer == "Oui":
            st.session_state.current_question = "finalQuestion"
        else:
            st.session_state.result = "DLC"
    elif current_question == "finalQuestion":
        st.session_state.result = "DDM" if answer == "Oui" else "DLC"

if __name__ == "__main__":
    main()
