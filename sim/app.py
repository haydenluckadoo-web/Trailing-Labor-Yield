import streamlit as st
import pandas as pd
import numpy as np
import os

CSV_FILE = "saved_simulations.csv"

def load_saved_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    return pd.DataFrame()

def save_simulation(sim_name, params, results):
    df = load_saved_data()
    record = {"Sim_Name": sim_name}
    record.update({f"Param_{k}": v for k, v in params.items()})
    record.update({f"Result_{k}": v for k, v in results.items()})
    new_row = pd.DataFrame([record])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

def delete_simulation(index):
    df = load_saved_data()
    if not df.empty and index in df.index:
        df = df.drop(index)
        df.to_csv(CSV_FILE, index=False)

def generate_trajectory(base_val, periods, mode="Constant", volatility=0.0):
    if mode == "Constant":
        return np.full(periods, base_val)
    elif mode == "Volatile (Normal)":
        return np.random.normal(loc=base_val, scale=volatility, size=periods)
    else:
        return np.full(periods, base_val)

def run_dynamic_sim(p):
    periods = p["horizon_periods"]
    
    worker_growth = generate_trajectory(p["worker_growth"], periods, "Constant", 0.0)
    wage_growth = generate_trajectory(p["wage_growth"], periods, "Constant", 0.0)
    accrual_share = generate_trajectory(p["accrual_share"], periods, "Constant", 0.0) 
    
    records = []
    
    current_workers = p["initial_workers"]
    current_wage = p["wage_per_worker"]
    historical_pay_pool = 0.0  
    
    # List of dicts: {'amount': initial_bonus, 'age': 0}
    legacy_cohorts = []
    
    for t in range(periods):
        if t > 0:
            current_workers *= (1.0 + worker_growth[t])
            current_wage *= (1.0 + wage_growth[t])
            
        base_payroll = current_workers * current_wage
        
        # Gross Profit Model based on Company Profile
        revenue = base_payroll * p["revenue_multiplier"]
        gross_profit = revenue * p["gross_margin"]
        
        # Active Bonus Calculation
        active_bonus_payout = (historical_pay_pool + base_payroll) * accrual_share[t]
        
        # Legacy Payout with Decay
        current_legacy_payout = 0.0
        for cohort in legacy_cohorts:
            if cohort["age"] < p["legacy_payout_years"]:
                # Apply decay formula: Amount * (1 - decay)^age
                payout_this_year = cohort["amount"] * ((1.0 - p["annuity_decay_rate"]) ** cohort["age"])
                current_legacy_payout += payout_this_year
                cohort["age"] += 1
                
        total_cash_outflow = base_payroll + active_bonus_payout + current_legacy_payout
        annuity_pct_of_gross_profit = current_legacy_payout / gross_profit if gross_profit > 0 else 0
        
        records.append({
            "Period": t,
            "Workers": current_workers,
            "Gross_Profit": gross_profit,
            "Base_Payroll": base_payroll,
            "Historical_Pay_Pool": historical_pay_pool,
            "Active_Bonus_Payout": active_bonus_payout,
            "Legacy_Annuity_Payout": current_legacy_payout,
            "Total_Cash_Outflow": total_cash_outflow,
            "Annuity_Pct_of_GP": annuity_pct_of_gross_profit * 100 # stored as percentage
        })
        
        # Transition to Next Period
        new_legacy_cohort = active_bonus_payout * p["turnover_rate"]
        legacy_cohorts.append({"amount": new_legacy_cohort, "age": 0})
        
        total_active_comp = base_payroll + active_bonus_payout
        historical_pay_pool = (historical_pay_pool + total_active_comp) * (1.0 - p["turnover_rate"])

    df = pd.DataFrame(records)
    
    final_results = {
        "Final_Gross_Profit": df.iloc[-1]["Gross_Profit"],
        "Final_Legacy_Payout": df.iloc[-1]["Legacy_Annuity_Payout"],
        "Final_Annuity_Burden_Pct": df.iloc[-1]["Annuity_Pct_of_GP"]
    }
    
    return df, final_results

# --- STREAMLIT UI ---
st.set_page_config(page_title="Compounding Annuity Dashboard", layout="wide")
st.title("Decaying Annuity & Company Profiles Simulator")

tab1, tab2, tab_data = st.tabs(["Workspace A", "Workspace B", "Data Manager"])

