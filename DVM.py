import streamlit as st
import pandas as pd
import os

# Fonction pour sauvegarder les décisions
def save_decision(data):
    df = pd.DataFrame(data)
    df.to_csv('decisions.csv', mode='a', index=False, header=False)

def main():
    st.set_page_config(page_title="Détermination DLC ou DDM", layout="wide")
    st.markdown(
        """
        <style>
        .stApp {
            font-family: 'Arial', sans-serif;
            background-color: #f5f5f5;
            padding: 20px;
        }

        .stTitle {
            color: #007bff;
            font-size: 2.5em;
            margin-bottom: 1em;
            text-align: center;
        }

        .stButton > button {
            background-color: #007bff !important;
            color: white !important;
            padding: 10px 20px !important;
            border: none !important;
            border-radius: 4px !important;
            cursor: pointer !important;
            margin-bottom: 1em !important;
        }

        .stButton > button:hover {
            background-color: #0056b3 !important;
        }

        .stFileUpload, .stTextArea, .stRadio, .stSelectbox {
            margin-bottom: 1em;
        }

        .stMarkdown h2 {
            color: #333;
            font-size: 1.5em;
            margin-bottom: 0.5em;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("Détermination DLC ou DDM")

    st.markdown(
        """
        <div class="stApp">
            <h2 class="stTitle">Bienvenue dans l'outil de détermination de la DLC ou DDM</h2>
            <p>Utilisez cet outil pour déterminer si un produit alimentaire doit avoir une Date Limite de Consommation (DLC) ou une Date de Durabilité Minimale (DDM).
            Suivez les questions et répondez en fonction de votre produit.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    decisions = []

    # Fonction pour afficher les informations détaillées de la note DGAL après chaque réponse
    def display_dgal_info(step):
        st.markdown(f"""
        <div class="stMarkdown">
            <h2>Informations de la note DGAL pour l'étape {step}</h2>
            <ul>
                <li><strong>Règlement (UE) n° 1169/2011</strong> : concerne l'information des consommateurs sur les denrées alimentaires.</li>
                <li><strong>Critères microbiologiques</strong> : basés sur le règlement (CE) n° 2073/2005 concernant les critères microbiologiques applicables aux denrées alimentaires.</li>
                <li><strong>Études de vieillissement</strong> : recommandées pour valider la durée de vie microbiologique des produits.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Question 1
    st.markdown("""
    ## **Q1 : Le produit alimentaire est-il exempt de la DLC conformément au règlement (UE) n° 1169/2011 ou est-il couvert par d'autres dispositions de l'Union imposant d'autres types de marquage de la date ?**
    """)
    q1 = st.radio("", ("Oui", "Non"), key="q1")
    if q1 == "Oui":
        st.success("Étiquetage selon réglementation en vigueur")
        display_dgal_info("Q1")
        decisions.append({"Question": "Q1", "Réponse": q1, "Décision": "Étiquetage selon réglementation en vigueur"})
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

    # Question 2
    st.markdown("""
    ## **Q2 : Le produit alimentaire est-il congelé ?**
    """)
    q2 = st.radio("", ("Oui", "Non"), key="q2")
    if q2 == "Oui":
        # Question 3
        st.markdown("""
        ## **Q3 : Le produit alimentaire subit-il un traitement assainissant validé éliminant toutes les spores des bactéries pathogènes ?**
        """)
        q3 = st.radio("", ("Oui", "Non"), key="q3")
        
        if q3 == "Oui":
            # Question 5a
            st.markdown("""
            ## **Q5a : Existe-t-il un risque de recontamination du produit alimentaire avant l'emballage ?**
            """)
            q5a = st.radio("", ("Oui", "Non"), key="q5a")
            
            if q5a == "Oui":
                # Question 6
                st.markdown("""
                ## **Q6 : Le produit alimentaire subit-il un second traitement assainissant validé éliminant toutes les cellules végétatives des bactéries pathogènes d'origine ?**
                """)
                q6 = st.radio("", ("Oui", "Non"), key="q6")
                
                if q6 == "Oui":
                    st.success("DDM")
                    display_dgal_info("Q6")
                    decisions.append({"Question": "Q6", "Réponse": q6, "Décision": "DDM"})
                else:
                    st.error("DLC")
                    display_dgal_info("Q6")
                    decisions.append({"Question": "Q6", "Réponse": q6, "Décision": "DLC"})
            else:
                st.success("DDM")
                display_dgal_info("Q5a")
                decisions.append({"Question": "Q5a", "Réponse": q5a, "Décision": "DDM"})
        else:
            st.error("DLC")
            display_dgal_info("Q3")
            decisions.append({"Question": "Q3", "Réponse": q3, "Décision": "DLC"})
    else:
        # Question 4
        st.markdown("""
        ## **Q4 : Le produit alimentaire est-il soumis à un traitement assainissant validé éliminant toutes les cellules végétatives des bactéries pathogènes d'origine alimentaire ?**
        """)
        q4 = st.radio("", ("Oui", "Non"), key="q4")
        
        if q4 == "Oui":
            # Question 5b
            st.markdown("""
            ## **Q5b : Y a-t-il un risque de recontamination du produit alimentaire avant son emballage ?**
            """)
            q5b = st.radio("", ("Oui", "Non"), key="q5b")
            
            if q5b == "Oui":
                # Question 6
                st.markdown("""
                ## **Q6 : Le produit alimentaire subit-il un second traitement assainissant validé éliminant toutes les cellules végétatives des bactéries pathogènes d'origine ?**
                """)
                q6 = st.radio("", ("Oui", "Non"), key="q6_2")
                
                if q6 == "Oui":
                    st.success("DDM")
                    display_dgal_info("Q6")
                    decisions.append({"Question": "Q6", "Réponse": q6, "Décision": "DDM"})
                else:
                    st.error("DLC")
                    display_dgal_info("Q6")
                    decisions.append({"Question": "Q6", "Réponse": q6, "Décision": "DLC"})
            else:
                st.success("DDM")
                display_dgal_info("Q5b")
                decisions.append({"Question": "Q5b", "Réponse": q5b, "Décision": "DDM"})
        else:
            # Question 7
            st.markdown("""
            ## **Q7 : Le traitement assainissant est-il appliqué à des produits emballés ou suivi d'un emballage aseptique ?**
            """)
            q7 = st.radio("", ("Oui", "Non"), key="q7")
            
            if q7 == "Oui":
                st.success("DDM")
                display_dgal_info("Q7")
                decisions.append({"Question": "Q7", "Réponse": q7, "Décision": "DDM"})
            else:
                # Question 8
                st.subheader("Q8 : Le produit alimentaire favorise-t-il la croissance des bactéries ?")
                aw = st.selectbox("aw", ["<0,88", "0,88 à 0,9", ">0,9 à 0,92", "0,92 à 0,96", ">0,96"], key="aw")
                ph = st.selectbox("pH", ["1,9 à 4,0", "4,0 à 4,2", "4,2 à 4,4", "4,4 à 5", ">5"], key="ph")
                
                if (aw, ph) in [
                    ("<0,88", "1,9 à 4,0"),
                    ("<0,88", "4,0 à 4,2"),
                    ("0,88 à 0,9", "1,9 à 4,0"),
                    # Ajouter toutes les combinaisons qui ne favorisent pas la croissance
                ]:
                    st.success("DDM")
                    display_dgal_info("Q8")
                    decisions.append({"Question": "Q8", "Réponse": f"aw: {aw}, pH: {ph}", "Décision": "DDM"})
                else:
                    # Question 9
                    st.subheader("Q9 : Le produit alimentaire favorise-t-il la germination, la croissance et la production de toxines ?")
                    aw2 = st.selectbox("aw2", ["<0,92", "0,92 à 0,95", ">0,95"], key="aw2")
                    ph2 = st.selectbox("pH2", ["<4,6", "4,6-5,6", ">5,6"], key="ph2")
                    
                    if (aw2, ph2) in [
                        ("<0,92", "<4,6"),
                        ("<0,92", "4,6-5,6"),
                        # Ajouter toutes les combinaisons qui ne favorisent pas la production de toxines
                    ]:
                        st.success("DDM")
                        display_dgal_info("Q9")
                        decisions.append({"Question": "Q9", "Réponse": f"aw: {aw2}, pH: {ph2}", "Décision": "DDM"})
                    else:
                        st.error("DLC")
                        display_dgal_info("Q9")
                        decisions.append({"Question": "Q9", "Réponse": f"aw: {aw2}, pH: {ph2}", "Décision": "DLC"})

    # Sauvegarde des décisions
    if st.button("Sauvegarder les décisions", key="save_button"):
        save_decision(decisions)
        st.success("Décisions sauvegardées avec succès")

if __name__ == "__main__":
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    main()
