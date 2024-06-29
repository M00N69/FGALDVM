import streamlit as st

def main():
    st.title("Détermination DLC ou DDM")
    st.write("Utilisez cet outil pour déterminer si votre produit alimentaire doit être étiqueté avec une Date Limite de Consommation (DLC) ou une Date de Durabilité Minimale (DDM).")

    # Etiquetage selon la réglementation en vigueur
    st.markdown("---")
    st.subheader("1. Étiquetage selon la réglementation en vigueur:")
    q1 = st.radio("Q1 : Le produit alimentaire est-il exempt de la DLC conformément au règlement (UE) n° 1169/2011 ou est-il couvert par d'autres dispositions de l'Union imposant d'autres types de marquage de la date ?", ["Oui", "Non"])

    if q1 == "Oui":
        st.success("Etiquetage selon la réglementation en vigueur.")
        st.stop()

    # Congélation du produit
    st.markdown("---")
    st.subheader("2. Congélation du produit:")
    q2 = st.radio("Q2 : Le produit alimentaire est-il congelé ?", ["Oui", "Non"])

    # Traitement assainissant validé
    if q2 == "Non":
        st.markdown("---")
        st.subheader("3. Traitement assainissant validé:")
        q3 = st.radio("Q3 : Le produit alimentaire subit-il un traitement assainissant valide éliminant toutes les spores des bactéries pathogènes ?", ["Oui", "Non"])

    # Risque de recontamination
    if (q2 == "Non" and q3 == "Oui") or (q2 == "Non" and q3 == "Non"):
        st.markdown("---")
        st.subheader("4. Risque de recontamination:")
        q4 = st.radio("Q4 : Le produit alimentaire est-il soumis à un traitement assainissant valide éliminant toutes les cellules végétatives des bactéries pathogènes d'origine alimentaire ?", ["Oui", "Non"])

    # Risque de recontamination (bis)
    if q4 == "Non":
        st.markdown("---")
        st.subheader("5. Risque de recontamination (bis):")
        q5a = st.radio("Q5a : Existe-t-il un risque de recontamination du produit alimentaire avant l'emballage ?", ["Oui", "Non"])
        if q5a == "Oui":
            q5b = st.radio("Q5b : Y-a-t-il un risque de recontamination du produit alimentaire avant son emballage ?", ["Oui", "Non"])

    # Second traitement assainissant validé
    if (q4 == "Oui" or (q4 == "Non" and (q5a == "Non" or (q5a == "Oui" and q5b == "Non")))):
        st.markdown("---")
        st.subheader("6. Second traitement assainissant validé:")
        q6 = st.radio("Q6 : Le produit alimentaire subit-il un second traitement assainissant validé éliminant toutes les cellules végétatives des bactéries pathogènes d'origine ?", ["Oui", "Non"])

    # Traitement assainissant appliqué à des produits emballés ou suivi d'un emballage aseptique
    if q6 == "Oui":
        st.markdown("---")
        st.subheader("7. Traitement assainissant appliqué à des produits emballés ou suivi d'un emballage aseptique:")
        q7 = st.radio("Q7 : Le traitement assainissant est-il appliqué à des produits emballés ou suivi d'un emballage aseptique ?", ["Oui", "Non"])

    # Croissance des bactéries
    if q7 == "Oui":
        st.markdown("---")
        st.subheader("8. Croissance des bactéries:")
        st.write("Pour répondre, vérifiez le tableau suivant :")
        st.write("F : Favorise la croissance | NF : Ne favorise pas la croissance")

        aw = st.slider("Choisissez la valeur de l'activité de l'eau (aw) : ", 0.0, 1.0, 0.88, step=0.01)
        ph = st.slider("Choisissez la valeur du pH : ", 1.0, 7.0, 4.6, step=0.1)

        if aw < 0.88:
            q8 = "NF"
        elif aw < 0.9:
            q8 = "NF"
        elif aw < 0.92:
            q8 = "NF"
        elif aw < 0.96:
            q8 = "NF"
        elif aw < 1.0:
            q8 = "NF"
        else:
            q8 = "NF"

        if ph < 4.6:
            q8 = "NF"
        elif ph < 5.6:
            q8 = "NF"
        else:
            q8 = "F"

        st.write(f"a<sub>w</sub> : {aw} | pH : {ph} | Favorise la croissance : {q8}")

    # Croissance et production de toxines
    if q8 == "F":
        st.markdown("---")
        st.subheader("9. Croissance et production de toxines:")
        st.write("Pour répondre, consultez le tableau suivant :")
        st.write("T : Favorise la production de toxines | NT : Ne pas soutenir la production de toxines")

        aw = st.slider("Choisissez la valeur de l'activité de l'eau (aw) : ", 0.0, 1.0, 0.92, step=0.01)
        ph = st.slider("Choisissez la valeur du pH : ", 4.0, 7.0, 5.6, step=0.1)

        if aw < 0.92:
            q9 = "NT"
        elif aw < 0.95:
            q9 = "NT"
        else:
            q9 = "T"

        if ph < 4.6:
            q9 = "NT"
        elif ph < 5.6:
            q9 = "NT"
        else:
            q9 = "T"

        st.write(f"a<sub>w</sub> : {aw} | pH : {ph} | Favorise la production de toxines : {q9}")

    # Capacité à démontrer une approche par étapes
    if q8 == "F" and q9 == "T":
        st.markdown("---")
        st.subheader("10. Capacité à démontrer une approche par étapes:")
        q10 = st.radio("Q10 : L'opérateur est-il en mesure de démontrer (approche par étapes décrite à la section 3.4) que le produit alimentaire ne favorise pas la croissance et/ou la production de toxines de bactéries pathogènes dans des conditions de température raisonnablement prévisibles pendant la distribution ?", ["Oui", "Non"])

    # Conclusion
    st.markdown("---")
    st.subheader("Conclusion:")
    if q10 == "Oui":
        st.success("Le produit alimentaire peut être étiqueté avec une DLC.")
    else:
        st.success("Le produit alimentaire peut être étiqueté avec une DDM.")
        st.write("**Pas de croissance ni de production de toxines de bactéries pathogènes pendant la durée de conservation.** Le produit alimentaire peut être conservé à température ambiante sauf si des raisons de qualité exigent une réfrigération.")

if __name__ == "__main__":
    main()
