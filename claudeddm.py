import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from io import BytesIO
import base64
import requests
from PIL import Image

# Définition des questions et explications (inchangée)
questions = {
    'q1': {
        'question': "Le produit alimentaire est-il exempté de la DLC conformément au règlement (UE) n° 1169/2011 ou est-il couvert par d'autres dispositions de l'Union imposant d'autres types de marquage de la date ?",
        'explanation': "Cette question vise à identifier si le produit est soumis à des réglementations spécifiques concernant l'étiquetage des dates."
    },
    # ... (autres questions inchangées)
}

def check_growth_factors(ph, aw):
    ph = float(ph)
    aw = float(aw)
    
    if aw <= 0.88:
        return 'NF'
    elif 0.88 < aw <= 0.92:
        if ph <= 4.2:
            return 'NF'
        elif 4.2 < ph <= 4.6:
            return 'F'
        else:
            return 'F'
    elif 0.92 < aw <= 0.95:
        if ph <= 4.6:
            return 'NT'
        else:
            return 'T'
    else:  # aw > 0.95
        if ph <= 5.6:
            return 'T'
        else:
            return 'T'

def get_growth_factor_explanation(factor):
    explanations = {
        'NF': "NF : Ne favorise pas la croissance de bactéries",
        'F': "F : Favorise la croissance de bactéries",
        'NT': "NT : Ne favorise pas la production de toxines",
        'T': "T : Favorise la production de toxines"
    }
    return explanations.get(factor, "")

# Fonctions generate_pdf_report et generate_download_link inchangées

def reset_session_state():
    st.session_state.current_question = 'q1'
    st.session_state.history = []
    st.session_state.result = None

def handle_answer(answer):
    st.session_state.history.append((st.session_state.current_question, answer))
    
    if st.session_state.current_question == 'q1':
        if answer == 'Oui':
            st.session_state.result = 'Étiquetage selon réglementation en vigueur'
        else:
            st.session_state.current_question = 'q2'
    elif st.session_state.current_question == 'q2':
        st.session_state.current_question = 'q3' if answer == 'Non' else 'DDM'
    elif st.session_state.current_question == 'q3':
        st.session_state.current_question = 'q5a' if answer == 'Oui' else 'q4'
    elif st.session_state.current_question == 'q4':
        st.session_state.current_question = 'q5b' if answer == 'Oui' else 'DLC'
    elif st.session_state.current_question in ['q5a', 'q5b']:
        st.session_state.current_question = 'q6' if answer == 'Oui' else 'q7'
    elif st.session_state.current_question == 'q6':
        st.session_state.current_question = 'q7' if answer == 'Oui' else 'DLC'
    elif st.session_state.current_question == 'q7':
        st.session_state.current_question = 'q8' if answer == 'Oui' else 'DLC'
    elif st.session_state.current_question == 'q8':
        st.session_state.current_question = 'q9' if answer in ['F', 'NT', 'T'] else 'DDM'
    elif st.session_state.current_question == 'q9':
        st.session_state.current_question = 'q10' if answer in ['F', 'T'] else 'DDM'
    elif st.session_state.current_question == 'q10':
        st.session_state.result = 'DDM' if answer == 'Oui' else 'DLC'

def main():
    # Code pour l'affichage de l'image de bannière (inchangé)

    st.title("Arbre de décision EFSA : DLC ou DDM")
    st.write("Cet outil vous guide à travers l'arbre de décision EFSA pour déterminer si votre produit alimentaire nécessite une Date Limite de Consommation (DLC) ou une Date de Durabilité Minimale (DDM).")

    if 'current_question' not in st.session_state:
        reset_session_state()

    if st.session_state.result is None:
        current_q = questions[st.session_state.current_question]
        st.subheader(current_q['question'])
        st.info(current_q['explanation'])

        if st.session_state.current_question in ['q8', 'q9']:
            col1, col2 = st.columns(2)
            with col1:
                ph = st.number_input("pH:", min_value=0.0, max_value=14.0, step=0.1)
            with col2:
                aw = st.number_input("Aw:", min_value=0.0, max_value=1.0, step=0.01)
            if st.button("Vérifier"):
                factor = check_growth_factors(ph, aw)
                st.session_state.history.append((st.session_state.current_question, f"pH: {ph}, Aw: {aw}, Résultat: {factor}"))
                st.write(get_growth_factor_explanation(factor))
                handle_answer(factor)
        else:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Oui"):
                    handle_answer('Oui')
            with col2:
                if st.button("Non"):
                    handle_answer('Non')

        progress = (list(questions.keys()).index(st.session_state.current_question) + 1) / len(questions)
        st.progress(progress)

    else:
        st.success(f"Résultat final : {st.session_state.result}")
        if st.session_state.result == 'DLC':
            st.write("Votre produit nécessite une Date Limite de Consommation (DLC). La DLC indique la date jusqu'à laquelle le produit peut être consommé sans risque pour la santé.")
        elif st.session_state.result == 'DDM':
            st.write("Votre produit peut utiliser une Date de Durabilité Minimale (DDM). La DDM indique la date jusqu'à laquelle le produit conserve ses qualités spécifiques dans des conditions de conservation appropriées.")
        
        if st.button("Recommencer"):
            reset_session_state()
            st.experimental_rerun()

        st.markdown(generate_download_link(st.session_state.history, st.session_state.result), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
