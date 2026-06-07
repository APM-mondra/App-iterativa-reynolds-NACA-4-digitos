import streamlit as st
import numpy as np
import aerosandbox as asb
import neuralfoil as nf
import plotly.graph_objects as go
import pandas as pd

# --- ORRIAREN KONFIGURAZIOA ---
st.set_page_config(page_title="Hegalaren Diseinu Iteratiboa", page_icon="🌬️", layout="wide")

# --- ESTAERA-ALDAGAIEN HASIERATZEA ---
if "fase" not in st.session_state:
    st.session_state.fase = "KONFIG" 
    st.session_state.iterazioa = 1
    st.session_state.uneko_estazioa = 0
    
    st.session_state.puntu_kopurua = 8
    # Balio berriak eskala txikirako
    st.session_state.erradio_min = 0.05 # Hub-aren erradioa (m)
    st.session_state.erradio_max = 0.80 # Gehienezko erradioa (m)
    st.session_state.korda_base = 0.12  # Oinarrizko korda (m)
    st.session_state.rpm = 200.0
    st.session_state.v_rated = 4.0
    
    st.session_state.kordak = np.full(st.session_state.puntu_kopurua, st.session_state.korda_base) 
    # Linspace erabiliz estazioak hasieratik amaierara ondo banatzeko
    st.session_state.erradioak = np.linspace(st.session_state.erradio_min, st.session_state.erradio_max, st.session_state.puntu_kopurua)
    
    st.session_state.alpha_min = -5.0
    st.session_state.alpha_max = 20.0
    st.session_state.alpha_steps = 100
    
    st.session_state.m_hautatua = "0"
    st.session_state.p_hautatua = "0"
    st.session_state.amaierako_nacak = []

# --- FUNTZIO LAGUNTZAILEAK ---
def kalkulatu_reynolds(erradioa, korda):
    p_air = 1.225
    mu = 1.789e-5
    
    omega = st.session_state.rpm * np.pi / 30
    v_wind = st.session_state.v_rated
    
    lambda_r = (omega * erradioa) / v_wind
    phi_rad = (2.0 / 3.0) * np.arctan(1.0 / lambda_r)
    
    a = 1.0 / 3.0
    u_rel = v_wind * (1 - a) / np.sin(phi_rad)
    
    return korda * u_rel * p_air / mu

def grafikoak_sortu(reynolds, naca_zerrenda, izenburua):
    alphas = np.linspace(st.session_state.alpha_min, st.session_state.alpha_max, st.session_state.alpha_steps)
    fig_eff = go.Figure()
    fig_cl = go.Figure()
    
    naca_baliodunak = []
    for naca in naca_zerrenda:
        try:
            m, p = int(naca[0]), int(naca[1])
            if (m > 0 and p == 0) or (m == 0 and p > 0): continue
            
            aero = nf.get_aero_from_airfoil(asb.Airfoil(f"naca{naca}"), alphas, reynolds)
            cl = aero["CL"]
            cd = aero["CD"]
            cl_cds = np.divide(cl, cd, out=np.zeros_like(cl), where=(cd>0))
            
            if np.max(cl_cds) > 0:
                fig_eff.add_trace(go.Scatter(x=alphas, y=cl_cds, mode='lines', name=f"NACA {naca}", line=dict(width=3)))
                fig_cl.add_trace(go.Scatter(x=alphas, y=cl, mode='lines', name=f"NACA {naca}", line=dict(width=3)))
                naca_baliodunak.append(naca)
        except (ValueError, KeyError, RuntimeError, TypeError):
            continue
            
    diseinu_komuna = dict(
        xaxis_title="Eraso-angelua (Alpha) [deg]",
        hovermode="x unified",
        template="plotly_white",
        legend=dict(
            title="Profilak", bgcolor="rgba(255,255,255,0.8)",
            bordercolor="#E5E7EB", borderwidth=1,
            orientation="v", yanchor="top", y=1, xanchor="left", x=1.02
        ),
        margin=dict(l=40, r=150, t=60, b=40) 
    )
    
    fig_eff.update_layout(title=dict(text=f"{izenburua} - Efizientzia", font=dict(size=18, color='#2C3E50')), yaxis_title="Eraginkortasuna (Cl/Cd)", **diseinu_komuna)
    fig_cl.update_layout(title=dict(text=f"{izenburua} - Sustentazioa", font=dict(size=18, color='#2C3E50')), yaxis_title="Sustentazioa (Cl)", **diseinu_komuna)
    
    fig_eff.add_hline(y=0, line_dash="dash", line_color="#7F8C8D", line_width=1.5)
    fig_cl.add_hline(y=0, line_dash="dash", line_color="#7F8C8D", line_width=1.5)
    fig_cl.add_hline(y=1.0, line_dash="dot", line_color="#E74C3C", line_width=2, annotation_text="Cl helburua ≈ 1.0")
    
    return fig_eff, fig_cl, naca_baliodunak

