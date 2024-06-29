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
    current_step = 1
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

    # Navigation dans l'arbre de décision
    current_node = tree["Q1"]
    decision_path = []
    justifications = {}
    uploaded_files = {}

    # Fonction pour afficher les questions et les réponses
    def display_question(question, options, key):
        st.markdown(f"## **{question}**")
        answer = st.radio("", options, key=key)
        return answer

    # Fonction pour gérer les étapes de l'arbre de décision
    def next_step(node, answer):
        if answer in node:
            return node[answer]
        else:
            st.error("Erreur dans l'arbre de décision.")
            return None

    # Processus de l'arbre de décision
    while current_step < 11:
        if "Décision" in current_node:
            final_decision = current_node["Décision"]
            final_explanation = current_node["Explication"]
            break
        else:
            if current_step == 1:
                question = "Q1 : Le produit alimentaire est-il exempt de la DLC conformément au règlement (UE) n° 1169/2011 ou est-il couvert par d'autres dispositions de l'Union imposant d'autres types de marquage de la date ?"
                key = "q1"
            elif current_step == 2:
                question = "Q2 : Le produit alimentaire est-il congelé ?"
                key = "q2"
            elif current_step == 3:
                question = "Q3 : Le produit alimentaire subit-il un traitement assainissant validé éliminant toutes les spores des bactéries pathogènes ?"
                key = "q3"
            elif current_step == 4:
                question = "Q4 : Le produit alimentaire est-il soumis à un traitement assainissant validé éliminant toutes les cellules végétatives des bactéries pathogènes d'origine alimentaire ?"
                key = "q4"
            elif current_step == 5:
                question = "Q5a : Existe-t-il un risque de recontamination du produit alimentaire avant l'emballage ?"
                key = "q5a"
            elif current_step == 6:
                question = "Q5b : Y a-t-il un risque de recontamination du produit alimentaire avant son emballage ?"
                key = "q5b"
            elif current_step == 7:
                question = "Q6 : Le produit alimentaire subit-il un second traitement assainissant validé éliminant toutes les cellules végétatives des bactéries pathogènes d'origine ?"
                key = "q6"
            elif current_step == 8:
                question = "Q7 : Le traitement assainissant est-il appliqué à des produits emballés ou suivi d'un emballage aseptique ?"
                key = "q7"
            elif current_step == 9:
                question = "Q8 : Le produit alimentaire favorise-t-il la croissance des bactéries ?"
                key = "q8"
            elif current_step == 10:
                question = "Q9 : Le produit alimentaire favorise-t-il la germination, la croissance et la production de toxines ?"
                key = "q9"

            answer = display_question(question, ["Oui", "Non"], key)
            if answer in current_node:
                current_node = current_node[answer]
            else:
                st.error("Erreur dans l'arbre de décision.")
                break
            decision_path.append((question, answer))
            justification = st.text_area(f"Justifiez votre réponse ({key})", key=f"justification_{key}")
            doc = st.file_uploader(f"Téléchargez un document justificatif ({key})", key=f"doc_{key}", type=["pdf", "jpg", "png"])
            if doc:
                doc_name = doc.name
                with open(os.path.join("uploads", doc_name), "wb") as f:
                    f.write(doc.getbuffer())
                uploaded_files[key] = doc_name
            justifications[key] = justification
            current_step += 1

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
