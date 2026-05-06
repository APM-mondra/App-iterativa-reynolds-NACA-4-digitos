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
    
    # Parametro nagusiak
    st.session_state.puntu_kopurua = 8
    st.session_state.erradio_max = 61.5
    st.session_state.korda_base = 4.7
    st.session_state.rpm = 12.1
    st.session_state.v_rated = 12.0
    
    # Array-ak
    st.session_state.kordak = np.full(st.session_state.puntu_kopurua, st.session_state.korda_base) 
    st.session_state.erradioak = np.arange(1, st.session_state.puntu_kopurua + 1) * st.session_state.erradio_max / st.session_state.puntu_kopurua + 1.5
    
    st.session_state.alpha_min = -5.0
    st.session_state.alpha_max = 20.0
    st.session_state.alpha_steps = 100
    
    st.session_state.m_hautatua = "0"
    st.session_state.p_hautatua = "0"
    st.session_state.amaierako_nacak = []

# --- FUNTZIO LAGUNTZAILEAK ---
def kalkulatu_reynolds(erradioa, korda):
    """Reynolds kalkulua MATLABeko Schmitz/Betz eredu zehatzarekin"""
    p_air = 1.225
    mu = 1.789e-5
    
    omega = st.session_state.rpm * np.pi / 30
    v_wind = st.session_state.v_rated
    
    # Tip-Speed Ratio lokala (lambda_r)
    lambda_r = (omega * erradioa) / v_wind
    
    # Fluxuaren angelu optimoa
    phi_rad = (2.0 / 3.0) * np.arctan(1.0 / lambda_r)
    
    # Abiadura erlatiboa (a = 1/3 induzio axial optimoarekin)
    a = 1.0 / 3.0
    u_rel = v_wind * (1 - a) / np.sin(phi_rad)
    
    return korda * u_rel * p_air / mu

def grafikoa_sortu(reynolds, naca_zerrenda, izenburua):
    alphas = np.linspace(st.session_state.alpha_min, st.session_state.alpha_max, st.session_state.alpha_steps)
    fig = go.Figure()
    
    naca_baliodunak = []
    for naca in naca_zerrenda:
        try:
            m, p = int(naca[0]), int(naca[1])
            if (m > 0 and p == 0) or (m == 0 and p > 0): continue
            
            aero = nf.get_aero_from_airfoil(asb.Airfoil(f"naca{naca}"), alphas, reynolds)
            cl_cds = np.divide(aero["CL"], aero["CD"], out=np.zeros_like(aero["CL"]), where=(aero["CD"]>0))
            
            if np.max(cl_cds) > 0:
                fig.add_trace(go.Scatter(x=alphas, y=cl_cds, mode='lines', name=f"NACA {naca}", line=dict(width=3)))
                naca_baliodunak.append(naca)
        except:
            continue
            
    fig.update_layout(
        title=dict(text=izenburua, font=dict(size=20, color='#2C3E50')),
        xaxis_title="Eraso-angelua (Alpha) [deg]",
        yaxis_title="Eraginkortasuna (Cl/Cd)",
        hovermode="x unified",
        template="plotly_white",
        legend=dict(
            title="Profilak<br>(Klik ezkutatzeko)",
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="#E5E7EB",
            borderwidth=1,
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02
        ),
        margin=dict(l=40, r=150, t=80, b=40) 
    )
    fig.add_hline(y=0, line_dash="dash", line_color="#7F8C8D", line_width=1.5)
    return fig, naca_baliodunak

def fasea_aldatu(fase_berria):
    st.session_state.fase = fase_berria
    st.rerun()

def estazioa_atzera():
    if st.session_state.uneko_estazioa > 0:
        st.session_state.uneko_estazioa -= 1
        st.session_state.amaierako_nacak.pop() 
        fasea_aldatu("3_URRATSA")
    else:
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
    """NACA profil baten koordenatuak Selig formatuan sortzen ditu."""
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
    col_info2.metric("📏 Erradioa", f"{r_unekoa:.2f} m")
    col_info3.metric("📐 Korda", f"{c_unekoa:.2f} m")
    col_info4.metric("🌪️ Reynolds Lokala", f"{re_unekoa:.2e}")
    
    st.progress((idx) / st.session_state.puntu_kopurua)
    st.markdown("<br>", unsafe_allow_html=True)

# --- EGOERA MAKINA ---

