"""Testu guztiak euskara baturen arabera."""

APP_TITLE = "Hegalaren diseinu iteratiboa"
APP_CAPTION = "Profil NACA 4 zifrak hautatzeko tresna | NeuralFoil"

LANDING = {
    "title": "Ongi etorri hegalaren diseinu iteratibora",
    "intro": (
        "Aplikazio honek haize-errota baten pala diseinatzen laguntzen du, estazio "
        "(erradio) bakoitzean profil aerodinamiko egokiena hautatuz. Estazio bakoitzean "
        "Reynolds zenbaki lokala kalkulatzen da eta, horren arabera, NACA 4 zifrak "
        "iragazten dira hiru urratsetan: kurbadura, kurbaduraren posizioa eta lodiera."
    ),
    "steps_title": "Prozesuaren urrats nagusiak",
    "steps": [
        {
            "title": "1. Konfigurazioa",
            "body": (
                "Zehaztu parametro nominalak (RPM, haize-abiadura), palaren geometria "
                "(erradioak eta kordak) eta estazio kopurua."
            ),
        },
        {
            "title": "2. Estazioen analisia",
            "body": (
                "Zatitu pala estazioetan. Estazio bakoitzean, iragazi profilak hiru "
                "urratsetan: lehenengo kurbadura (M), gero posizioa (P) eta azkenik lodiera (T)."
            ),
        },
        {
            "title": "3. Laburpena eta iterazioa",
            "body": (
                "Ikusi emaitzak, deskargatu profilen koordenatuak eta prestatu hurrengo "
                "iterazioa kordak doitzeko."
            ),
        },
    ],
    "naca_title": "NACA 4 zifrak nola iragazten diren",
    "naca_body": (
        "Kode bakoitza lau zifretan banatzen da. Adibidez, **NACA 2412** profil batean: "
        "lehen zifrak kurbadura maximoa (% kordaren arabera), bigarrenak kurbaduraren "
        "posizioa (x/10), eta azken bi zifrek lodiera maximoa (% kordaren arabera) adierazten dute. "
        "Aplikazioak urrats horietan banan-banan iragazten du aukerak."
    ),
    "reynolds_title": "Zergatik da garrantzitsua Reynolds zenbakia?",
    "reynolds_body": (
        "Profil berak portaera desberdina du eraso-angelu eta Reynolds zenbaki "
        "desberdinetan. Estazio bakoitzean korda, erradioa, RPM eta haize-abiadura "
        "kontuan hartuta kalkulatzen da Reynolds lokala, eta horren arabera "
        "konparatzen dira profil alternatiboak NeuralFoil erabiliz."
    ),
    "details_title": "Xehetasun gehiago",
    "details_body": (
        "- **TSR (lambda)**: erradio bakoitzeko abiadura-ratioa, ω·r / v_haizea\n"
        "- **Reynolds lokala**: korda eta abiadura erlatiboaren arabera kalkulatzen da\n"
        "- **Iragazketa**: urrats bakoitzean Cl/Cd maximoa duen profila nabarmentzen da"
    ),
    "cta": "Konfiguratzera joan",
}

MACRO_PHASES = [
    {"id": "HASIERA", "label": "Ongietorria"},
    {"id": "KONFIG", "label": "Konfigurazioa"},
    {"id": "ANALISIA", "label": "Profilen hautaketa"},
    {"id": "LABURPENA", "label": "Laburpena"},
]

PHASES = {
    "HASIERA": {
        "label": "Ongietorria",
        "title": "Ongi etorri",
        "description": "Irakurri prozesua eta hasi konfigurazioa prest dagoenean.",
    },
    "KONFIG": {
        "label": "Konfigurazioa",
        "title": "Iterazioaren konfigurazioa",
        "description": (
            "Definitu parametro nominalak eta palaren geometria. Hautaketak hasi aurretik "
            "berrikusi kordak eta Reynolds-en banaketa."
        ),
    },
    "1_URRATSA": {
        "label": "Kurbadura (M)",
        "title": "1. urratsa: kurbaduraren aukeraketa",
        "description": (
            "Hautatu lehen zifra (M), kurbadura maximoa definitzen duena. "
            "Konparatu profilen eraginkortasuna (Cl/Cd) uneko estazioaren Reynolds zenbakian."
        ),
    },
    "2_URRATSA": {
        "label": "Kurbaduraren posizioa (P)",
        "title": "2. urratsa: kurbaduraren posizioa",
        "description": (
            "Bigarren zifrak (P) zehazten du kurbadura kordaren luzeran non kokatzen den. "
            "Aukeratu profil egokiena grafikoetan eta sailkapenean oinarrituta."
        ),
    },
    "3_URRATSA": {
        "label": "Lodiera (T)",
        "title": "3. urratsa: lodieraren aukeraketa",
        "description": (
            "Azken bi zifrek lodiera egiturazkoa definitzen dute. Hautatu profila eta "
            "jarraitu hurrengo estaziora, edo joan laburpenera azken estazioa bada."
        ),
    },
    "LABURPENA": {
        "label": "Laburpena",
        "title": "Iterazioaren emaitzak",
        "description": (
            "Berrikusi estazio bakoitzean hautatutako profilak, deskargatu datuak eta "
            "prestatu hurrengo iterazioa."
        ),
    },
}

