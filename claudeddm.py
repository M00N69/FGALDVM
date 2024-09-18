import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from io import BytesIO
import base64
import requests
from PIL import Image

# Définition des questions et explications
questions = {
    'q1': {
        'question': "Le produit alimentaire est-il exempté de la DLC conformément au règlement (UE) n° 1169/2011 ou est-il couvert par d'autres dispositions de l'Union imposant d'autres types de marquage de la date ?",
        'explanation': "Cette question vise à identifier si le produit est soumis à des réglementations spécifiques concernant l'étiquetage des dates."
    },
    'q2': {
        'question': "Le produit alimentaire est-il congelé ?",
        'explanation': "Les produits congelés ont des considérations spéciales en termes de durée de conservation."
    },
    'q3': {
        'question': "Le produit alimentaire subit-il un traitement assainissant valide éliminant toutes les spores des bactéries pathogènes ?",
        'explanation': "Un traitement assainissant qui élimine toutes les spores bactériennes pathogènes est un processus très intensif."
    },
    'q4': {
        'question': "Le produit alimentaire est-il soumis à un traitement assainissant valide éliminant toutes les cellules végétatives des bactéries pathogènes d'origine alimentaire ?",
        'explanation': "Ce traitement élimine les cellules bactériennes vivantes, mais pas nécessairement les spores."
    },
    'q5a': {
        'question': "Existe-t-il un risque de recontamination du produit alimentaire avant l'emballage ?",
        'explanation': "La recontamination peut se produire si le produit est exposé à l'environnement après le traitement."
    },
    'q5b': {
        'question': "Y a-t-il un risque de recontamination du produit alimentaire avant son emballage ?",
        'explanation': "Similaire à q5a, mais dans le contexte d'un produit qui n'a pas subi de traitement éliminant toutes les spores."
    },
    'q6': {
        'question': "Le produit alimentaire subit-il un second traitement assainissant valide éliminant toutes les cellules végétatives des bactéries pathogènes d'origine ?",
        'explanation': "Un second traitement peut être nécessaire si une recontamination s'est produite."
    },
    'q7': {
        'question': "Le traitement assainissant est-il appliqué à des produits emballés ou suivi d'un emballage aseptique ?",
        'explanation': "L'emballage aseptique aide à prévenir la recontamination après le traitement."
    },
    'q8': {
        'question': "Le produit alimentaire favorise-t-il la croissance de bactéries ?",
        'explanation': "Certains aliments fournissent un environnement propice à la croissance bactérienne."
    },
    'q9': {
        'question': "Le produit alimentaire favorise-t-il la germination, la croissance et la production de toxines ?",
        'explanation': "Certains aliments peuvent favoriser non seulement la croissance, mais aussi la production de toxines."
    },
    'q10': {
        'question': "L'opérateur est-il en mesure de démontrer (approche par étapes décrite à la section 3.4) que le produit alimentaire ne favorise pas la croissance et/ou la production de toxines de bactéries pathogènes dans des conditions de température raisonnablement prévisibles pendant la distribution ?",
        'explanation': "Cette démonstration nécessite généralement des tests et des analyses approfondis."
    },
    'finalQuestion': {
        'question': "Pas de croissance ni de production de toxines de bactéries pathogènes pendant la durée de conservation. Le produit alimentaire peut être conservé à température ambiante sauf si des raisons de qualité exigent une réfrigération.",
        'explanation': "Cette question finale détermine si le produit peut être conservé à température ambiante ou s'il nécessite une réfrigération."
    }
}

def check_growth_factors(ph, aw):
    ph = float(ph)
    aw = float(aw)
    
    if ph <= 3.9 or aw <= 0.88:
        return 'NF'
    if (3.9 < ph <= 4.2) and (0.88 < aw <= 0.92):
        return 'NF'
    if (4.2 < ph <= 4.5) and (0.92 < aw <= 0.94):
        return 'NF'
    if (4.5 < ph <= 5.0) and aw > 0.94:
        return 'F'
    if ph > 5.0:
        return 'F'
    if aw <= 0.92:
        return 'NT'
    if (0.92 < aw <= 0.95) and ph <= 4.6:
        return 'NT'
    if aw > 0.95 and ph <= 5.2:
        return 'NT'
    
    return 'T'

def get_growth_factor_explanation(factor):
    explanations = {
        'NF': "NF : Ne favorise pas la croissance de bactéries",
        'F': "F : Favorise la croissance de bactéries",
        'NT': "NT : Ne favorise pas la production de toxines",
        'T': "T : Favorise la production de toxines"
    }
    return explanations.get(factor, "")

def generate_pdf_report(history, result):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    subtitle_style = styles['Heading2']
    normal_style = styles['Normal']

    # Titre
    elements.append(Paragraph("Rapport de décision EFSA : DLC ou DDM", title_style))
    elements.append(Spacer(1, 0.25*inch))

    # Résultat final
    elements.append(Paragraph(f"Résultat final : {result}", subtitle_style))
    elements.append(Spacer(1, 0.25*inch))

    # Historique des questions et réponses
    for question, answer in history:
        q_text = questions[question]['question']
        explanation = questions[question]['explanation']
        elements.append(Paragraph(f"Q: {q_text}", styles['Heading3']))
        elements.append(Paragraph(f"R: {answer}", normal_style))
        elements.append(Paragraph(f"Explication: {explanation}", normal_style))
        elements.append(Spacer(1, 0.1*inch))

    doc.build(elements)
    buffer.seek(0)
    return buffer