if st.session_state.fase == "KONFIG":
    st.header("⚙️ 1. Iterazioaren Konfigurazioa")
    st.markdown("Egokitu parametroak analisia hasi aurretik.")
    
    col_param, col_sec, col_alpha = st.columns(3)
    
    with col_param:
        st.subheader("🍃 Parametro Nagusiak")
        with st.container(border=True):
            rpm_berria = st.number_input("RPM:", min_value=1.0, value=st.session_state.rpm, step=0.1)
            v_rated_berria = st.number_input("Haize-abiadura (m/s):", min_value=1.0, value=st.session_state.v_rated, step=0.1)
            erradio_max_berria = st.number_input("Gehienezko Erradioa (m):", min_value=1.0, value=st.session_state.erradio_max, step=1.0)
            korda_base_berria = st.number_input("Oinarrizko Korda (m):", min_value=0.1, value=st.session_state.korda_base, step=0.1)
            
            if (rpm_berria != st.session_state.rpm or 
                v_rated_berria != st.session_state.v_rated or
                erradio_max_berria != st.session_state.erradio_max or 
                korda_base_berria != st.session_state.korda_base):
                
                st.session_state.rpm = rpm_berria
                st.session_state.v_rated = v_rated_berria
                st.session_state.erradio_max = erradio_max_berria
                st.session_state.korda_base = korda_base_berria
                
                st.session_state.kordak = np.full(st.session_state.puntu_kopurua, korda_base_berria)
                st.session_state.erradioak = np.arange(1, st.session_state.puntu_kopurua + 1) * erradio_max_berria / st.session_state.puntu_kopurua + 1.5
                st.rerun()

    with col_sec:
        st.subheader("📏 Hegalaren Sekzioak")
        with st.container(border=True):
            sekzio_berriak = st.number_input("Estazio (puntu) kopurua:", min_value=2, max_value=30, value=st.session_state.puntu_kopurua, step=1)
            if sekzio_berriak != st.session_state.puntu_kopurua:
                st.session_state.puntu_kopurua = sekzio_berriak
                st.session_state.kordak = np.full(sekzio_berriak, st.session_state.korda_base)
                st.session_state.erradioak = np.arange(1, sekzio_berriak + 1) * st.session_state.erradio_max / sekzio_berriak + 1.5
                st.rerun()

    with col_alpha:
        st.subheader("📊 Alpha Analisia")
        with st.container(border=True):
            st.session_state.alpha_min = st.number_input("Gutxienekoa (°)", value=st.session_state.alpha_min, step=1.0)
            st.session_state.alpha_max = st.number_input("Gehienezkoa (°)", value=st.session_state.alpha_max, step=1.0)

    st.subheader("📐 Uneko Kordak eta Reynolds Datuak")
    
    # Reynolds-ak array osoarentzat kalkulatu
    reynolds_array = kalkulatu_reynolds(st.session_state.erradioak, st.session_state.kordak)
    
    df_kordak = pd.DataFrame({
        "Estazioa": range(1, st.session_state.puntu_kopurua + 1),
        "Erradioa [m]": np.round(st.session_state.erradioak, 2), 
        "Korda [m]": st.session_state.kordak,
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
    fig, validos = grafikoa_sortu(re, nacas_p1, "Kurbaduraren Aldakuntza (P=4, T=12 finkatuta)")
    
    with st.container(border=True):
        st.plotly_chart(fig, use_container_width=True)
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
        fig, validos = grafikoa_sortu(re, nacas_p2, f"Posizioaren Aldakuntza (Kurbadura M={st.session_state.m_hautatua})")
        
        with st.container(border=True):
            st.plotly_chart(fig, use_container_width=True)
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
    
    espesores = [8, 10, 12, 14, 15, 16, 18, 20, 21, 24, 26, 30]
    nacas_p3 = [f"{st.session_state.m_hautatua}{st.session_state.p_hautatua}{t:02d}" for t in espesores]
    fig, validos = grafikoa_sortu(re, nacas_p3, f"Lodieraren Doikuntza (NACA {st.session_state.m_hautatua}{st.session_state.p_hautatua}XX)")
    
    with st.container(border=True):
        st.plotly_chart(fig, use_container_width=True)
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
    
    # Azken taularako Reynolds-ak birkalkulatzen ditugu uneko datuekin
    reynolds_amaiera = kalkulatu_reynolds(st.session_state.erradioak, st.session_state.kordak)
    
    df_emaitzak = pd.DataFrame({
        "Estazioa": range(1, st.session_state.puntu_kopurua + 1),
        "Erradioa [m]": np.round(st.session_state.erradioak, 2),
        "Erabilitako Korda [m]": st.session_state.kordak,
        "Reynolds": [f"{re:.2e}" for re in reynolds_amaiera], # <--- Hemen sartu da Reynolds zutabea
        "Aukeratutako NACA": st.session_state.amaierako_nacak
    })
    st.table(df_emaitzak)

    # --- .TXT DESKARGAK ---
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
    st.markdown("Profilak definitu ondoren, korda teoriko berriak kalkulatu ditzakezu zure BEM sisteman. Sartu korda berriak hemen Reynolds-a doitzeko eta hurrengo iterazioa abiarazteko.")
    
    with st.container(border=True):
        df_berriak = st.data_editor(pd.DataFrame({
            "Estazioa": range(1, st.session_state.puntu_kopurua + 1),
            "Korda Berria [m]": st.session_state.kordak
        }), hide_index=True, use_container_width=True)
    
    _, col_btn, _ = st.columns([1, 2, 1])
    with col_btn:
        if st.button("🚀 Iterazio Berria Hasi", type="primary", use_container_width=True):
            st.session_state.kordak = df_berriak["Korda Berria [m]"].values
            st.session_state.iterazioa += 1
            fasea_aldatu("KONFIG")
