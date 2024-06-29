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

    # Navigation dans l'arbre de décision
    current_node = tree
    decision_path = []  # Liste pour stocker le chemin de décision
    justifications = {}  # Dictionnaire pour stocker les justifications
    uploaded_files = {}  # Dictionnaire pour stocker les fichiers téléchargés

    # Fonction pour afficher les questions et les réponses
    def display_question(question, options, key):
        st.markdown(f"## **{question}**")
        answer = st.radio("", options, key=key)
        return answer

    # Question 1
    if current_step == 1:
        q1 = display_question("Q1 : Le produit alimentaire est-il exempt de la DLC conformément au règlement (UE) n° 1169/2011 ou est-il couvert par d'autres dispositions de l'Union imposant d'autres types de marquage de la date ?", ["Oui", "Non"], "q1")
        if q1 == "Oui":
            st.success(f"Décision : {current_node[q1]['Décision']}")  # Accès direct au dictionnaire
            st.write(f"Explication : {current_node[q1]['Explication']}")
            display_dgal_info(current_step)
            decisions.append({"Question": "Q1", "Réponse": q1, "Décision": current_node[q1]['Décision']})
            current_step = 10 # Fin de l'arbre
        else:
            decision_path.append(("Q1", q1))
            current_node = current_node[q1]
            current_step += 1

    # Question 2
    if current_step == 2:
        q2 = display_question("Q2 : Le produit alimentaire est-il congelé ?", ["Oui", "Non"], "q2")
        decision_path.append(("Q2", q2))
        current_node = current_node[q2]
        current_step += 1

    # Question 3
    if current_step == 3:
        q3 = display_question("Q3 : Le produit alimentaire subit-il un traitement assainissant validé éliminant toutes les spores des bactéries pathogènes ?", ["Oui", "Non"], "q3")
        decision_path.append(("Q3", q3))
        current_node = current_node[q3]
        if q3 == "Oui":
            current_step += 1 # Passer à Q5a
        else:
            st.error(f"Décision : {current_node['Décision']}")
            st.write(f"Explication : {current_node['Explication']}")
            display_dgal_info(current_step)
            decisions.append({"Question": "Q3", "Réponse": q3, "Décision": current_node['Décision']})
            current_step = 10 # Fin de l'arbre

    # Question 4
    if current_step == 4:
        q4 = display_question("Q4 : Le produit alimentaire est-il soumis à un traitement assainissant validé éliminant toutes les cellules végétatives des bactéries pathogènes d'origine alimentaire ?", ["Oui", "Non"], "q4")
        decision_path.append(("Q4", q4))
        current_node = current_node[q4]
        if q4 == "Oui":
            current_step += 1 # Passer à Q5b
        else:
            current_step += 2 # Passer à Q7

    # Question 5a
    if current_step == 5:
        q5a = display_question("Q5a : Existe-t-il un risque de recontamination du produit alimentaire avant l'emballage ?", ["Oui", "Non"], "q5a")
        decision_path.append(("Q5a", q5a))
        current_node = current_node[q5a]
        if q5a == "Oui":
            current_step += 1 # Passer à Q6
        else:
            st.success(f"Décision : {current_node['Décision']}")
            st.write(f"Explication : {current_node['Explication']}")
            display_dgal_info(current_step)
            decisions.append({"Question": "Q5a", "Réponse": q5a, "Décision": current_node['Décision']})
            current_step = 10 # Fin de l'arbre

    # Question 5b
    if current_step == 6:
        q5b = display_question("Q5b : Y a-t-il un risque de recontamination du produit alimentaire avant son emballage ?", ["Oui", "Non"], "q5b")
        decision_path.append(("Q5b", q5b))
        current_node = current_node[q5b]
        if q5b == "Oui":
            current_step += 1 # Passer à Q6
        else:
            st.success(f"Décision : {current_node['Décision']}")
            st.write(f"Explication : {current_node['Explication']}")
            display_dgal_info(current_step)
            decisions.append({"Question": "Q5b", "Réponse": q5b, "Décision": current_node['Décision']})
            current_step = 10 # Fin de l'arbre

    # Question 6
    if current_step == 7:
        q6 = display_question("Q6 : Le produit alimentaire subit-il un second traitement assainissant validé éliminant toutes les cellules végétatives des bactéries pathogènes d'origine ?", ["Oui", "Non"], "q6")
        decision_path.append(("Q6", q6))
        current_node = current_node[q6]
        if q6 == "Oui":
            st.success(f"Décision : {current_node['Décision']}")
            st.write(f"Explication : {current_node['Explication']}")
            display_dgal_info(current_step)
            decisions.append({"Question": "Q6", "Réponse": q6, "Décision": current_node['Décision']})
            current_step = 10 # Fin de l'arbre
        else:
            st.error(f"Décision : {current_node['Décision']}")
            st.write(f"Explication : {current_node['Explication']}")
            display_dgal_info(current_step)
            decisions.append({"Question": "Q6", "Réponse": q6, "Décision": current_node['Décision']})
            current_step = 10 # Fin de l'arbre

    # Question 7
    if current_step == 8:
        q7 = display_question("Q7 : Le traitement assainissant est-il appliqué à des produits emballés ou suivi d'un emballage aseptique ?", ["Oui", "Non"], "q7")
        decision_path.append(("Q7", q7))
        current_node = current_node[q7]
        if q7 == "Oui":
            st.success(f"Décision : {current_node['Décision']}")
            st.write(f"Explication : {current_node['Explication']}")
            display_dgal_info(current_step)
            decisions.append({"Question": "Q7", "Réponse": q7, "Décision": current_node['Décision']})
            current_step = 10 # Fin de l'arbre
        else:
            current_step += 1 # Passer à Q8

    # Question 8
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
            st.success(f"Décision : {current_node['Q8']['Décision']}")
            st.write(f"Explication : {current_node['Q8']['Explication']}")
            display_dgal_info(current_step)
            decisions.append({"Question": "Q8", "Réponse": f"aw: {aw}, pH: {ph}", "Décision": current_node['Q8']['Décision']})
            current_step = 10 # Fin de l'arbre
        else:
            current_step += 1 # Passer à Q9

    # Question 9
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
            st.success(f"Décision : {current_node['Q9']['Décision']}")
            st.write(f"Explication : {current_node['Q9']['Explication']}")
            display_dgal_info(current_step)
            decisions.append({"Question": "Q9", "Réponse": f"aw: {aw2}, pH: {ph2}", "Décision": current_node['Q9']['Décision']})
            current_step = 11 # Fin de l'arbre
        else:
            st.error(f"Décision : {current_node['Q9']['Décision']}")
            st.write(f"Explication : {current_node['Q9']['Explication']}")
            display_dgal_info(current_step)
            decisions.append({"Question": "Q9", "Réponse": f"aw: {aw2}, pH: {ph2}", "Décision": current_node['Q9']['Décision']})
            current_step = 11 # Fin de l'arbre

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
