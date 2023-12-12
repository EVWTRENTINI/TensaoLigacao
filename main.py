# INICIO INTERFACE
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
# FIM INTERFACE

from lib.graf import *
from lib.calc import *


# Classe necessaria pra alinhar os textos nas tabelas
class AlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter


# Classe que gera a interface do programa
class MatplotlibWidget(QMainWindow):
    def __init__(self):
        # Cria a janela feita no designer
        QMainWindow.__init__(self)
        loadUi("interfaceTensao.ui", self)  # É aqui que entra o arquivo da interface

        # Customiza a janela importada do designer
        self.setWindowTitle("Tensão em ligações")
        self.setFixedSize(self.size())

        ## Altera a largura das colunas da tabela de forças
        self.forcasTable.setColumnWidth(0, int(self.forcasTable.width() / 6) - 1)
        self.forcasTable.setColumnWidth(1, int(self.forcasTable.width() / 6) - 1)
        self.forcasTable.setColumnWidth(2, int(self.forcasTable.width() / 6) - 1)
        self.forcasTable.setColumnWidth(3, int(self.forcasTable.width() / 6) - 1)
        self.forcasTable.setColumnWidth(4, int(self.forcasTable.width() / 6) - 1)
        self.forcasTable.setColumnWidth(5, int(self.forcasTable.width() / 6) - 1)
        ## Insere valores iniciais na tabela de forças
        self.forcasTable.setItem(0, 0, QTableWidgetItem("0"))
        self.forcasTable.setItem(0, 1, QTableWidgetItem("0"))
        self.forcasTable.setItem(0, 2, QTableWidgetItem("0"))
        self.forcasTable.setItem(0, 3, QTableWidgetItem("0"))
        self.forcasTable.setItem(0, 4, QTableWidgetItem("0"))
        self.forcasTable.setItem(0, 5, QTableWidgetItem("0"))
        ## Centraliza valores da tabela de forças
        delegate = AlignDelegate(self.forcasTable)  # Necessario para centralizar a tabela
        self.forcasTable.setItemDelegate(delegate)  # Centraliza toda a tabela
        ## Altera a largura das colunas da tabela de parafusos
        self.parafusoTable.setColumnWidth(0, 60)
        self.parafusoTable.setColumnWidth(1, 30)
        self.parafusoTable.setColumnWidth(2, 30)
        ## Insere valores iniciais na tabela de parafusos
        self.parafusoTable.setRowCount(6)
        ### Diametro
        self.parafusoTable.setItem(0, 0, QTableWidgetItem("2.2"))
        self.parafusoTable.setItem(1, 0, QTableWidgetItem("2.2"))
        self.parafusoTable.setItem(2, 0, QTableWidgetItem("2.2"))
        self.parafusoTable.setItem(3, 0, QTableWidgetItem("2.2"))
        self.parafusoTable.setItem(4, 0, QTableWidgetItem("2.2"))
        self.parafusoTable.setItem(5, 0, QTableWidgetItem("2.2"))
        ### Coordenada x
        self.parafusoTable.setItem(0, 1, QTableWidgetItem("-7.5"))
        self.parafusoTable.setItem(1, 1, QTableWidgetItem("7.5"))
        self.parafusoTable.setItem(2, 1, QTableWidgetItem("-7.5"))
        self.parafusoTable.setItem(3, 1, QTableWidgetItem("7.5"))
        self.parafusoTable.setItem(4, 1, QTableWidgetItem("-7.5"))
        self.parafusoTable.setItem(5, 1, QTableWidgetItem("7.5"))
        ### Coordenada y
        self.parafusoTable.setItem(0, 2, QTableWidgetItem("7.5"))
        self.parafusoTable.setItem(1, 2, QTableWidgetItem("7.5"))
        self.parafusoTable.setItem(2, 2, QTableWidgetItem("0"))
        self.parafusoTable.setItem(3, 2, QTableWidgetItem("0"))
        self.parafusoTable.setItem(4, 2, QTableWidgetItem("-7.5"))
        self.parafusoTable.setItem(5, 2, QTableWidgetItem("-7.5"))
        ## Centraliza valores da tabela de parafusos
        delegate = AlignDelegate(self.parafusoTable)  # Necessário para centralizar a tabela
        self.parafusoTable.setItemDelegate(delegate)  # Centraliza toda a tabela
        ## Altera a largura das coluna da tabela de soldas
        self.soldaTable.setColumnWidth(0, 60)
        self.soldaTable.setColumnWidth(1, 50)
        self.soldaTable.setColumnWidth(2, 50)
        self.soldaTable.setColumnWidth(3, 50)
        self.soldaTable.setColumnWidth(4, 50)
        ## Centraliza valores da tabela de soldas
        delegate = AlignDelegate(self.soldaTable)  # Necessário para centralizar a tabela
        self.soldaTable.setItemDelegate(delegate)  # Centraliza toda a tabela

        # Liga o clicar dos botões da interface com as funções criadas aqui dentro
        ## Botoes de adicionar e demover linhas
        self.parafusoAddButton.clicked.connect(self.parafusoAddAction)
        self.parafusoRemoveButton.clicked.connect(self.parafusoRemoveAction)
        self.soldaAddButton.clicked.connect(self.soldaAddAction)
        self.soldaRemoveButton.clicked.connect(self.soldaRemoveAction)
        ## Botao de desenhar
        self.desenharButton.clicked.connect(self.desenharAction)
        ## Botao de calcular
        self.calcularButton.clicked.connect(self.calcularAction)  # Botão mesmo
        self.escalaSpinBox.valueChanged.connect(self.calcularAction)  # Ao alterar a escada
        self.componenteRadioButton.toggled.connect(self.calcularAction)  # Ao trocar de resultante para componentes

    def atualizaInterfaceSucesso(self, At, cgx, cgy, Ix, Iy, Ixy):
        """
        Função chamada em caso de sucesso de validação dos dados.
        Ela atualiza os valores das propriedades da ligação e o status do programa.
        """

        # Atualiza propriedades na interface
        self.centroidXLabel.setText('%.2f' % cgx)
        self.centroidYLabel.setText('%.2f' % cgy)
        self.areaLabel.setText('%.2f' % At)
        self.inerciaXLabel.setText('%.2f' % Ix)
        self.inerciaYLabel.setText('%.2f' % Iy)
        self.inerciaXYLabel.setText('%.2f' % Ixy)

        # Atualiza mensagem do status. A formatação em HTML é para centralizar o texto
        self.statusLabel.setText(
            '<html><head/><body><p align="center">Pronto para analisar</p></body></html>')

    def atualizaInterfaceFalha(self):
        """
        Função chamada em caso de falha de validação dos dados.
        Ela deixa vazios os valores das propriedades da ligação altera e o status do programa.
        """
        # Deixa vazia as propriedades na interface
        self.centroidXLabel.setText('')
        self.centroidYLabel.setText('')
        self.areaLabel.setText('')
        self.inerciaXLabel.setText('')
        self.inerciaYLabel.setText('')
        self.inerciaXYLabel.setText('')

        # Atualiza mensagem do status. A formatação em HTML é para centralizar o texto
        self.statusLabel.setText(
            '<html><head/><body><p align="center">Insira valores numéricos válidos para os elementos de ligação!</p></body></html>')

        # Cria variaveis vazias para a função ter o que retornar e não crashar
        d = []
        x = []
        y = []
        At = 0
        cgx = 0
        cgy = 0
        Ix = 0
        Iy = 0
        Ixy = 0

        return d, x, y, At, cgx, cgy, Ix, Iy, Ixy

    # Define as funções que são chamadas ao clicar nos botões
    def pegaDadosTabelas(self):
        """
        Essa função salva os dados das tabelas de parafusos e soldas nas listas.
        Esta função tambem valida a entrada de dados, e chama as funções que determinam as propriedades da ligação
        :return: diametro_parafuso, coord_x_parafuso, coord_y_parafuso, At, cgx, cgy, Ix, Iy, Ixy
        """

        # Inicializa as variaveis para trabalhar com parafusos
        diametro_parafuso = []
        coord_x_parafuso = []
        coord_y_parafuso = []
        d = []
        x = []
        y = []

        # Inicializa as variaveis para trabalhar com soldas
        # Todo(Eduardo): Inicializa as variaveis para trabalhar com soldas
        '''#######
        ##########
        FAZER AQUI
        ##########
        #######'''

        try:  # Esse try é para ver se a aquisição de dados é realizada com sucesso
            # Aqui inicia a aquisição de dados da tabela de parafusos
            rowCount = self.parafusoTable.rowCount()
            for row in range(rowCount):
                d.append(float(self.parafusoTable.item(row, 0).text()))
                x.append(float(self.parafusoTable.item(row, 1).text()))
                y.append(float(self.parafusoTable.item(row, 2).text()))
            # Caso o 'for' acima tenha concluido sem nenhum erro é então copiada os valores para as variaveis definitivas
            diametro_parafuso = d[:]
            coord_x_parafuso = x[:]
            coord_y_parafuso = y[:]

            # Aquisição de dados da tabela de soldas
            # Todo(Eduardo): Aquirir dados da tabela de soldas
            '''#######
            ##########
            FAZER AQUI
            ##########
            #######'''

            # Determina as propriedades da ligação considerando parafusos e soldas
            # Todo(Eduardo): A determinaPropriedadesLigacao() deve ser completada leia TODO dentro dela
            At, cgx, cgy, Ix, Iy, Ixy = determinaPropriedadesLigacao(diametro_parafuso, coord_x_parafuso,
                                                                     coord_y_parafuso)

            # Atualiza a interface com os valores calculados
            self.atualizaInterfaceSucesso(At, cgx, cgy, Ix, Iy, Ixy)

        except:  # Caso a aquisição de dados falhe
            # Atualiza a interface em caso de falha
            d, x, y, At, cgx, cgy, Ix, Iy, Ixy = self.atualizaInterfaceFalha()  # Retorna valores para não crashar # Todo(Eduardo): adicionar parametros das soldas

        return diametro_parafuso, coord_x_parafuso, coord_y_parafuso, At, cgx, cgy, Ix, Iy, Ixy  # Todo(Eduardo): adicionar parametros das soldas

    def desenharAction(self):
        """
        Chama as funções que adquirem os dados das tabelas.
        Chama as funções que determinam as propriedades das ligações.
        Chama as funções que desenham.
        Retorna os valores das tabelas e as propriedades das ligações para o cálculo das tensões.
        """

        # Chama as funções que adquirem os dados das tabelas.
        diametro_parafuso, coord_x_parafuso, coord_y_parafuso, At, cgx, cgy, Ix, Iy, Ixy = self.pegaDadosTabelas() # Todo(Eduardo): adicionar parametros das soldas

        # Prepara a figura
        self.MplWidget.canvas.axes.clear()  # Limpa a figura para evitar sobreposição que ocasiona em lag
        self.MplWidget.canvas.axes.set_box_aspect([1, 1, 1])  # Não sei se é necessário

        ## Ajusta o tamanho da figura para caber a ligação
        # Todo(Eduardo): Repensar em como é feito esse ajuste quando alem de parafusos existirem soldas
        if len(diametro_parafuso) > 0:  # Checa se tem parafuso e define o tamanho da figura em relação a eles
            maiorValorEscala = max(max(coord_x_parafuso), max(coord_y_parafuso), max(diametro_parafuso))
            self.MplWidget.canvas.axes.set_xlim3d(-maiorValorEscala * 1.25,
                                                  maiorValorEscala * 1.25)  # tamanho da grade do desenho em 3D
            self.MplWidget.canvas.axes.set_ylim3d(-maiorValorEscala * 1.25,
                                                  maiorValorEscala * 1.25)  # fazer em relação ao tamanho do desenho dps
            self.MplWidget.canvas.axes.set_zlim3d(-maiorValorEscala * 1.25, maiorValorEscala * 1.25)
            self.MplWidget.canvas.axes.axis('off')  # Remove o grid do fundo da figura

            # Chama a função que desenha os parafusos
            if len(diametro_parafuso) > 0:  # Checa se existe parafuso na ligação
                for k in range(0, len(diametro_parafuso)):  # Para cada parafuso
                    self.MplWidget.canvas.axes = drawParafuso(coord_x_parafuso[k], coord_y_parafuso[k],
                                                              diametro_parafuso[k], self.MplWidget.canvas.axes)

        self.MplWidget.canvas.draw()  # Mostra o que foi mandado ser desenhado

        return diametro_parafuso, coord_x_parafuso, coord_y_parafuso, At, cgx, cgy, Ix, Iy, Ixy  # Todo(Eduardo): adicionar parametros das soldas

    def calcularAction(self):
        """
        Cálcula e desenha as tensões
        """

        diametro_parafuso, coord_x_parafuso, coord_y_parafuso, At, cgx, cgy, Ix, Iy, Ixy = self.desenharAction()  # Todo(Eduardo): adicionar parametros das soldas

        # Verifica se a aquisição de dados foi realizada com sucesso, caso contrario termina a execução
        if diametro_parafuso == []:  # Todo(Eduardo): Pensar em uma verificação quando tiver solda tambem. Tente algo do tipo: "if diametro_parafuso == [] and espessura_solda == []:"
            # No caso de falha a atualização da interface já foi feita na função self.desenharAction()
            return

        try:  # Verifica se as forças foram introduzidas corretamente
            Fxsd = float(self.forcasTable.item(0, 0).text())
            Fysd = float(self.forcasTable.item(0, 1).text())
            Fzsd = float(self.forcasTable.item(0, 2).text())
            Mxsd = float(self.forcasTable.item(0, 3).text())
            Mysd = float(self.forcasTable.item(0, 4).text())
            Mzsd = float(self.forcasTable.item(0, 5).text())
        except:  # Caso as forças foram introduzidas corretamente
            self.statusLabel.setText(
            '<html><head/><body><p align="center">Insira valores numéricos válidos para as solicitações!</p></body></html>')
            return

        # Corrige os esforços para os valores quando os mesmos atuam no centróide da ligação
        Mxsd = Mxsd - Fzsd * cgy
        Mysd = Mysd + Fzsd * cgx
        Mzsd = Mzsd + Fxsd*cgy - Fysd*cgx
        print('Conferir correção dos esforços!!!')

        # Corrige coordenadas para a nova referência que é o centróide
        coord_x_parafuso_cg = coord_x_parafuso - cgx
        coord_y_parafuso_cg = coord_y_parafuso - cgy
        # Todo(Eduardo): Alterar as coordenadas das soldas dentro deste escopo


        # Desenha tensões nos parafusos
        scale = float(self.escalaSpinBox.text())  # Recebe o valor da escala do spin box
        for k in range(0, len(diametro_parafuso)):  # Para cada parafuso
            # Calcula tensões
            SIGwsd = tensaoNormal(Fzsd, At, Iy, Ix, Ixy, Mxsd, Mysd, coord_x_parafuso_cg[k],
                                  coord_y_parafuso_cg[k])
            TAUwxsd, TAUwysd, TAUwsd = calculoCisalhamento(Fxsd, Fysd, At, Mzsd, coord_x_parafuso_cg[k],
                                                           coord_y_parafuso_cg[k], Ix, Iy)

            # Desenha Tensões normais
            self.MplWidget.canvas.axes.text(SIGwsd * scale * 1.2, coord_x_parafuso[k], coord_y_parafuso[k],
                                            str(round(SIGwsd, 2)), c='red',
                                            ha='center', ma='center', zorder=1000)
            self.MplWidget.canvas.axes.arrow3D(0, coord_x_parafuso[k], coord_y_parafuso[k],
                                               0 + SIGwsd * scale, 0, 0,
                                               mutation_scale=20,
                                               color='red', zorder=1000)
            # Desenha Tensões de cisalhamento
            if not self.componenteRadioButton.isChecked():  # Desenhando a RESULTANTE
                self.MplWidget.canvas.axes.text(0, coord_x_parafuso[k] + TAUwxsd * scale * 1.2,
                                                coord_y_parafuso[k] + TAUwysd * scale * 1.2,
                                                str(round(TAUwsd, 2)), c='darkcyan',
                                                ha='center', ma='center', zorder=1000)
                self.MplWidget.canvas.axes.arrow3D(0, coord_x_parafuso[k], coord_y_parafuso[k],
                                                   0, TAUwxsd * scale, TAUwysd * scale,
                                                   mutation_scale=20,
                                                   color='darkcyan')
            else:  # Desenhando as COMPONENTES
                # Coordenada x
                self.MplWidget.canvas.axes.text(0, coord_x_parafuso[k] + TAUwxsd * scale * 1.2, coord_y_parafuso[k],
                                                str(round(TAUwxsd, 2)), c='green',
                                                ha='center', ma='center', zorder=1000)
                self.MplWidget.canvas.axes.arrow3D(0, coord_x_parafuso[k], coord_y_parafuso[k],
                                                   0, 0 + TAUwxsd * scale, 0,
                                                   mutation_scale=20,
                                                   color='green')
                # Coordenada y
                self.MplWidget.canvas.axes.text(0, coord_x_parafuso[k], coord_y_parafuso[k] + TAUwysd * scale * 1.2,
                                                str(round(TAUwysd, 2)), c='blue',
                                                ha='center', ma='center', zorder=1000)
                self.MplWidget.canvas.axes.arrow3D(0, coord_x_parafuso[k], coord_y_parafuso[k],
                                                   0, 0, 0 + TAUwysd * scale,
                                                   mutation_scale=20,
                                                   color='blue')
        self.statusLabel.setText(
            '<html><head/><body><p align="center">Tensões determinadas com sucesso.</p></body></html>')

        self.MplWidget.canvas.draw()  # Mostra o desenho

    def parafusoAddAction(self):
        currentRow = self.parafusoTable.currentRow()
        self.parafusoTable.insertRow(currentRow + 1)

    def parafusoRemoveAction(self):
        currentRow = self.parafusoTable.currentRow()
        rowCount = self.parafusoTable.rowCount()
        if self.parafusoTable.rowCount() > 0:
            if not currentRow == -1:
                self.parafusoTable.removeRow(currentRow)
            else:
                self.parafusoTable.removeRow(rowCount - 1)

    def soldaAddAction(self):
        currentRow = self.soldaTable.currentRow()
        self.soldaTable.insertRow(currentRow + 1)

    def soldaRemoveAction(self):
        currentRow = self.soldaTable.currentRow()
        rowCount = self.soldaTable.rowCount()
        if self.soldaTable.rowCount() > 0:
            if not currentRow == -1:
                self.soldaTable.removeRow(currentRow)
            else:
                self.soldaTable.removeRow(rowCount - 1)


app = QApplication([])  # Cria, instancia a aplicação
window = MatplotlibWidget()  # Cria, instancia a janela
window.show()  # Mostra a janela
app.exec_()  # Roda o programa