def generate_download_link(history, result):
    pdf = generate_pdf_report(history, result)
    b64 = base64.b64encode(pdf.getvalue()).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="decision_tree_results.pdf">Télécharger le rapport (PDF)</a>'
    return href

def reset_session_state():
    st.session_state.current_question = 'q1'
    st.session_state.history = []
    st.session_state.result = None
    st.session_state.ph = 0
    st.session_state.aw = 0.1
    st.session_state.growth_factor = None

def handle_answer(answer):
    st.session_state.history.append((st.session_state.current_question, answer))
    
    if st.session_state.current_question == 'q1':
        if answer == 'Oui':
            st.session_state.result = 'Étiquetage selon réglementation en vigueur'
        else:
            st.session_state.current_question = 'q2'
    elif st.session_state.current_question == 'q2':
        st.session_state.current_question = 'q4' if answer == 'Oui' else 'q3'
    elif st.session_state.current_question == 'q3':
        st.session_state.current_question = 'q5a' if answer == 'Oui' else 'q4'
    elif st.session_state.current_question == 'q4':
        if answer == 'Oui':
            st.session_state.current_question = 'q5b'
        else:
            st.session_state.result = 'DLC'
    elif st.session_state.current_question in ['q5a', 'q5b']:
        st.session_state.current_question = 'q6' if answer == 'Oui' else 'q7'
    elif st.session_state.current_question == 'q6':
        if answer == 'Oui':
            st.session_state.current_question = 'q7'
        else:
            st.session_state.result = 'DLC'
    elif st.session_state.current_question == 'q7':
        if answer == 'Oui':
            st.session_state.current_question = 'q8'
        else:
            st.session_state.result = 'DLC'
    elif st.session_state.current_question == 'q8':
        if answer == 'F':
            st.session_state.result = 'DLC'
        else:
            st.session_state.current_question = 'q9'
    elif st.session_state.current_question == 'q9':
        if answer in ['F', 'T']:
            st.session_state.current_question = 'q10'
        else:
            st.session_state.current_question = 'finalQuestion'
    elif st.session_state.current_question == 'q10':
        st.session_state.result = 'DDM' if answer == 'Oui' else 'DLC'
    elif st.session_state.current_question == 'finalQuestion':
        st.session_state.result = 'DDM' if answer == 'Oui' else 'DLC'

def main():
    # Passer en mode large
    st.set_page_config(layout="wide")

    # --- Custom CSS ---
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            background-color: #2398B2;  
        }
        .banner {
            background-image: url('https://github.com/M00N69/BUSCAR/blob/main/logo%2002%20copie.jpg?raw=true');
            background-size: cover;
            padding: 75px;
            text-align: center;
        }
        .dataframe td {
            white-space: normal !important;
            word-wrap: break-word !important;
        }
        </style>
        <div class="banner"></div>
        """,
        unsafe_allow_html=True
    )

    # --- Logo and Link in Sidebar ---
    st.sidebar.markdown(
        f"""
        <div class="sidebar-logo-container">
            <a href="https://www.visipilot.com" target="_blank">
                <img src="https://raw.githubusercontent.com/M00N69/RAPPELCONSO/main/logo%2004%20copie.jpg" alt="Visipilot Logo" class="sidebar-logo">
            </a>
        </div>
        """, unsafe_allow_html=True
    )

    # Explication de l'application dans un expander
    with st.sidebar.expander("À propos de l'application", expanded=True):
        st.write("""
            Cet outil vous guide à travers l'arbre de décision EFSA pour déterminer si votre produit alimentaire nécessite une 
            Date Limite de Consommation (DLC) ou une Date de Durabilité Minimale (DDM). Répondez aux questions et obtenez un rapport
            basé sur vos réponses.
        """)

    st.title("Arbre de décision EFSA : DLC ou DDM")

    if 'current_question' not in st.session_state:
        reset_session_state()

    if st.session_state.result is None:
        current_q = st.session_state.current_question
        if current_q in questions:
            st.subheader(questions[current_q]['question'])
            st.info(questions[current_q]['explanation'])

            if st.session_state.current_question in ['q8', 'q9']:
                col1, col2 = st.columns(2)
                with col1:
                    ph = st.slider("pH:", min_value=0.0, max_value=12.0, step=0.1, key='ph')
                with col2:
                    aw = st.slider("Aw:", min_value=0.1, max_value=1.0, step=0.01, key='aw')
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

            # Barre de progression
            progress = (list(questions.keys()).index(st.session_state.current_question) + 1) / len(questions)
            st.progress(progress)
        else:
            st.error("Question non trouvée dans le dictionnaire.")
    else:
        st.success(f"Résultat final : {st.session_state.result}")
        if st.session_state.result == 'DLC':
            st.write("Votre produit nécessite une Date Limite de Consommation (DLC). La DLC indique la date jusqu'à laquelle le produit peut être consommé sans risque pour la santé.")
        elif st.session_state.result == 'DDM':
            st.write("Votre produit peut utiliser une Date de Durabilité Minimale (DDM). La DDM indique la date jusqu'à laquelle le produit conserve ses qualités spécifiques dans des conditions de conservation appropriées.")
        
        if st.button("Recommencer"):
            reset_session_state()

        # Ajout du lien de téléchargement du PDF
        st.markdown(generate_download_link(st.session_state.history, st.session_state.result), unsafe_allow_html=True)

if __name__ == "__main__":
    main()





