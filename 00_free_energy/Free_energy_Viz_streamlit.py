import streamlit as st
import numpy as np
import sympy as sp
import pandas as pd
from pycalphad import Database, Model, variables as v
import plotly.graph_objects as go
from fparser import *  # Custom module, assumed available

def curves_two():
    # Streamlit app configuration
    st.set_page_config(page_title="Gibbs Free Energy 3D Plots", layout="wide")
    st.title("Gibbs Free Energy 3D Visualization")
    st.markdown("Explore Gibbs free energy for LIQUID and FCC phases across compositions of Co, Cr, and Fe.")

    # Load the thermodynamic database
    db_filename = 'tdb_files/FeNi.TDB'
    try:
        db = Database(db_filename)
    except Exception as e:
        st.error(f"Error loading TDB file: {e}")
        st.stop()

    phases = ['LIQUID', 'FCC_A1', 'BCC_A2']

    # Initialize models and Gibbs free energy expressions
    for i in range(3):
        constituents = ['FE', 'NI', 'VA']
        m = Model(db, constituents, phases[i])
        if i == 0:
            G_LIQ = m.ast.subs({'T':'temp', 'LIQUID0FE':'c1', 'LIQUID0NI':'(1-c1)', 'FCC_A10FE':'c2', 'FCC_A10NI':'(1-c2)', 'BCC_A20FE':'c3', 'BCC_A20NI':'(1-c3)', 'FCC_A11VA':1, 'BCC_A21VA':1, 'P':101325})
        if i == 1:
            G_FCC = m.ast.subs({'T':'temp', 'LIQUID0FE':'c1', 'LIQUID0NI':'(1-c1)', 'FCC_A10FE':'c2', 'FCC_A10NI':'(1-c2)', 'BCC_A20FE':'c3', 'BCC_A20NI':'(1-c3)', 'FCC_A11VA':1, 'BCC_A21VA':1, 'P':101325})
        else:
            G_BCC = m.ast.subs({'T':'temp', 'LIQUID0FE':'c1', 'LIQUID0NI':'(1-c1)', 'FCC_A10FE':'c2', 'FCC_A10NI':'(1-c2)', 'BCC_A20FE':'c3', 'BCC_A20NI':'(1-c3)', 'FCC_A11VA':1, 'BCC_A21VA':1, 'P':101325})

    # Streamlit sidebar with styled inputs for each variable
    st.sidebar.header("Composition Settings")
    st.sidebar.markdown("**Configure ranges and intervals for each composition variable.**")

    # Inputs for c_Fe
    st.sidebar.subheader("c_Fe Settings")
    min_val_fe = st.sidebar.number_input("c_Fe Minimum", min_value=0.0, max_value=1.0, value=0.0, step=0.01, key="fe_min")
    max_val_fe = st.sidebar.number_input("c_Fe Maximum", min_value=0.0, max_value=1.0, value=1.0, step=0.01, key="fe_max")
    interval_fe = st.sidebar.number_input("c_Fe Interval", min_value=0.001, max_value=0.1, value=0.05, step=0.01, key="fe_interval")

    max_Temp = st.sidebar.number_input("T Maximum", min_value=350.0, max_value=3000.0, value=1500.0, step=1.00, key="T_max")

    # Validate inputs
    for var, min_val, max_val, interval in [("c_Fe", min_val_fe, max_val_fe, interval_fe)]:
        if min_val >= max_val:
            st.error(f"{var}: Minimum value must be less than maximum value.")
            st.stop()
        if interval <= 0:
            st.error(f"{var}: Interval must be positive.")
            st.stop()

    # Define composition ranges and temperature
    comp_values_fe = np.arange(min_val_fe, max_val_fe + interval_fe / 2, interval_fe)
    temp = np.linspace(300, max_Temp, 50)  # Reduced points for performance

    # Initialize arrays for each variable
    data = {
        'c_Fe': {'comp_values': comp_values_fe, 'F_LIQ': np.zeros((len(comp_values_fe), len(temp))), 'F_FCC': np.zeros((len(comp_values_fe), len(temp))), 'F_BCC': np.zeros((len(comp_values_fe), len(temp)))}
    }

    # Compute Gibbs free energy for each variable
    for variable in ['c_Fe']:
        comp_values = data[variable]['comp_values']
        F_LIQ_data = data[variable]['F_LIQ']
        F_FCC_data = data[variable]['F_FCC']
        F_BCC_data = data[variable]['F_BCC']
        
        for i, val in enumerate(comp_values):
            c_Fe = val if variable == "c_Fe" else 0.88
            c_Ni = 1 - c_Fe
            
            if c_Ni < 0:
                st.warning(f"Negative c_Ni ({c_Ni:.3f}) for {variable} = {val:.3f}. Skipping this value.")
                continue

            LIQ_G = G_LIQ.subs({'c1': c_Fe,})
            FCC_G = G_FCC.subs({'c2': c_Fe,})
            BCC_G = G_BCC.subs({'c3': c_Fe,})
            
            temperature_subs_LIQ = sp.lambdify('temp', LIQ_G, modules="numpy")
            temperature_subs_FCC = sp.lambdify('temp', FCC_G, modules="numpy")
            temperature_subs_BCC = sp.lambdify('temp', BCC_G, modules="numpy")
            
            F_LIQ_data[i] = temperature_subs_LIQ(temp)
            F_FCC_data[i] = temperature_subs_FCC(temp)
            F_BCC_data[i] = temperature_subs_BCC(temp)

    # Find global minimum for z-axis
    z_min = min([
        data['c_Fe']['F_LIQ'].min(), data['c_Fe']['F_FCC'].min(), data['c_Fe']['F_BCC'].min() 
    ])
    z_max = 0  # Fixed maximum as requested

    variable = 'c_Fe'
    fig = go.Figure()
    comp_values = data[variable]['comp_values']
    COMP, TEMP = np.meshgrid(comp_values, temp)
    
    # Add LIQUID surface
    fig.add_trace(go.Surface(
        x=TEMP.T, y=COMP.T, z=data[variable]['F_LIQ'],
        name='LIQUID', colorscale='Reds_r', opacity=1.0,
        showscale=False, lighting=dict(ambient=0.8, diffuse=0.9)
    ))
    
    # Add FCC surface
    fig.add_trace(go.Surface(
        x=TEMP.T, y=COMP.T, z=data[variable]['F_FCC'],
        name='FCC', colorscale='Greens', opacity=1.0,
        showscale=False, lighting=dict(ambient=0.8, diffuse=0.9)
    ))
    
    # Add BCC surface
    fig.add_trace(go.Surface(
        x=TEMP.T, y=COMP.T, z=data[variable]['F_BCC'],
        name='BCC', colorscale='Blues', opacity=1.0,
        showscale=False, lighting=dict(ambient=0.8, diffuse=0.9)
    ))
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=f'Gibbs Free Energy vs Temp and {variable}',
            font=dict(size=20, family='Arial', color='black', weight='bold'),
            x=0.5, xanchor='center'
        ),
        scene=dict(
            xaxis=dict(
                title='Temperature (K)',
                titlefont=dict(size=16, family='Arial', weight='bold'),
                tickfont=dict(size=12, family='Arial', weight='bold'),
                backgroundcolor='rgba(240, 240, 240, 0.95)',
                gridcolor='white',
                showbackground=True
            ),
            yaxis=dict(
                title=f'{variable} (mole fraction)',
                titlefont=dict(size=16, family='Arial', weight='bold'),
                tickfont=dict(size=12, family='Arial', weight='bold'),
                backgroundcolor='rgba(240, 240, 240, 0.95)',
                gridcolor='white',
                showbackground=True
            ),
            zaxis=dict(
                title='Gibbs Free Energy (J/mol)',
                titlefont=dict(size=16, family='Arial', weight='bold'),
                tickfont=dict(size=12, family='Arial', weight='bold'),
                backgroundcolor='rgba(240, 240, 240, 0.95)',
                gridcolor='white',
                showbackground=True,
                range=[z_min, z_max]
            ),
            bgcolor='white'
        ),
        legend=dict(
            x=0.05, y=0.95, 
            font=dict(size=14, family='Arial', weight='bold'),
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor='black',
            borderwidth=1
        ),
        # margin=dict(l=10, r=10, t=60, b=10),
        width=800,  # Adjusted for side-by-side layout
        height=1500
    )
    fig.update_layout(scene_camera=dict(eye=dict(x=0, y=-2.5, z=0.5), up=dict(x=0, y=0, z=1)))
    
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Note:** All plots share the same Gibbs free energy scale (minimum: {:.2f} J/mol, maximum: 0 J/mol) for direct comparison.".format(z_min))
    return 0

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################


curves_two()
# only_minimum()
