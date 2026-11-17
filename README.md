# 🍔 Inteligência Comportamental de Clientes — Online Food Delivery

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Altair](https://img.shields.io/badge/Vega--Altair-F97316?style=for-the-badge&logo=vega&logoColor=white)
![Status](https://img.shields.io/badge/Status-Concluído-10B981?style=for-the-badge)

> **Dashboard executivo e motor de Triagem Inteligente de CRM** desenvolvido em Python com Streamlit para análise de retenção, sentimento (*Feedback Rate*), geolocalização de pedidos e segmentação multidimensional de clientes de plataformas de entrega de comida online.

---

## 📌 1. Visão Geral e Problema de Negócio

Plataformas de *Food Delivery* operam em mercados de alta competitividade, onde o Custo de Aquisição de Clientes (CAC) exige **forte retenção (recompra)** e **gestão ativa da experiência do usuário**.

Este projeto transforma a base de dados **`online food delivery dataset.csv`** (388 registros de clientes na região metropolitana de Bangalore) em uma aplicação analítica e acionável de **Business Intelligence & Growth CRM**, respondendo a perguntas críticas de negócio:

1. **Qual é a real Taxa de Retenção da plataforma e quem são os clientes fiéis vs. em risco de churn?**
2. **Qual o impacto direto de uma avaliação negativa (*Feedback Rate*) no cancelamento do cliente?**
3. **Como o comportamento de compra varia por Renda Mensal, Ocupação, Idade, Sexo e Estado Matrimonial?**
4. **Quais ações de CRM (cupons de preço, *service recovery* ou programas VIP) devem ser disparadas para cada grupo de clientes e em quais CEPs auditar a operação?**

---

## 📊 2. Apresentação dos Dados e Principais Descobertas (Insights)

Durante a etapa de higienização (*Data Cleaning*), o pipeline em `app.py` remove automaticamente colunas órfãs do CSV bruto e padroniza strings com espaços residuais (como `"Negative "` na coluna `Feedback`).

| Indicador / Dimensão | Resultado na Base ($N = 388$) | Insight Estratégico |
| :--- | :--- | :--- |
| **Taxa de Retenção (`Output = Yes`)** | **77,6%** (301 retidos / 87 em churn) | Forte base ativa, porém com oportunidades claras de reativação segmentada. |
| **Clientes Recorrentes (`Regular + Frequent`)** | **93,8%** (364 clientes) | **51,3%** são clientes *Regulares*, **43,0%** *Frequentes* e **5,7%** *Novos*. |
| **Análise de Sentimento (`Feedback Rate`)** | **81,7% Positivo** vs. **18,3% Negativo** | **Net Sentiment Score (NSS)** de **+63,4** (escala de -100 a +100). |
| **Impacto Sentimento × Retenção** | **92,1%** vs. **12,7%** | Clientes com feedback positivo retêm a **92,1%**; quando o feedback é negativo, a retenção cai para **12,7%**. |
| **Perfil Demográfico Dominante** | **24,6 anos** (18 a 33 anos) | Jovens de **22 a 25 anos** representam **59,8%** da base; **69,1%** são solteiros(as). |
| **Recorte Socioeconômico** | **53,4% Estudantes** / **30,4% Empregados** | Universitários (*Sem Renda* ou *Até Rs. 10.000*) formam o maior volume e sustentam **88,8%** de retenção. |

---

## 🚀 3. Funcionalidades do Dashboard

### 🎯 Barra Lateral de Filtros Globais
Permite filtrar toda a aplicação em tempo real por:
- **Faixa de Idade** (`Slider` de 18 a 33 anos)
- **Sexo / Gênero** (*Masculino*, *Feminino*)
- **Estado Matrimonial** (*Solteiro(a)*, *Casado(a)*, *Prefere não informar*)
- **Ocupação** (*Estudante*, *Empregado*, *Autônomo*, *Dona de Casa*)
- **Renda Mensal** (ordenada de *Sem Renda* até *Acima de Rs. 50.000*)
- **Tipo de Cliente** (*Novo*, *Regular*, *Frequente*)

### 📈 Cards de KPIs Estratégicos com Comparativo (*Delta*)
Cinco cartões no topo monitoram instantaneamente a amostra filtrada e calculam a variação em pontos percentuais (`p.p.`) em relação à base total:
1. **Taxa de Retenção (`Output = Yes`)**
2. **Clientes Recorrentes (`Regular + Frequent`)**
3. **Feedback Positivo (`Sentimento`)**
4. **Net Sentiment Score (`% Positivo − % Negativo`)**
5. **Perfil Médio da Amostra (`Idade Média` & `Tamanho Médio da Família`)**

### 🗂️ Quatro Abas Analíticas Interativas
1. **👥 Segmentação Comportamental (5 Dimensões):**
   - Gráficos Vega-Altair dedicados para **Renda Mensal**, **Ocupação**, **Idade / Faixa Etária**, **Sexo** e **Estado Matrimonial**.
   - **Tabela Executiva Consolidada** com seletor dinâmico de dimensão e barras de progresso integradas.
2. **🔄 Taxa de Retenção & Fidelização:**
   - Taxa de retenção por estágio de fidelidade (*Novo*, *Regular*, *Frequente*).
   - Cruzamento de impacto do sentimento na retenção, curva etária de retenção e retenção por tamanho da família.
3. **💬 Análise de Sentimento (Feedback Rate):**
   - Gráfico de rosca de distribuição geral de sentimento.
   - Barras empilhadas 100% de sentimento por faixa de renda.
   - **Mapa de Calor (*Heatmap*)** cruzando *Ocupação × Estado Matrimonial* pela taxa de avaliações positivas.
4. **🗺️ Mapa Geográfico & Explorador de Dados:**
   - Mapa interativo (`st.map`) com geolocalização (`latitude`, `longitude`) dos pedidos.
   - Ranking **Top 10 Regiões (CEP / Pin Code)** por volume de clientes, retenção e satisfação.
   - Explorador da base filtrada com exportação em CSV (`⬇️ Baixar Dados Filtrados`).

---

## 🤖 4. Diferencial: Agente de Retenção & Triagem Inteligente de CRM

Mais do que exibir gráficos passivos, o painel conta com um **Motor de Decisão de CRM** no rodapé que elimina o "ponto cego da média" e classifica cada cliente em **5 Buckets Acionáveis**:

1. **🎟️ Reativação por Preço/Hábito (`Churn` com `Feedback Positivo`):** Clientes que gostaram da experiência, mas pararam de pedir — público de maior conversão para cupons de desconto.
2. **⚠️ Retido em Risco Iminente (`Ativo` com `Feedback Negativo`):** Clientes que ainda compram, mas estão insatisfeitos e exigem *Service Recovery* imediato antes que cancelem.
3. **🚨 Recuperação Crítica (`Churn` com `Feedback Negativo`):** Clientes perdidos por falha operacional/experiência.
4. **🌱 Onboarding 2ª Compra (`Novo` e `Ativo`):** Clientes recém-adquiridos que precisam de estímulo para criar hábito.
5. **🌟 Promotor Fidelizado (`Ativo` com `Feedback Positivo`):** Clientes VIPs ideais para programas de indicação (*Member Get Member*) e assinatura.

O Agente também entrega **3 Cards de Ação Imediata**:
- **🎯 Oferta Personalizada para o Perfil Dominante:** Sugere automaticamente a mecânica promocional e o cupom ideal conforme o público filtrado (`UNI15FREE` para estudantes, `FAMILIA20` para famílias $\ge 4$ pessoas, `VIPEXPRESS` para alta renda).
- **🧭 Diagnóstico de Causa-Raiz (Churn × Feedback):** Quantifica exatamente quantos clientes estão em cada estágio.
- **📍 CEPs Prioritários para Auditoria Logística:** Lista os 3 CEPs com maior concentração de perda e avaliações negativas no filtro atual.
- **📬 Fila de Disparo Exportável:** Permite selecionar qualquer um dos 5 grupos diagnosticados e baixar o arquivo `lista_disparo_agente_crm.csv` pronto para campanhas de WhatsApp, Push ou E-mail Marketing.

---

## 📁 5. Estrutura do Repositório

```text
📦 customer_analysis
 ┣ 📜 app.py                              # Aplicação completa do Dashboard Streamlit + Agente de CRM
 ┣ 📜 online food delivery dataset.csv    # Base de dados original (388 clientes)
 ┣ 📜 requirements.txt                    # Dependências do projeto (Streamlit, Pandas, Altair)
 ┣ 📜 .gitignore                          # Arquivos e pastas ignorados pelo Git
 ┗ 📜 README.md                           # Documentação executiva e técnica do projeto
```

---

## ⚙️ 6. Como Executar o Projeto Localmente

### Pré-requisitos
- **Python 3.10+** instalado

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/SEU-USUARIO/NOME-DO-REPOSITORIO.git
   cd NOME-DO-REPOSITORIO
   ```

2. **(Opcional) Crie e ative um ambiente virtual:**
   ```bash
   python -m venv .venv
   # No Windows (PowerShell):
   .\.venv\Scripts\Activate.ps1
   # No Linux/macOS:
   source .venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o dashboard Streamlit:**
   ```bash
   streamlit run app.py
   ```

5. Acesse no navegador em **`http://localhost:8501`**.

---

## 🌐 7. Deploy no Streamlit Community Cloud

Este repositório já está pronto para deploy gratuito com 1 clique no **[Streamlit Community Cloud](https://share.streamlit.io/)**:
1. Suba este repositório para a sua conta do **GitHub**.
2. Acesse [share.streamlit.io](https://share.streamlit.io/) e clique em **Create app**.
3. Selecione o seu repositório, a branch `main` e defina o arquivo principal como **`app.py`**.
4. Clique em **Deploy** — o Streamlit instalará automaticamente o `requirements.txt` e gerará um link público para o seu portfólio!