def fasea_aldatu(fase_berria):
    st.session_state.fase = fase_berria
    st.rerun()

def estazioa_atzera():
    if st.session_state.uneko_estazioa > 0:
        st.session_state.uneko_estazioa -= 1
        if st.session_state.amaierako_nacak:
            st.session_state.amaierako_nacak.pop()
        st.session_state.m_hautatua = "0"
        st.session_state.p_hautatua = "0"
        fasea_aldatu("1_URRATSA")
    else:
        st.session_state.amaierako_nacak = []
        st.session_state.uneko_estazioa = 0
        st.session_state.m_hautatua = "0"
        st.session_state.p_hautatua = "0"
        fasea_aldatu("KONFIG")

def marraztu_botoi_sarea(aukerak, gakoa, zutabe_kop=4):
    st.markdown("<p style='font-size:1.1rem; color:#1F618D; margin-bottom: 0px;'><strong>👉 Egin klik profil batean zuzenean hurrengo urratsera pasatzeko:</strong></p>", unsafe_allow_html=True)
    cols = st.columns(zutabe_kop)
    aukeratua = None
    for i, aukera in enumerate(aukerak):
        if cols[i % zutabe_kop].button(f"NACA {aukera}", key=f"{gakoa}_{aukera}", use_container_width=True):
            aukeratua = aukera
    return aukeratua

def sortu_naca_txt(naca):
    m = int(naca[0]) * 1.0
    p = int(naca[1]) * 10.0
    t = int(naca[2:]) * 1.0
    goiburua = f"NACA {naca} Airfoil M={m}% P={p}% T={t}%"
    
    perfila = asb.Airfoil(f"naca{naca}")
    koordenatuak = perfila.coordinates
    
    lerroak = [goiburua]
    for x, y in koordenatuak:
        lerroak.append(f" {x:9.6f}  {y:9.6f}")
        
    return "\n".join(lerroak)

# --- UI NAGUSIA ---
st.markdown(f"<h1 style='text-align: center; color: #1F618D;'>🔄 Hegalaren Diseinua - {st.session_state.iterazioa}. Iterazioa</h1>", unsafe_allow_html=True)
st.markdown("---")

if st.session_state.fase not in ["KONFIG", "LABURPENA"]:
    idx = st.session_state.uneko_estazioa
    r_unekoa = st.session_state.erradioak[idx]
    c_unekoa = st.session_state.kordak[idx]
    re_unekoa = kalkulatu_reynolds(r_unekoa, c_unekoa)
    
    col_info1, col_info2, col_info3, col_info4 = st.columns(4)
    col_info1.metric("📍 Estazioa", f"{idx+1} / {st.session_state.puntu_kopurua}")
    col_info2.metric("📏 Erradioa", f"{r_unekoa:.3f} m")
    col_info3.metric("📐 Korda", f"{c_unekoa:.3f} m")
    col_info4.metric("🌪️ Reynolds Lokala", f"{re_unekoa:.2e}")
    
    st.progress((idx) / st.session_state.puntu_kopurua)
    st.markdown("<br>", unsafe_allow_html=True)

