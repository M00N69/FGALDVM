import streamlit as st
import pandas as pd
import os
from PIL import Image

# Fonction pour sauvegarder les décisions
def save_decision(data):
    df = pd.DataFrame(data)
    df.to_csv('decisions.csv', mode='a', index=False, header=False)

def main():
    st.set_page_config(page_title="Détermination DLC ou DDM", layout="wide")
    st.title("Détermination DLC ou DDM")
    st.markdown(
        """
        <style>
        .stApp {
            font-family: 'Arial', sans-serif;
            line-height: 1.5;
            color: #333;
            background-color: #f5f5f5;
        }

        .stTitle {
            color: #007bff;
            font-size: 2.5em;
            margin-bottom: 1em;
            text-align: center;
        }

        .stButton {
            background-color: #007bff;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin-bottom: 1em;
        }

        .stButton:hover {
            background-color: #0056b3;
        }

        .stFileUpload {
            margin-bottom: 1em;
        }

        .stRadio {
            margin-bottom: 0.5em;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    decisions = []
    current_step = 1

    # Fonction pour afficher les informations détaillées de la note DGAL après chaque réponse
    def display_dgal_info(step):
        st.markdown(f"""
        **Informations de la note DGAL pour l'étape {step}** :
        - **Règlement (UE) n° 1169/2011** : concerne l'information des consommateurs sur les denrées alimentaires.
        - **Critères microbiologiques** : basés sur le règlement (CE) n° 2073/2005 concernant les critères microbiologiques applicables aux denrées alimentaires.
        - **Études de vieillissement** : recommandées pour valider la durée de vie microbiologique des produits.
        """)

    # Question 1
    if current_step == 1:
        st.markdown("""
        ## **Q1 : Le produit alimentaire est-il exempt de la DLC conformément au règlement (UE) n° 1169/2011 ou est-il couvert par d'autres dispositions de l'Union imposant d'autres types de marquage de la date ?**
        """)
        q1 = st.radio("", ("Oui", "Non"), key="q1")
        if q1 == "Oui":
            st.success("Étiquetage selon réglementation en vigueur")
            display_dgal_info(current_step)
            decisions.append({"Question": "Q1", "Réponse": q1, "Décision": "Étiquetage selon réglementation en vigueur"})
            current_step += 1
        else:
            # Justification et upload de documents
            justification_q1 = st.text_area("Justifiez votre réponse (Q1)", key="justification_q1")
            doc_q1 = st.file_uploader("Téléchargez un document justificatif (Q1)", key="doc_q1", type=["pdf", "jpg", "png"])
            
            if doc_q1:
                doc_q1_name = doc_q1.name
                with open(os.path.join("uploads", doc_q1_name), "wb") as f:
                    f.write(doc_q1.getbuffer())
                decisions.append({"Question": "Q1", "Justification": justification_q1, "Document": doc_q1_name})
            else:
                decisions.append({"Question": "Q1", "Justification": justification_q1})
            current_step += 1

    # Question 2
    if current_step == 2:
        st.markdown("""
        ## **Q2 : Le produit alimentaire est-il congelé ?**
        """)
        q2 = st.radio("", ("Oui", "Non"), key="q2")
        if q2 == "Oui":
            current_step += 1
        else:
            current_step += 4 # Passer à Q4

    # Question 3
    if current_step == 3:
        st.markdown("""
        ## **Q3 : Le produit alimentaire subit-il un traitement assainissant validé éliminant toutes les spores des bactéries pathogènes ?**
        """)
        q3 = st.radio("", ("Oui", "Non"), key="q3")
        if q3 == "Oui":
            current_step += 1  # Passer à Q5a
        else:
            st.error("DLC")
            display_dgal_info(current_step)
            decisions.append({"Question": "Q3", "Réponse": q3, "Décision": "DLC"})
            current_step = 10 # Fin de l'arbre

    # Question 4
    if current_step == 4:
        st.markdown("""
        ## **Q4 : Le produit alimentaire est-il soumis à un traitement assainissant validé éliminant toutes les cellules végétatives des bactéries pathogènes d'origine alimentaire ?**
        """)
        q4 = st.radio("", ("Oui", "Non"), key="q4")
        if q4 == "Oui":
            current_step += 1 # Passer à Q5b
        else:
            # Question 7
            st.markdown("""
            ## **Q7 : Le traitement assainissant est-il appliqué à des produits emballés ou suivi d'un emballage aseptique ?**
            """)
            q7 = st.radio("", ("Oui", "Non"), key="q7")
            
            if q7 == "Oui":
                st.success("DDM")
                display_dgal_info(current_step)
                decisions.append({"Question": "Q7", "Réponse": q7, "Décision": "DDM"})
                current_step = 10 # Fin de l'arbre
            else:
                current_step += 2 # Passer à Q8

    # Question 5a
    if current_step == 5:
        st.markdown("""
        ## **Q5a : Existe-t-il un risque de recontamination du produit alimentaire avant l'emballage ?**
        """)
        q5a = st.radio("", ("Oui", "Non"), key="q5a")
        if q5a == "Oui":
            current_step += 1 # Passer à Q6
        else:
            st.success("DDM")
            display_dgal_info(current_step)
            decisions.append({"Question": "Q5a", "Réponse": q5a, "Décision": "DDM"})
            current_step = 10 # Fin de l'arbre

    # Question 5b
    if current_step == 6:
        st.markdown("""
        ## **Q5b : Y a-t-il un risque de recontamination du produit alimentaire avant son emballage ?**
        """)
        q5b = st.radio("", ("Oui", "Non"), key="q5b")
        if q5b == "Oui":
            current_step += 1 # Passer à Q6
        else:
            st.success("DDM")
            display_dgal_info(current_step)
            decisions.append({"Question": "Q5b", "Réponse": q5b, "Décision": "DDM"})
            current_step = 10 # Fin de l'arbre

    # Question 6
    if current_step == 7:
        st.markdown("""
        ## **Q6 : Le produit alimentaire subit-il un second traitement assainissant validé éliminant toutes les cellules végétatives des bactéries pathogènes d'origine ?**
        """)
        q6 = st.radio("", ("Oui", "Non"), key="q6")
        if q6 == "Oui":
            st.success("DDM")
            display_dgal_info(current_step)
            decisions.append({"Question": "Q6", "Réponse": q6, "Décision": "DDM"})
            current_step = 10 # Fin de l'arbre
        else:
            st.error("DLC")
            display_dgal_info(current_step)
            decisions.append({"Question": "Q6", "Réponse": q6, "Décision": "DLC"})
            current_step = 10 # Fin de l'arbre

    # Question 8
    if current_step == 8:
        st.markdown("""
        ## **Q8 : Le produit alimentaire favorise-t-il la croissance des bactéries ?**
        """)
        aw = st.selectbox("aw", ["<0,88", "0,88 à 0,9", ">0,9 à 0,92", "0,92 à 0,96", ">0,96"], key="aw")
        ph = st.selectbox("pH", ["1,9 à 4,0", "4,0 à 4,2", "4,2 à 4,4", "4,4 à 5", ">5"], key="ph")
        
        if (aw, ph) in [
            ("<0,88", "1,9 à 4,0"),
            ("<0,88", "4,0 à 4,2"),
            ("0,88 à 0,9", "1,9 à 4,0"),
            # Ajouter toutes les combinaisons qui ne favorisent pas la croissance
        ]:
            st.success("DDM")
            display_dgal_info(current_step)
            decisions.append({"Question": "Q8", "Réponse": f"aw: {aw}, pH: {ph}", "Décision": "DDM"})
            current_step = 10 # Fin de l'arbre
        else:
            current_step += 1 # Passer à Q9

    # Question 9
    if current_step == 9:
        st.markdown("""
        ## **Q9 : Le produit alimentaire favorise-t-il la germination, la croissance et la production de toxines ?**
        """)
        aw2 = st.selectbox("aw2", ["<0,92", "0,92 à 0,95", ">0,95"], key="aw2")
        ph2 = st.selectbox("pH2", ["<4,6", "4,6-5,6", ">5,6"], key="ph2")
        
        if (aw2, ph2) in [
            ("<0,92", "<4,6"),
            ("<0,92", "4,6-5,6"),
            # Ajouter toutes les combinaisons qui ne favorisent pas la production de toxines
        ]:
            st.success("DDM")
            display_dgal_info(current_step)
            decisions.append({"Question": "Q9", "Réponse": f"aw: {aw2}, pH: {ph2}", "Décision": "DDM"})
            current_step = 10 # Fin de l'arbre
        else:
            st.error("DLC")
            display_dgal_info(current_step)
            decisions.append({"Question": "Q9", "Réponse": f"aw: {aw2}, pH: {ph2}", "Décision": "DLC"})
            current_step = 10 # Fin de l'arbre

    if current_step == 10:
        st.markdown("## **Fin du processus de détermination**")
        st.write("Cliquez sur le bouton ci-dessous pour sauvegarder vos décisions.")

    # Sauvegarde des décisions
    if st.button("Sauvegarder les décisions", key="save_button"):
        save_decision(decisions)
        st.success("Décisions sauvegardées avec succès")

if __name__ == "__main__":
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    main()
