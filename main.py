import streamlit as st
from PIL import Image
import login as lg
import pandas as pd
import io
import requests
import mysql.connector
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
div.stButton > button:first-child {
    background-color:  #0000cd;
    color: white;
    height:2m;
    border-radius:10px 10px 10px 10px;
    }

</style>

"""
conexao = mysql.connector.connect(
    host = 'dubaienergy.com.br',
    user ='u251704477_DubaiEnergy',
    password='@Dubai102102',
    database='u251704477_Dubai',
)

cursor = conexao.cursor()


url="https://raw.githubusercontent.com/ArturTertuliano/Teste-Serve/teste/advertising.csv"
s=requests.get(url).content
tabela = pd.read_csv(io.StringIO(s.decode('utf-8')),sep=",")

st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


col1, col2,col3 = st.columns(3)


image = Image.open('Imagens/dubai.png')

new_image = image.resize((500, 250))

col2.image(new_image)

def show_main_page():
    
    bar.title("Bem Vindo")
    lg.main()
    
    
    

def Admin():
          
    bar.title("Bem Vindo")
    col1, col2 = st.columns(2)
    lista = []
    Placa = col1.number_input ("Módulo",min_value=0)
    Op = col2.selectbox ('Opções do Módulo',['Adicionar','Remover'])
    AlterarValores1 = st.button("ADICIONAR/REMOVER")

    if AlterarValores1:
        
       



            if Op == 'Adicionar':
            
                try:
                    
                    comando = f'SELECT * FROM placas WHERE Modulo = {Placa}'
                    cursor.execute(comando)
                    resultado = cursor.fetchall()
                    st.error("Placa já cadastrada!")
                    
                except:
            
                    valor =1
                    comando = f'INSERT INTO placas (Modulo, A, B, C) VALUES ({Placa},{valor},{valor},{valor})'
                    cursor.execute(comando)
                    conexao.commit()
                    st.success("Módulo adicionado com sucesso!")

            if Op == "Remover":
                
                try:
                    
                    comando = f'DELETE FROM placas WHERE Modulo = {Placa}'
                    cursor.execute(comando)
                    conexao.commit()
                    st.success("Módulo removido com sucesso!")
                    
                except:
                    
                    st.error("Placa não está cadastrada!")
                    
    
    Tarifa = st.number_input ("Alterar tarifa",min_value=0.0)
    AlterarValores2 = st.button("ALTERAR TARIFA")

    if AlterarValores2:

        comando = f'INSERT INTO tarifa (tarifa) VALUES ({Tarifa})'
        cursor.execute(comando)
        conexao.commit()
        
        st.success("Tarifa alterada com sucesso!")

    comando = f'SELECT * FROM placas'
    cursor.execute(comando)
    resultado = cursor.fetchall()

    for i in range(len(resultado)):
        lista.append(resultado[i][1])
    
    Placa2 = st.selectbox ('Opções de Módulo',lista)
    ValorA = st.number_input ("Alterar valor A",min_value=0)
    ValorB = st.number_input ("Alterar valor B",min_value=0)
    ValorC = st.number_input ("Alterar valor C",min_value=0)
    AlterarValores3 = st.button("ALTERAR FORMULA")

    if AlterarValores3:

        comando = f'UPDATE placas SET A = {ValorA}, B = {ValorB}, C = {ValorC} WHERE Modulo = {Placa2}'
        cursor.execute(comando)
        conexao.commit()
        
            
        st.success("Formula alterada com sucesso!")

    x12 = st.number_input ("Parcela 12x",min_value=0.0)
    x24 = st.number_input ("Parcela 24x",min_value=0.0)
    x36 = st.number_input ("Parcela 36x",min_value=0.0)
    x60 = st.number_input ("Parcela 60x",min_value=0.0)
    x72 = st.number_input ("Parcela 72x",min_value=0.0)
    AlterarValores4 = st.button("ALTERAR PARCELAS")
    
    if AlterarValores4:

        comando = f'UPDATE parcelas SET x12 = {x12}, x24 = {x24}, x36 = {x36}, x60 = {x60}, x72 = {x72} WHERE idparcelas = {1}'
        cursor.execute(comando)
        conexao.commit()
        
        st.success("Parcelas alteradas com sucesso!")

    user = st.text_input ("Adicionar usuário *")
    email = st.text_input ("Adicionar email")
    nc = st.text_input ("Adicionar Nome Completo *")
    Telefone = st.text_input ("Adicionar telefone")
    passw = st.text_input ("Criar password *")
    AlterarValores5 = st.button("ADICIONAR USUÁRIO")

    if AlterarValores5:
        if user == '' or passw == '' or nc == '':
            
            st.error("Alguma informação obrigatório não foi fornecido!")
            
        else:
           
            comando = f'INSERT INTO usuario (user,email,senha,nome,telefone) VALUES ("{user}","{email}","{passw}","{nc}","{Telefone}")'
            cursor.execute(comando)
            conexao.commit()
            st.success("Usuário adicionado com sucesso!")
        
    AlterarValores6 = st.button("BUSCAR USUÁRIO")  
    
    if AlterarValores6:

        comando = f'SELECT * FROM cliente'
        cursor.execute(comando)
        resultado = cursor.fetchall()

        df = pd.DataFrame(
        resultado,
        columns=['Proposta','Nome','Estado','Cidade','Geração','Preço','Data']
        )
        st.table(df)
     
            
            
def LoggedOut_Clicked():
    if st.session_state['loggedIn']:
        
        st.session_state['loggedIn'] = False
        
    if st.session_state['key']:
        st.session_state['key'] = False
    
def show_logout_page1():

    with logOutSection1:

        st.sidebar.title("Sair da sua conta")
        st.sidebar.button ("Sair", key="logout", on_click=LoggedOut_Clicked)

def show_logout_page2():

    with logOutSection2:

        st.sidebar.title("Sair da sua conta")
        st.sidebar.button ("Sair", key="logout2", on_click=LoggedOut_Clicked)
    
def LoggedIn_Clicked(userName, password):
    try:
        comando = f'SELECT * FROM usuario WHERE user = "{userName}"'
        cursor.execute(comando)
        resultado = cursor.fetchall()
        user = resultado[0][1]
        senha = resultado[0][3]
    
     
        if userName == "admin" and password == senha:

            st.session_state['key'] = True

        if userName == user and password == senha:
            lg.a = user
            st.session_state['loggedIn'] = True

        if userName != user or password != senha:
            st.session_state['loggedIn'] = False
            st.error("Usuário ou senha inválido!")
            
    except:
        pass
          
        
def show_login_page():
    
    with loginSection:
        
        if st.session_state['loggedIn'] == False:
            with st.form("my_form3"):
                userName = st.text_input ("Usuário")
                password = st.text_input ("Senha", type="password")
                st.form_submit_button ("Entrar", on_click=LoggedIn_Clicked, args= (userName, password))
                
                
                

def finish():
    cursor.close()
    conexao.close()

headerSection = st.container()
mainSection = st.container()
loginSection = st.container()
logOutSection1 = st.container()
logOutSection2 = st.container()
CadastrarSection = st.container()


with headerSection:

    bar = st.title("Acesse sua conta")
    
    
        
    if 'key' not in st.session_state:
        st.session_state['key'] = False
    
    else:
        if st.session_state['key'] == True:
            show_logout_page2()    
            Admin()
        else:
            show_login_page()

    if 'loggedIn' not in st.session_state:
        st.session_state['loggedIn'] = False
        show_login_page()
    else:
        if st.session_state['loggedIn'] == True and st.session_state['key'] == False:
        
            show_logout_page1()    
            show_main_page()
        
tabela.to_csv(io.StringIO(s.decode('utf-8')),index = False)         
