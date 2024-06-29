    # ... (code précédent)

    # Question 1
    if current_step == 1:
        q1 = display_question("Q1 : Le produit alimentaire est-il exempt de la DLC conformément au règlement (UE) n° 1169/2011 ou est-il couvert par d'autres dispositions de l'Union imposant d'autres types de marquage de la date ?", ["Oui", "Non"], "q1")
        decision_path.append(("Q1", q1))
        current_node = current_node[q1]
        current_step += 1

    # ... (code pour les autres questions)

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
            decision_path.append(("Q8", f"aw: {aw}, pH: {ph}"))
            current_node = current_node['Q8'] # Accéder au noeud suivant 
            current_step += 1
        else:
            current_step += 1

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
            decision_path.append(("Q9", f"aw: {aw2}, pH: {ph2}"))
            current_node = current_node['Q9'] # Accéder au noeud suivant 
            current_step += 1
        else:
            current_step += 1

    # Affichage de la décision finale
    if current_step == 11:
        if "Décision" in current_node: # Vérification de la présence de la clé
            final_decision = current_node['Décision']
            final_explanation = current_node['Explication']
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