MICRO_STEPS = [
    {"id": "1_URRATSA", "label": "Kurbadura (M)"},
    {"id": "2_URRATSA", "label": "Posizioa (P)"},
    {"id": "3_URRATSA", "label": "Lodiera (T)"},
]

SIDEBAR = {
    "title_analysis": "Uneko egoera",
    "title_summary": "Iterazioaren laburpena",
    "nominal_title": "Parametro nominalak",
    "rpm": "RPM",
    "wind_speed": "Haize-abiadura (m/s)",
    "iteration": "Iterazioa",
    "station": "Uneko estazioa",
    "selected_profiles": "Hautatutako profilak",
    "no_profiles_yet": "Oraindik ez da profilik hautatu.",
    "back_to_config": "Konfiguraziora itzuli",
    "back_to_config_warning": (
        "Kontuz: konfiguraziora itzultzen bazara, uneko hautaketak galduko dira. "
        "Ziur zaude jarraitu nahi duzula?"
    ),
    "back_to_home": "Hasierara itzuli",
    "confirm_reset": "Bai, berrezarri",
    "cancel": "Utzi",
}

CONFIG = {
    "nominal_title": "Parametro nominalak",
    "nominal_help": (
        "Balio hauek iterazio osoan konstanteak dira. Analisia hasi ondoren ez dira aldatzen."
    ),
    "rpm": "RPM",
    "wind_speed": "Haize-abiadura nominala (m/s)",
    "geometry_title": "Palaren geometria",
    "hub_radius": "Hasierako erradioa — hub (m)",
    "max_radius": "Gehienezko erradioa (m)",
    "base_chord": "Oinarrizko korda (m)",
    "sections_title": "Hegalaren sekzioak",
    "station_count": "Estazio kopurua",
    "aero_title": "Analisia aerodinamikoa",
    "aero_expander": "Eraso-angeluen tartea (parametro aurreratuak)",
    "alpha_min": "Gutxieneko eraso-angelua (°)",
    "alpha_max": "Gehienezko eraso-angelua (°)",
    "alpha_steps": "Eraso-angelu urratsak",
    "alpha_steps_help": "Urrats gutxiagorekin kalkulua azkarragoa da, baina kurbak ez dira hain leunak izango.",
    "metrics_blade_length": "Palaren luzera",
    "metrics_tsr_mean": "TSR batez bestekoa",
    "metrics_re_min": "Reynolds minimoa",
    "metrics_re_max": "Reynolds maximoa",
    "chords_title": "Kordak eta Reynolds datuak",
    "tab_planform": "Planoa",
    "tab_reynolds": "Reynolds",
    "tab_tsr": "TSR",
    "col_station": "Estazioa",
    "col_radius": "Erradioa [m]",
    "col_chord": "Korda [m]",
    "col_reynolds": "Reynolds",
    "start_analysis": "Estazioen analisia hasi",
    "back_to_landing": "Hasierara itzuli",
}

STEPS = {
    "no_valid_profiles": "Ez da profil baliodunik aurkitu uneko parametroekin.",
    "select_prompt": "Egin klik profil batean edo hautatu zerrendatik:",
    "select_profile": "Profila hautatu",
    "select_placeholder": "Hautatu...",
    "preview": "Geometriaren aurrebista",
    "symmetric_warning": (
        "Profil simetrikoa hautatu da (kurbadura = 0). "
        "Kurbaduraren posizioaren urratsa saltatuko da."
    ),
    "btn_previous": "Aurrekoa",
    "btn_to_thickness": "Lodieraren urratsera joan",
    "back_station": "Aurreko estaziora itzuli",
    "back_step1": "Kurbaduraren urratsera itzuli (1. urratsa)",
    "back_step2": "Posizioaren urratsera itzuli (2. urratsa)",
    "tab_efficiency": "Eraginkortasuna (Cl/Cd)",
    "tab_cl": "Sustentazioa (Cl)",
    "tab_cd": "Erresistentzia (Cd)",
    "tab_polar": "Polarra (Cl–Cd)",
    "tab_ranking": "Sailkapena",
    "rank_naca": "NACA",
    "rank_cl_cd_max": "Cl/Cd max",
    "rank_alpha_opt": "Eraso-angelu optimoa (°)",
    "rank_cl_opt": "Cl optimoan",
    "rank_cd_opt": "Cd optimoan",
}

