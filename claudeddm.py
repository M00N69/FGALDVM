import streamlit as st
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
from PIL import Image
import base64

# [Le dictionnaire 'questions' reste inchangé]

def check_growth_factors(ph, aw):
    # [Cette fonction reste inchangée]

def get_growth_factor_explanation(factor):
    # [Cette fonction reste inchangée]

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
        elements.append(Paragraph(f"Q: {q_text}", styles['Heading3']))
        elements.append(Paragraph(f"R: {answer}", normal_style))
        elements.append(Paragraph(f"Explication: {questions[question]['explanation']}", normal_style))
        elements.append(Spacer(1, 0.1*inch))

    doc.build(elements)
    buffer.seek(0)
    return buffer

def generate_download_link(history, result):
    pdf = generate_pdf_report(history, result)
    b64 = base64.b64encode(pdf.getvalue()).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="decision_tree_results.pdf">Télécharger le rapport (PDF)</a>'
    return href

def main():
    # Ajouter la bannière Visipilot
    st.image("visipilot_banner.PNG", use_column_width=True)

    st.title("Arbre de décision EFSA : DLC ou DDM")
    st.write("Cet outil vous guide à travers l'arbre de décision EFSA pour déterminer si votre produit alimentaire nécessite une Date Limite de Consommation (DLC) ou une Date de Durabilité Minimale (DDM).")

    if 'current_question' not in st.session_state:
        st.session_state.current_question = 'q1'
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'result' not in st.session_state:
        st.session_state.result = None

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
                factor, explanation = check_growth_factors(ph, aw)
                st.session_state.history.append((st.session_state.current_question, f"pH: {ph}, Aw: {aw}, Résultat: {factor}"))
                st.write(get_growth_factor_explanation(factor))
                st.write(explanation)
                if st.session_state.current_question == 'q8':
                    if factor == 'F':
                        st.session_state.result = 'DLC'
                    else:
                        st.session_state.current_question = 'q9'
                elif st.session_state.current_question == 'q9':
                    if factor in ['F', 'T']:
                        st.session_state.current_question = 'q10'
                    else:
                        st.session_state.current_question = 'finalQuestion'
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
        st.success(f"Résultat final : {st.session_state.result}")
        if st.session_state.result == 'DLC':
            st.write("Votre produit nécessite une Date Limite de Consommation (DLC). La DLC indique la date jusqu'à laquelle le produit peut être consommé sans risque pour la santé.")
        elif st.session_state.result == 'DDM':
            st.write("Votre produit peut utiliser une Date de Durabilité Minimale (DDM). La DDM indique la date jusqu'à laquelle le produit conserve ses qualités spécifiques dans des conditions de conservation appropriées.")
        
        if st.button("Recommencer"):
            st.session_state.current_question = 'q1'
            st.session_state.history = []
            st.session_state.result = None
            st.experimental_rerun()

        # Ajout du lien de téléchargement du PDF
        st.markdown(generate_download_link(st.session_state.history, st.session_state.result), unsafe_allow_html=True)

def handle_answer(answer):
    # [Cette fonction reste inchangée]

if __name__ == "__main__":
    main()
