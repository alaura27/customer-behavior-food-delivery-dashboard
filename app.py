import os
import streamlit as st
import pandas as pd
import altair as alt

# -----------------------------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Dashboard de Comportamento de Clientes | Food Delivery",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilo CSS customizado para visual executivo e moderno
st.markdown(
    """
    <style>
    .main-header {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: #f8fafc;
        padding: 1.75rem 2rem;
        border-radius: 14px;
        margin-bottom: 1.25rem;
        border-left: 6px solid #f97316;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    }
    .main-header h1 {
        margin: 0;
        font-size: 1.95rem;
        font-weight: 800;
        color: #ffffff !important;
        letter-spacing: -0.02em;
    }
    .main-header p {
        margin: 0.45rem 0 0 0;
        font-size: 1rem;
        color: #cbd5e1;
        line-height: 1.5;
    }
    .intro-card {
        background-color: rgba(249, 115, 22, 0.07);
        border: 1px solid rgba(249, 115, 22, 0.25);
        border-radius: 12px;
        padding: 1.15rem 1.4rem;
        margin-bottom: 1.25rem;
    }
    .intro-card h4 {
        margin-top: 0;
        margin-bottom: 0.5rem;
        color: #ea580c;
        font-weight: 700;
    }
    .kpi-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 12px;
        padding: 1.1rem 1.2rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
        height: 100%;
    }
    .kpi-label {
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        color: #64748b;
        margin-bottom: 0.35rem;
    }
    .kpi-value {
        font-size: 1.85rem;
        font-weight: 800;
        margin-bottom: 0.25rem;
        line-height: 1.15;
    }
    .kpi-sub {
        font-size: 0.82rem;
        color: #64748b;
    }
    .badge-pos {
        display: inline-block;
        padding: 0.15rem 0.55rem;
        border-radius: 999px;
        font-size: 0.76rem;
        font-weight: 600;
        background: rgba(16, 185, 129, 0.15);
        color: #059669;
    }
    .badge-neg {
        display: inline-block;
        padding: 0.15rem 0.55rem;
        border-radius: 999px;
        font-size: 0.76rem;
        font-weight: 600;
        background: rgba(239, 68, 68, 0.15);
        color: #dc2626;
    }
    .badge-neutral {
        display: inline-block;
        padding: 0.15rem 0.55rem;
        border-radius: 999px;
        font-size: 0.76rem;
        font-weight: 600;
        background: rgba(59, 130, 246, 0.15);
        color: #2563eb;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# CARREGAMENTO E TRATAMENTO DOS DADOS
# -----------------------------------------------------------------------------
@st.cache_data
def load_data() -> pd.DataFrame:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "online food delivery dataset.csv")
    if not os.path.exists(csv_path):
        csv_path = "online food delivery dataset.csv"

    df = pd.read_csv(csv_path, index_col=False)

    # Remove colunas extras vazias ou sem nome geradas por vírgula final no cabeçalho
    unnamed_cols = [c for c in df.columns if str(c).startswith("Unnamed") or str(c).strip() == ""]
    if unnamed_cols:
        df = df.drop(columns=unnamed_cols)

    # Padronização de strings (remoção de espaços extras como "Negative ")
    for col in df.select_dtypes(include=["object", "string"]).columns:
        df[col] = df[col].astype(str).str.strip()

    # Mapeamentos em Português para leitura executiva clara
    gender_map = {"Male": "Masculino", "Female": "Feminino"}
    marital_map = {
        "Single": "Solteiro(a)",
        "Married": "Casado(a)",
        "Prefer not to say": "Prefere não informar",
    }
    occupation_map = {
        "Student": "Estudante",
        "Employee": "Empregado (CLT/Privado)",
        "Self Employeed": "Autônomo",
        "House wife": "Dona de Casa",
    }
    income_map = {
        "No Income": "Sem Renda",
        "Below Rs.10000": "Até Rs. 10.000",
        "10001 to 25000": "Rs. 10.001 a 25.000",
        "25001 to 50000": "Rs. 25.001 a 50.000",
        "More than 50000": "Acima de Rs. 50.000",
    }
    education_map = {
        "Uneducated": "Sem Instrução Formal",
        "School": "Ensino Básico/Médio",
        "Graduate": "Graduação",
        "Post Graduate": "Pós-Graduação",
        "Ph.D": "Doutorado (Ph.D)",
    }
    cust_type_map = {
        "New": "Novo",
        "Regular": "Regular",
        "Frequent": "Frequente",
    }
    feedback_map = {
        "Positive": "Positivo",
        "Negative": "Negativo",
    }
    output_map = {
        "Yes": "Retido (Ativo)",
        "No": "Inativo / Churn",
    }

    df["Gênero"] = df["Gender"].map(gender_map).fillna(df["Gender"])
    df["Estado Matrimonial"] = df["Marital Status"].map(marital_map).fillna(df["Marital Status"])
    df["Ocupação"] = df["Occupation"].map(occupation_map).fillna(df["Occupation"])
    df["Renda Mensal"] = df["Monthly Income"].map(income_map).fillna(df["Monthly Income"])
    df["Escolaridade"] = (
        df["Educational Qualifications"].map(education_map).fillna(df["Educational Qualifications"])
    )
    df["Tipo de Cliente"] = df["Customer Type"].map(cust_type_map).fillna(df["Customer Type"])
    df["Sentimento (Feedback)"] = df["Feedback"].map(feedback_map).fillna(df["Feedback"])
    df["Status de Retenção"] = df["Output"].map(output_map).fillna(df["Output"])

    # Indicadores binários para cálculo de taxas
    df["Retido_Bin"] = (df["Output"] == "Yes").astype(int)
    df["Feedback_Pos_Bin"] = (df["Feedback"] == "Positive").astype(int)
    df["Recorrente_Bin"] = df["Customer Type"].isin(["Regular", "Frequent"]).astype(int)

    # Faixas etárias para segmentação
    df["Faixa Etária"] = pd.cut(
        df["Age"],
        bins=[17, 21, 25, 29, 40],
        labels=["18–21 anos", "22–25 anos", "26–29 anos", "30+ anos"],
    ).astype(str)

    return df


INCOME_ORDER = [
    "Sem Renda",
    "Até Rs. 10.000",
    "Rs. 10.001 a 25.000",
    "Rs. 25.001 a 50.000",
    "Acima de Rs. 50.000",
]

AGE_GROUP_ORDER = ["18–21 anos", "22–25 anos", "26–29 anos", "30+ anos"]
CUST_TYPE_ORDER = ["Novo", "Regular", "Frequente"]

df_raw = load_data()

# -----------------------------------------------------------------------------
# SIDEBAR - FILTROS GLOBAIS INTERATIVOS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🎯 Filtros de Segmentação")
    st.caption("Refine a análise selecionando os perfis demográficos e comportamentais abaixo.")

    min_age, max_age = int(df_raw["Age"].min()), int(df_raw["Age"].max())
    selected_age = st.slider(
        "Faixa de Idade (Anos)",
        min_value=min_age,
        max_value=max_age,
        value=(min_age, max_age),
    )

    all_genders = sorted(df_raw["Gênero"].unique().tolist())
    selected_genders = st.multiselect("Sexo / Gênero", options=all_genders, default=all_genders)

    all_marital = sorted(df_raw["Estado Matrimonial"].unique().tolist())
    selected_marital = st.multiselect(
        "Estado Matrimonial", options=all_marital, default=all_marital
    )

    all_occupations = sorted(df_raw["Ocupação"].unique().tolist())
    selected_occupations = st.multiselect(
        "Ocupação", options=all_occupations, default=all_occupations
    )

    available_incomes = [inc for inc in INCOME_ORDER if inc in df_raw["Renda Mensal"].unique()]
    selected_incomes = st.multiselect(
        "Renda Mensal", options=available_incomes, default=available_incomes
    )

    available_cust_types = [
        ct for ct in CUST_TYPE_ORDER if ct in df_raw["Tipo de Cliente"].unique()
    ]
    selected_cust_types = st.multiselect(
        "Tipo de Cliente", options=available_cust_types, default=available_cust_types
    )

    st.divider()

    # Aplicação dos filtros
    df = df_raw[
        (df_raw["Age"].between(selected_age[0], selected_age[1]))
        & (df_raw["Gênero"].isin(selected_genders))
        & (df_raw["Estado Matrimonial"].isin(selected_marital))
        & (df_raw["Ocupação"].isin(selected_occupations))
        & (df_raw["Renda Mensal"].isin(selected_incomes))
        & (df_raw["Tipo de Cliente"].isin(selected_cust_types))
    ].copy()

    pct_filtered = (len(df) / len(df_raw) * 100) if len(df_raw) > 0 else 0
    st.metric(
        "Amostra Selecionada",
        f"{len(df)} clientes",
        f"{pct_filtered:.1f}% da base total ({len(df_raw)})",
    )

# -----------------------------------------------------------------------------
# CABEÇALHO PRINCIPAL E APRESENTAÇÃO INICIAL DOS DADOS
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="main-header">
        <h1>🍔 Inteligência Comportamental de Clientes — Online Food Delivery</h1>
        <p>Monitoramento executivo de Retenção de Clientes, Análise de Sentimento (Feedback Rate) e Segmentação Demográfica & Socioeconômica.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.expander("📖 Apresentação Inicial dos Dados & Contexto Analítico (Clique para recolher/expandir)", expanded=True):
    col_intro_1, col_intro_2 = st.columns([1.55, 1])

    with col_intro_1:
        st.markdown(
            """
            <div class="intro-card">
                <h4>📌 Sobre o Dataset (Online Food Delivery)</h4>
                <p style="margin-bottom: 0.5rem;">
                A base de dados reúne <strong>388 registros de clientes</strong> de plataformas de entrega de comida online (região metropolitana de Bangalore, Índia), mapeando o ciclo de relacionamento entre perfil socioeconômico, frequência de pedidos, satisfação e retenção ativa.
                </p>
                <ul style="margin-bottom: 0; padding-left: 1.2rem;">
                    <li><strong>Perfil Etário Jovem:</strong> Idades entre <strong>18 e 33 anos</strong> (média de <strong>24,6 anos</strong>), com forte concentração universitária e jovens profissionais (22–25 anos representam 59,8% da base).</li>
                    <li><strong>Dinâmica Socioeconômica:</strong> Predominância de <strong>Estudantes (53,4%)</strong> e <strong>Empregados (30,4%)</strong>. Cerca de 48,2% ainda não possuem renda própria (dependentes/universitários), mas apresentam a maior taxa de recompra (88,8%).</li>
                    <li><strong>Forte Correlação Sentimento × Retenção:</strong> Clientes com feedback <strong>Positivo (81,7% da base)</strong> apresentam uma taxa de retenção de <strong>92,1%</strong>, enquanto entre clientes com feedback <strong>Negativo (18,3%)</strong> a retenção despenca para apenas <strong>12,7%</strong>.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_intro_2:
        summary_df = pd.DataFrame(
            {
                "Dimensão Analisada": [
                    "Total de Registros",
                    "Faixa Etária (Mín – Máx)",
                    "Tamanho da Família",
                    "Tipos de Cliente",
                    "Variáveis Demográficas",
                    "KPIs de Performance",
                ],
                "Descrição na Base": [
                    f"{len(df_raw)} clientes únicos / pedidos avaliados",
                    f"{df_raw['Age'].min()} a {df_raw['Age'].max()} anos (Média: {df_raw['Age'].mean():.1f} anos)",
                    f"{df_raw['Family size'].min()} a {df_raw['Family size'].max()} pessoas (Média: {df_raw['Family size'].mean():.1f})",
                    "Frequente (43,0%), Regular (51,3%), Novo (5,7%)",
                    "Renda, Ocupação, Idade, Sexo, Estado Civil, Escolaridade",
                    "Taxa de Retenção (Output) & Feedback Rate (Sentimento)",
                ],
            }
        )
        st.dataframe(summary_df, use_container_width=True, hide_index=True)

if df.empty:
    st.warning(
        "⚠️ Nenhum registro encontrado para a combinação atual de filtros. Ajuste as opções na barra lateral."
    )
    st.stop()

# -----------------------------------------------------------------------------
# CÁLCULO DOS KPIS MONITORADOS
# -----------------------------------------------------------------------------
total_clientes = len(df)
retencao_rate = df["Retido_Bin"].mean() * 100
base_retencao_rate = df_raw["Retido_Bin"].mean() * 100
delta_retencao = retencao_rate - base_retencao_rate

recorrencia_rate = df["Recorrente_Bin"].mean() * 100
feedback_pos_rate = df["Feedback_Pos_Bin"].mean() * 100
feedback_neg_rate = 100 - feedback_pos_rate
net_sentiment = feedback_pos_rate - feedback_neg_rate

base_feedback_pos = df_raw["Feedback_Pos_Bin"].mean() * 100
delta_feedback = feedback_pos_rate - base_feedback_pos

idade_media = df["Age"].mean()
familia_media = df["Family size"].mean()

st.markdown("### 📈 KPIs Estratégicos Monitorados")
kpi_cols = st.columns(5)

with kpi_cols[0]:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Taxa de Retenção (Output = Yes)</div>
            <div class="kpi-value" style="color: #10b981;">{retencao_rate:.1f}%</div>
            <div class="kpi-sub">
                <span class="{'badge-pos' if delta_retencao >= 0 else 'badge-neg'}">
                    {delta_retencao:+.1f} p.p. vs base
                </span>
                &nbsp;{int(df['Retido_Bin'].sum())} de {total_clientes} retidos
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi_cols[1]:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Clientes Recorrentes</div>
            <div class="kpi-value" style="color: #3b82f6;">{recorrencia_rate:.1f}%</div>
            <div class="kpi-sub">
                <span class="badge-neutral">Regular + Frequente</span>
                &nbsp;{int(df['Recorrente_Bin'].sum())} clientes fiéis
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi_cols[2]:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Feedback Positivo (Sentimento)</div>
            <div class="kpi-value" style="color: #f97316;">{feedback_pos_rate:.1f}%</div>
            <div class="kpi-sub">
                <span class="{'badge-pos' if delta_feedback >= 0 else 'badge-neg'}">
                    {delta_feedback:+.1f} p.p. vs base
                </span>
                &nbsp;Negativo: {feedback_neg_rate:.1f}%
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi_cols[3]:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Net Sentiment Score (NSS)</div>
            <div class="kpi-value" style="color: {'#10b981' if net_sentiment >= 50 else '#eab308'};">{net_sentiment:+.1f}</div>
            <div class="kpi-sub">
                <span class="badge-pos">% Positivo − % Negativo</span>
                &nbsp;Escala -100 a +100
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi_cols[4]:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Perfil Médio da Amostra</div>
            <div class="kpi-value" style="color: #8b5cf6;">{idade_media:.1f} anos</div>
            <div class="kpi-sub">
                <span class="badge-neutral">Família: {familia_media:.1f} pessoas</span>
                &nbsp;N = {total_clientes}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

# -----------------------------------------------------------------------------
# FUNÇÕES AUXILIARES DE GRÁFICOS ALTAIR
# -----------------------------------------------------------------------------
def build_segment_summary(data: pd.DataFrame, group_col: str, order_list=None) -> pd.DataFrame:
    grouped = (
        data.groupby(group_col, observed=False)
        .agg(
            Clientes=("Age", "count"),
            Retidos=("Retido_Bin", "sum"),
            Taxa_Retencao=("Retido_Bin", lambda x: round(x.mean() * 100, 1)),
            Feedback_Pos=("Feedback_Pos_Bin", "sum"),
            Taxa_Feedback_Pos=("Feedback_Pos_Bin", lambda x: round(x.mean() * 100, 1)),
            Idade_Media=("Age", lambda x: round(x.mean(), 1)),
        )
        .reset_index()
    )
    grouped["Participacao_%"] = (grouped["Clientes"] / len(data) * 100).round(1)
    grouped["Taxa_Feedback_Neg"] = (100.0 - grouped["Taxa_Feedback_Pos"]).round(1)
    if order_list:
        grouped[group_col] = pd.Categorical(grouped[group_col], categories=order_list, ordered=True)
        grouped = grouped.sort_values(group_col).reset_index(drop=True)
    else:
        grouped = grouped.sort_values("Clientes", ascending=False).reset_index(drop=True)
    return grouped


# -----------------------------------------------------------------------------
# ABAS PRINCIPAIS DE ANÁLISE
# -----------------------------------------------------------------------------
tab_seg, tab_ret, tab_sent, tab_geo = st.tabs(
    [
        "👥 1. Segmentação Comportamental (5 Dimensões)",
        "🔄 2. Taxa de Retenção & Fidelização",
        "💬 3. Análise de Sentimento (Feedback Rate)",
        "🗺️ 4. Mapa Geográfico & Explorador de Dados",
    ]
)

# =============================================================================
# ABA 1: SEGMENTAÇÃO COMPORTAMENTAL (RENDA, OCUPAÇÃO, IDADE, SEXO, ESTADO CIVIL)
# =============================================================================
with tab_seg:
    st.markdown(
        "#### 🔍 Segmentação Comportamental Multidimensional"
    )
    st.caption(
        "Análise detalhada do comportamento do cliente por **Renda Mensal**, **Ocupação**, **Idade**, **Sexo** e **Estado Matrimonial**, combinando volume de clientes, taxa de retenção e taxa de feedback positivo."
    )

    # --- LINHA 1: RENDA MENSAL & OCUPAÇÃO ---
    col_r1, col_r2 = st.columns(2)

    with col_r1:
        st.markdown("##### 💰 1. Segmentação por Renda Mensal")
        inc_summary = build_segment_summary(df, "Renda Mensal", order_list=INCOME_ORDER)

        base_inc = alt.Chart(inc_summary).encode(
            y=alt.Y("Renda Mensal:N", sort=INCOME_ORDER, title="Faixa de Renda Mensal")
        )
        bars_inc = base_inc.mark_bar(cornerRadiusEnd=5, height=24).encode(
            x=alt.X("Clientes:Q", title="Volume de Clientes"),
            color=alt.Color(
                "Taxa_Retencao:Q",
                title="Retenção (%)",
                scale=alt.Scale(scheme="tealblues", domain=[40, 100]),
            ),
            tooltip=[
                alt.Tooltip("Renda Mensal:N", title="Faixa de Renda"),
                alt.Tooltip("Clientes:Q", title="Total de Clientes"),
                alt.Tooltip("Participacao_%:Q", title="Participação (%)"),
                alt.Tooltip("Taxa_Retencao:Q", title="Taxa de Retenção (%)"),
                alt.Tooltip("Taxa_Feedback_Pos:Q", title="Feedback Positivo (%)"),
            ],
        )
        text_inc = base_inc.mark_text(align="left", dx=5, fontWeight="bold").encode(
            x=alt.X("Clientes:Q"),
            text=alt.Text("Taxa_Retencao:Q", format=".1f"),
        )
        st.altair_chart((bars_inc + text_inc).properties(height=270), use_container_width=True)
        st.caption("As barras indicam o volume de clientes; a cor e o rótulo à direita mostram a **Taxa de Retenção (%)** em cada faixa de renda.")

    with col_r2:
        st.markdown("##### 💼 2. Segmentação por Ocupação")
        occ_summary = build_segment_summary(df, "Ocupação")

        occ_long = occ_summary.melt(
            id_vars=["Ocupação", "Clientes", "Participacao_%"],
            value_vars=["Taxa_Retencao", "Taxa_Feedback_Pos"],
            var_name="Indicador",
            value_name="Taxa (%)",
        )
        occ_long["Indicador"] = occ_long["Indicador"].map(
            {
                "Taxa_Retencao": "Taxa de Retenção (%)",
                "Taxa_Feedback_Pos": "Feedback Positivo (%)",
            }
        )

        chart_occ = (
            alt.Chart(occ_long)
            .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
            .encode(
                x=alt.X("Ocupação:N", sort="-y", title="Ocupação", axis=alt.Axis(labelAngle=0)),
                y=alt.Y("Taxa (%):Q", scale=alt.Scale(domain=[0, 105]), title="Percentual (%)"),
                xOffset="Indicador:N",
                color=alt.Color(
                    "Indicador:N",
                    scale=alt.Scale(
                        domain=["Taxa de Retenção (%)", "Feedback Positivo (%)"],
                        range=["#10b981", "#f97316"],
                    ),
                    legend=alt.Legend(orient="top", title=None),
                ),
                tooltip=[
                    alt.Tooltip("Ocupação:N", title="Ocupação"),
                    alt.Tooltip("Indicador:N", title="Métrica"),
                    alt.Tooltip("Taxa (%):Q", title="Valor (%)"),
                    alt.Tooltip("Clientes:Q", title="Volume de Clientes"),
                    alt.Tooltip("Participacao_%:Q", title="Share da Amostra (%)"),
                ],
            )
            .properties(height=270)
        )
        st.altair_chart(chart_occ, use_container_width=True)
        st.caption("Comparativo lado a lado entre **Taxa de Retenção** e **Feedback Positivo** para cada grupo ocupacional.")

    st.divider()

    # --- LINHA 2: IDADE, SEXO E ESTADO MATRIMONIAL ---
    col_r3, col_r4, col_r5 = st.columns([1.25, 0.9, 1.05])

    with col_r3:
        st.markdown("##### 🎂 3. Segmentação por Idade e Faixa Etária")
        age_chart = (
            alt.Chart(df)
            .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
            .encode(
                x=alt.X("Age:O", title="Idade (Anos)", axis=alt.Axis(labelAngle=0)),
                y=alt.Y("count():Q", title="Nº de Clientes"),
                color=alt.Color(
                    "Tipo de Cliente:N",
                    sort=CUST_TYPE_ORDER,
                    scale=alt.Scale(
                        domain=["Novo", "Regular", "Frequente"],
                        range=["#94a3b8", "#3b82f6", "#f97316"],
                    ),
                    legend=alt.Legend(orient="top", title="Tipo de Cliente"),
                ),
                tooltip=[
                    alt.Tooltip("Age:O", title="Idade"),
                    alt.Tooltip("Tipo de Cliente:N", title="Tipo de Cliente"),
                    alt.Tooltip("count():Q", title="Quantidade"),
                ],
            )
            .properties(height=260)
        )
        st.altair_chart(age_chart, use_container_width=True)

    with col_r4:
        st.markdown("##### 🚻 4. Segmentação por Sexo")
        gen_summary = build_segment_summary(df, "Gênero")

        donut_gen = (
            alt.Chart(gen_summary)
            .mark_arc(innerRadius=55, outerRadius=95)
            .encode(
                theta=alt.Theta("Clientes:Q"),
                color=alt.Color(
                    "Gênero:N",
                    scale=alt.Scale(
                        domain=["Masculino", "Feminino"],
                        range=["#3b82f6", "#ec4899"],
                    ),
                    legend=alt.Legend(orient="top", title=None),
                ),
                tooltip=[
                    alt.Tooltip("Gênero:N", title="Sexo"),
                    alt.Tooltip("Clientes:Q", title="Clientes"),
                    alt.Tooltip("Participacao_%:Q", title="Participação (%)"),
                    alt.Tooltip("Taxa_Retencao:Q", title="Taxa de Retenção (%)"),
                    alt.Tooltip("Taxa_Feedback_Pos:Q", title="Feedback Positivo (%)"),
                ],
            )
            .properties(height=200)
        )
        st.altair_chart(donut_gen, use_container_width=True)
        st.dataframe(
            gen_summary[["Gênero", "Clientes", "Taxa_Retencao", "Taxa_Feedback_Pos"]].rename(
                columns={
                    "Taxa_Retencao": "Retenção (%)",
                    "Taxa_Feedback_Pos": "Sent. Positivo (%)",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

    with col_r5:
        st.markdown("##### 💍 5. Segmentação por Estado Matrimonial")
        mar_summary = build_segment_summary(df, "Estado Matrimonial")

        mar_chart = (
            alt.Chart(mar_summary)
            .mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5)
            .encode(
                x=alt.X(
                    "Estado Matrimonial:N",
                    sort="-y",
                    title="Estado Civil",
                    axis=alt.Axis(labelAngle=0),
                ),
                y=alt.Y("Clientes:Q", title="Total de Clientes"),
                color=alt.Color(
                    "Taxa_Feedback_Pos:Q",
                    title="Sent. Positivo (%)",
                    scale=alt.Scale(scheme="oranges", domain=[50, 95]),
                ),
                tooltip=[
                    alt.Tooltip("Estado Matrimonial:N", title="Estado Matrimonial"),
                    alt.Tooltip("Clientes:Q", title="Clientes"),
                    alt.Tooltip("Participacao_%:Q", title="Share (%)"),
                    alt.Tooltip("Taxa_Retencao:Q", title="Retenção (%)"),
                    alt.Tooltip("Taxa_Feedback_Pos:Q", title="Feedback Positivo (%)"),
                ],
            )
            .properties(height=200)
        )
        st.altair_chart(mar_chart, use_container_width=True)
        st.dataframe(
            mar_summary[
                ["Estado Matrimonial", "Clientes", "Taxa_Retencao", "Taxa_Feedback_Pos"]
            ].rename(
                columns={
                    "Estado Matrimonial": "Estado Civil",
                    "Taxa_Retencao": "Retenção (%)",
                    "Taxa_Feedback_Pos": "Sent. Positivo (%)",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

    st.divider()

    # --- MATRIZ CONSOLIDADA DAS 5 DIMENSÕES ---
    st.markdown("##### 📋 Tabela Executiva Consolidada por Segmento")
    dim_choice = st.radio(
        "Selecione a dimensão para inspecionar métricas detalhadas:",
        options=[
            "Renda Mensal",
            "Ocupação",
            "Faixa Etária",
            "Gênero",
            "Estado Matrimonial",
            "Escolaridade",
        ],
        horizontal=True,
    )

    order_to_use = (
        INCOME_ORDER
        if dim_choice == "Renda Mensal"
        else (AGE_GROUP_ORDER if dim_choice == "Faixa Etária" else None)
    )
    seg_table = build_segment_summary(df, dim_choice, order_list=order_to_use)

    st.dataframe(
        seg_table,
        use_container_width=True,
        hide_index=True,
        column_config={
            dim_choice: st.column_config.TextColumn(dim_choice),
            "Clientes": st.column_config.NumberColumn("Total de Clientes", format="%d"),
            "Participacao_%": st.column_config.ProgressColumn(
                "Participação na Base (%)", format="%.1f%%", min_value=0, max_value=100
            ),
            "Retidos": st.column_config.NumberColumn("Clientes Retidos", format="%d"),
            "Taxa_Retencao": st.column_config.ProgressColumn(
                "Taxa de Retenção (%)", format="%.1f%%", min_value=0, max_value=100
            ),
            "Feedback_Pos": st.column_config.NumberColumn("Avaliações Positivas", format="%d"),
            "Taxa_Feedback_Pos": st.column_config.ProgressColumn(
                "Feedback Positivo (%)", format="%.1f%%", min_value=0, max_value=100
            ),
            "Taxa_Feedback_Neg": st.column_config.NumberColumn(
                "Feedback Negativo (%)", format="%.1f%%"
            ),
            "Idade_Media": st.column_config.NumberColumn("Idade Média (Anos)", format="%.1f"),
        },
    )


# =============================================================================
# ABA 2: TAXA DE RETENÇÃO & FIDELIZAÇÃO
# =============================================================================
with tab_ret:
    st.markdown("#### 🔄 Diagnóstico de Retenção de Clientes e Recorrência")
    st.caption(
        "Análise da **Taxa de Retenção (`Output = Yes`)** e da estrutura de fidelidade (**Novo**, **Regular** e **Frequente**)."
    )

    col_ret_1, col_ret_2 = st.columns(2)

    with col_ret_1:
        st.markdown("##### 🏆 Retenção por Tipo de Cliente (Novo, Regular, Frequente)")
        ct_summary = build_segment_summary(df, "Tipo de Cliente", order_list=CUST_TYPE_ORDER)

        chart_ct = (
            alt.Chart(ct_summary)
            .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=55)
            .encode(
                x=alt.X(
                    "Tipo de Cliente:N",
                    sort=CUST_TYPE_ORDER,
                    title="Estágio de Fidelidade do Cliente",
                    axis=alt.Axis(labelAngle=0),
                ),
                y=alt.Y(
                    "Taxa_Retencao:Q",
                    title="Taxa de Retenção (%)",
                    scale=alt.Scale(domain=[0, 105]),
                ),
                color=alt.Color(
                    "Tipo de Cliente:N",
                    sort=CUST_TYPE_ORDER,
                    scale=alt.Scale(
                        domain=["Novo", "Regular", "Frequente"],
                        range=["#64748b", "#3b82f6", "#10b981"],
                    ),
                    legend=None,
                ),
                tooltip=[
                    alt.Tooltip("Tipo de Cliente:N", title="Segmento"),
                    alt.Tooltip("Clientes:Q", title="Volume de Clientes"),
                    alt.Tooltip("Participacao_%:Q", title="Participação (%)"),
                    alt.Tooltip("Taxa_Retencao:Q", title="Taxa de Retenção (%)"),
                    alt.Tooltip("Taxa_Feedback_Pos:Q", title="Feedback Positivo (%)"),
                ],
            )
            .properties(height=300)
        )
        st.altair_chart(chart_ct, use_container_width=True)

    with col_ret_2:
        st.markdown("##### 🔗 Impacto do Sentimento na Retenção de Clientes")
        sent_ret = (
            df.groupby(["Sentimento (Feedback)", "Status de Retenção"], observed=False)
            .size()
            .reset_index(name="Quantidade")
        )
        sent_totals = sent_ret.groupby("Sentimento (Feedback)")["Quantidade"].transform("sum")
        sent_ret["Percentual (%)"] = (sent_ret["Quantidade"] / sent_totals * 100).round(1)

        chart_sent_ret = (
            alt.Chart(sent_ret)
            .mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5, size=65)
            .encode(
                x=alt.X(
                    "Sentimento (Feedback):N",
                    title="Sentimento do Feedback Recebido",
                    axis=alt.Axis(labelAngle=0),
                ),
                y=alt.Y("Percentual (%):Q", title="Proporção de Clientes (%)"),
                color=alt.Color(
                    "Status de Retenção:N",
                    scale=alt.Scale(
                        domain=["Retido (Ativo)", "Inativo / Churn"],
                        range=["#10b981", "#ef4444"],
                    ),
                    legend=alt.Legend(orient="top", title="Status de Retenção"),
                ),
                tooltip=[
                    alt.Tooltip("Sentimento (Feedback):N", title="Feedback"),
                    alt.Tooltip("Status de Retenção:N", title="Status"),
                    alt.Tooltip("Quantidade:Q", title="Clientes"),
                    alt.Tooltip("Percentual (%):Q", title="Proporção no Grupo (%)"),
                ],
            )
            .properties(height=300)
        )
        st.altair_chart(chart_sent_ret, use_container_width=True)

    st.divider()

    # Curva de retenção por Idade e Tamanho de Família
    col_ret_3, col_ret_4 = st.columns(2)

    with col_ret_3:
        st.markdown("##### 📉 Taxa de Retenção por Faixa Etária")
        age_grp_summary = build_segment_summary(df, "Faixa Etária", order_list=AGE_GROUP_ORDER)
        line_age_ret = (
            alt.Chart(age_grp_summary)
            .mark_line(point=alt.OverlayMarkDef(size=90, filled=True), strokeWidth=3, color="#10b981")
            .encode(
                x=alt.X("Faixa Etária:N", sort=AGE_GROUP_ORDER, title="Faixa Etária", axis=alt.Axis(labelAngle=0)),
                y=alt.Y("Taxa_Retencao:Q", title="Taxa de Retenção (%)", scale=alt.Scale(domain=[0, 105])),
                tooltip=[
                    alt.Tooltip("Faixa Etária:N", title="Faixa Etária"),
                    alt.Tooltip("Clientes:Q", title="Clientes"),
                    alt.Tooltip("Taxa_Retencao:Q", title="Retenção (%)"),
                    alt.Tooltip("Taxa_Feedback_Pos:Q", title="Feedback Positivo (%)"),
                ],
            )
            .properties(height=260)
        )
        st.altair_chart(line_age_ret, use_container_width=True)

    with col_ret_4:
        st.markdown("##### 👨‍👩‍👧‍👦 Taxa de Retenção por Tamanho da Família")
        fam_summary = build_segment_summary(df, "Family size")
        fam_summary = fam_summary.sort_values("Family size")
        bar_fam = (
            alt.Chart(fam_summary)
            .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4, color="#3b82f6")
            .encode(
                x=alt.X("Family size:O", title="Número de Membros na Família", axis=alt.Axis(labelAngle=0)),
                y=alt.Y("Taxa_Retencao:Q", title="Taxa de Retenção (%)", scale=alt.Scale(domain=[0, 105])),
                tooltip=[
                    alt.Tooltip("Family size:O", title="Tamanho da Família"),
                    alt.Tooltip("Clientes:Q", title="Total de Clientes"),
                    alt.Tooltip("Taxa_Retencao:Q", title="Taxa de Retenção (%)"),
                    alt.Tooltip("Taxa_Feedback_Pos:Q", title="Feedback Positivo (%)"),
                ],
            )
            .properties(height=260)
        )
        st.altair_chart(bar_fam, use_container_width=True)


# =============================================================================
# ABA 3: ANÁLISE DE SENTIMENTO (FEEDBACK RATE)
# =============================================================================
with tab_sent:
    st.markdown("#### 💬 Análise de Sentimento e Satisfação (Feedback Rate)")
    st.caption(
        "Mapeamento das avaliações **Positivas** vs **Negativas**, identificação de focos de insatisfação e cruzamento socioeconômico."
    )

    col_s1, col_s2 = st.columns([1, 1.45])

    with col_s1:
        st.markdown("##### 🎯 Distribuição Geral de Sentimento")
        sent_counts = (
            df.groupby("Sentimento (Feedback)", observed=False)
            .size()
            .reset_index(name="Clientes")
        )
        sent_counts["Percentual (%)"] = (sent_counts["Clientes"] / len(df) * 100).round(1)

        donut_sent = (
            alt.Chart(sent_counts)
            .mark_arc(innerRadius=65, outerRadius=110)
            .encode(
                theta=alt.Theta("Clientes:Q"),
                color=alt.Color(
                    "Sentimento (Feedback):N",
                    scale=alt.Scale(
                        domain=["Positivo", "Negativo"],
                        range=["#10b981", "#ef4444"],
                    ),
                    legend=alt.Legend(orient="top", title="Sentimento"),
                ),
                tooltip=[
                    alt.Tooltip("Sentimento (Feedback):N", title="Sentimento"),
                    alt.Tooltip("Clientes:Q", title="Total de Clientes"),
                    alt.Tooltip("Percentual (%):Q", title="Proporção (%)"),
                ],
            )
            .properties(height=280)
        )
        st.altair_chart(donut_sent, use_container_width=True)
        st.dataframe(sent_counts, use_container_width=True, hide_index=True)

    with col_s2:
        st.markdown("##### 📊 Taxa de Sentimento (Positivo vs Negativo) por Renda Mensal")
        inc_sent = (
            df.groupby(["Renda Mensal", "Sentimento (Feedback)"], observed=False)
            .size()
            .reset_index(name="Clientes")
        )
        inc_totals = inc_sent.groupby("Renda Mensal")["Clientes"].transform("sum")
        inc_sent["Percentual (%)"] = (inc_sent["Clientes"] / inc_totals * 100).round(1)

        stacked_inc_sent = (
            alt.Chart(inc_sent)
            .mark_bar(cornerRadiusEnd=4, height=28)
            .encode(
                y=alt.Y("Renda Mensal:N", sort=INCOME_ORDER, title="Faixa de Renda"),
                x=alt.X("Percentual (%):Q", title="Proporção de Feedback (%)", scale=alt.Scale(domain=[0, 100])),
                color=alt.Color(
                    "Sentimento (Feedback):N",
                    scale=alt.Scale(
                        domain=["Positivo", "Negativo"],
                        range=["#10b981", "#ef4444"],
                    ),
                    legend=alt.Legend(orient="top", title="Sentimento"),
                ),
                tooltip=[
                    alt.Tooltip("Renda Mensal:N", title="Renda Mensal"),
                    alt.Tooltip("Sentimento (Feedback):N", title="Feedback"),
                    alt.Tooltip("Clientes:Q", title="Clientes"),
                    alt.Tooltip("Percentual (%):Q", title="Participação na Faixa (%)"),
                ],
            )
            .properties(height=280)
        )
        st.altair_chart(stacked_inc_sent, use_container_width=True)

    st.divider()

    # Mapa de calor Ocupação x Estado Matrimonial -> Feedback Positivo
    st.markdown("##### 🔥 Mapa de Calor: Taxa de Feedback Positivo (%) por Ocupação × Estado Matrimonial")
    heat_data = (
        df.groupby(["Ocupação", "Estado Matrimonial"], observed=False)
        .agg(
            Clientes=("Age", "count"),
            Feedback_Pos_Rate=("Feedback_Pos_Bin", lambda x: round(x.mean() * 100, 1)),
            Retencao_Rate=("Retido_Bin", lambda x: round(x.mean() * 100, 1)),
        )
        .reset_index()
    )
    heat_data = heat_data[heat_data["Clientes"] > 0]

    heatmap = (
        alt.Chart(heat_data)
        .mark_rect(cornerRadius=6)
        .encode(
            x=alt.X("Ocupação:N", title="Ocupação", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Estado Matrimonial:N", title="Estado Matrimonial"),
            color=alt.Color(
                "Feedback_Pos_Rate:Q",
                title="Feedback Positivo (%)",
                scale=alt.Scale(scheme="redyellowgreen", domain=[40, 100]),
            ),
            tooltip=[
                alt.Tooltip("Ocupação:N", title="Ocupação"),
                alt.Tooltip("Estado Matrimonial:N", title="Estado Civil"),
                alt.Tooltip("Clientes:Q", title="Clientes no Cruzamento"),
                alt.Tooltip("Feedback_Pos_Rate:Q", title="Feedback Positivo (%)"),
                alt.Tooltip("Retencao_Rate:Q", title="Taxa de Retenção (%)"),
            ],
        )
    )
    heat_text = (
        alt.Chart(heat_data)
        .mark_text(fontWeight="bold", fontSize=13)
        .encode(
            x=alt.X("Ocupação:N"),
            y=alt.Y("Estado Matrimonial:N"),
            text=alt.Text("Feedback_Pos_Rate:Q", format=".1f"),
            color=alt.condition(
                alt.datum.Feedback_Pos_Rate > 70,
                alt.value("#0f172a"),
                alt.value("#ffffff"),
            ),
        )
    )
    st.altair_chart((heatmap + heat_text).properties(height=250), use_container_width=True)


# =============================================================================
# ABA 4: MAPA GEOGRÁFICO & EXPLORADOR DE DADOS
# =============================================================================
with tab_geo:
    st.markdown("#### 🗺️ Geolocalização dos Clientes & Base de Dados Completa")
    col_map, col_pin = st.columns([1.4, 1])

    with col_map:
        st.markdown("##### 📍 Distribuição Espacial dos Pedidos (Latitude / Longitude)")
        map_df = df[["latitude", "longitude"]].dropna()
        st.map(map_df, zoom=11)

    with col_pin:
        st.markdown("##### 🏙️ Top 10 Regiões (Pin Code / CEP) por Volume de Clientes")
        pin_summary = (
            df.groupby("Pin code", observed=False)
            .agg(
                Clientes=("Age", "count"),
                Retencao_Pct=("Retido_Bin", lambda x: round(x.mean() * 100, 1)),
                Feedback_Pos_Pct=("Feedback_Pos_Bin", lambda x: round(x.mean() * 100, 1)),
            )
            .reset_index()
            .sort_values("Clientes", ascending=False)
            .head(10)
        )
        pin_summary["Pin code"] = pin_summary["Pin code"].astype(str)
        st.dataframe(
            pin_summary.rename(
                columns={
                    "Pin code": "CEP (Pin Code)",
                    "Retencao_Pct": "Retenção (%)",
                    "Feedback_Pos_Pct": "Feedback Positivo (%)",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

    st.divider()
    st.markdown("##### 🗂️ Explorador Interativo da Base de Dados Filtrada")
    display_cols = [
        "Age",
        "Faixa Etária",
        "Gênero",
        "Estado Matrimonial",
        "Ocupação",
        "Renda Mensal",
        "Escolaridade",
        "Family size",
        "Tipo de Cliente",
        "Status de Retenção",
        "Sentimento (Feedback)",
        "Pin code",
    ]
    st.dataframe(
        df[display_cols].rename(
            columns={
                "Age": "Idade",
                "Family size": "Tam. Família",
                "Pin code": "CEP",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

    csv_export = df[display_cols].to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        label="⬇️ Baixar Dados Filtrados (CSV)",
        data=csv_export,
        file_name="clientes_food_delivery_filtrado.csv",
        mime="text/csv",
    )

st.divider()

# -----------------------------------------------------------------------------
# 7. TRIAGEM INTELIGENTE (AGENTE DE CRM MULTIDIMENSIONAL)
# -----------------------------------------------------------------------------
taxa_retencao = retencao_rate
st.subheader("🤖 Insights do Agente de Retenção & Triagem Inteligente de CRM")
st.caption(
    "Motor de decisão que cruza **Taxa de Retenção**, **Sentimento (Feedback)**, **Perfil Socioeconômico Dominante** e **Geolocalização (CEP)** para recomendar campanhas acionáveis."
)

# Classificação de cada cliente da amostra em Buckets de Ação de CRM
def classify_crm_bucket(row):
    if row["Retido_Bin"] == 1 and row["Feedback_Pos_Bin"] == 0:
        return "⚠️ Retido em Risco (Ativo c/ Feedback Negativo)"
    elif row["Retido_Bin"] == 0 and row["Feedback_Pos_Bin"] == 1:
        return "🎟️ Reativação por Preço/Hábito (Churn c/ Feedback Positivo)"
    elif row["Retido_Bin"] == 0 and row["Feedback_Pos_Bin"] == 0:
        return "🚨 Recuperação Crítica (Churn c/ Feedback Negativo)"
    elif row["Tipo de Cliente"] == "Novo" and row["Retido_Bin"] == 1:
        return "🌱 Onboarding 2ª Compra (Novo Ativo)"
    else:
        return "🌟 Promotor Fidelizado (Ativo c/ Feedback Positivo)"


df["Bucket_CRM"] = df.apply(classify_crm_bucket, axis=1)

qtd_risco_ativo = int((df["Bucket_CRM"] == "⚠️ Retido em Risco (Ativo c/ Feedback Negativo)").sum())
qtd_reativacao_preco = int(
    (df["Bucket_CRM"] == "🎟️ Reativação por Preço/Hábito (Churn c/ Feedback Positivo)").sum()
)
qtd_churn_critico = int(
    (df["Bucket_CRM"] == "🚨 Recuperação Crítica (Churn c/ Feedback Negativo)").sum()
)
qtd_onboarding = int((df["Bucket_CRM"] == "🌱 Onboarding 2ª Compra (Novo Ativo)").sum())
qtd_promotores = int(
    (df["Bucket_CRM"] == "🌟 Promotor Fidelizado (Ativo c/ Feedback Positivo)").sum()
)

# 1) Alerta Principal Combinado (Retenção × Sentimento)
if taxa_retencao > 75 and feedback_pos_rate >= 80:
    st.success(
        f"✅ **Análise Saudável (Retenção: {taxa_retencao:.1f}% | Sentimento Positivo: {feedback_pos_rate:.1f}%):** "
        f"O perfil selecionado apresenta forte fidelização ({qtd_promotores} clientes promotores). "
        f"Mesmo neste cenário saudável, o Agente identificou **{qtd_risco_ativo} cliente(s) ativo(s) em risco** (com feedback negativo) "
        f"e **{qtd_reativacao_preco} cliente(s) inativo(s) com avaliação positiva** que podem ser recuperados via cupom."
    )
elif taxa_retencao > 75 and feedback_pos_rate < 80:
    st.warning(
        f"⚠️ **Alerta Preventivo de Erosão (Retenção: {taxa_retencao:.1f}%, mas Sentimento Positivo caiu para {feedback_pos_rate:.1f}%):** "
        f"Os clientes ainda estão comprando, porém o índice de reclamações está elevado ({qtd_risco_ativo} ativos insatisfeitos). "
        f"**Ação de CRM:** Enviar voucher de pedido de desculpas (*Service Recovery*) antes que migrem para a concorrência."
    )
elif taxa_retencao > 50:
    st.warning(
        f"⚠️ **Atenção — Ação de CRM Requerida (Retenção Mediana: {taxa_retencao:.1f}% | Sentimento Positivo: {feedback_pos_rate:.1f}%):** "
        f"Sugestão: Disparar cupons de desconto focados nos **{qtd_reativacao_preco} clientes em churn por preço/hábito** "
        f"e acionar campanha de recuperação para os **{qtd_churn_critico} detratores inativos**."
    )
else:
    st.error(
        f"🚨 **Alerta Crítico de Churn (Retenção: {taxa_retencao:.1f}% | Feedback Negativo: {feedback_neg_rate:.1f}%):** "
        f"Risco severo de perda no segmento selecionado ({qtd_churn_critico + qtd_reativacao_preco} clientes perdidos). "
        f"O feedback e o tempo de entrega nos CEPs críticos devem ser revistos imediatamente antes de escalar gastos promocionais."
    )

# Identificação do Perfil Dominante na Amostra Filtrada para Personalização da Oferta
ocupacao_dom = df["Ocupação"].mode().iloc[0] if not df["Ocupação"].mode().empty else "Geral"
renda_dom = df["Renda Mensal"].mode().iloc[0] if not df["Renda Mensal"].mode().empty else "Geral"
estado_civil_dom = (
    df["Estado Matrimonial"].mode().iloc[0]
    if not df["Estado Matrimonial"].mode().empty
    else "Geral"
)

if ocupacao_dom == "Estudante" or renda_dom in ["Sem Renda", "Até Rs. 10.000"]:
    oferta_recomendada = "🎓 Cupom Pocket / Cashback Universitário + Frete Grátis"
    codigo_cupom = "UNI15FREE"
    racional_oferta = (
        "Perfil com alta frequência de pedidos e forte sensibilidade a taxa de entrega. "
        "Combos individuais econômicos e isenção de frete maximizam a conversão sem exigir descontos altos no prato."
    )
elif familia_media >= 4.0 or estado_civil_dom == "Casado(a)":
    oferta_recomendada = "👨‍👩‍👧‍👦 Combo Família Fim de Semana (Desconto Progressivo)"
    codigo_cupom = "FAMILIA20"
    racional_oferta = (
        f"Tamanho médio familiar de {familia_media:.1f} pessoas ({estado_civil_dom}). "
        "Ofertas em porções compartilhadas aumentam o ticket médio e blindam a recorrência nas sextas e domingos."
    )
elif renda_dom in ["Rs. 25.001 a 50.000", "Acima de Rs. 50.000"]:
    oferta_recomendada = "⚡ Upgrade Entrega Prioritária (VIP Express) + Mimos Gastronômicos"
    codigo_cupom = "VIPEXPRESS"
    racional_oferta = (
        f"Público de maior poder aquisitivo ({renda_dom}) onde o churn é fortemente correlacionado à qualidade/atraso (Feedback Negativo) e não ao preço. "
        "Prioridade logística converte mais que desconto direto."
    )
else:
    oferta_recomendada = "🎟️ Cupom de Reengajamento Progressivo (Leve 3, Ganhe 1)"
    codigo_cupom = "VOLTA15"
    racional_oferta = (
        "Campanha de estímulo ao hábito para elevar clientes Regulares ao estágio Frequente."
    )

# CEPs (Pin codes) mais críticos na seleção atual
cep_critico_df = (
    df.groupby("Pin code", observed=False)
    .agg(
        Total=("Age", "count"),
        Churn_Count=("Retido_Bin", lambda x: int((x == 0).sum())),
        Taxa_Churn=("Retido_Bin", lambda x: round((1 - x.mean()) * 100, 1)),
        Feedback_Neg_Pct=("Feedback_Pos_Bin", lambda x: round((1 - x.mean()) * 100, 1)),
    )
    .reset_index()
)
cep_critico_df = cep_critico_df[cep_critico_df["Churn_Count"] > 0].sort_values(
    by=["Churn_Count", "Taxa_Churn"], ascending=False
)

col_crm1, col_crm2, col_crm3 = st.columns(3)

with col_crm1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">🎯 Oferta Personalizada para o Perfil</div>
            <div style="font-size: 1.08rem; font-weight: 700; color: #f97316; margin: 0.35rem 0;">
                {oferta_recomendada}
            </div>
            <div class="kpi-sub" style="margin-bottom: 0.45rem;">
                <span class="badge-neutral">Cupom Sugerido: {codigo_cupom}</span>
                &nbsp;<span class="badge-pos">Perfil: {ocupacao_dom}</span>
            </div>
            <div style="font-size: 0.84rem; color: #64748b; line-height: 1.4;">
                {racional_oferta}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_crm2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">🧭 Diagnóstico de Causa-Raiz (Churn × Feedback)</div>
            <div style="font-size: 0.92rem; margin-top: 0.4rem; line-height: 1.65;">
                • <strong>Reativação por Preço/Hábito:</strong> <span class="badge-neutral">{qtd_reativacao_preco} clientes</span> <small>(Gostaram, mas pararam de pedir)</small><br>
                • <strong>Retidos em Risco Iminente:</strong> <span class="badge-neg">{qtd_risco_ativo} clientes</span> <small>(Ativos c/ avaliação negativa)</small><br>
                • <strong>Churn por Experiência Ruim:</strong> <span class="badge-neg">{qtd_churn_critico} clientes</span> <small>(Inativos c/ avaliação negativa)</small><br>
                • <strong>Onboarding (2ª Compra):</strong> <span class="badge-pos">{qtd_onboarding} novos</span> | <strong>VIPs:</strong> <span class="badge-pos">{qtd_promotores}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_crm3:
    if not cep_critico_df.empty:
        top_ceps_html = "".join(
            [
                f"<li><strong>CEP {int(r['Pin code'])}:</strong> {int(r['Churn_Count'])} em churn "
                f"({r['Taxa_Churn']:.0f}% churn | {r['Feedback_Neg_Pct']:.0f}% feed. neg.)</li>"
                for _, r in cep_critico_df.head(3).iterrows()
            ]
        )
    else:
        top_ceps_html = "<li>Nenhum CEP com churn registrado no filtro atual.</li>"

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">📍 CEPs Prioritários para Auditoria & Ação</div>
            <div style="font-size: 0.9rem; font-weight: 600; margin: 0.35rem 0; color: #ef4444;">
                Concentração Geográfica de Perda (Top 3)
            </div>
            <ul style="font-size: 0.84rem; color: #64748b; padding-left: 1.15rem; margin-bottom: 0; line-height: 1.55;">
                {top_ceps_html}
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

with st.expander("📬 Fila de Disparo Inteligente de CRM — Selecionar Público-Alvo e Exportar Campanha", expanded=True):
    bucket_options = [
        "🎟️ Reativação por Preço/Hábito (Churn c/ Feedback Positivo)",
        "⚠️ Retido em Risco (Ativo c/ Feedback Negativo)",
        "🚨 Recuperação Crítica (Churn c/ Feedback Negativo)",
        "🌱 Onboarding 2ª Compra (Novo Ativo)",
        "🌟 Promotor Fidelizado (Ativo c/ Feedback Positivo)",
    ]
    selected_bucket = st.selectbox(
        "Selecione o grupo de clientes diagnosticado pelo Agente para visualizar e exportar a lista de disparo:",
        options=bucket_options,
        index=0,
    )

    acao_por_bucket = {
        "🎟️ Reativação por Preço/Hábito (Churn c/ Feedback Positivo)": (
            f"Enviar push/WhatsApp com o cupom **{codigo_cupom}** (15% OFF + Frete Grátis). "
            "Como o feedback anterior foi positivo, a chance de reconversão imediata é alta."
        ),
        "⚠️ Retido em Risco (Ativo c/ Feedback Negativo)": (
            "Disparar mensagem proativa de *Customer Success* com voucher de cortesia na próxima entrega e prioridade logística, evitando o cancelamento."
        ),
        "🚨 Recuperação Crítica (Churn c/ Feedback Negativo)": (
            "Auditar os restaurantes/entregadores do CEP correspondente e enviar pedido formal de desculpas com cupom de recuperação de 25% OFF."
        ),
        "🌱 Onboarding 2ª Compra (Novo Ativo)": (
            "Enviar régua de boas-vindas com benefício progressivo para o 2º e 3º pedidos em até 7 dias."
        ),
        "🌟 Promotor Fidelizado (Ativo c/ Feedback Positivo)": (
            "Não queimar margem com descontos agressivos: convidar para programa *Indique e Ganhe* ou Clube de Assinatura VIP."
        ),
    }

    df_target = df[df["Bucket_CRM"] == selected_bucket].copy()
    st.info(
        f"💡 **Plano de Ação para este Grupo ({len(df_target)} clientes encontrados):** {acao_por_bucket[selected_bucket]}"
    )

    if not df_target.empty:
        cols_crm_export = [
            "Bucket_CRM",
            "Age",
            "Gênero",
            "Estado Matrimonial",
            "Ocupação",
            "Renda Mensal",
            "Family size",
            "Tipo de Cliente",
            "Status de Retenção",
            "Sentimento (Feedback)",
            "Pin code",
        ]
        st.dataframe(
            df_target[cols_crm_export].rename(
                columns={
                    "Bucket_CRM": "Segmento de Ação CRM",
                    "Age": "Idade",
                    "Family size": "Tam. Família",
                    "Pin code": "CEP",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )
        csv_crm = df_target[cols_crm_export].to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label=f"📥 Exportar Lista de Disparo ({len(df_target)} clientes) — CSV",
            data=csv_crm,
            file_name="lista_disparo_agente_crm.csv",
            mime="text/csv",
        )
    else:
        st.caption("Nenhum cliente se enquadra neste grupo para a combinação atual de filtros.")


