import streamlit as st
import pandas as pd
import base64
from io import BytesIO

# Définition des questions
questions = {
    'q1': "Le produit alimentaire est-il exempté de la DLC conformément au règlement (UE) n° 1169/2011 ou est-il couvert par d'autres dispositions de l'Union imposant d'autres types de marquage de la date ?",
    'q2': "Le produit alimentaire est-il congelé ?",
    'q3': "Le produit alimentaire subit-il un traitement assainissant valide éliminant toutes les spores des bactéries pathogènes ?",
    'q4': "Le produit alimentaire est-il soumis à un traitement assainissant valide éliminant toutes les cellules végétatives des bactéries pathogènes d'origine alimentaire ?",
    'q5a': "Existe-t-il un risque de recontamination du produit alimentaire avant l'emballage ?",
    'q5b': "Y a-t-il un risque de recontamination du produit alimentaire avant son emballage ?",
    'q6': "Le produit alimentaire subit-il un second traitement assainissant valide éliminant toutes les cellules végétatives des bactéries pathogènes d'origine ?",
    'q7': "Le traitement assainissant est-il appliqué à des produits emballés ou suivi d'un emballage aseptique ?",
    'q8': "Le produit alimentaire favorise-t-il la croissance de bactéries ?",
    'q9': "Le produit alimentaire favorise-t-il la germination, la croissance et la production de toxines ?",
    'q10': "L'opérateur est-il en mesure de démontrer (approche par étapes décrite à la section 3.4) que le produit alimentaire ne favorise pas la croissance et/ou la production de toxines de bactéries pathogènes dans des conditions de température raisonnablement prévisibles pendant la distribution ?",
    'finalQuestion': "Pas de croissance ni de production de toxines de bactéries pathogènes pendant la durée de conservation. Le produit alimentaire peut être conservé à température ambiante sauf si des raisons de qualité exigent une réfrigération."
}

# Définition des infobulles
tooltips = {
    'q1': "Cette question vise à identifier si le produit est soumis à des réglementations spécifiques concernant l'étiquetage des dates.",
    'q2': "Les produits congelés ont des considérations spéciales en termes de durée de conservation.",
    'q3': "Un traitement assainissant qui élimine toutes les spores bactériennes pathogènes est un processus très intensif.",
    'q4': "Ce traitement élimine les cellules bactériennes vivantes, mais pas nécessairement les spores.",
    'q5a': "La recontamination peut se produire si le produit est exposé à l'environnement après le traitement.",
    'q5b': "Similaire à q5a, mais dans le contexte d'un produit qui n'a pas subi de traitement éliminant toutes les spores.",
    'q6': "Un second traitement peut être nécessaire si une recontamination s'est produite.",
    'q7': "L'emballage aseptique aide à prévenir la recontamination après le traitement.",
    'q8': "Certains aliments fournissent un environnement propice à la croissance bactérienne.",
    'q9': "Certains aliments peuvent favoriser non seulement la croissance, mais aussi la production de toxines.",
    'q10': "Cette démonstration nécessite généralement des tests et des analyses approfondis.",
    'finalQuestion': "Cette question finale détermine si le produit peut être conservé à température ambiante ou s'il nécessite une réfrigération."
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

def generate_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="decision_tree_results.csv">Télécharger les résultats (CSV)</a>'
    return href

def main():
    st.title("Arbre de décision EFSA : DLC ou DDM")

    if 'current_question' not in st.session_state:
        st.session_state.current_question = 'q1'
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'result' not in st.session_state:
        st.session_state.result = None

    if st.session_state.result is None:
        st.write(questions[st.session_state.current_question])
        st.info(tooltips[st.session_state.current_question])

        if st.session_state.current_question in ['q8', 'q9']:
            col1, col2 = st.columns(2)
            with col1:
                ph = st.number_input("pH:", min_value=0.0, max_value=14.0, step=0.1)
            with col2:
                aw = st.number_input("Aw:", min_value=0.0, max_value=1.0, step=0.01)
            if st.button("Vérifier"):
                factor = check_growth_factors(ph, aw)
                st.session_state.history.append((st.session_state.current_question, factor))
                st.write(get_growth_factor_explanation(factor))
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
        if st.button("Recommencer"):
            st.session_state.current_question = 'q1'
            st.session_state.history = []
            st.session_state.result = None
            st.experimental_rerun()

        # Création du DataFrame pour l'historique
        df = pd.DataFrame(st.session_state.history, columns=['Question', 'Réponse'])
        df['Résultat'] = st.session_state.result
        
        # Ajout du lien de téléchargement
        st.markdown(generate_download_link(df), unsafe_allow_html=True)

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
        st.session_state.current_question = 'q6' if answer == 'Oui' else 'q8'
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
    elif st.session_state.current_question == 'q10':
        if answer == 'Oui':
            st.session_state.current_question = 'finalQuestion'
        else:
            st.session_state.result = 'DLC'
    elif st.session_state.current_question == 'finalQuestion':
        st.session_state.result = 'DDM' if answer == 'Oui' else 'DLC'

    st.experimental_rerun()

if __name__ == "__main__":
    main()
