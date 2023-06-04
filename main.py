from kivy.app import App
from kivy.lang import Builder
from telas import *
from botoes import *
import requests
from bannervacinacao import banner_vacinacao
from bannerconsultas import banner_consulta
from bannerexames import banner_exame
from functools import partial
from firebase import MyFirebase
import os
import certifi


os.environ['SSL_CERT_FILE']=certifi.where()

#interface gráfica
gui=Builder.load_file("main.kv")
class MainApp(App):
    # localId=1
        
    def build (self):
        self.firebase=MyFirebase()
        return gui

    def on_start(self):
        # self.carregar_infos_usuario()
        pass
        
    def carregar_infos_usuario(self):
        # try:
        #mapeando conexão com banco de dados firebase
        print(f'cheguei aqui, estou acessando o link: https://aplicativosaudetcc-default-rtdb.firebaseio.com/{self.localId}.json')
        requisicao=requests.get(f"https://aplicativosaudetcc-default-rtdb.firebaseio.com/{self.localId}.json?auth={self.idToken}")
        requisicao_dic=requisicao.json()

        #Preencher foto de perfil
        avatar=requisicao_dic['icone']
        foto_perfil_menu=self.root.ids.Menu_Principal.ids["foto_perfil_menu"]
        foto_perfil_menu.source=f"icones/{avatar}"

        #Preencher dados do paciente no Menu_Principal
        nome=requisicao_dic['nome']
        endereco=requisicao_dic['endereco']
        municipio=requisicao_dic['municipio']
        data_nascimento=requisicao_dic['nascimento']
        idade=requisicao_dic['idade']
        sigla_estado=requisicao_dic['sigla_estado']
        CPF=requisicao_dic['CPF']
        cartao_sus=requisicao_dic['cartao_sus']
        plano=requisicao_dic['plano']
        nome_plano=requisicao_dic['nome_plano']
        n_carteirinha=requisicao_dic['n_carteirinha']

        dados_paciente_menu=self.root.ids.Menu_Principal.ids["dados_paciente"]
        dados_paciente_menu.text=f"Nome: {nome}\nData de Nascimento: {data_nascimento}\n{idade} anos\nEndereço: {endereco}\n{municipio} - {sigla_estado}"
        
        #Preencher dados do paciente no Visualizar_Dados
        foto_perfil_editar=self.root.ids.Visualizar_Dados.ids["foto_perfil_editar"]
        foto_perfil_editar.source=f"icones/{avatar}"
        self.root.ids.Visualizar_Dados.ids["nome_paciente"].text=nome
        self.root.ids.Visualizar_Dados.ids["tela_editar_endereco"].text=f"{endereco}\n{municipio} - {sigla_estado}\n\n\n\nCPF: {CPF}\nCartão SUS: {cartao_sus}\n\n\n\nPossui plano: {plano}\nQual? {nome_plano}\nNº Carteirinha: {n_carteirinha}"
        

        #Preencher vacinas
        try: #caso tenha vacinas, vou exibi-las
            vacinas=requisicao_dic['Vacinas']
            print('olhar aqui para o dicionário de vacinas:')
            print(vacinas)
            pagina_vacina=self.root.ids['Vacinacao']
            lista_vacinas=pagina_vacina.ids["lista_vacinas"]
            for vacina in vacinas.items():
                banner=banner_vacinacao(data=vacina[1]['data'],enfermeiro=vacina[1]['enfermeiro'],
                                        tipo=vacina[1]['tipo'],lote=vacina[1]['lote'],local=vacina[1]['local'])
                lista_vacinas.add_widget(banner) #adicionando um item a lista de vacinas           

        except: #caso não tenha vacinas, preencher vazio
            pass

        #Preencher exames - fazer essa parte
        try: #caso tenha exames, vou exibi-las
            lista_exames_banco=requisicao_dic['Exames'][1:]
            print('olhar aqui para o dicionário de exames:')
            print(lista_exames_banco)
            pagina_exame=self.root.ids['Exames']
            lista_exames=pagina_exame.ids["lista_exames"]
            for exames in lista_exames_banco:
                print(exames)
                banner=banner_exame(data=exames['data'],tipo=exames['tipo'],
                                    situacao=exames['situacao'])
                lista_exames.add_widget(banner) #adicionando um item a lista de exames          
        except Exception as erro: #caso não tenha exames, preencher vazio
            print(erro)

        #Preencher consultas
        try: #caso tenha consultas, vou exibi-las
            lista_consultas_banco=requisicao_dic['Consultas'][1:]
            print('olhar aqui para o dicionário de consultas:')
            print(lista_consultas_banco)
            pagina_consulta=self.root.ids['Consultas']
            lista_vacinas=pagina_consulta.ids["lista_consultas"]
            for consulta in lista_consultas_banco:
                banner=banner_consulta(data=consulta['data'],medico=consulta['medico'],
                                    horario=consulta['horario'],especialidade=consulta['especialidade'])
                lista_vacinas.add_widget(banner) #adicionando um item a lista de consultas
                print(lista_vacinas)        

        except: #caso não tenha consultas, preencher vazio
            pass
        # except:
        #     pass
    
    def mudar_foto_perfil(self,foto,*args):
        #mudei minha foto de perfil:
        foto_perfil_menu=self.root.ids.Menu_Principal.ids["foto_perfil_menu"]
        foto_perfil_menu.source=f"icones/{foto}"

        #editar a foto no banco de dados:
        info=f'{{"avatar": "{foto}"}}' #criar um dicionário com as informações que vc quer e enviar nesse formato específico pq cada valor do dicionário deve estar entre aspas duplas
        requests.patch(f'https://aplicativosaudetcc-default-rtdb.firebaseio.com/{self.localId}.json?auth={self.idToken}',data=info)
        
        '''
         ---------aqui será necessário identificar como fazer a funcionalidade de definir a foto----------------
        pagina_editardados=self.root.ids["Visualizar_Dados"]
        foto_perfil=pagina_editardados.ids["foto_perfil_editar"]
        definir_foto()
        foto='teste_mudar_foto.JPG'
        imagem=ImageButton(source=f"icones/{foto}",on_release=partial(self.mudar_foto_perfil,foto))
        foto_perfil.add_widget(imagem)
        '''

    def mudar_tela(self,id_tela):
        print(id_tela)
        #direcionando para o arquivo kv que vc quer, caso vc queira ir para o main é só usar o self.root
        gerenciador_telas=self.root.ids["screen_manager"]
        gerenciador_telas.current=id_tela

MainApp().run()



#enviar informação para banco de dados: post
#pegar informação do banco de dados: get
#atualizar informação do banco de dados: patch