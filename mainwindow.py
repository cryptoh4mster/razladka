import matplotlib.figure
import wx
import pandas as pd

import settings
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from matplotlib.backends.backend_wx import NavigationToolbar2Wx


class MainWindow(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        super(MainWindow, self).__init__(*args, **kwds)

        self.SetTitle(u"Сегментирование временных рядов")

        # Дискрет, с которым будет строиться график
        # self._graphStep = 1

        # Установим размер главного окна
        self.SetSize((1920, 1080))

        # Заполнить главное окно элементами управления
        self._createGui()
        self.updateBtn.Bind(wx.EVT_BUTTON, handler=self._onUpdateClick)
        self.cusumBtn.Bind(wx.EVT_BUTTON, handler=self._onCusumClick)
        self.segmentBtn.Bind(wx.EVT_BUTTON, handler=self._onSegmentationClick)

    def _createGui(self):
        """
        Заполнить главное окно элементами управления
        """
        # Элементы управления для ввода m
        mLabel = wx.StaticText(self, -1, u"         Введите значение m - ")
        self.mText = wx.TextCtrl(self, -1, "1")
        self.mText.SetMinSize((40, -1))

        # Элементы управления для ввода n
        nLabel = wx.StaticText(self, -1, u"         Введите значение n  - ")
        self.nText = wx.TextCtrl(self, -1, "2")
        self.nText.SetMinSize((40, -1))

        # Элементы управления для ввода k
        kLabel = wx.StaticText(self, -1, u"             Введите значение k(глубина памяти) -")
        self.kText = wx.TextCtrl(self, -1, "1")
        self.kText.SetMinSize((40, -1))

        # Элементы управления для ввода h
        hLabel = wx.StaticText(self, -1, u"             Введите значение h(порог)                   -")
        self.hText = wx.TextCtrl(self, -1, "0")
        self.hText.SetMinSize((40, -1))

        # Кнопки для построения графиков
        self.updateBtn = wx.Button(self, -1, u"Построить график")
        self.updateBtn.SetMinSize((200, 20))
        self.cusumBtn = wx.Button(self, -1, u"Найти разладку")
        self.cusumBtn.SetMinSize((200, 20))
        self.segmentBtn = wx.Button(self, -1, u"Сегментировать участки")
        self.segmentBtn.SetMinSize((200, 20))

        # Сайзер для верхней строки с "Выберите..."
        labelSizer = wx.FlexGridSizer(1, 3, 0, 0)
        parametersLabel = wx.StaticText(self, -1, u"         Введите значения параметров:")
        graphLabel = wx.StaticText(self, -1, u"         Выберите временной ряд:")
        doLabel = wx.StaticText(self, -1, u"Выберите необходимое действие:")
        labelSizer.Add(parametersLabel, flag=wx.RIGHT, border=368)
        labelSizer.Add(graphLabel, flag=wx.RIGHT, border=100)
        labelSizer.Add(doLabel, flag=wx.RIGHT, border=2)

        # Сайзеры для m,k,radiobutton, button; n,h,radiobutton,button;
        mkSizer = wx.FlexGridSizer(1, 6, 0, 0)
        nhSizer = wx.FlexGridSizer(1, 6, 0, 0)
        radioSizer = wx.FlexGridSizer(1, 2, 0, 0)

        self.rb1 = wx.RadioButton(self, label='Нестационарный ряд', style=wx.RB_GROUP)
        self.rb2 = wx.RadioButton(self, label='Стационарный ряд')
        self.rb3 = wx.RadioButton(self, label='Выберите excel файл')

        # Добавление лейблов, кнопок и radiobutton в сайзеры
        mkSizer.Add(mLabel, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
        mkSizer.Add(self.mText, flag=wx.ALL | wx.ALIGN_LEFT, border=2)
        mkSizer.Add(kLabel, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
        mkSizer.Add(self.kText, flag=wx.RIGHT | wx.ALIGN_RIGHT, border=100)
        mkSizer.Add(self.rb1, flag=wx.RIGHT | wx.ALIGN_RIGHT, border=105)
        mkSizer.Add(self.updateBtn, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
        nhSizer.Add(nLabel, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
        nhSizer.Add(self.nText, flag=wx.ALL | wx.ALIGN_LEFT, border=2)
        nhSizer.Add(hLabel, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
        nhSizer.Add(self.hText, flag=wx.RIGHT | wx.RIGHT, border=100)
        nhSizer.Add(self.rb2, flag=wx.RIGHT | wx.ALIGN_RIGHT, border=120)
        nhSizer.Add(self.cusumBtn, flag=wx.ALL | wx.ALIGN_RIGHT, border=2)
        radioSizer.Add(self.rb3, flag=wx.LEFT, border=590)
        radioSizer.Add(self.segmentBtn, flag=wx.LEFT, border=111)

        # 1. Создание фигуры
        self.figure = matplotlib.figure.Figure(figsize=(4, 3), tight_layout=True)
        self.figure1 = matplotlib.figure.Figure(figsize=(4, 3), tight_layout=True)

        # 2. Создание осей
        self.axes = self.figure.add_subplot(1, 1, 1)
        self.axes1 = self.figure1.add_subplot(1, 1, 1)

        # 3. Создание панели для рисования с помощью Matplotlib
        self.canvas = FigureCanvasWxAgg(self, -1, self.figure)
        self.canvas.SetSize(100, 100)
        self.canvas1 = FigureCanvasWxAgg(self, -1, self.figure1)
        self.canvas.SetSize(100, 100)

        navToolbar = NavigationToolbar2Wx(self.canvas)
        navToolbar.BackgroundColour = 'White'
        navToolbar.SetMinSize((1600, -1))
        navToolbar1 = NavigationToolbar2Wx(self.canvas1)
        navToolbar1.SetMinSize((1600, -1))
        navToolbar1.BackgroundColour = 'White'

        # Размещение элементов управления в окне
        mainSizer = wx.FlexGridSizer(0, 1, 0, 0)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableRow(5)
        self.SetBackgroundColour('#f3f76a')

        # Размещение элементов интерфейса
        mainSizer.Add(labelSizer, flag=wx.ALL | wx.EXPAND, border=5)
        mainSizer.Add(mkSizer, flag=wx.ALL | wx.EXPAND, border=5)
        mainSizer.Add(nhSizer, flag=wx.ALL | wx.EXPAND, border=5)
        mainSizer.Add(radioSizer, flag=wx.ALL | wx.EXPAND, border=5)
        mainSizer.Add(navToolbar, flag=wx.TOP, border=5)
        mainSizer.Add(self.canvas, flag=wx.ALL | wx.EXPAND, border=0)
        mainSizer.Add(navToolbar1)
        mainSizer.Add(self.canvas1, flag=wx.ALL | wx.EXPAND, border=0)
        self.SetSizer(mainSizer)
        self.Layout()

    # Обработчик нажатия кнопки построения графика
    def _onUpdateClick(self, event):
        self._drawGraph()

    # Обработчик нажатия кнопки расчета кумулятивных сумм
    def _onCusumClick(self, event):
        self._drawCusum()

    # Обработчик нажатия кнопки сегментации
    def _onSegmentationClick(self, event):
        self._drawSegmentation()

    # Функция для отрисовки временного ряда
    def _drawGraph(self):
        global valuesY
        global valuesX
        global length
        valuesY = []
        if self.rb1.GetValue():
            excel = pd.read_excel('C:/22_11_2011.xlsx', sheet_name='Входное напряжение АВ')
            # values = excel['xi']
            # excel = pd.read_excel('C:/26_06_2013.xlsx', sheet_name='Sheet1')
            values = excel['xi']
            excel_values = values.values
            length = 500
            for i in range(0, length):
                valuesY.append(excel_values[i])
        if self.rb2.GetValue():
            excel = pd.read_excel('C:/stacionar1.xlsx', sheet_name='Лист1')
            values = excel['Генерация']
            excel_values = values.values
            length = 500
            for i in range(0, length):
                valuesY.append(excel_values[i])
        if self.rb3.GetValue():
            dialog = wx.FileDialog(None, 'Open')
            if dialog.ShowModal() == wx.ID_OK:
                path = dialog.GetPath()
            excel = pd.read_excel(path, sheet_name='Лист1')
            values = excel['xi']
            excel_values = values.values
            length = len(excel_values)
            for i in range(0, length):
                valuesY.append(excel_values[i])

        yvals = valuesY
        # !!!
        # Удалим предыдущий график, если он есть
        self.axes.clear()

        # Нарисуем новый график
        self.axes.plot(yvals, 'r-')

        # Включим сетку
        self.axes.grid()

        self.axes.legend([u"Временной ряд"])

        # Установим пределы по осям
        self.axes.set_xlim([0, length])

        # Обновим окно
        self.canvas.draw()

    # Функция для отрисовки кумулятивных сумм
    def _drawCusum(self):

        global s
        global h
        global k
        global l

        m = int(self.mText.Value)
        n = int(self.nText.Value)
        k = int(self.kText.Value)
        h = int(self.hText.Value)
        l = m+n
        values_s = settings.cumulative_sum(k, n, m, valuesY)
        s = values_s

        self.axes1.clear()
        self.axes1.plot(values_s, 'g-')
        self.axes1.grid()
        self.axes1.legend([u"Кумулятивные суммы"])
        self.axes1.set_xlim([0, length])
        self.canvas1.draw()

    # Функция для отрисовки сегментов
    def _drawSegmentation(self):
        self.axes.clear()
        disorders = settings.find_disorders(s, h)
        segments_data = settings.segmentation(disorders, valuesY, k, s, l)
        segments = segments_data[0]
        segments_lines = segments_data[1]
        min_value = min(valuesY)
        max_value = max(valuesY)
        self.axes.plot(valuesY, 'r-')
        self.axes.legend([u"Сегментированные участки"])
        self.axes.grid()
        self.axes.set_xlim([0, len(valuesY)])
        for i in range(len(segments_lines)):
            self.axes.vlines(segments_lines[i], min_value, max_value)
        self.canvas.draw()