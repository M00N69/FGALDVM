import streamlit as st
import pandas as pd
import os

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
    current_step = "Q1"
    final_decision = None
    final_explanation = None

    # Fonction pour afficher les informations détaillées de la note DGAL après chaque réponse
    def display_dgal_info(step):
        st.markdown(f"""
        **Informations de la note DGAL pour l'étape {step}** :
        - **Règlement (UE) n° 1169/2011** : concerne l'information des consommateurs sur les denrées alimentaires.
        - **Critères microbiologiques** : basés sur le règlement (CE) n° 2073/2005 concernant les critères microbiologiques applicables aux denrées alimentaires.
        - **Études de vieillissement** : recommandées pour valider la durée de vie microbiologique des produits.
        """)

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
                                            "Oui": {
                                                "Décision": "DDM",
                                                "Explication": "Le produit ne favorise pas la croissance des bactéries.",
                                            },
                                            "Non": {
                                                "Q9": {
                                                    "Oui": {
                                                        "Décision": "DDM",
                                                        "Explication": "Le produit ne favorise pas la germination, la croissance et la production de toxines.",
                                                    },
                                                    "Non": {
                                                        "Décision": "DLC",
                                                        "Explication": "Le produit favorise la germination, la croissance et la production de toxines.",
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    decision_path = []
    justifications = {}
    uploaded_files = {}

    # Fonction pour afficher les questions et les réponses
    def display_question(step, question, options):
        st.markdown(f"## **{question}**")
        return st.radio("", options, key=step)

    while True:
        if current_step in ["Q1", "Q2", "Q3", "Q4", "Q5a", "Q5b", "Q6", "Q7", "Q8", "Q9"]:
            if current_step == "Q1":
                answer = display_question(current_step, "Le produit alimentaire est-il exempt de la DLC conformément au règlement (UE) n° 1169/2011 ou est-il couvert par d'autres dispositions de l'Union imposant d'autres types de marquage de la date ?", ["Oui", "Non"])
                justification = st.text_area("Justifiez votre réponse (Q1)", key="justification_q1")
                justifications["Q1"] = justification

            if current_step == "Q2":
                answer = display_question(current_step, "Le produit alimentaire est-il congelé ?", ["Oui", "Non"])
                justification = st.text_area("Justifiez votre réponse (Q2)", key="justification_q2")
                doc = st.file_uploader("Téléchargez un document justificatif (Q2)", key="doc_q2", type=["pdf", "jpg", "png"])
                if doc:
                    doc_name = doc.name
                    with open(os.path.join("uploads", doc_name), "wb") as f:
                        f.write(doc.getbuffer())
                    uploaded_files["Q2"] = doc_name
                justifications["Q2"] = justification

            if current_step == "Q3":
                answer = display_question(current_step, "Le produit alimentaire subit-il un traitement assainissant validé éliminant toutes les spores des bactéries pathogènes ?", ["Oui", "Non"])
                justification = st.text_area("Justifiez votre réponse (Q3)", key="justification_q3")
                doc = st.file_uploader("Téléchargez un document justificatif (Q3)", key="doc_q3", type=["pdf", "jpg", "png"])
                if doc:
                    doc_name = doc.name
                    with open(os.path.join("uploads", doc_name), "wb") as f:
                        f.write(doc.getbuffer())
                    uploaded_files["Q3"] = doc_name
                justifications["Q3"] = justification

            if current_step == "Q4":
                answer = display_question(current_step, "Le produit alimentaire est-il soumis à un traitement assainissant validé éliminant toutes les cellules végétatives des bactéries pathogènes d'origine alimentaire ?", ["Oui", "Non"])
                justification = st.text_area("Justifiez votre réponse (Q4)", key="justification_q4")
                doc = st.file_uploader("Téléchargez un document justificatif (Q4)", key="doc_q4", type=["pdf", "jpg", "png"])
                if doc:
                    doc_name = doc.name
                    with open(os.path.join("uploads", doc_name), "wb") as f:
                        f.write(doc.getbuffer())
                    uploaded_files["Q4"] = doc_name
                justifications["Q4"] = justification

            if current_step == "Q5a":
                answer = display_question(current_step, "Existe-t-il un risque de recontamination du produit alimentaire avant l'emballage ?", ["Oui", "Non"])
                justification = st.text_area("Justifiez votre réponse (Q5a)", key="justification_q5a")
                doc = st.file_uploader("Téléchargez un document justificatif (Q5a)", key="doc_q5a", type=["pdf", "jpg", "png"])
                if doc:
                    doc_name = doc.name
                    with open(os.path.join("uploads", doc_name), "wb") as f:
                        f.write(doc.getbuffer())
                    uploaded_files["Q5a"] = doc_name
                justifications["Q5a"] = justification

            if current_step == "Q5b":
                answer = display_question(current_step, "Y a-t-il un risque de recontamination du produit alimentaire avant son emballage ?", ["Oui", "Non"])
                justification = st.text_area("Justifiez votre réponse (Q5b)", key="justification_q5b")
                doc = st.file_uploader("Téléchargez un document justificatif (Q5b)", key="doc_q5b", type=["pdf", "jpg", "png"])
                if doc:
                    doc_name = doc.name
                    with open(os.path.join("uploads", doc_name), "wb") as f:
                        f.write(doc.getbuffer())
                    uploaded_files["Q5b"] = doc_name
                justifications["Q5b"] = justification

            if current_step == "Q6":
                answer = display_question(current_step, "Le produit alimentaire subit-il un second traitement assainissant validé éliminant toutes les cellules végétatives des bactéries pathogènes d'origine ?", ["Oui", "Non"])
                justification = st.text_area("Justifiez votre réponse (Q6)", key="justification_q6")
                doc = st.file_uploader("Téléchargez un document justificatif (Q6)", key="doc_q6", type=["pdf", "jpg", "png"])
                if doc:
                    doc_name = doc.name
                    with open(os.path.join("uploads", doc_name), "wb") as f:
                        f.write(doc.getbuffer())
                    uploaded_files["Q6"] = doc_name
                justifications["Q6"] = justification

            if current_step == "Q7":
                answer = display_question(current_step, "Le traitement assainissant est-il appliqué à des produits emballés ou suivi d'un emballage aseptique ?", ["Oui", "Non"])
                justification = st.text_area("Justifiez votre réponse (Q7)", key="justification_q7")
                doc = st.file_uploader("Téléchargez un document justificatif (Q7)", key="doc_q7", type=["pdf", "jpg", "png"])
                if doc:
                    doc_name = doc.name
                    with open(os.path.join("uploads", doc_name), "wb") as f:
                        f.write(doc.getbuffer())
                    uploaded_files["Q7"] = doc_name
                justifications["Q7"] = justification

            if current_step == "Q8":
                st.markdown("## **Q8 : Le produit alimentaire favorise-t-il la croissance des bactéries ?**")
                aw = st.selectbox("aw", ["<0,88", "0,88 à 0,9", ">0,9 à 0,92", "0,92 à 0,96", ">0,96"], key="aw")
                ph = st.selectbox("pH", ["1,9 à 4,0", "4,0 à 4,2", "4,2 à 4,4", "4,4 à 5", ">5"], key="ph")
                answer = (aw, ph)
                justification = st.text_area("Justifiez votre réponse (Q8)", key="justification_q8")
                doc = st.file_uploader("Téléchargez un document justificatif (Q8)", key="doc_q8", type=["pdf", "jpg", "png"])
                if doc:
                    doc_name = doc.name
                    with open(os.path.join("uploads", doc_name), "wb") as f:
                        f.write(doc.getbuffer())
                    uploaded_files["Q8"] = doc_name
                justifications["Q8"] = justification

            if current_step == "Q9":
                st.markdown("## **Q9 : Le produit alimentaire favorise-t-il la germination, la croissance et la production de toxines ?**")
                aw2 = st.selectbox("aw2", ["<0,92", "0,92 à 0,95", ">0,95"], key="aw2")
                ph2 = st.selectbox("pH2", ["<4,6", "4,6-5,6", ">5,6"], key="ph2")
                answer = (aw2, ph2)
                justification = st.text_area("Justifiez votre réponse (Q9)", key="justification_q9")
                doc = st.file_uploader("Téléchargez un document justificatif (Q9)", key="doc_q9", type=["pdf", "jpg", "png"])
                if doc:
                    doc_name = doc.name
                    with open(os.path.join("uploads", doc_name), "wb") as f:
                        f.write(doc.getbuffer())
                    uploaded_files["Q9"] = doc_name
                justifications["Q9"] = justification

            decision_path.append((current_step, answer))
            if "Décision" in tree[current_step][answer]:
                final_decision = tree[current_step][answer]["Décision"]
                final_explanation = tree[current_step][answer]["Explication"]
                break
            else:
                current_step = list(tree[current_step][answer].keys())[0]

    # Affichage de la décision finale
    if final_decision:
        st.success(f"Décision : {final_decision}")
        st.write(f"Explication : {final_explanation}")
        display_dgal_info(current_step)
        decisions.append({"Question": "Décision finale", "Réponse": "N/A", "Décision": final_decision})
    else:
        st.error("Erreur dans l'arbre de décision.")

    # Sauvegarde des décisions
    if st.button("Sauvegarder les décisions", key="save_button"):
        save_decision(decisions)
        st.success("Décisions sauvegardées avec succès")

if __name__ == "__main__":
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    main()
