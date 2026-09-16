import streamlit as st
import pandas as pd
from datetime import datetime
import calendar
import urllib.parse
import requests

# 1. Configuración de página
st.set_page_config(page_title="BapSync - Seguridad Escolar BAPES", page_icon="🛡️", layout="centered")

# 2. Inyección CSS con alto contraste y fondo nítido
st.markdown("""
    <style>
    /* Fondo con imagen de colegio sutilmente oscurecida */
    .stApp {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.45), rgba(15, 23, 42, 0.55)),
                    url("https://images.unsplash.com/photo-1580582932707-520aed937b7b?auto=format&fit=crop&w=1920&q=80") no-repeat center center fixed;
        background-size: cover;
    }

    #MainMenu, footer, header {visibility: hidden;}

    /* Contenedor central como tarjeta blanca limpia */
    .block-container {
        max-width: 680px;
        background: #ffffff;
        padding: 30px 32px 40px 32px !important;
        margin-top: 30px;
        margin-bottom: 40px;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.25);
    }

    /* Tipografías y colores con alto contraste */
    h1, h2, h3, h4, p, span, label, div {
        color: #1e293b !important;
        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    }

    /* Banner institucional superior */
    .header-banner {
        background: linear-gradient(135deg, #0c5c3c, #166534);
        border-radius: 14px;
        padding: 16px 20px;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 22px;
        box-shadow: 0 4px 12px rgba(12, 92, 60, 0.2);
    }
    .header-banner h4 {
        color: #ffffff !important;
        margin: 0;
        font-weight: 800;
        letter-spacing: 0.5px;
        font-size: 19px;
    }
    .header-banner p {
        color: #e2e8f0 !important;
        margin: 6px 0 0 0;
        font-size: 13.5px;
    }

    /* Botón de acción principal */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #0c5c3c, #15803d) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        padding: 14px 20px !important;
        font-size: 16px !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(12, 92, 60, 0.3) !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(12, 92, 60, 0.4) !important;
        background: #08432b !important;
    }

    /* Estilo de pestañas */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #f1f5f9;
        padding: 5px;
        border-radius: 12px;
        gap: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 600;
        border: none !important;
        background-color: transparent;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    }

    /* Tarjetas de avisos de WhatsApp */
    .card-recordatorio {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-left: 5px solid #22c55e;
        padding: 14px 16px;
        border-radius: 10px;
        margin-bottom: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# Credenciales de dirección
ADMIN_PIN = "Bp$2026#SecDir!"
API_URL = st.secrets.get("SHEET_API_URL", "")

def cargar_turnos():
    if not API_URL:
        return pd.DataFrame()
    try:
        url_fresca = f"{API_URL}?t={datetime.now().timestamp()}"
        res = requests.get(url_fresca, timeout=12, allow_redirects=True)
        if res.status_code == 200:
            datos = res.json()
            if isinstance(datos, list) and len(datos) > 0:
                return pd.DataFrame(datos)
        return pd.DataFrame()
    except Exception:
        return pd.DataFrame()

def generar_enlace_google_calendar(fecha_str, turno, padre, estudiante):
    f = fecha_str.replace("-", "")
    if "Mañana" in turno:
        start_time = f"{f}T123000Z"
        end_time = f"{f}T131500Z"
    else:
        start_time = f"{f}T191500Z"
        end_time = f"{f}T200000Z"

    titulo = "🛡️ Turno BAPES: Seguridad Escolar"
    detalles = (
        f"Apoderado: {padre}\n"
        f"Estudiante: {estudiante}\n"
        f"Turno: {turno}\n\n"
        f"Recuerda asistir puntualmente con tu distintivo de BAPES."
    )
    ubicacion = "Puerta Principal del Colegio"

    params = {
        "action": "TEMPLATE",
        "text": titulo,
        "dates": f"{start_time}/{end_time}",
        "details": detalles,
        "location": ubicacion
    }
    return f"https://calendar.google.com/calendar/render?{urllib.parse.urlencode(params)}"

# Logo institucional centrado
col_izq, col_centro, col_der = st.columns([1, 2.5, 1])
with col_centro:
    try:
        st.image("logo_bapsync.png", use_container_width=True)
    except Exception:
        st.markdown("<h2 style='text-align: center; color: #0c5c3c;'>🛡️ BapSync</h2>", unsafe_allow_html=True)

# Lógica de fechas
hoy = datetime.today()
meses_nombres = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                 "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
dias_nombres = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

mes_actual_nombre = meses_nombres[hoy.month - 1]
total_dias_mes = calendar.monthrange(hoy.year, hoy.month)[1]
fecha_hoy_str = hoy.strftime("%Y-%m-%d")

# Banner institucional superior
st.markdown(f"""
    <div class='header-banner'>
        <h4>SEGURIDAD ESCOLAR BAPES</h4>
        <p>Rol Oficial — Mes de {mes_actual_nombre} {hoy.year}<br>
        Mañana (07:30 - 08:15) | Tarde (02:15 - 03:00) • Máx. 5 apoderados por turno</p>
    </div>
""", unsafe_allow_html=True)

# Días hábiles
dias_mes_dict = {}
for dia_num in range(1, total_dias_mes + 1):
    fecha_obj = datetime(hoy.year, hoy.month, dia_num)
    if fecha_obj.weekday() < 5:
        nombre_d = dias_nombres[fecha_obj.weekday()]
        etiqueta = f"{nombre_d} {dia_num:02d} de {mes_actual_nombre}"
        dias_mes_dict[etiqueta] = {
            "fecha_str": fecha_obj.strftime("%Y-%m-%d"),
            "dia": nombre_d,
            "dia_num": dia_num
        }

df_turnos = cargar_turnos()

tab_registro, tab_horario, tab_notif = st.tabs(["📝 Inscribirme", "📅 Rol Mensual", "🔒 Dirección"])

# --- TAB 1: INSCRIPCIÓN ---
with tab_registro:
    st.markdown("#### 1. Selecciona fecha y horario")
    dia_elegido_label = st.selectbox("Día de asistencia (Lunes a Viernes):", list(dias_mes_dict.keys()))
    info_dia = dias_mes_dict[dia_elegido_label]
    
    turnos_disponibles = [
        "🌅 Mañana: 07:30 a 08:15 (Entrada)",
        "🌇 Tarde: 02:15 a 03:00 (Salida)"
    ]
    turno_elegido = st.radio("Horario disponible:", turnos_disponibles)

    # Conteo de cupos
    if not df_turnos.empty and "fecha" in df_turnos.columns and "turno" in df_turnos.columns:
        fechas_col = df_turnos["fecha"].astype(str).str.strip().str[:10]
        turnos_col = df_turnos["turno"].astype(str).str.strip()
        ocupados = len(df_turnos[(fechas_col == info_dia["fecha_str"]) & (turnos_col == turno_elegido)])
    else:
        ocupados = 0

    libres = 5 - ocupados

    if libres > 0:
        st.success(f"🟢 **{libres} de 5 cupos disponibles** para el {dia_elegido_label}")
    else:
        st.error("🔴 **Turno completo (5/5).** Selecciona otra fecha o turno.")

    st.markdown("---")
    st.markdown("#### 2. Datos del Apoderado")
    nombre_padre = st.text_input("Nombres y Apellidos del Apoderado:")
    telefono_padre = st.text_input("Celular / WhatsApp (9 dígitos):", max_chars=9)
    estudiante = st.text_input("Nombre completo del Estudiante:")
    grado = st.text_input("Grado y Sección (Ej: 3ro B Primaria):")

    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)

    if st.button("Confirmar mi Turno en BAPES"):
        if not (nombre_padre and telefono_padre and estudiante and grado):
            st.warning("⚠️ Todos los campos son obligatorios para validar el registro.")
        elif libres <= 0:
            st.error("No es posible completar la inscripción: Cupos agotados.")
        elif not API_URL:
            st.error("Error técnico: URL de base de datos no configurada.")
        else:
            payload = {
                "fecha": str(info_dia["fecha_str"]),
                "dia": str(info_dia["dia"]),
                "turno": str(turno_elegido),
                "padre": str(nombre_padre).strip(),
                "telefono": str(telefono_padre).strip(),
                "estudiante": str(estudiante).strip(),
                "grado": str(grado).strip(),
                "creado": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            try:
                r = requests.post(API_URL, json=payload, timeout=15, allow_redirects=True)
                if r.status_code in [200, 302] or "ok" in r.text.lower():
                    st.success("🎉 ¡Tu turno ha sido registrado correctamente!")
                    
                    url_calendar = generar_enlace_google_calendar(
                        info_dia["fecha_str"], turno_elegido, nombre_padre, estudiante
                    )
                    mensaje_wa = f"Hola {nombre_padre}, confirmaste tu turno en BAPES para el {dia_elegido_label} ({turno_elegido}). ¡Agradecemos tu compromiso con la seguridad estudiantil!"
                    url_whatsapp = f"https://wa.me/51{telefono_padre}?text={urllib.parse.quote(mensaje_wa)}"
                    
                    st.markdown("#### 🔔 Activa tu recordatorio personal:")
                    col_b1, col_b2 = st.columns(2)
                    with col_b1:
                        st.markdown(f"""
                            <a href='{url_calendar}' target='_blank' style='display:block; text-align:center; background-color:#1a73e8; color:white !important; padding:12px; border-radius:10px; text-decoration:none; font-weight:700;'>
                                📅 Google Calendar
                            </a>
                        """, unsafe_allow_html=True)
                    with col_b2:
                        st.markdown(f"""
                            <a href='{url_whatsapp}' target='_blank' style='display:block; text-align:center; background-color:#25D366; color:white !important; padding:12px; border-radius:10px; text-decoration:none; font-weight:700;'>
                                📲 WhatsApp
                            </a>
                        """, unsafe_allow_html=True)
                else:
                    st.error(f"Error en el servidor: {r.status_code}")
            except Exception as ex:
                st.error(f"Error de red al conectar: {ex}")

# --- TAB 2: ROL MENSUAL ---
with tab_horario:
    st.markdown(f"#### 📋 Rol de Vigilancia ({mes_actual_nombre} {hoy.year})")
    if st.button("🔄 Actualizar Tabla"):
        st.rerun()

    if not df_turnos.empty and "padre" in df_turnos.columns:
        mes_prefijo = hoy.strftime("%Y-%m")
        if "fecha" in df_turnos.columns:
            df_turnos["fecha_corta"] = df_turnos["fecha"].astype(str).str.strip().str[:10]
            df_mes = df_turnos[df_turnos["fecha_corta"].str.startswith(mes_prefijo)].copy()
        else:
            df_mes = pd.DataFrame()

        df_mostrar = df_mes if not df_mes.empty else df_turnos

        if "fecha_corta" in df_mostrar.columns:
            try:
                df_mostrar["fecha_formato"] = pd.to_datetime(df_mostrar["fecha_corta"]).dt.strftime("%d/%m/%Y")
            except Exception:
                df_mostrar["fecha_formato"] = df_mostrar["fecha_corta"]
        else:
            df_mostrar["fecha_formato"] = df_mostrar.get("fecha", "")

        df_mostrar = df_mostrar.rename(columns={"fecha_formato": "Fecha_Limpia"})
        cols_deseadas = [c for c in ["dia", "Fecha_Limpia", "turno", "padre", "estudiante", "grado"] if c in df_mostrar.columns]
        
        vista = df_mostrar[cols_deseadas].sort_values(by="Fecha_Limpia", ascending=True).copy()
        vista.columns = ["Día", "Fecha", "Turno", "Apoderado", "Estudiante", "Grado"]
        st.dataframe(vista, use_container_width=True, hide_index=True)
    else:
        st.info("Aún no hay turnos registrados en este mes.")

# --- TAB 3: ACCESO ADMINISTRATIVO ---
with tab_notif:
    st.markdown("#### 🔒 Panel Exclusivo de Coordinación")
    pin = st.text_input("Ingrese la clave institucional:", type="password")

    if pin:
        if pin == ADMIN_PIN:
            st.success("Acceso administrativo autorizado.")
            st.markdown(f"##### 🔔 Turnos de Hoy ({hoy.strftime('%d/%m/%Y')})")
            
            if not df_turnos.empty and "fecha" in df_turnos.columns:
                df_turnos["fecha_corta"] = df_turnos["fecha"].astype(str).str.strip().str[:10]
                padres_hoy = df_turnos[df_turnos["fecha_corta"] == fecha_hoy_str]

                if not padres_hoy.empty:
                    st.write(f"Total para hoy: **{len(padres_hoy)} apoderado(s)**")
                    for _, fila in padres_hoy.iterrows():
                        padre_nom = fila.get("padre", "Apoderado")
                        turno_nom = fila.get("turno", "Turno")
                        tel = str(fila.get("telefono", "")).replace(".0", "").strip()
                        est = fila.get("estudiante", "el estudiante")

                        msg_hoy = (
                            f"Estimado/a {padre_nom}, le recordamos su turno de vigilancia BAPES hoy ({turno_nom}), "
                            f"resguardando la seguridad de su hijo/a {est}. ¡Agradecemos su puntualidad!"
                        )
                        url_aviso = f"https://wa.me/51{tel}?text={urllib.parse.quote(msg_hoy)}"

                        st.markdown(f"""
                            <div class='card-recordatorio'>
                                <b style='color:#0f172a;'>👤 {padre_nom}</b> — <i>{turno_nom}</i><br>
                                <span style='font-size:13.5px; color:#475569;'>Estudiante: {est} | Celular: {tel}</span><br><br>
                                <a href='{url_aviso}' target='_blank' style='background-color:#25D366; color:white !important; padding:8px 16px; border-radius:8px; text-decoration:none; font-weight:700; font-size:13.5px; display:inline-block;'>
                                    📲 Enviar Recordatorio WhatsApp
                                </a>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No hay turnos registrados para el día de hoy.")
            else:
                st.info("No hay registros en la base de datos.")
        else:
            st.error("Credenciales incorrectas.")