# --- EGOERA MAKINA ---

if st.session_state.fase == "KONFIG":
    st.header("⚙️ 1. Iterazioaren Konfigurazioa")
    
    col_param, col_sec, col_alpha = st.columns(3)
    
    with col_param:
        st.subheader("🍃 Parametro Nagusiak")
        with st.container(border=True):
            rpm_berria = st.number_input("RPM:", min_value=1.0, value=st.session_state.rpm, step=1.0)
            v_rated_berria = st.number_input("Haize-abiadura (m/s):", min_value=0.1, value=st.session_state.v_rated, step=0.1)
            erradio_min_berria = st.number_input("Hasierako Erradioa - Hub (m):", min_value=0.01, value=st.session_state.erradio_min, step=0.01)
            erradio_max_berria = st.number_input("Gehienezko Erradioa (m):", min_value=0.05, value=st.session_state.erradio_max, step=0.01)
            korda_base_berria = st.number_input("Oinarrizko Korda (m):", min_value=0.01, value=st.session_state.korda_base, step=0.01)
            
            if (rpm_berria != st.session_state.rpm or 
                v_rated_berria != st.session_state.v_rated or
                erradio_min_berria != st.session_state.erradio_min or
                erradio_max_berria != st.session_state.erradio_max or 
                korda_base_berria != st.session_state.korda_base):
                
                st.session_state.rpm = rpm_berria
                st.session_state.v_rated = v_rated_berria
                st.session_state.erradio_min = erradio_min_berria
                st.session_state.erradio_max = erradio_max_berria
                st.session_state.korda_base = korda_base_berria
                
                st.session_state.kordak = np.full(st.session_state.puntu_kopurua, korda_base_berria)
                st.session_state.erradioak = np.linspace(erradio_min_berria, erradio_max_berria, st.session_state.puntu_kopurua)
                st.rerun()

    with col_sec:
        st.subheader("📏 Hegalaren Sekzioak")
        with st.container(border=True):
            sekzio_berriak = st.number_input("Estazio (puntu) kopurua:", min_value=2, max_value=30, value=st.session_state.puntu_kopurua, step=1)
            if sekzio_berriak != st.session_state.puntu_kopurua:
                st.session_state.puntu_kopurua = sekzio_berriak
                st.session_state.kordak = np.full(sekzio_berriak, st.session_state.korda_base)
                st.session_state.erradioak = np.linspace(st.session_state.erradio_min, st.session_state.erradio_max, sekzio_berriak)
                st.rerun()

    with col_alpha:
        st.subheader("📊 Alpha Analisia")
        with st.container(border=True):
            st.session_state.alpha_min = st.number_input("Gutxienekoa (°)", value=st.session_state.alpha_min, step=1.0)
            st.session_state.alpha_max = st.number_input("Gehienezkoa (°)", value=st.session_state.alpha_max, step=1.0)

    st.subheader("📐 Uneko Kordak eta Reynolds Datuak")
    
    reynolds_array = kalkulatu_reynolds(st.session_state.erradioak, st.session_state.kordak)
    
    df_kordak = pd.DataFrame({
        "Estazioa": range(1, st.session_state.puntu_kopurua + 1),
        "Erradioa [m]": np.round(st.session_state.erradioak, 3), 
        "Korda [m]": np.round(st.session_state.kordak, 3),
        "Reynolds": [f"{re:.2e}" for re in reynolds_array]
    })
    
    df_editatua = st.data_editor(
        df_kordak, 
        num_rows="fixed", 
        hide_index=True, 
        use_container_width=True,
        disabled=["Estazioa", "Erradioa [m]", "Reynolds"]
    )
    
    st.session_state.kordak = df_editatua["Korda [m]"].values

    st.markdown("<br>", unsafe_allow_html=True)
    _, col_btn, _ = st.columns([1, 2, 1])
    with col_btn:
        if st.button("🚀 Estazioen Analisia Hasi", type="primary", use_container_width=True):
            st.session_state.amaierako_nacak = []
            st.session_state.uneko_estazioa = 0
            fasea_aldatu("1_URRATSA")

