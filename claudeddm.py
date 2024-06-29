import streamlit as st
# ... (autres imports inchangés)

# ... (le reste du code reste inchangé jusqu'à la fonction main)

def main():
    # ... (code précédent inchangé)

    if 'current_question' not in st.session_state:
        reset_session_state()

    if st.session_state.result is None:
        current_q = questions.get(st.session_state.current_question)
        if current_q is None:
            st.error("Une erreur s'est produite. Veuillez recommencer.")
            reset_session_state()
            st.experimental_rerun()
        else:
            st.subheader(current_q['question'])
            st.info(current_q['explanation'])

            if st.session_state.current_question in ['q8', 'q9']:
                # ... (code pour les questions q8 et q9 inchangé)
            else:
                # ... (code pour les autres questions inchangé)

            # Calcul de la progression corrigé
            question_list = list(questions.keys())
            if st.session_state.current_question in question_list:
                progress = (question_list.index(st.session_state.current_question) + 1) / len(question_list)
            else:
                progress = 0
            st.progress(progress)

    else:
        # ... (code pour l'affichage du résultat inchangé)

    # ... (reste du code inchangé)

if __name__ == "__main__":
    main()
