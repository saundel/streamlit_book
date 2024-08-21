from model_classes import g, Trial
from distribution_classes import Exponential
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Simple DES Simulation")

input_col_1, input_col_2 = st.columns(2)

with input_col_1:

    receiptionists = st.slider("👨‍💻👩‍💻 How Many Receptionists Are Available?", 1, 15,
                               step=1, value=2)

    nurses = st.slider("👨‍⚕️👩‍⚕️ How Many Nurses Are Available?", 1, 15, step=1, value=3)

    n_reps = st.slider("🔁 How many times should the simulation run?",
                    1, 100,
                    step=1, value=10)

    run_time_days = st.slider("🗓️ How many days should we run the simulation for each time?",
                            1, 40,
                            step=1, value=10)


    mean_arrivals_per_day = st.slider("🧍 How many patients should arrive per day on average?",
                                    10, 300,
                                    step=5, value=120)

with input_col_2:
    consult_time_recep = st.slider("⏱️ How long (in minutes) do people spend with the receptionist on average?",
                                1, 15, step=1, value=4)

    exp_dist_recep = Exponential(consult_time_recep, random_seed=42)
    exp_fig_recep = px.histogram(exp_dist_recep.sample(size=2500), height=175)
    exp_fig_recep.update_layout(yaxis_title="", xaxis_title="Consultation Time (Minutes)",
                                margin=dict(t=0, b=0))
    exp_fig_recep.update_xaxes(tick0=0, dtick=10, range=[0, 200])
    st.plotly_chart(exp_fig_recep,
                    use_container_width=True,
                    config = {'displayModeBar': False})

    consult_time_nurse = st.slider("🕔 🕣 How long (in minutes) do people spend with the nurse on average?",
                            5, 60, step=1, value=20)

    exp_dist_nurse = Exponential(consult_time_nurse, random_seed=42)
    exp_fig_nurse = px.histogram(exp_dist_nurse.sample(size=2500), height=175)
    exp_fig_nurse.update_layout(yaxis_title="", xaxis_title="Consultation Time (Minutes)",
                                margin=dict(t=0, b=0))
    exp_fig_nurse.update_xaxes(tick0=0, dtick=10, range=[0, 360])
    st.plotly_chart(exp_fig_nurse,
                    use_container_width=True,
                    config = {'displayModeBar': False})


# A user must press a streamlit button to run the model
button_run_pressed = st.button("Run simulation")

if button_run_pressed:

    # add a spinner and then display success box
    with st.spinner('Simulating the system...'):
        g.mean_reception_time = consult_time_recep
        g.mean_n_consult_time = consult_time_nurse
        g.number_of_receptionists = receiptionists
        g.number_of_nurses = nurses
        g.number_of_runs = n_reps
        g.patient_inter = 1440 / mean_arrivals_per_day
        g.sim_duration = 1440 * run_time_days

        trial = Trial()

        trial_results_df = trial.run_trial()

        output_col_1, output_col_2 = st.columns(2)
        with output_col_1:
            st.write(f"Average queue time for receptionist: {trial_results_df["Mean Q Time Recep"].mean().round(1)} minutes")
            st.write(f"Average queue time for nurse: {trial_results_df["Mean Q Time Nurse"].mean().round(1)} minutes")

            st.dataframe(trial_results_df.round(1))


        with output_col_2:
            st.plotly_chart(px.box(trial_results_df, "Mean Q Time Recep",
                                   title="Time Spent Queueing for Receptionist - Run Variation"))

            st.plotly_chart(px.box(trial_results_df, "Mean Q Time Nurse",
                                   title="Time Spent Queueing for Nurse - Run Variation"))