elif st.session_state.fase == "1_URRATSA":
    st.subheader("1. Urratsa: Kurbaduraren Aukeraketa (Lehen digitua)")
    re = kalkulatu_reynolds(st.session_state.erradioak[st.session_state.uneko_estazioa], st.session_state.kordak[st.session_state.uneko_estazioa])
    
    nacas_p1 = ["0012"] + [f"{m}412" for m in range(1, 10)]
    fig_eff, fig_cl, validos = grafikoak_sortu(re, nacas_p1, "P=4, T=12 finkatuta")
    
    with st.container(border=True):
        tab1, tab2 = st.tabs(["📈 Eraginkortasuna (Cl/Cd)", "🪁 Sustentazioa (Cl)"])
        with tab1:
            st.plotly_chart(fig_eff, use_container_width=True)
        with tab2:
            st.plotly_chart(fig_cl, use_container_width=True)
        aukera = marraztu_botoi_sarea(validos, "p1")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬅️ Aurreko Estaziora Atzera", use_container_width=False):
        estazioa_atzera()
        
    if aukera:
        st.session_state.m_hautatua = aukera[0]
        fasea_aldatu("2_URRATSA")

elif st.session_state.fase == "2_URRATSA":
    if st.session_state.m_hautatua == "0":
        st.warning("⚠️ Profil simetrikoa detektatu da (Kurbadura = 0). Kurbaduraren posizioa saltatzen.")
        st.session_state.p_hautatua = "0"
        
        col_atzera, col_huts, col_aurrera = st.columns([1, 4, 1])
        if col_atzera.button("⬅️ Aurrekoa", use_container_width=True):
            fasea_aldatu("1_URRATSA")
        if col_aurrera.button("Lodierara joan ➡️", type="primary", use_container_width=True):
            fasea_aldatu("3_URRATSA")
    else:
        st.subheader("2. Urratsa: Kurbaduraren Posizioa (Bigarren digitua)")
        re = kalkulatu_reynolds(st.session_state.erradioak[st.session_state.uneko_estazioa], st.session_state.kordak[st.session_state.uneko_estazioa])
        
        nacas_p2 = [f"{st.session_state.m_hautatua}{p}12" for p in range(1, 10)]
        fig_eff, fig_cl, validos = grafikoak_sortu(re, nacas_p2, f"M={st.session_state.m_hautatua}")
        
        with st.container(border=True):
            tab1, tab2 = st.tabs(["📈 Eraginkortasuna (Cl/Cd)", "🪁 Sustentazioa (Cl)"])
            with tab1:
                st.plotly_chart(fig_eff, use_container_width=True)
            with tab2:
                st.plotly_chart(fig_cl, use_container_width=True)
            aukera = marraztu_botoi_sarea(validos, "p2")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⬅️ Kurbadurara Atzera (1. Urratsa)", use_container_width=False):
            fasea_aldatu("1_URRATSA")
            
        if aukera:
            st.session_state.p_hautatua = aukera[1]
            fasea_aldatu("3_URRATSA")

