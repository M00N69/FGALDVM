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
                                            "Décision": "DDM",
                                            "Explication": "Le produit ne favorise pas la croissance des bactéries.",
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "Q8": {
            "Oui": {
                "Décision": "DDM",
                "Explication": "Le produit ne favorise pas la croissance des bactéries."
            },
            "Non": {
                "Q9": {
                    "Oui": {
                        "Décision": "DDM",
                        "Explication": "Le produit ne favorise pas la germination, la croissance et la production de toxines."
                    },
                    "Non": {
                        "Décision": "DLC",
                        "Explication": "Le produit favorise la germination, la croissance et la production de toxines."
                    }
                }
            }
        }
    }

    # Variables pour la navigation dans l'arbre de décision
    current_node = tree["Q1"]
    current_step = "Q1"

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

    decision_path = []  # Liste pour stocker le chemin de décision
    justifications = {}  # Dictionnaire pour stocker les justifications
    uploaded_files = {}  # Dictionnaire pour stocker les fichiers téléchargés

    while True:
        if "Décision" in current_node:
            st.success(f"Décision : {current_node['Décision']}")
            st.write(f"Explication : {current_node['Explication']}")
            display_dgal_info(current_step)
            decisions.append({"Question": current_step, "Réponse": answer, "Décision": current_node['Décision']})
            break
        else:
            question = current_step + " : " + list(current_node.keys())[0]
            options = list(current_node[list(current_node.keys())[0]].keys())
            answer = display_question(question, options, current_step)
            current_node = next_step(current_node[list(current_node.keys())[0]], answer)
            if current_node is None:
                break
            decision_path.append((current_step, answer))
            justification = st.text_area(f"Justifiez votre réponse ({current_step})", key=f"justification_{current_step}")
            doc = st.file_uploader(f"Téléchargez un document justificatif ({current_step})", key=f"doc_{current_step}", type=["pdf", "jpg", "png"])
            if doc:
                doc_name = doc.name
                with open(os.path.join("uploads", doc_name), "wb") as f:
                    f.write(doc.getbuffer())
                uploaded_files[current_step] = doc_name
            justifications[current_step] = justification
            current_step = answer

    # Fin du processus
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


