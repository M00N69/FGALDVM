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

    # Arbre de décision
    tree = {
        "Q1": {
            "Oui": {
                "Décision": "Étiquetage selon réglementation en vigueur",
                "Explication": "Le produit est exempt de la DLC et suit la réglementation en vigueur.",
            },
            "Non": {
                "Q2": {
                    "Oui": {
                        "Q3": {
                            "Oui": {
                                "Q5a": {
                                    "Oui": {
                                        "Q6": {
                                            "Oui": {
                                                "Décision": "DDM",
                                                "Explication": "Le produit subit un double traitement assainissant et ne risque pas de recontamination.",
                                            },
                                            "Non": {
                                                "Décision": "DLC",
                                                "Explication": "Le produit subit un double traitement, mais il y a un risque de recontamination.",
                                            }
                                        }
                                    },
                                    "Non": {
                                        "Décision": "DDM",
                                        "Explication": "Le produit subit un traitement assainissant et ne risque pas de recontamination.",
                                    }
                                }
                            },
                            "Non": {
                                "Décision": "DLC",
                                "Explication": "Le produit ne subit pas un traitement assainissant éliminant toutes les spores.",
                            }
                        }
                    },
                    "Non": {
                        "Q4": {
                            "Oui": {
                                "Q5b": {
                                    "Oui": {
                                        "Q6": {
                                            "Oui": {
                                                "Décision": "DDM",
                                                "Explication": "Le produit subit un double traitement assainissant et ne risque pas de recontamination.",
                                            },
                                            "Non": {
                                                "Décision": "DLC",
                                                "Explication": "Le produit subit un double traitement, mais il y a un risque de recontamination.",
                                            }
                                        }
                                    },
                                    "Non": {
                                        "Décision": "DDM",
                                        "Explication": "Le produit subit un traitement assainissant et ne risque pas de recontamination.",
                                    }
                                }
                            },
                            "Non": {
                                "Q7": {
                                    "Oui": {
                                        "Décision": "DDM",
                                        "Explication": "Le traitement assainissant est appliqué à des produits emballés ou suivi d'un emballage aseptique.",
                                    },
                                    "Non": {
                                        "Q8": {
                                            # Ajouter les conditions pour aw et pH
                                            "Décision": "DDM",
                                            "Explication": "Le produit ne favorise pas la croissance des bactéries.",
                                        },
                                        "Q9": {
                                            # Ajouter les conditions pour aw2 et pH2
                                            "Décision": "DDM",
                                            "Explication": "Le produit ne favorise pas la germination, la croissance et la production de toxines.",
                                        },
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    # Variables pour la navigation dans l'arbre de décision
    current_node = tree["Q1"]
    current_step = 1

    # Fonction pour afficher les questions et les réponses
    def display_question(question, options, key):
        st.markdown(f"## **{question}**")
        answer = st.radio("", options, key=key)
        return answer

    # Fonction pour gérer les étapes de l'arbre de décision
    def next_step(question, key, node):
        answer = display_question(question, ["Oui", "Non"], key)
        if answer in node:
            return node[answer], answer
        else:
            st.error("Erreur dans l'arbre de décision.")
            return None, None

    decision_path = []  # Liste pour stocker le chemin de décision
    justifications = {}  # Dictionnaire pour stocker les justifications
    uploaded_files = {}  # Dictionnaire pour stocker les fichiers téléchargés

    # Processus de l'arbre de décision
    if current_step == 1:
        q1 = display_question("Q1 : Le produit alimentaire est-il exempt de la DLC conformément au règlement (UE) n° 1169/2011 ou est-il couvert par d'autres dispositions de l'Union imposant d'autres types de marquage de la date ?", ["Oui", "Non"], "q1")
        if q1 == "Oui":
            st.success(f"Décision : {current_node[q1]['Décision']}")
            st.write(f"Explication : {current_node[q1]['Explication']}")
            display_dgal_info("Q1")
            decisions.append({"Question": "Q1", "Réponse": q1, "Décision": current_node[q1]['Décision']})
            current_step = 11  # Fin de l'arbre
        else:
            current_node = current_node[q1]
            decision_path.append(("Q1", q1))
            justification_q1 = st.text_area("Justifiez votre réponse (Q1)", key="justification_q1")
            doc_q1 = st.file_uploader("Téléchargez un document justificatif (Q1)", key="doc_q1", type=["pdf", "jpg", "png"])
            if doc_q1:
                doc_q1_name = doc_q1.name
                with open(os.path.join("uploads", doc_q1_name), "wb") as f:
                    f.write(doc_q1.getbuffer())
                uploaded_files["Q1"] = doc_q1_name
            justifications["Q1"] = justification_q1
            current_step += 1

    if current_step == 2:
        current_node, answer = next_step("Q2 : Le produit alimentaire est-il congelé ?", "q2", current_node)
        if current_node:
            decision_path.append(("Q2", answer))
            justification_q2 = st.text_area("Justifiez votre réponse (Q2)", key="justification_q2")
            doc_q2 = st.file_uploader("Téléchargez un document justificatif (Q2)", key="doc_q2", type=["pdf", "jpg", "png"])
            if doc_q2:
                doc_q2_name = doc_q2.name
                with open(os.path.join("uploads", doc_q2_name), "wb") as f:
                    f.write(doc_q2.getbuffer())
                uploaded_files["Q2"] = doc_q2_name
            justifications["Q2"] = justification_q2
            current_step += 1

    if current_step == 3:
        current_node, answer = next_step("Q3 : Le produit alimentaire subit-il un traitement assainissant validé éliminant toutes les spores des bactéries pathogènes ?", "q3", current_node)
        if current_node:
            decision_path.append(("Q3", answer))
            justification_q3 = st.text_area("Justifiez votre réponse (Q3)", key="justification_q3")
            doc_q3 = st.file_uploader("Téléchargez un document justificatif (Q3)", key="doc_q3", type=["pdf", "jpg", "png"])
            if doc_q3:
                doc_q3_name = doc_q3.name
                with open(os.path.join("uploads", doc_q3_name), "wb") as f:
                    f.write(doc_q3.getbuffer())
                uploaded_files["Q3"] = doc_q3_name
            justifications["Q3"] = justification_q3
            if answer == "Oui":
                current_step = 5
            else:
                st.error(f"Décision : {current_node['Décision']}")
                st.write(f"Explication : {current_node['Explication']}")
                display_dgal_info("Q3")
                decisions.append({"Question": "Q3", "Réponse": answer, "Décision": current_node['Décision']})
                current_step = 11

    if current_step == 4:
        current_node, answer = next_step("Q4 : Le produit alimentaire est-il soumis à un traitement assainissant validé éliminant toutes les cellules végétatives des bactéries pathogènes d'origine alimentaire ?", "q4", current_node)
        if current_node:
            decision_path.append(("Q4", answer))
            justification_q4 = st.text_area("Justifiez votre réponse (Q4)", key="justification_q4")
            doc_q4 = st.file_uploader("Téléchargez un document justificatif (Q4)", key="doc_q4", type=["pdf", "jpg", "png"])
            if doc_q4:
                doc_q4_name = doc_q4.name
                with open(os.path.join("uploads", doc_q4_name), "wb") as f:
                    f.write(doc_q4.getbuffer())
                uploaded_files["Q4"] = doc_q4_name
            justifications["Q4"] = justification_q4
            if answer == "Oui":
                current_step = 6
            else:
                current_step = 8

    if current_step == 5:
        current_node, answer = next_step("Q5a : Existe-t-il un risque de recontamination du produit alimentaire avant l'emballage ?", "q5a", current_node)
        if current_node:
            decision_path.append(("Q5a", answer))
            justification_q5a = st.text_area("Justifiez votre réponse (Q5a)", key="justification_q5a")
            doc_q5a = st.file_uploader("Téléchargez un document justificatif (Q5a)", key="doc_q5a", type=["pdf", "jpg", "png"])
            if doc_q5a:
                doc_q5a_name = doc_q5a.name
                with open(os.path.join("uploads", doc_q5a_name), "wb") as f:
                    f.write(doc_q5a.getbuffer())
                uploaded_files["Q5a"] = doc_q5a_name
            justifications["Q5a"] = justification_q5a
            if answer == "Oui":
                current_step = 7
            else:
                st.success(f"Décision : {current_node['Décision']}")
                st.write(f"Explication : {current_node['Explication']}")
                display_dgal_info("Q5a")
                decisions.append({"Question": "Q5a", "Réponse": answer, "Décision": current_node['Décision']})
                current_step = 11

    if current_step == 6:
        current_node, answer = next_step("Q5b : Y a-t-il un risque de recontamination du produit alimentaire avant son emballage ?", "q5b", current_node)
        if current_node:
            decision_path.append(("Q5b", answer))
            justification_q5b = st.text_area("Justifiez votre réponse (Q5b)", key="justification_q5b")
            doc_q5b = st.file_uploader("Téléchargez un document justificatif (Q5b)", key="doc_q5b", type=["pdf", "jpg", "png"])
            if doc_q5b:
                doc_q5b_name = doc_q5b.name
                with open(os.path.join("uploads", doc_q5b_name), "wb") as f:
                    f.write(doc_q5b.getbuffer())
                uploaded_files["Q5b"] = doc_q5b_name
            justifications["Q5b"] = justification_q5b
            if answer == "Oui":
                current_step = 7
            else:
                st.success(f"Décision : {current_node['Décision']}")
                st.write(f"Explication : {current_node['Explication']}")
                display_dgal_info("Q5b")
                decisions.append({"Question": "Q5b", "Réponse": answer, "Décision": current_node['Décision']})
                current_step = 11

    if current_step == 7:
        current_node, answer = next_step("Q6 : Le produit alimentaire subit-il un second traitement assainissant validé éliminant toutes les cellules végétatives des bactéries pathogènes d'origine ?", "q6", current_node)
        if current_node:
            decision_path.append(("Q6", answer))
            justification_q6 = st.text_area("Justifiez votre réponse (Q6)", key="justification_q6")
            doc_q6 = st.file_uploader("Téléchargez un document justificatif (Q6)", key="doc_q6", type=["pdf", "jpg", "png"])
            if doc_q6:
                doc_q6_name = doc_q6.name
                with open(os.path.join("uploads", doc_q6_name), "wb") as f:
                    f.write(doc_q6.getbuffer())
                uploaded_files["Q6"] = doc_q6_name
            justifications["Q6"] = justification_q6
            if answer == "Oui":
                st.success(f"Décision : {current_node['Décision']}")
                st.write(f"Explication : {current_node['Explication']}")
                display_dgal_info("Q6")
                decisions.append({"Question": "Q6", "Réponse": answer, "Décision": current_node['Décision']})
                current_step = 11
            else:
                st.error(f"Décision : {current_node['Décision']}")
                st.write(f"Explication : {current_node['Explication']}")
                display_dgal_info("Q6")
                decisions.append({"Question": "Q6", "Réponse": answer, "Décision": current_node['Décision']})
                current_step = 11

    if current_step == 8:
        current_node, answer = next_step("Q7 : Le traitement assainissant est-il appliqué à des produits emballés ou suivi d'un emballage aseptique ?", "q7", current_node)
        if current_node:
            decision_path.append(("Q7", answer))
            justification_q7 = st.text_area("Justifiez votre réponse (Q7)", key="justification_q7")
            doc_q7 = st.file_uploader("Téléchargez un document justificatif (Q7)", key="doc_q7", type=["pdf", "jpg", "png"])
            if doc_q7:
                doc_q7_name = doc_q7.name
                with open(os.path.join("uploads", doc_q7_name), "wb") as f:
                    f.write(doc_q7.getbuffer())
                uploaded_files["Q7"] = doc_q7_name
            justifications["Q7"] = justification_q7
            if answer == "Oui":
                st.success(f"Décision : {current_node['Décision']}")
                st.write(f"Explication : {current_node['Explication']}")
                display_dgal_info("Q7")
                decisions.append({"Question": "Q7", "Réponse": answer, "Décision": current_node['Décision']})
                current_step = 11
            else:
                current_step += 1

    if current_step == 9:
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
            st.success(f"Décision : {current_node['Décision']}")
            st.write(f"Explication : {current_node['Explication']}")
            display_dgal_info("Q8")
            decisions.append({"Question": "Q8", "Réponse": f"aw: {aw}, pH: {ph}", "Décision": current_node['Décision']})
            current_step = 11
        else:
            current_step += 1

    if current_step == 10:
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
            st.success(f"Décision : {current_node['Décision']}")
            st.write(f"Explication : {current_node['Explication']}")
            display_dgal_info("Q9")
            decisions.append({"Question": "Q9", "Réponse": f"aw: {aw2}, pH: {ph2}", "Décision": current_node['Décision']})
            current_step = 11
        else:
            st.error(f"Décision : {current_node['Décision']}")
            st.write(f"Explication : {current_node['Explication']}")
            display_dgal_info("Q9")
            decisions.append({"Question": "Q9", "Réponse": f"aw: {aw2}, pH: {ph2}", "Décision": current_node['Décision']})
            current_step = 11

    # Fin du processus
    if current_step == 11:
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

