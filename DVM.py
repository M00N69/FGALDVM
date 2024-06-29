import streamlit as st
import pandas as pd
import os

# Fonction pour sauvegarder les décisions
def save_decision(data):
    df = pd.DataFrame(data)
    df.to_csv('decisions.csv', mode='a', index=False, header=False)

def display_dgal_info(step):
    st.markdown(f"""
    **Informations de la note DGAL pour l'étape {step}** :
    - **Règlement (UE) n° 1169/2011** : concerne l'information des consommateurs sur les denrées alimentaires.
    - **Critères microbiologiques** : basés sur le règlement (CE) n° 2073/2005 concernant les critères microbiologiques applicables aux denrées alimentaires.
    - **Études de vieillissement** : recommandées pour valider la durée de vie microbiologique des produits.
    """)

def display_question(question, options, key):
    st.markdown(f"## **{question}**")
    return st.radio("", options, key=key)

def initialize_state():
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1
    if 'decision_path' not in st.session_state:
        st.session_state.decision_path = []
    if 'final_decision' not in st.session_state:
        st.session_state.final_decision = None
    if 'final_explanation' not in st.session_state:
        st.session_state.final_explanation = None
    if 'decisions' not in st.session_state:
        st.session_state.decisions = []

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

    initialize_state()

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
                                            "Décision": "DDM",
                                            "Explication": "Le produit ne favorise pas la croissance des bactéries.",
                                        },
                                        "Q9": {
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

    def navigate_tree(node, step, question, options, key):
        answer = display_question(question, options, key)
        st.session_state.decision_path.append((key, answer))
        if answer in node:
            next_node = node[answer]
            if "Décision" in next_node:
                st.session_state.final_decision = next_node["Décision"]
                st.session_state.final_explanation = next_node["Explication"]
                st.session_state.current_step = 11
            else:
                st.session_state.current_step = step + 1
                st.session_state.current_node = next_node
        else:
            st.error(f"Option invalide sélectionnée pour {key}.")

    current_step = st.session_state.current_step
    if current_step == 1:
        navigate_tree(tree["Q1"], current_step,
                      "Q1 : Le produit alimentaire est-il exempt de la DLC conformément au règlement (UE) n° 1169/2011 ou est-il couvert par d'autres dispositions de l'Union imposant d'autres types de marquage de la date ?",
                      ["Oui", "Non"], "q1")

    elif current_step == 2:
        navigate_tree(st.session_state.current_node, current_step,
                      "Q2 : Le produit alimentaire est-il congelé ?", ["Oui", "Non"], "q2")

    elif current_step == 3:
        navigate_tree(st.session_state.current_node, current_step,
                      "Q3 : Le produit alimentaire subit-il un traitement assainissant validé éliminant toutes les spores des bactéries pathogènes ?", ["Oui", "Non"], "q3")

    elif current_step == 4:
        navigate_tree(st.session_state.current_node, current_step,
                      "Q4 : Le produit alimentaire est-il soumis à un traitement assainissant validé éliminant toutes les cellules végétatives des bactéries pathogènes d'origine alimentaire ?", ["Oui", "Non"], "q4")

    elif current_step == 5:
        navigate_tree(st.session_state.current_node, current_step,
                      "Q5a : Existe-t-il un risque de recontamination du produit alimentaire avant l'emballage ?", ["Oui", "Non"], "q5a")

    elif current_step == 6:
        navigate_tree(st.session_state.current_node, current_step,
                      "Q5b : Y a-t-il un risque de recontamination du produit alimentaire avant son emballage ?", ["Oui", "Non"], "q5b")

    elif current_step == 7:
        navigate_tree(st.session_state.current_node, current_step,
                      "Q6 : Le produit alimentaire subit-il un second traitement assainissant validé éliminant toutes les cellules végétatives des bactéries pathogènes d'origine ?", ["Oui", "Non"], "q6")

    elif current_step == 8:
        navigate_tree(st.session_state.current_node, current_step,
                      "Q7 : Le traitement assainissant est-il appliqué à des produits emballés ou suivi d'un emballage aseptique ?", ["Oui", "Non"], "q7")

    elif current_step == 9:
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
            st.session_state.final_decision = st.session_state.current_node['Q8']['Décision']
            st.session_state.final_explanation = st.session_state.current_node['Q8']['Explication']
            st.session_state.current_step = 11
        else:
            st.session_state.current_step += 1

    elif current_step == 10:
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
            st.session_state.final_decision = st.session_state.current_node['Q9']['Décision']
            st.session_state.final_explanation = st.session_state.current_node['Q9']['Explication']
            st.session_state.current_step = 11
        else:
            st.session_state.final_decision = st.session_state.current_node['Q9']['Décision']
            st.session_state.final_explanation = st.session_state.current_node['Q9']['Explication']
            st.session_state.current_step = 11

    if st.session_state.current_step == 11:
        if st.session_state.final_decision:
            st.success(f"Décision : {st.session_state.final_decision}")
            st.write(f"Explication : {st.session_state.final_explanation}")
            display_dgal_info(st.session_state.current_step)
            st.session_state.decisions.append({"Question": "Décision finale", "Réponse": "N/A", "Décision": st.session_state.final_decision})
        else:
            st.error("Erreur dans l'arbre de décision.")

    if st.button("Sauvegarder les décisions", key="save_button"):
        save_decision(st.session_state.decisions)
        st.success("Décisions sauvegardées avec succès")

if __name__ == "__main__":
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    main()
