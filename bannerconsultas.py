from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color,Rectangle

class banner_consulta(GridLayout):
    def __init__(self,**kwargs):
        self.rows= 1
        super().__init__()

        with self.canvas:
            Color(rgb=(0,0,0,1))
            self.rec=Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.atualizar_rec,size=self.atualizar_rec)


        data=kwargs['data']
        medico=kwargs['medico']
        especialidade=kwargs['especialidade']
        horario=kwargs['horario']

        esquerda=FloatLayout()
        esquerda_label=Label(pos_hint={"right":0.7, "top":0.8},
                            size_hint=(0.5,0.5),text=data, bold= True)
        esquerda.add_widget(esquerda_label)

        meio=FloatLayout()
        meio_label=Label(pos_hint={"right":0.4, "top":0.9},
                            size_hint=(0.5,0.5),text=medico, bold= True)
        meio_label_lote=Label(pos_hint={"right":0.4, "top":0.6},
                            size_hint=(0.5,0.5),text=f"{especialidade}")
        meio.add_widget(meio_label)
        meio.add_widget(meio_label_lote)

        self.add_widget(esquerda)
        self.add_widget(meio)

        
    def atualizar_rec(self,*args):
        self.rec.pos=self.pos
        self.rec.size=self.size


