import requests
from kivy.app import App
from datetime import datetime
from bannerexames import banner_exame
from bannervacinacao import banner_vacinacao
from bannerconsultas import banner_consulta


class MyFirebase():
    chaveAPI="AIzaSyAELw6mJ-Mv0P61Q3hZ1K6SCegVS13GabA"

    def criar_conta(self,email,senha):
        global localIdx
        link=f'https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.chaveAPI}'
        print(email,senha)
        info={"email":email,
              "password": senha,
              "returnSecureToken":True}
        requisicao=requests.post(link,data=info)
        requisicao_dic=requisicao.json()
        if requisicao.ok:
            print("Usuário Criado")
            meu_aplicativo=App.get_running_app()
            pagina_login=meu_aplicativo.root.ids['Entrar']
            pagina_login.ids['mensagem_login'].text="Usuário cadastrado com sucesso"
            pagina_login.ids['mensagem_login'].color=(1,0,0,1)
            #variáveis:
            idToken=requisicao_dic['idToken'] # autenticação(só editar as informações dele mesmo)
            refreshToken=requisicao_dic['refreshToken'] #token que mantém o usuário logado
            localId=requisicao_dic['localId'] #id do usuário
            #Criando as variáveis no meu aplicativo:
            meu_aplicativo.idToken=idToken
            meu_aplicativo.localId=localId
            localIdx=localId
            with open ("refreshtoken.txt","w") as arquivo:
                arquivo.write(refreshToken)
            
            with open ("localid.txt","w") as arquivo:
                arquivo.write(localId)

            link=f"https://aplicativosaudetcc-default-rtdb.firebaseio.com/{localId}.json"

            info_usuario='{"CPF":"", "Consultas":"","Exames":"","Vacinas":"","icone":"avatar.png","cartao_sus":"","endereco":"","municipio":"","nome":"","idade":"","n_carteirinha":"","nascimento":"","nome_plano":"","plano":false,"sigla_estado":""}'
            requisicao_usuario=requests.patch(link,data=info_usuario)
            meu_aplicativo.mudar_tela("PreencherCadastro")
        else:
            mensagem_erro=requisicao_dic['error']['message']
            meu_aplicativo=App.get_running_app()
            pagina_login=meu_aplicativo.root.ids['Entrar']
            if mensagem_erro=='INVALID_EMAIL':
                pagina_login.ids['mensagem_login'].text="E-mail inválido"
                pagina_login.ids['mensagem_login'].color=(1,0,0,1)
            elif mensagem_erro=='MISSING_PASSWORD':
                pagina_login.ids['mensagem_login'].text="Insira uma senha"
                pagina_login.ids['mensagem_login'].color=(1,0,0,1)
            elif mensagem_erro=='WEAK_PASSWORD':
                pagina_login.ids['mensagem_login'].text="Senha deve ter pelo menos 6 caracteres"
                pagina_login.ids['mensagem_login'].color=(1,0,0,1)
            elif mensagem_erro=='EMAIL_EXISTS':
                pagina_login.ids['mensagem_login'].text="E-mail já cadastrado"
                pagina_login.ids['mensagem_login'].color=(1,0,0,1)
            elif mensagem_erro=='INVALID_PASSWORD':
                pagina_login.ids['mensagem_login'].text="Senha incorreta"
                pagina_login.ids['mensagem_login'].color=(1,0,0,1)
            print(mensagem_erro)
        
    def preencher_dados_cadastrais(self,nome,cpf,data_nascimento,endereco,municipio,estado):
        #atualziando os dados cadastrais do usuário que acabou de criar
        # idade= calcular aqui a idade automaticamente
        meu_aplicativo=App.get_running_app()
        meu_aplicativo.localId=localIdx
        print(localIdx)

        date_format = '%d/%m/%Y'
        try:
            date_obj = datetime.strptime(data_nascimento, date_format)
        except:
            pagina_cadastro=meu_aplicativo.root.ids['PreencherCadastro']
            pagina_cadastro.ids['mensagem_erro_cadastro'].text="Data de nascimento deve ser no formato dd/mm/aaaa"
            pagina_cadastro.ids['mensagem_erro_cadastro'].color=(1,0,0,1)
            return

        today = datetime.today()
        idade=int((today - date_obj).days/365.25)

        dic_dados_cadastrais=f'{{"nome":"{nome}","CPF":"{cpf}","nascimento":"{data_nascimento}","idade":"{idade}","endereco":"{endereco}","municipio":"{municipio}","sigla_estado":"{estado}","variavelvacina":"{0}","variavelexame":"{0}","variavelconsulta":"{0}"}}'
        print(dic_dados_cadastrais)
        link=f"https://aplicativosaudetcc-default-rtdb.firebaseio.com/{localIdx}.json?auth={meu_aplicativo.idToken}"
        requests.patch(link,data=dic_dados_cadastrais)
        meu_aplicativo.carregar_infos_usuario()
        meu_aplicativo.mudar_tela("Menu_Principal")

    def fazer_login(self,email,senha):
        global localIdx
        link=f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.chaveAPI}"
        info={"email":email,
              "password": senha,
              "returnSecureToken":True}
        requisicao=requests.post(link,data=info)
        requisicao_dic=requisicao.json()

        if requisicao.ok:
            meu_aplicativo=App.get_running_app()
            idToken=requisicao_dic['idToken'] # autenticação(só editar as informações dele mesmo)
            refreshToken=requisicao_dic['refreshToken'] #token que mantém o usuário logado
            localId=requisicao_dic['localId'] #id do usuário
            localIdx=localId
            print(f'esse é o idToken: {localId}')
            #Criando as variáveis no meu aplicativo:
            meu_aplicativo.idToken=idToken
            meu_aplicativo.localId=localId
            with open ("refreshtoken.txt","w") as arquivo:
                arquivo.write(refreshToken)
            
            meu_aplicativo.carregar_infos_usuario()
            meu_aplicativo.mudar_tela("Menu_Principal")

        else:
            mensagem_erro=requisicao_dic['error']['message']
            meu_aplicativo=App.get_running_app()
            pagina_login=meu_aplicativo.root.ids['Entrar']
            if mensagem_erro=='INVALID_EMAIL':
                pagina_login.ids['mensagem_login'].text="E-mail inválido"
                pagina_login.ids['mensagem_login'].color=(1,0,0,1)
            elif mensagem_erro=='MISSING_PASSWORD':
                pagina_login.ids['mensagem_login'].text="Insira a senha"
                pagina_login.ids['mensagem_login'].color=(1,0,0,1)
            elif mensagem_erro=='INVALID_PASSWORD':
                pagina_login.ids['mensagem_login'].text="Senha incorreta"
                pagina_login.ids['mensagem_login'].color=(1,0,0,1)
            elif mensagem_erro=='EMAIL_NOT_FOUND':
                pagina_login.ids['mensagem_login'].text="Não encontramos seu e-mail, faça seu cadastro!"
                pagina_login.ids['mensagem_login'].color=(1,0,0,1)
            else:
                pagina_login.ids['mensagem_login'].text=mensagem_erro
                pagina_login.ids['mensagem_login'].color=(1,0,0,1)

    def atualizar_dados_cadastrais(self,cpf,data_nascimento,endereco,municipio,estado,cartao_sus,nome_plano,n_carteirinha):
        #atualziando os dados cadastrais do usuário já existente
        meu_aplicativo=App.get_running_app()
        meu_aplicativo.localId=localIdx
        date_format = '%d/%m/%Y'

        try:
            date_obj = datetime.strptime(data_nascimento, date_format)
        except:
            pagina_cadastro=meu_aplicativo.root.ids['PreencherCadastro']
            pagina_cadastro.ids['mensagem_erro_cadastro'].text="Data de nascimento deve ser no formato dd/mm/aaaa"
            pagina_cadastro.ids['mensagem_erro_cadastro'].color=(1,0,0,1)
            return
        today = datetime.today()

        idade=str(int((today - date_obj).days/365.25))
        print(localIdx)
        if nome_plano=="":
            plano="Nao"
        else:
            plano="Sim"
        dic_dados_cadastrais=f'{{"CPF":"{cpf}","nascimento":"{data_nascimento}","idade":"{idade}","endereco":"{endereco}","municipio":"{municipio}","sigla_estado":"{estado}","cartao_sus":"{cartao_sus}","plano":"{plano}","nome_plano":"{nome_plano}","n_carteirinha":"{n_carteirinha}"}}'        
        print(dic_dados_cadastrais)
        link=f"https://aplicativosaudetcc-default-rtdb.firebaseio.com/{localIdx}.json?auth={meu_aplicativo.idToken}"
        requests.patch(link,data=dic_dados_cadastrais)
        meu_aplicativo.carregar_infos_usuario()
        meu_aplicativo.mudar_tela("Visualizar_Dados")

    def atualizar_vacinas(self,data_vacina,profissional,local,lote,tipo):
        print('entrei aqui - atualziar vacinas')
        meu_aplicativo=App.get_running_app()
        meu_aplicativo.localId=localIdx
        try:
            date_obj = datetime.strptime(data_vacina,'%d/%m/%Y')
        except:
            pagina_atualizar_vacina=meu_aplicativo.root.ids['Adicionar_Vacinacao']
            pagina_atualizar_vacina.ids['mensagem_erro_data'].text="Data deve ser no formato dd/mm/aaaa"
            pagina_atualizar_vacina.ids['mensagem_erro_data'].color=(1,0,0,1)
            return
        
        #----Identificando qual o id da vacina a ser adicionada
        link=f"https://aplicativosaudetcc-default-rtdb.firebaseio.com/{localIdx}.json?auth={meu_aplicativo.idToken}"
        requisicao=requests.get(link)
        requisicao_dic=requisicao.json()
        variavelvacina=int(requisicao_dic['variavelvacina'])+1
        print(variavelvacina)
        dic_variavelvacina=f'{{"variavelvacina":"{variavelvacina}"}}'
        requests.patch(link,data=dic_variavelvacina)

        #----Adicionando os dados no id identificado
        link=f"https://aplicativosaudetcc-default-rtdb.firebaseio.com/{localIdx}/Vacinas/{variavelvacina}.json?auth={meu_aplicativo.idToken}"
        dic_inserir_vacina=f'{{"data":"{data_vacina}","enfermeiro":"{profissional}","local":"{local}","lote":"{lote}","tipo":"{tipo}"}}'
        print(dic_inserir_vacina)
        requests.patch(link,data=dic_inserir_vacina)
        pagina_vacina=meu_aplicativo.root.ids['Vacinacao']
        lista_vacinas=pagina_vacina.ids["lista_vacinas"]
        banner=banner_vacinacao(data=data_vacina,enfermeiro=profissional,tipo=tipo,lote=lote,local=local)
        lista_vacinas.add_widget(banner)
        meu_aplicativo.mudar_tela("Vacinacao")
    
    def atualizar_consultas(self,data,horario,especialidade,medico):
        print('entrei aqui - atualizar consultas')
        meu_aplicativo=App.get_running_app()
        meu_aplicativo.localId=localIdx
        try:
            date_obj = datetime.strptime(data,'%d/%m/%Y')
        except:
            pagina_atualizar_consultas=meu_aplicativo.root.ids['Adicionar_Consultas']
            pagina_atualizar_consultas.ids['mensagem_erro_data'].text="Data deve ser no formato dd/mm/aaaa"
            pagina_atualizar_consultas.ids['mensagem_erro_data'].color=(1,0,0,1)
            return
        
        #----Identificando qual o id da vacina a ser adicionada
        link=f"https://aplicativosaudetcc-default-rtdb.firebaseio.com/{localIdx}.json?auth={meu_aplicativo.idToken}"
        requisicao=requests.get(link)
        requisicao_dic=requisicao.json()
        variavelconsulta=int(requisicao_dic['variavelconsulta'])+1
        print(variavelconsulta)
        dic_variavelconsulta=f'{{"variavelconsulta":"{variavelconsulta}"}}'
        requests.patch(link,data=dic_variavelconsulta)

        #----Adicionando os dados no id identificado
        link=f"https://aplicativosaudetcc-default-rtdb.firebaseio.com/{localIdx}/Consultas/{variavelconsulta}.json?auth={meu_aplicativo.idToken}"
        dic_inserir_consulta=f'{{"data":"{data}","horario":"{horario}","especialidade":"{especialidade}","medico":"{medico}"}}'
        print(dic_inserir_consulta)
        requests.patch(link,data=dic_inserir_consulta)
        pagina_consulta=meu_aplicativo.root.ids['Consultas']
        lista_consultas=pagina_consulta.ids["lista_consultas"]
        banner=banner_consulta(data=data,medico=medico,horario=horario,especialidade=especialidade)
        lista_consultas.add_widget(banner)
        meu_aplicativo.mudar_tela("Consultas")


    def atualizar_exames(self,data,tipo,situacao):
        print('entrei aqui - atualizar exames')
        meu_aplicativo=App.get_running_app()
        meu_aplicativo.localId=localIdx
        try:
            date_obj = datetime.strptime(data,'%d/%m/%Y')
        except:
            pagina_atualizar_consultas=meu_aplicativo.root.ids['Adicionar_Consultas']
            pagina_atualizar_consultas.ids['mensagem_erro_data'].text="Data deve ser no formato dd/mm/aaaa"
            pagina_atualizar_consultas.ids['mensagem_erro_data'].color=(1,0,0,1)
            return
        
        #----Identificando qual o id da vacina a ser adicionada
        link=f"https://aplicativosaudetcc-default-rtdb.firebaseio.com/{localIdx}.json?auth={meu_aplicativo.idToken}"
        requisicao=requests.get(link)
        requisicao_dic=requisicao.json()
        variavelexame=int(requisicao_dic['variavelexame'])+1
        print(variavelexame)
        dic_variavelexame=f'{{"variavelexame":"{variavelexame}"}}'
        requests.patch(link,data=dic_variavelexame)

        #----Adicionando os dados no id identificado
        link=f"https://aplicativosaudetcc-default-rtdb.firebaseio.com/{localIdx}/Exames/{variavelexame}.json?auth={meu_aplicativo.idToken}"
        dic_inserir_exame=f'{{"data":"{data}","tipo":"{tipo}","situacao":"{situacao}"}}'
        print(dic_inserir_exame)
        requests.patch(link,data=dic_inserir_exame)
        pagina_exame=meu_aplicativo.root.ids['Exames']
        lista_exames=pagina_exame.ids["lista_exames"]
        banner=banner_exame(data=data,tipo=tipo,situacao=situacao)
        lista_exames.add_widget(banner) #adicionando um item a lista de exames   
        meu_aplicativo.mudar_tela("Exames")