elif st.session_state.fase == "3_URRATSA":
    st.subheader("3. Urratsa: Lodiera Egituralaren Aukeraketa")
    re = kalkulatu_reynolds(st.session_state.erradioak[st.session_state.uneko_estazioa], st.session_state.kordak[st.session_state.uneko_estazioa])
    
    espesores = [8, 10, 12, 14, 15, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40]
    nacas_p3 = [f"{st.session_state.m_hautatua}{st.session_state.p_hautatua}{t:02d}" for t in espesores]
    fig_eff, fig_cl, validos = grafikoak_sortu(re, nacas_p3, f"NACA {st.session_state.m_hautatua}{st.session_state.p_hautatua}XX")
    
    with st.container(border=True):
        tab1, tab2 = st.tabs(["📈 Eraginkortasuna (Cl/Cd)", "🪁 Sustentazioa (Cl)"])
        with tab1:
            st.plotly_chart(fig_eff, use_container_width=True)
        with tab2:
            st.plotly_chart(fig_cl, use_container_width=True)
        aukera = marraztu_botoi_sarea(validos, "p3", zutabe_kop=6) 
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬅️ Posiziora Atzera (2. Urratsa)", use_container_width=False):
        if st.session_state.m_hautatua == "0":
            fasea_aldatu("1_URRATSA")
        else:
            fasea_aldatu("2_URRATSA")
            
    if aukera:
        st.session_state.amaierako_nacak.append(aukera)
        if st.session_state.uneko_estazioa < st.session_state.puntu_kopurua - 1:
            st.session_state.uneko_estazioa += 1
            fasea_aldatu("1_URRATSA")
        else:
            fasea_aldatu("LABURPENA")

elif st.session_state.fase == "LABURPENA":
    st.success(f"✨ {st.session_state.iterazioa}. Iterazioa arrakastaz amaitu da!")
    
    st.header("📊 Uneko Iterazioaren Emaitzak")
    
    reynolds_amaiera = kalkulatu_reynolds(st.session_state.erradioak, st.session_state.kordak)
    
    df_emaitzak = pd.DataFrame({
        "Estazioa": range(1, st.session_state.puntu_kopurua + 1),
        "Erradioa [m]": np.round(st.session_state.erradioak, 3),
        "Erabilitako Korda [m]": np.round(st.session_state.kordak, 3),
        "Reynolds": [f"{re:.2e}" for re in reynolds_amaiera],
        "Aukeratutako NACA": st.session_state.amaierako_nacak
    })
    st.table(df_emaitzak)

    st.header("💾 Profilen Koordenatuak Deskargatu")
    st.markdown("Hemen dituzu iterazio honetan hautatu dituzun profil guztien **.txt** fitxategiak (Selig formatuan) deskargatzeko prest:")
    
    naca_bakarrak = list(set(st.session_state.amaierako_nacak))
    
    botoi_zutabeak = st.columns(len(naca_bakarrak) if len(naca_bakarrak) > 0 else 1)
    
    for i, naca in enumerate(naca_bakarrak):
        txt_edukia = sortu_naca_txt(naca)
        with botoi_zutabeak[i % len(botoi_zutabeak)]:
            st.download_button(
                label=f"📥 NACA {naca}.txt",
                data=txt_edukia,
                file_name=f"NACA_{naca}.txt",
                mime="text/plain",
                use_container_width=True
            )
    
    st.divider()
    st.header("🔄 Hurrengo Iterazioa Prestatu")
    
    with st.container(border=True):
        df_berriak = st.data_editor(pd.DataFrame({
            "Estazioa": range(1, st.session_state.puntu_kopurua + 1),
            "Korda Berria [m]": np.round(st.session_state.kordak, 3)
        }), hide_index=True, use_container_width=True)
    
    _, col_btn, _ = st.columns([1, 2, 1])
    with col_btn:
        if st.button("🚀 Iterazio Berria Hasi", type="primary", use_container_width=True):
            st.session_state.kordak = df_berriak["Korda Berria [m]"].values
            st.session_state.iterazioa += 1
            st.session_state.amaierako_nacak = []
            st.session_state.uneko_estazioa = 0
            st.session_state.m_hautatua = "0"
            st.session_state.p_hautatua = "0"
            fasea_aldatu("KONFIG")
