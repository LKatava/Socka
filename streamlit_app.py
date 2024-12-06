import streamlit as st
import pandas as pd

# Inicializacija ili učitavanje podataka
if 'data' not in st.session_state:
    st.session_state['data'] = pd.DataFrame(columns=['Volonter', 'Datum', 'Sati'])

# Forma za unos podataka
st.header("Logiranje volonterskih sati")
with st.form(key="log_form"):
    volonter = st.text_input("Ime volontera:")
    datum = st.date_input("Datum volontiranja:")
    sati = st.number_input("Broj sati:", min_value=0.0, step=0.5)
    submit_button = st.form_submit_button("Dodaj")

    if submit_button and volonter:
        new_row = {'Volonter': volonter, 'Datum': datum, 'Sati': sati}
        st.session_state['data'] = pd.concat(
            [st.session_state['data'], pd.DataFrame([new_row])], ignore_index=True
        )
        st.success(f"Volonter {volonter} je dodan s {sati} sati za datum {datum}.")

# Prikaz podataka
st.header("Popis volontera")
if not st.session_state['data'].empty:
    st.dataframe(st.session_state['data'])

    # Ukupno sati po volonteru
    ukupno = st.session_state['data'].groupby('Volonter')['Sati'].sum().reset_index()
    st.subheader("Ukupno sati po volonteru")
    st.dataframe(ukupno)

    # Filtriranje po datumu
    st.subheader("Filtriraj po datumu")
    start_date = st.date_input("Početni datum:", value=st.session_state['data']['Datum'].min())
    end_date = st.date_input("Krajnji datum:", value=st.session_state['data']['Datum'].max())

    if start_date and end_date:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        filtered_data = st.session_state['data'][
            (st.session_state['data']['Datum'] >= start_date) &
            (st.session_state['data']['Datum'] <= end_date)
        ]
        st.dataframe(filtered_data)

    # Vizualizacija
    st.subheader("Vizualizacija sati po datumu")
    if not filtered_data.empty:
        daily_summary = filtered_data.groupby('Datum')['Sati'].sum().reset_index()
        st.line_chart(daily_summary.set_index('Datum'))

    # Preuzimanje podataka
    csv = st.session_state['data'].to_csv(index=False)
    st.download_button("Preuzmi podatke kao CSV", csv, "volonteri.csv", "text/csv")
else:
    st.info("Nema podataka za prikaz.")