# Predefined Company Profiles
PROFILES = {
    "Custom": {"rev_mult": 2.5, "margin": 0.50, "growth": 0.02, "turnover": 0.08},
    "High-Growth SaaS": {"rev_mult": 3.5, "margin": 0.80, "growth": 0.15, "turnover": 0.15},
    "Stable Agency/Consulting": {"rev_mult": 2.0, "margin": 0.50, "growth": 0.05, "turnover": 0.10},
    "Low-Margin Retail": {"rev_mult": 4.0, "margin": 0.30, "growth": 0.02, "turnover": 0.30}
}

def render_sim_workspace(tab_key):
    st.header(f"Simulation {tab_key}")
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        st.subheader("Base Parameters")
        sim_name = st.text_input("Simulation Name", f"Sim_{tab_key}", key=f"name_{tab_key}")
        horizon = st.number_input("Periods", 10, 200, 80, key=f"h_{tab_key}")
        
        st.subheader("Company Profile")
        profile_choice = st.selectbox("Select Business Model", list(PROFILES.keys()), key=f"prof_{tab_key}")
        prof = PROFILES[profile_choice]
        
        rev_mult = st.number_input("Revenue to Payroll Multiplier", 1.0, 10.0, prof["rev_mult"], key=f"rm_{tab_key}")
        margin = st.slider("Gross Margin", 0.01, 0.99, prof["margin"], key=f"gm_{tab_key}")
        w_growth = st.number_input("Worker Growth", -0.10, 0.50, prof["growth"], key=f"wg_{tab_key}")
        turnover_rate = st.slider("Turnover Rate", 0.0, 0.50, prof["turnover"], key=f"tr_{tab_key}")

    with col2:
        st.subheader("Compensation Rules")
        init_workers = st.number_input("Init Workers", 0, 100000, 1000, key=f"iw_{tab_key}")
        init_wage = st.number_input("Init Wage", 0, 500000, 100000, key=f"iwa_{tab_key}")
        wage_growth = st.number_input("Wage Growth Base", -0.05, 0.20, 0.02, key=f"wag_{tab_key}")
        
        st.divider()
        accrual = st.number_input("Accrual Share Base", 0.0, 0.20, 0.01, 0.005, format="%.3f", key=f"ac_{tab_key}")
        legacy_years = st.number_input("Legacy Payout Years", 1, 100, 25, key=f"lpy_{tab_key}")
        decay_rate = st.number_input("Annuity Annual Decay Rate", 0.0, 0.50, 0.05, 0.01, format="%.2f", key=f"dec_{tab_key}", help="The percentage by which a departed worker's legacy payout drops each year.")

    params = {
        "horizon_periods": horizon, "initial_workers": init_workers, "wage_per_worker": init_wage,
        "worker_growth": w_growth, "wage_growth": wage_growth, "accrual_share": accrual, 
        "turnover_rate": turnover_rate, "legacy_payout_years": legacy_years, 
        "annuity_decay_rate": decay_rate, "revenue_multiplier": rev_mult, "gross_margin": margin
    }

    with col3:
        st.subheader("Simulation Results")
        if st.button(f"Run Simulation {tab_key}", type="primary"):
            df, final_metrics = run_dynamic_sim(params)
            st.session_state[f"df_{tab_key}"] = df
            st.session_state[f"metrics_{tab_key}"] = final_metrics
            st.session_state[f"params_{tab_key}"] = params

        if f"df_{tab_key}" in st.session_state:
            df = st.session_state[f"df_{tab_key}"]
            
            st.write("**Gross Profit vs Total Cash Outflows ($)**")
            st.line_chart(df.set_index("Period")[["Gross_Profit", "Total_Cash_Outflow"]])
            
            st.write("**Annuity Burden (% of Gross Profit)**")
            st.line_chart(df.set_index("Period")[["Annuity_Pct_of_GP"]])
            
            st.write("**Cash Outflows Breakdown ($)**")
            st.area_chart(df.set_index("Period")[["Base_Payroll", "Active_Bonus_Payout", "Legacy_Annuity_Payout"]])
            
            if st.button(f"Save '{sim_name}' to Database", icon="💾", key=f"save_{tab_key}"):
                save_simulation(sim_name, st.session_state[f"params_{tab_key}"], st.session_state[f"metrics_{tab_key}"])
                st.success(f"Saved {sim_name} to CSV!")

with tab1: render_sim_workspace("A")
with tab2: render_sim_workspace("B")

with tab_data:
    st.header("Saved Simulations Database")
    db_df = load_saved_data()
    if not db_df.empty:
        st.dataframe(db_df, use_container_width=True)
        col_del1, col_del2 = st.columns([1, 4])
        with col_del1:
            row_to_delete = st.selectbox("Select Row Index to Delete", db_df.index)
            if st.button("Delete Selected Row", type="primary"):
                delete_simulation(row_to_delete)
                st.rerun()