SUMMARY = {
    "success": "{n}. iterazioa arrakastaz amaitu da!",
    "tab_table": "Taula",
    "tab_spanwise": "NACA banaketa",
    "tab_dual": "Korda eta Reynolds",
    "tab_profiles": "Profilen gainjartzea",
    "download_csv": "CSV deskargatu",
    "download_profiles_title": "Profilen koordenatuak deskargatu",
    "download_profiles_body": (
        "Hemen dituzu iterazio honetan hautatu dituzun profilen .txt fitxategiak "
        "(Selig formatua)."
    ),
    "next_iteration_title": "Hurrengo iterazioa prestatu",
    "col_used_chord": "Erabilitako korda [m]",
    "col_selected_naca": "Hautatutako NACA",
    "col_new_chord": "Korda berria [m]",
    "start_new_iteration": "Iterazio berria hasi",
}

TRACKER = {
    "blade_progress": "Pala osatuta: {pct}%",
    "station_label": "Estazioa {current} / {total}",
    "substep_label": "Uneko estazioko urratsa",
    "station_map_title": "Estazioen mapa",
    "completed": "Osatuta",
    "active": "Aktiboa",
    "pending": "Zain",
}

ERRORS = {
    "unknown_phase": "Egoera ezezaguna. Itzuli hasierara.",
    "no_valid_profiles": "Ez da profil baliodunik aurkitu uneko parametroekin.",
    "invalid_geometry": "Geometria baliogabea: hasierako erradioa gehienezko erradioa baino txikiagoa izan behar da.",
    "invalid_alpha": "Eraso-angeluen tartea baliogabea: gutxienekoa gehienezkoa baino txikiagoa izan behar da.",
    "invalid_chord": "Korda positiboa izan behar da estazio guztietan.",
    "naca_download_failed": "Ezin izan da profila deskargatu:",
    "geometry_unavailable": "Geometria ez dago eskuragarri profil honetarako.",
}

SIDEBAR_SUMMARY = {
    "station_count": "Estazio kopurua",
}

METRICS = {
    "station": "Estazioa",
    "radius": "Erradioa",
    "chord": "Korda",
    "reynolds": "Reynolds lokala",
    "tsr": "TSR (lambda)",
}

PLOTS = {
    "legend_profiles": "Profilak",
    "axis_alpha": "Eraso-angelua (α) [°]",
    "efficiency_y": "Eraginkortasuna (Cl/Cd)",
    "cl_y": "Sustentazioa (Cl)",
    "cd_y": "Erresistentzia (Cd)",
    "cl_target": "Cl helburua ≈ 1.0",
    "efficiency_suffix": "Eraginkortasuna",
    "cl_suffix": "Sustentazioa",
    "cd_suffix": "Erresistentzia",
    "polar_suffix": "Polarra (Cl–Cd)",
    "polar_x": "Cd",
    "polar_y": "Cl",
    "ranking_title": "Sailkapena — gehienezko Cl/Cd",
    "ranking_x": "Profila",
    "ranking_y": "Cl/Cd max",
    "geometry_title": "NACA {naca} geometria",
    "geometry_x": "x/c",
    "geometry_y": "y/c",
    "planform_title": "Hegalaren planoa (erradioa vs korda)",
    "planform_x": "Erradioa [m]",
    "planform_y": "Korda [m]",
    "reynolds_title": "Reynolds lokala estazio bakoitzean",
    "reynolds_x": "Estazioa",
    "reynolds_y": "Reynolds",
    "tsr_title": "TSR (lambda) estazio bakoitzean",
    "tsr_x": "Estazioa",
    "tsr_y": "Lambda",
    "spanwise_title": "NACA banaketa estazioaren arabera",
    "spanwise_x": "Estazioa",
    "spanwise_y": "Profila",
    "dual_title": "Korda eta Reynolds banaketa",
    "dual_chord": "Korda [m]",
    "dual_reynolds": "Reynolds",
    "overlay_title": "Profilen gainjartzea",
}
