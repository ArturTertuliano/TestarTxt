import base64
import math
from datetime import datetime
import matplotlib.pyplot as plt
import numpy
import streamlit as st
from fpdf import FPDF
from PIL import Image
import pandas as pd
import mysql.connector
import main as mn




def convertImage(nomeImage): 
    img = Image.open(nomeImage) 
    img = img.convert("RGBA") 
  
    datas = img.getdata() 
  
    newData = [] 
  
    for item in datas: 
        if item[0] == 255 and item[1] == 255 and item[2] == 255: 
            newData.append((255, 255, 255, 0)) 
        else: 
            newData.append(item) 
  
    img.putdata(newData) 
    img.save(nomeImage, "PNG") 
    

def thousand_sep(num):
        return ("{:,}".format(num))

def create_download_link(val, filename):
        b64 = base64.b64encode(val)  # val looks like b'...'
        return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'

def CpfVer(Cpf):
    v = 0
    teste = []
    if Cpf != '':
        for i in range(len(Cpf)):
            teste.append(int(Cpf[i]))
        
        if sum(teste) == 33 or sum(teste) == 44 or sum(teste) == 55 or sum (teste) == 66:

            v = 1
        else:
            v = 2 
    else:
        v = 3
    return v

def main():
    try:
        
        
        conexao = mysql.connector.connect(
        host = 'dubaienergy.com.br',
        user ='u251704477_DubaiEnergy',
        password='@Dubai102102',
        database='u251704477_Dubai',
        )

        cursor = conexao.cursor()

        comando = f'SELECT * FROM tarifa'
        cursor.execute(comando)
        resultado = cursor.fetchall()

        UF = ['AC','AL','AM','AP','BA','CE','DF','ES','GO','MA','MG','MS','MT','PA','PB','PE','PI','PR','RJ','RN','RO','RR','RS','SC','SE','SP','TO']
        lista = []
        a = []
        A,B,C,D = 1.05,1,0.9,0.8
        inclinacao1 = ['A','B','C','D']
        desconto = [0,1,2,3,4,5]
        Inversor = ['Inversor','Micro Inversor']
        Estrutura = ['Sem Estrutura','Colonial','Fibrocimento','Mini Trilho','Laje','Solo','']
        TipoPessoa = ['','Juridica','Fisica']
        carencia = ['1','2','3','4','5','6']

        RendimentoSistema = 0.845
        TipoLigacao, Tarifa= ['MONOFASICO','BIFASICO','TRIFASICO'], resultado[0][1]

        comando = f'SELECT * FROM iluminacao'
        cursor.execute(comando)
        resultado = cursor.fetchall()

        ContaLuz = resultado[0][1]

        comando = f'SELECT * FROM usuario'
        cursor.execute(comando)
        resultado = cursor.fetchall()

        for i in range(2,len(resultado)):

            a.append(resultado[i][4])

        Usuario1 = st.selectbox("Selecione o vendedor *",a)
        Pessoa = st.selectbox("Selecione o tipo de pessoa *",TipoPessoa)
        Cpf = st.text_input("CPF/CNPJ")
        Nome = st.text_input("Nome do Cliente *")
        Email = st.text_input("Email")
        Telefone = st.text_input("Telefone")
        Cep = st.text_input("CEP")
        Endereco = st.text_input("Endere??o")
        Estados = st.selectbox("Selecione um Estado",UF)

        with open("Text/Cidades_Estados.txt","r", encoding = "utf-8") as arquivo:

            nome = arquivo.readlines()

        verificar = 0

        for i in nome:
            i = i[:-2]
            i = i.split(', ') 

            if Estados == i[1]:
                lista.append(i[2])
                verificar = 1
                continue
            elif verificar == 0:
                continue

            if verificar == 1:
                break

        Cidade = st.selectbox("Selecione uma Cidade",lista)

        comando = f'SELECT * FROM placas'
        cursor.execute(comando)
        resultado = cursor.fetchall()
        fa = []
        for i in range(len(resultado)):
            fa.append(resultado[i][1])

        Potencia = st.selectbox("Selecione um M??dulo",fa)
        inclinacao = st.selectbox("Inclina????o adequada",inclinacao1)
        TipoLigacao1 = st.selectbox("Tipo de liga????o",TipoLigacao)
        ConsumoMensal = st.text_input("Digite o consumo mensal (kWh) *")
        Porcentagem = st.text_input("Digite a porcentagem desejada *")
        Estrutura1 = st.selectbox("Selecione uma estrutura",Estrutura)
        Inversor1 = st.selectbox("Selecione um inversor",Inversor)
        carencia1 = st.selectbox("Car??ncia (M??s)",carencia)
        desconto1 = st.selectbox("Desconto %",desconto)

        export_as_pdf = st.button("Gerar PDF")
        
        if inclinacao == 'A':
            RendimentoSistema = RendimentoSistema * A
        elif inclinacao == 'B':
            RendimentoSistema = RendimentoSistema * B
        elif inclinacao == 'C':
            RendimentoSistema = RendimentoSistema * C
        elif inclinacao == 'D':
            RendimentoSistema = RendimentoSistema * D
        if export_as_pdf:
        

            Verificarcpf = CpfVer(Cpf)
            if Verificarcpf == 1 or Verificarcpf == 3:
                if Pessoa != '' and Nome !='' and ConsumoMensal != '' and Porcentagem != '': 

                    bar = st.progress(0)

                    Digite = Estados+", "+ Cidade
                    lista1 = Digite.split(', ')
                    if TipoLigacao1 == 'MONOFASICO':
                        TipoLigacao1 = 30
                    elif TipoLigacao1 == 'BIFASICO':
                        TipoLigacao1 = 50
                    elif TipoLigacao1 == 'TRIFASICO':
                        TipoLigacao1 = 100
                    PotenciaPlaca = float(Potencia)
                    ConsumoMedio = float(ConsumoMensal)
                    PorcentagemEnergia = (float(Porcentagem)+100)/100

                    #Salvando os valores da latitude e longitude da cidade desejada
                    for i in nome:
                        i = i[:-2]
                        i = i.split(', ')     

                        if lista1[0] == i[1]:

                            if lista1[1] == i[2]:
                                Latitude = float(i[3])
                                Longitude = float(i[4])
                                break



                    #Calculo para poder converter os valores de latitude e longitudo ao modelo da tabela de irradia????o
                    b = Latitude - round(Latitude,1)
                    b = round(b*10,1)

                    if b == 0.5:

                        b = round(Latitude + 0.01,2)
                        Latitude = round(b,1)

                    else:

                        Latitude = round(Latitude,1)+round(b)

                    d = round(Longitude,1)

                    if((d-Longitude) < 0):
                        Longitude = round(d + 0.05,2)
                    else:
                        Longitude = round(d - 0.05,2)




                    #Verificar e abrir arquivo da tabela de irradia????o
                    with open("Text/TabelaIrradiacaoPYTHON.txt","r", encoding = "utf-8") as arquivo:

                        Radiacao = arquivo.readlines()


                    #Verificando os dados da cidades com a da tabela irradia????o e salvando seus dados
                    for i in Radiacao:

                        Table = i.split(" ", 15)
                        for i in range(16):

                            Table[i] = float(Table[i])

                        if Table[1] == Latitude and Table[2] == Longitude:

                            break



                    #Calculos para saber quantas placas s??o nescessarias
                    HSPDia = 0
                    for i in range(12):

                        HSPDia = (HSPDia + Table[i + 4])

                    HSPDia = float(round((HSPDia/12)/1000,1))
                    HSPMes = float(HSPDia * 30)
                    HSPAno = float(round(HSPMes * 12))

                    ConsumoDia = float(ConsumoMedio / 30)
                    QtdPlacas = math.ceil((((ConsumoDia * PorcentagemEnergia)/(HSPDia * RendimentoSistema))* 1000)/PotenciaPlaca)
                    if QtdPlacas < 4 and Inversor1 == 'Micro Inversor':
                        QtdPlacas = 4
                    if QtdPlacas < 5 and Inversor1 == 'Inversor':
                        QtdPlacas = 5
                    potenciaFotovoltaica = (QtdPlacas * PotenciaPlaca) / 1000

                    ConsumoAno = float(ConsumoMedio * 12)

                    #(HSPAno)
                    RelacaoConsumo = round(((PotenciaPlaca * QtdPlacas * 0.845)/1000) * HSPAno)

                    PorcentReal = round((RelacaoConsumo / ConsumoAno)* 100, 2)

                    bar.progress(10)

                    if Estrutura1 == "Solo":
                        if Inversor1 == 'Inversor':
                            for i in range(len(fa)):
                                if fa[i] == PotenciaPlaca:
                                    x1 = resultado[i][2]
                                    x2 = resultado[i][3]
                                    x3 = resultado[i][4]
                                    break

                            CapitalInicial = (round(-1*(1.15*(((x1 * QtdPlacas) + x2) / x3))))
                            CapitalFixo = -1 * CapitalInicial
                        else:
                            tabela2 = pd.read_csv("advertising2.csv",sep=",")
                            x1 = tabela2['micro'][0]
                            x2 = tabela2['micro'][1]
                            x3 = tabela2['micro'][2]
                            CapitalInicial = (round(-1*(1.15*(((x1 * QtdPlacas) + x2) / x3))))
                            CapitalFixo = -1 * CapitalInicial
                    else:
                        if Inversor1 == 'Inversor':
                            for i in range(len(fa)):
                                if fa[i] == PotenciaPlaca:
                                    x1 = resultado[i][2]
                                    x2 = resultado[i][3]
                                    x3 = resultado[i][4]
                                    break
                            CapitalInicial = (round(-1*(((x1 * QtdPlacas) + x2) / x3)))
                            CapitalFixo = -1 * CapitalInicial

                        else:

                            tabela2 = pd.read_csv("advertising2.csv",sep=",")
                            x1 = tabela2['micro'][0]
                            x2 = tabela2['micro'][1]
                            x3 = tabela2['micro'][2]

                            CapitalInicial = (round(-1*((((x1 * QtdPlacas) + x2) / x3))))
                            CapitalFixo = -1 * CapitalInicial

                    Capital = format(CapitalInicial* -1,',d')
                    if desconto1 != 0:
                        desconto2 = (CapitalFixo*desconto1)/100
                    SimulacaoC = list(Table)

                    MediaSimulacao = 0
                    for i in range(12):

                        SimulacaoC[i] =  round((potenciaFotovoltaica * RendimentoSistema * Table[i+4] * 30) / 1000)
                        MediaSimulacao = float(MediaSimulacao + SimulacaoC[i])

                    MediaSimulacao =  MediaSimulacao / 12
                    MediaSimulacao = Tarifa * MediaSimulacao

                    for i in range(4):
                        del(SimulacaoC[12])

                    teste = []


                    for i in range(1,13):
                        teste.append(i)

                    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

                    plt.figure(dpi=150)
                    ax = plt.axes()
                    ax.set_facecolor("#fff99980")

                    ax1 = plt.gca()
                    ax1.set_frame_on(False)


                    largura = 0.35
                    r1 = numpy.arange(len(meses))

                    plt.bar((r1+1) + largura/2,SimulacaoC,largura,color = "deepskyblue",label ="Gera????o SFV Previsto (kWh)")
                    plt.bar((r1+1) - largura/2,ConsumoMedio,largura,color = "darkblue",label = "Hist??rico de Consumo (kWh)")

                    plt.legend(loc='upper left',frameon=False)
                    for i in range(len(meses)):
                        plt.text(i+1,SimulacaoC[i]+(ConsumoMedio/20),SimulacaoC[i],rotation=90,fontsize=9)
                        plt.text(i+0.6,ConsumoMedio+(ConsumoMedio/20),round(ConsumoMedio),rotation=90,fontsize=9)
                    plt.ylim(0,(max(SimulacaoC)/1.2)+ConsumoMedio)
                    plt.xticks(r1+1, meses)
                    plt.setp( ax.get_yticklabels(), visible=False)
                    nomeImage = 'Imagens/teste.png'
                    plt.savefig(nomeImage, format='png')
                    convertImage(nomeImage) 


                    #Calculos para gerar a mn.tabela de valores em real, no pdf q o excel gera o nome da mn.tabela ?? 'mn.tabela anal??tica da amortiza????o e retorno do investimento'
                    #O nome das variaveis est??o com o mesmo nome do pdf, ent??o ?? s?? vericar o pdf q d?? pra identificar oq esta retornando

                    TarifaCal, Entrou, EconomiaEnergia, ValorizacaCapital, Geracao = Tarifa, 0, 0, CapitalInicial, RelacaoConsumo
                    K = 90
                    J = 400

                    comando = f'SELECT * FROM usuario WHERE user = "{Usuario1}"'
                    cursor.execute(comando)
                    resultado = cursor.fetchall()
                    vendedor = resultado[0][4]

                    #proposta = '20'
                    uf = Digite.split(',')
                    data = datetime.now()
                    pdf = FPDF()



                    mult = numpy.zeros((27, 7))
                    var = []
                    car = []
                    ber = []
                    for i in range(1,26):
                        var.append(i)

                    bar.progress(20)
                    print(20)
                    mult[1][0] = Geracao
                    mult[1][1] = TarifaCal
                    mult[1][5] = EconomiaEnergia
                    mult[1][6] = ValorizacaCapital

                    for i in range(1,26):


                        if i > 0:   
                            IluminPublic = round(ContaLuz * 12, 2)
                            ConsumoMinimo = round(TipoLigacao1 * 12,2)
                            #PagaAno = round(IluminPublic + (ConsumoMinimo * TarifaCal),2)
                            mult[i][2] = round(IluminPublic + (ConsumoMinimo * mult[i][1]),2)

                            EconoAno = round(RelacaoConsumo * mult[i][1],2)


                            #FluxoCaixa = round(EconoAno - PagaAno,2)
                            mult[i][3] = round(EconoAno - mult[i][2],2)

                            #SaldoFuxoCaixa = round(CapitalInicial + FluxoCaixa)
                            mult[i][4] = round(CapitalInicial + mult[i][3])
                            #EconomiaEnergia = round(EconomiaEnergia + EconoAno)

                            mult[i][5] = round(mult[i][5] + EconoAno)
                            #ValorizacaCapital = round(ValorizacaCapital * (1 + 0.02))

                            mult[i][6] = round(mult[i][6] * (1 + 0.02))

                            if mult[i][4] > 0 and Entrou == 0:

                                PayBackAno = i - 1
                                PayBackMes = -1 * (round((SaldoAnterior / mult[i][3]) * 12))
                                Entrou = 1



                            mult[i+1][1] = round((mult[i][1] * 108) / 100,2)
                            car.append(mult[i][5])
                            ber.append(mult[i][4])
                            mult[i+1][0] = round(RelacaoConsumo * (1 - 0.01),2)
                            mult[i+1][5] = round(mult[i][5])
                            mult[i+1][6] = round(mult[i][6])
                            RelacaoConsumo = round(mult[i+1][0])
                            CapitalInicial = round(mult[i][4])
                            SaldoAnterior = round(mult[i][4])



                    bar.progress(30)

                    pdf.add_page()

                    pdf.image("Imagens/inicio.jpg",5,0,w=200)

                    pdf.add_page()

                    pdf.image("Imagens/fundoPDF.jpg",0,0,w=230)

                    pdf.set_text_color(255,255,255)
                    nomeImage = "Imagens/fundo.png"
                    pdf.image("Imagens/teste.png",5,185,w=200,h=100)
                    pdf.image(nomeImage,15,10,w=180,h=55)
                    pdf.image(nomeImage,15,140,w=150,h=30)
                    pdf.image("Imagens/fundo-cinza.png",15,147,w=150,h=30)
                    pdf.set_font('Times','B',size=12)
                    pdf.cell(190,10,'DUBAI ENERGY, PROPOSTA COMERCIAL PRELIMINAR PARA',ln=1,align='C')
                    pdf.cell(190,15,'INSTALA????O DE SISTEMA DE ENERGIA FOTOVOLTAICA',ln=1,align='C')

                    pdf.set_font('arial',size=10)
                    pdf.text(20, 145,txt='Detalhes do Projeto')
                    pdf.text(20,40,txt= Nome)
                    pdf.text(20,45,txt= str(Cep) +' ' +uf[1]+' - '+uf[0])
                    pdf.text(20,50,txt= Endereco)
                    pdf.text(20,55, txt ='Representante Comercial: '+vendedor)
                    pdf.text(20,60, txt='Telefone para contato: '+str(Telefone))
                    #pdf.text(150,50, txt='Proposta: '+proposta)
                    pdf.text(140,40, txt='Data: '+str(data.day)+' / '+str(data.month)+' / '+str(data.year))
                    pdf.text(140,45, txt='Validade da Proposta: 10 Dias')

                    pdf.set_text_color(0,0,0)

                    pdf.set_xy(15,85)
                    pdf.multi_cell(175,5,'A Energia solar fotovoltaica ?? a energia el??trica produzida a partir da luz solar. Quanto maior a radia????o solar nas placas solares e inclina????o adequada, maior ser?? a quantidade de energia el??trica produzida. A energia solar ?? considerada uma fonte de energia alternativa, renov??vel, limpa e sustent??vel. Depois de hidr??ulica e e??lica, a Energia fotovoltaica ?? terceira mais importante fonte de energia renov??vel em termos de capacidade instalada a n??vel mundial, mais de 100 pa??ses utilizam essa energia.')

                    pdf.set_xy(15,125)
                    pdf.multi_cell(175,5,'De acordo com o levantamento de vossas informa????es temos a seguintes informa????o de consumo e produ????o mensal necess??ria e consequentemente o valor em real desta produ????o:')



                    pdf.text(20,153,txt='Consumo m??dia m??s (kWh):     '+str(round(ConsumoMedio)))
                    pdf.text(20,158,txt='Produ????o m??dia m??s (kWh):    '+ str(round((ConsumoMedio * PorcentReal)/100))) 
                    pdf.text(20,163, txt= 'Rela????o Gera????o vs Consumo:    '+str(round(PorcentReal))+'%') 
                    pdf.text(20,168,txt='Pot??ncia Instalada do Projeto (kWp):    '+ str(potenciaFotovoltaica).replace(',','.'))
                    pdf.text(20,173,txt='Quantidade de M??dulos Fotovoltaico:    '+str(QtdPlacas)) 
                    pdf.text(120,153,txt= 'Tarifa(kWh):  R$ '+str(Tarifa).replace('.',',')) 
                    pdf.text(120,158, txt='Ilumina????o P??b.: R$ '+str(thousand_sep(round(ContaLuz))).replace(',','.')+',00')

                    pdf.set_font('Times','B',size=12)

                    pdf.text(15,75,txt='PANORAMA ENERG??TICO')
                    pdf.text(15, 185,txt=' ESTIMATIVA DE GERA????O VS CONSUMO')
                    pdf.text(15,120,txt= '1 - CEN??RIO DE CONSUMO/DIMENSIONAMENTO')




                    bar.progress(40)


                    pdf.add_page()

                    pdf.image("Imagens/fundoPDF.jpg",0,0,w=230)
                    largura = 0.35

                    plt.figure(dpi=150)
                    ax = plt.axes()
                    ax.set_facecolor("#FFFFFF")

                    ax1 = plt.gca()
                    ax1.set_frame_on(False)

                    r1 = numpy.arange(len(car))
                    Cap = numpy.arange(len(car))

                    Cap[0] = CapitalFixo
                    Cap[1] = round(CapitalFixo*1.04)
                    for i in range(2,25):
                        Cap[i] = Cap[i-1]*1.04

                    plt.bar((r1+1) - largura/2,car,largura,color = "deepskyblue",label ="Economia de Energia El??trica (R$)")
                    plt.bar((r1+1) + largura/2,Cap,largura,color = "darkblue",label = "Valoriza????o do Capital Invest. a TMA (R$)")
                    plt.xticks(var)

                    for i in range(len(var)):
                        esse = str(thousand_sep(round(car[i]))).replace(',','.')+',00'
                        plt.text(var[i]-0.6, car[i]+(max(car)/20), esse,rotation=90,fontsize=8)
                    plt.ylim(0,max(car)+(max(car)/2))
                    plt.setp( ax.get_yticklabels(), visible=False)
                    plt.legend(loc='upper left',frameon=False)
                    nomeImage = 'Imagens/teste2.png'
                    plt.savefig(nomeImage, format='png')
                    convertImage(nomeImage) 
                    pdf.image("Imagens/teste2.png",5,175,w=200,h=100)
                    pdf.image("Imagens/fundo.png",15,50,w=180,h=65)
                    pdf.image("Imagens/fundo-cinza.png",15,60,w=180,h=60)


                    pdf.set_font('Times','B',size=12)
                    pdf.text(15,15,txt='2 - COMPOSI????O DO SISTEMA/AN??LISE FINANCEIRA')

                    pdf.text(15,25,txt='2.1 - COMPOSI????O DO SISTEMA')
                    pdf.text(15,140,txt='2.2 - AN??LISE FINANCEIRA')
                    pdf.text(15,175,txt= 'GR??FICO COMPARATIVO DE INVESTIMENTOS AO ANO')

                    pdf.set_font('arial',size=10)
                    pdf.set_xy(15,35)
                    pdf.multi_cell(175,5, 'Na tabela abaixo ?? apresentata a composi????o do sistema e seus respectivos custos e formas de pagamento:',border = 0)

                    CC = QtdPlacas * 2
                    CA = math.ceil((QtdPlacas * 1)/3)

                    pdf.set_text_color(255,255,255)
                    pdf.set_font('arial',size=8)

                    pdf.text(20,57,txt= 'Descri????o do Item')
                    pdf.text(100,57, txt='Qtde')
                    pdf.text(125,57,txt= 'Valor Unit.')
                    pdf.text(165,57, txt='Sub Total Form. Pag.')
                    pdf.set_text_color(0,0,0)
                    l = 65
                    for i in range(9):
                        pdf.text(125,l, txt='Incluso R$.')
                        pdf.text(165,l, txt='- Financiado')
                        l += 5

                    pdf.text(20,65,txt= 'M??dulos Fotovoltaicos ('+str(round(PotenciaPlaca))+'W):')
                    if Inversor1 == 'Micro Inversor':
                        pdf.text(20,70,txt= 'Micro Inversor com 12 anos de Garantia')
                        pdf.text(100,70, str(math.ceil(QtdPlacas/4)))
                    else:

                        pdf.text(20,70,txt= 'Inversor Growatt com 10 anos de Garantia')
                        pdf.text(100,70, txt='1')
                    if Estrutura1 == 'Sem Estrutura':
                        pdf.text(20,75, txt= Estrutura1)
                    else:
                        pdf.text(20,75, txt='Estrutura '+Estrutura1)
                    pdf.text(20,80,txt= 'Cabo CC')
                    pdf.text(20,85,txt= 'Cabo CA')
                    pdf.text(20,90,txt= 'Kit Conectores e dispositivo de prote????o')
                    pdf.text(20,95,txt= 'Servi??o de Instala????o')
                    pdf.text(20,100,txt= 'Projeto T??cnico')
                    pdf.text(20,105,txt= 'Vistoria')
                    pdf.text(20,115,txt= 'Total Projeto')


                    pdf.text(100,65,txt = str(QtdPlacas))

                    pdf.text(100,75, txt='1')
                    pdf.text(100,80,txt = str(CC))
                    pdf.text(100,85,txt = str(CA))
                    pdf.text(100,90,txt = '1')
                    pdf.text(100,95, txt= '1')
                    pdf.text(100,100,txt= '1')
                    pdf.text(100,105,txt= '1')



                    pdf.text(165,115,txt= 'R$' + str(Capital).replace(',','.')+',00')

                    pdf.set_text_color(255,0,0)
                    pdf.set_xy(20,120)
                    pdf.multi_cell(170,5, 'A gera????o pretendida poder?? sofrer altera????es considerando a inclina????o do telhado e poss??veis sombreamentos. Os m??dulos nessa proposta possuem efici??ncia de 2,31 % em transforma????o de energia luminosa em engergia el??trica.',border = 0)
                    pdf.set_text_color(0,0,0)
                    pdf.set_font('arial',size=7)
                    pdf.text(150,128,txt= 'Valor total:  R$ '+ str(Capital).replace(',','.')+',00')
                    if desconto1 != 0:
                        pdf.text(150,131,txt= 'Desconto:  R$ ')
                        pdf.set_text_color(255,0,0)
                        pdf.text(168,131,txt= str(thousand_sep(round(desconto2))).replace(',','.')+',00')
                        pdf.set_text_color(0,0,0)
                        pdf.text(150,134,txt= 'Valor final:  R$ '+str(thousand_sep(round(CapitalFixo-desconto2))).replace(',','.')+',00')
                    pdf.set_font('arial',size=10)



                    pdf.set_text_color(0,0,0)
                    pdf.set_xy(15,150)
                    pdf.multi_cell(175,5, 'H?? dois indicadores no gr??fico abaixo. O primeiro corresponde a economia anual com energia el??trica com o sistema fotovoltaico. O segundo indicador, corresponde a valoriza????o do capital investido no sistema fotovoltaico, se aplicado a um investimento banc??rio ?? uma taxa m??nima de atratividade (TMA).',border = 0)



                    bar.progress(50)


                    pdf.add_page()



                    pdf.image("Imagens/fundoPDF.jpg",0,0,w=230)
                    plt.figure(dpi=150)
                    ax = plt.axes()
                    ax.set_facecolor("#FFFFFF")

                    ax1 = plt.gca()
                    ax1.set_frame_on(False)

                    plt.bar(var,ber,color = "deepskyblue")

                    for i in range(len(var)):
                        esse = str(thousand_sep(round(ber[i]))).replace(',','.')+',00'
                        if ber[i] <= 0:
                            plt.text(var[i]-0.4, ber[i]+(max(ber)/10), esse,rotation=90,fontsize=8, color='red')
                        else:
                            plt.text(var[i]-0.4, ber[i]+(max(ber)/20), esse,rotation=90,fontsize=8)
                    plt.ylim(min(ber),max(ber)+(max(ber)/2))
                    plt.legend(["Saldo do Fluxo de Caixa (R$)"],loc='upper left',frameon=False) 
                    plt.setp( ax.get_yticklabels(), visible=False)
                    plt.xticks(var)
                    nomeImage = 'Imagens/teste3.png'
                    plt.savefig(nomeImage, format='png')
                    convertImage(nomeImage) 


                    pdf.image("Imagens/teste3.png",5,35,w=200,h=100)
                    pdf.image("Imagens/fundo.png",15,180,w=180,h=40)
                    pdf.image("Imagens/fundo-cinza.png",15,190,w=180,h=30)

                    pdf.set_xy(15,15)
                    pdf.multi_cell(175,5, 'A amortiza????o do capital investido, ou seja, o retorno sobre o investimento com energia fotovoltaica, ?? representado pelo gr??fico abaixo:',border = 0)

                    pdf.set_font('Times','B',size=12)
                    pdf.text(15,35,txt= 'SALDO DO FLUXO DE CAIXA AO ANO')




                    pdf.set_font('arial',size=10)
                    pdf.set_xy(15,135)
                    pdf.multi_cell(175,5, 'O termo amortiza????o, tamb??m conhecido nos termos ingl??s como Payback (Tempo de retorno) e Return over Investment (Retorno do Investimento), indica o zeramento de valor investido pelo valor de retorno: '+str(PayBackAno)+' ano(s) e '+str(PayBackMes)+ ' m??s(s). A partir desse momento toda economia com energia solar ?? livre para outros investimentos.',border = 0)

                    pdf.set_xy(15,155)
                    pdf.multi_cell(175,5, 'As estimativas de gera????o de energia, custos e economia foi baseada e projetada com base nas informa????es de consumo apresentadas pelo cliente e no estudo de irradia????o solar local, tal como na an??lise da infla????o da compra de energia el??trica.',border = 0)

                    bar.progress(60)

                    pdf.text(20,195,txt='Economia mensal')
                    pdf.text(130,195,txt='R$ '+str(thousand_sep(round(MediaSimulacao))).replace(',','.')+',00')
                    pdf.text(20,200,txt='Previs??o de conta ap??s instala????o')
                    pdf.text(130,200,txt='R$ '+str(round(ContaLuz)).replace(',','.')+',00')
                    pdf.text(20,205,txt='Tempo de retorno')
                    pdf.text(130,205,txt=str(PayBackAno)+' Ano(s) '+str(PayBackMes)+' M??s(s)')
                    pdf.text(20,210,txt='Economia em 25 anos')
                    pdf.text(130,210,txt='R$ '+str(thousand_sep(round(mult[25][5]))).replace(',','.')+',00')
                    pdf.text(20,215,txt='Valor do investimento ?? vista')
                    pdf.text(130,215, txt='R$' + str(Capital).replace(',','.')+',00')


                    bar.progress(70)

                    pdf.add_page()
                    pdf.image("Imagens/fundoPDF.jpg",0,0,w=230)
                    pdf.image("Imagens/fundo.png",15,32,w=180,h=35)
                    pdf.image("Imagens/fundo-cinza.png",15,42,w=180,h=25)

                    pdf.set_font('arial',size=10)

                    pdf.text(20,48,txt='M??dulos Fotovoltaicos')
                    pdf.text(130,48,txt= '10 anos')
                    if Inversor1 == 'Micro Inversor':
                        pdf.text(20,53, txt='Micro Inversor')
                        pdf.text(130,53,txt= '12 anos')
                    else:
                        pdf.text(20,53, txt='Inversor')
                        pdf.text(130,53,txt= '10 anos')
                    pdf.text(20,58,txt= 'Estrutura Met??lica')
                    pdf.text(130,58,txt= '30 anos')
                    pdf.text(20,63,txt= 'Instala????o do Sistema')
                    pdf.text(130,63,txt= '1 ano')


                    pdf.set_xy(15,90)
                    pdf.multi_cell(175,5, '?? de responsabilidade da DUBAI ENERGY o dimensionamento do sistema; elabora????o do projeto; fornecimento dos equipamentos e materiais necess??rios; acompanhamento junto ?? distribuidora; instala????o do sistema; supervis??o e gerenciamento da obra.',border = 0)
                    pdf.set_xy(15,110)
                    pdf.multi_cell(175,5, 'Justificamos que a m??o de obra ?? qualificada, afirmando que todos os componentes s??o instalados de acordo com instru????es e orienta????es do fabricante, bem como com planos de engenharia, al??m de c??digos e exig??ncias de constru????o locais.',border = 0)
                    pdf.set_xy(15,130)
                    pdf.multi_cell(175,5, 'N??o ?? de responsabilidade da Empresa c??lculo e refor??o/modifica????es de estrutura; modifica????es na rede el??trica; adapta????o de transformador; armazenamento/seguro de material; seguran??a local; e ajuste de tens??o junto ?? distribuidora.',border = 0)

                    pdf.image("Imagens/assinatura.png",13,200,w=80,h=50)
                    pdf.text(26,245,txt= 'Assinatura do representante')
                    pdf.text(38,250,txt= 'Dubai Energy')
                    pdf.text(33,255,txt= '35.394.744/0001.12')
                    pdf.text(150,245, txt='Data: '+str(data.day)+' / '+str(data.month)+' / '+str(data.year))
                    pdf.line(20, 190, 80, 190)



                    pdf.cell(75,100,Nome,ln=1,align='C')
                    pdf.line(20, 240, 80, 240)
                    pdf.text(25,200,txt= 'Autoriza????o para vistoria t??cnica')

                    pdf.set_font('Times','B',size=12)
                    pdf.text(15,15,txt='3 - GARANTIA E RESPONSABILIDADE LEGAL')
                    pdf.text(15,25,txt='3.1 - GARANTIA DOS EQUIPAMENTOS')
                    pdf.text(15,80,txt='3.2 - RESPONSABILIDADE LEGAL')

                    if Inversor1 == 'Micro Inversor':

                        pdf.image("Imagens/micro.png",100,170,w=100,h=70)


                    bar.progress(80)

                    pdf.add_page()
                    pdf.image("Imagens/fundoPDF.jpg",0,0,w=230)
                    pdf.image("Imagens/dubai.png",83,15,w=40,h=20)
                    pdf.image("Imagens/fundo.png",40,60,w=130,h=50)
                    pdf.image("Imagens/fundo-cinza.png",40,80,w=130,h=85)

                    pdf.set_font('Times','B',size=15)



                    pdf.cell(190,70,'ESTIMATIVA DE PARCELAS',ln=1,align='C')

                    pdf.set_text_color(255,255,255)
                    pdf.set_font('arial', size=10)
                    pdf.text(45,70,txt='Valor do Financiamento: ')
                    pdf.text(45,75,txt='R$ '+str(thousand_sep(CapitalFixo)).replace(',','.')+',00')

                    pdf.text(100,70,txt='Entrada de: ')
                    pdf.text(100,75,txt='R$ 0,00 ')

                    pdf.text(135,70,txt='Car??ncia de:')
                    pdf.text(135,75,txt=str(int(carencia1)*30)+' Dias ('+str(carencia1)+' Meses) ')

                    pdf.set_text_color(0,0,0)

                    pdf.text(80,90,txt='Op????o de pagamento Pr??-Fixo')
                    pdf.text(88,95,txt='Sem corre????o anual')



                    pdf.text(55,105,txt='Prazo')
                    pdf.text(133,105,txt='Parcela')
                    pdf.text(130,110,txt='sem seguro')

                    pdf.text(55,120,txt='12x ')
                    pdf.text(55,130,txt='24x ')
                    pdf.text(55,140,txt='36x ')
                    pdf.text(55,150,txt='60x ')
                    pdf.text(55,160,txt='72x ')

                    comando = f'SELECT * FROM parcelas'
                    cursor.execute(comando)
                    resultado = cursor.fetchall()

                    juros = [resultado[0][1],resultado[0][2],resultado[0][3],resultado[0][4],resultado[0][5]]
                    parcelas= [-12,-24,-36,-60,-72]
                    l = 120
                    for i in range(5):
                        Valor = (CapitalFixo*(juros[i]/100))/(1-((1+(juros[i]/100))**parcelas[i]))
                        pdf.text(130,l,txt=str(thousand_sep(round(Valor))).replace(',','.')+',00')
                        l=l+10


                    pdf.set_text_color(255,0,0)
                    pdf.set_xy(15,180)
                    pdf.multi_cell(175,5,'Esta ?? uma simula????o com a m??dia de juros de mercado, podendo ter parcelas reduzidas ap??s simula????o no CPF ou CNPJ do cliente.')

                    nomeImage = "Imagens/financeiras.png"
                    convertImage(nomeImage) 

                    pdf.image(nomeImage,15,200,w=180,h=45)

                    bar.progress(85)


                    pdf.add_page()
                    pdf.set_text_color(0,0,0)

                    pdf.image("Imagens/fundoPDF.jpg",0,0,w=230)
                    pdf.image("Imagens/dubai.png",83,15,w=40,h=20)
                    pdf.set_font('Times','B',size=15)
                    pdf.image("Imagens/obras.png",15,60,w=175,h= 175)
                    pdf.cell(190,70,'ALGUMAS INSTALA????ES DUBAI ENERGY',ln=1,align='C')


                    pdf.add_page()


                    pdf.image("Imagens/fundoPDF.jpg",0,0,w=230)
                    pdf.image("Imagens/dubai.png",83,15,w=40,h=20)
                    pdf.set_font('Times','B',size=15)
                    pdf.cell(190,70,'DADOS PARA O SEU FINANCIAMENTO SOLAR',ln=1,align='C')
                    pdf.set_font('arial','B',size=10)

                    if Pessoa == 'Fisica':

                        pdf.text(20,60, txt='PESSOA F??SICA')
                        pdf.text(20,70, txt='NOME COMPLETO:_______________________________')
                        pdf.text(20,80, txt='RG:_______________________________')
                        pdf.text(20,90, txt='CPF:_______________________________')
                        pdf.text(20,100, txt='DATA DE NASCIMENTO:____/___/______')
                        pdf.text(20,110, txt='CELULAR: (__) 9______-__________')
                        pdf.text(20,120, txt='EMAIL PESSOAL:_________________')
                        pdf.text(20,130, txt='NOME DA M??E:_______________________________________________')
                        pdf.text(20,140, txt='ESTADO CIVIL:___________________________________')
                        pdf.text(20,150, txt='PROFISS??O:___________________________________')
                        pdf.text(20,160, txt='RENDA M??DIA LIQUIDA: R$:___________________________________')
                        pdf.text(20,170, txt='ESTADO:________________________________')
                        pdf.text(20,180, txt='CIDADE:________________________________')
                        pdf.text(20,190, txt='BAIRRO:________________________________')
                        pdf.text(20,200, txt='ENDERE??O:______________________________')
                        pdf.text(20,210, txt='CEP:_____________-_____________')
                        pdf.text(20,220, txt='POT??NCIA DO SISTEMA:_____________kW')
                        pdf.text(20,230, txt='PRODU????O M??DIA MENSAL:_________________kWh')
                        pdf.text(20,240, txt='TIPO DE ESTRUTURA:___________________')
                        pdf.text(20,250, txt='OBSERVA????O:___________________________________________________')
                        pdf.text(20,270, txt='OBS.: comprovantes de renda (HOLERITE, EXTRATO BANCARIO, IR ETC.)')


                    else:

                        pdf.text(20,60, txt='PESSOA JUR??DICA')
                        pdf.text(20,68, txt='NOME FANTASIA:_______________________________')
                        pdf.text(20,75, txt='CNPJ:_______________________________')
                        pdf.text(20,83, txt='SETOR DE ATUA????O:_______________________________')
                        pdf.text(20,91, txt='FATURAMENTO M??DIO MENSAL:____________________')
                        pdf.text(20,99, txt='TELEFONE:(__)9__________-___________')
                        pdf.text(20,107, txt='E-MAIL CORPORATIVO:_______________________________')
                        pdf.text(20,115, txt='DADOS DO(S) REPRESENTANTE(S) LEGAIS')
                        pdf.text(20,123, txt='NOME COMPLETO:_______________________________')
                        pdf.text(20,131, txt='RG:_______________________________')
                        pdf.text(20,139, txt='CPF:_______________________________')
                        pdf.text(20,147, txt='DATA DE NASCIMENTO:____/___/______')
                        pdf.text(20,155, txt='CELULAR: (__) 9______-__________')
                        pdf.text(20,163, txt='EMAIL PESSOAL:_________________')
                        pdf.text(20,171, txt='NOME DA M??E:_______________________________________________')
                        pdf.text(20,179, txt='ESTADO CIVIL:___________________________________')
                        pdf.text(20,187, txt='PROFISS??O:___________________________________')
                        pdf.text(20,195, txt='RENDA M??DIA LIQUIDA: R$:___________________________________')
                        pdf.text(20,203, txt='ESTADO:________________________________')
                        pdf.text(20,211, txt='CIDADE:________________________________')
                        pdf.text(20,219, txt='BAIRRO:________________________________')
                        pdf.text(20,227, txt='ENDERE??O:______________________________')
                        pdf.text(20,235, txt='CEP:_____________-_____________')
                        pdf.text(20,243, txt='POT??NCIA DO SISTEMA:_____________kW')
                        pdf.text(20,251, txt='PRODU????O M??DIA MENSAL:_________________kWh')
                        pdf.text(20,259, txt='TIPO DE ESTRUTURA:___________________')
                        pdf.text(20,267, txt='OBSERVA????O:___________________________________________________')
                        pdf.text(20,277, txt='OBS.: comprovantes de renda (HOLERITE, EXTRATO BANCARIO, IR ETC.)')

                    html = create_download_link(pdf.output(dest="S").encode("latin-1"), Nome+"_DubaiEnergy")  
                    st.markdown(html, unsafe_allow_html=True)

                    bar.progress(100)

                    tempo = str(data.day)+' / '+str(data.month)+' / '+str(data.year)
                    preco = str(Capital).replace(',','.')+',00'
                    comando = f'INSERT INTO cliente (nome, estado, cidade, geracao,preco,data,cpf,telefone,email,Vendedor) VALUES ("{Nome}","{Estados}","{Cidade}","{str(potenciaFotovoltaica)}","{preco}","{tempo}","{Cpf}","{Telefone}","{Email}","{vendedor}")'
                    cursor.execute(comando)
                    conexao.commit()

                    st.success("PDF pronto pra download!")
                    cursor.close()
                    conexao.close()
                else:
                    st.error("Alguma informa????o obrigat??ria n??o foi fornecida!")
                    st.error("Verifique novamente os dados acima.")
                    cursor.close()
                    conexao.close()
            else:
                st.error("Cpf Inv??lido!")
    except:
        st.error("Ocorreu algum erro!")
        st.error("Reinicie a plataforma.")
