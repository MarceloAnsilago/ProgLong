import streamlit as st
from streamlit_option_menu import option_menu
from ProgLongShort import carregar_dados_com_progresso

# Definindo a configuração da página
st.set_page_config(layout="wide", initial_sidebar_state="auto", page_title="Carregar Long & Short", page_icon="📊")

# Layout de colunas para aproveitar o espaço ampliado
col1, col2 = st.columns([1, 2])

# Parte da barra lateral
with col1:
    selecao = option_menu(
        menu_title="App",
        options=["Carregar Cotações", "Projetos", "Contatos"]
    )

# Parte do conteúdo principal
with col2:
    if selecao == "Carregar Cotações":
        st.title(f"Você Selecionou o menu {selecao}")

        # Botão "Carregar" com barra de progresso
        button_clicked = st.button("Carregar")
        progress_bar = st.progress(0)  # Inicia a barra de progresso
       

        if button_clicked:
            # Chamando a função para carregar os dados com a barra de progresso
            Portfolio = carregar_dados_com_progresso(progress_bar)

            # Exibindo o DataFrame carregado
            st.write("DataFrame carregado:")
            st.write(Portfolio)

    if selecao == "Projetos":
        st.title(f"Você Selecionou o menu {selecao}")

    if selecao == "Contatos":
        st.title(f"Você Selecionou o menu {selecao}")
