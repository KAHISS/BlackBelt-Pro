# libs of python ==========
from tkinter import ttk
from tkcalendar import DateEntry
# my modules ==============
from databaseConnection import Criptography
from functions import *
from interface import Interface


class Aplication(
    Interface,
    FunctionsOfSchedule,
    FunctionsOfStudentInformations,
    FunctionsOfCashManagement,
    FunctionsOfLogin,
    FunctionsOfConfigurations
):

    def __init__(self):
        self.lineTreeviewColor = {}
        self.lastSearch = {}
        self.dataBases = {
            'schedule': DataBase('resources/Agendamentos.db'),
            'informations': DataBase('resources/Informações.db'),
            'cash': DataBase('resources/Caixa.db'),
            'config': DataBase('resources/config.db')
        }
        self.criptography = Criptography()
        self.openColorPicker = True
        super().__init__()
        self.login_window()

    def login_window(self):
        self.loginWindow = Tk()
        self.loginWindow.title('Login - BlackBelt Pro')
        width = self.loginWindow.winfo_screenwidth()
        height = self.loginWindow.winfo_screenheight()
        posx = width / 2 - 700 / 2
        posy = height / 2 - 400 / 2
        self.loginWindow.geometry('700x400+%d+%d' % (posx, posy))
        self.loginWindow.config(bg="#ffffff")
        self.loginWindow.iconphoto(False, PhotoImage(file=self.dataBases['config'].searchDatabase('SELECT * FROM Logo')[0][0]))

        # logo image ==============================
        logoImage = self.labels(
            self.loginWindow, '', 0.009, 0.01, width=0.48, height=0.98, position=CENTER, custom='custom',
            photo=self.image('assets/logoPreta.png', (288, 203))[0]
        )

        # frame of inputs =========================
        frameInputs = self.frame(self.loginWindow, 0.5, 0.005, 0.49, 0.985, border=2, radius=10)

        # name login ---------------------------
        labelLogin = self.labels(
            frameInputs, '', 0.256, 0.05, width=0.65, height=0.2, position=CENTER, size=90, color='#3b321a',
            photo=self.image('assets/login.png', (200, 100))[0]
        )

        # user name and password -----------------------------
        userName = self.entry(
            frameInputs, 0.1, 0.3, 0.8, 0.12, type_entry='entryLogin', border=2, radius=10,
            place_text='Usuário'
        )
        userName.bind('<FocusIn>', lambda e: userName.configure(fg_color=self.colorsOfEntrys[0]))

        password = self.entry(
            frameInputs, 0.1, 0.5, 0.8, 0.12, type_entry='entryLogin', border=2, radius=10,
            place_text='Senha', show='*'
        )

        # visibility ---------------------------------
        visibilityPasswordBtn = self.button(
            frameInputs, '', 0.76, 0.53, 0.08, 0.05, photo=self.image('assets/icon_eyeClose.png', (26, 26))[0], custom='entry',
            type_btn='buttonPhoto', background='white', hover_cursor='white', function=lambda: self.toggle_visibility(password, visibilityPasswordBtn)
        )
        password.bind('<FocusIn>', lambda e: [password.configure(fg_color=self.colorsOfEntrys[0]), visibilityPasswordBtn.configure(fg_color=self.colorsOfEntrys[0])])
        password.bind('<Return>', lambda e: self.validating_user([userName, password, visibilityPasswordBtn], self.open_software, type_password='login', parameters={'e': ''}))

        # line separator higher --------------------
        lineHigher = self.line_separator(frameInputs, 0.05, 0.65)

        # button of login and button of register ----------------------
        loginBtn = self.button(
            frameInputs, 'Iniciar sessão', 0.1, 0.72, 0.8, 0.1,
            function=lambda: self.validating_user([userName, password, visibilityPasswordBtn], self.open_software, type_password='login', parameters={'e': ''}),
        )
        closeBtn = self.button(
            frameInputs, 'Fechar', 0.1, 0.85, 0.8, 0.1,
            function=lambda: self.loginWindow.destroy()
        )
        self.loginWindow.mainloop()

    # ================================== main window configure =======================================
    def main_window(self):
        # screen configure ===================================
        self.root = Toplevel()
        self.root.title('BlackBelt Pro')
        self.root.state('zoomed')
        self.root.geometry(f'{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}')
        self.root.configure(background="#ffffff")
        self.root.wm_protocol('WM_DELETE_WINDOW', lambda: [self.loginWindow.destroy(), self.backup_dataBaes_discret()])
        self.root.iconphoto(False, PhotoImage(file=self.dataBases['config'].searchDatabase('SELECT * FROM Logo')[0][0]))
        # event bind ============================================
        self.root.bind_all('<Control-b>', lambda e: self.backup_dataBaes())
        self.root.bind_all('<Control-l>', lambda e: self.loading_database())
        # style notebook
        style = ttk.Style()
        style.configure("TNotebook.Tab", font=("Helvetica", 13, "bold"), foreground=self.colorsOfLabels[1])

        # style treeviews ==================================================
        self.style_treeview = ttk.Style()
        self.style_treeview.theme_use('vista')
        self.style_treeview.configure('Treeview', rowheight=25, fieldbackground='#261c20', foreground=self.colorsOfTreeviews[2], font='Arial 13')
        self.style_treeview.map('Treeview',
                                background=[('selected', '#ff4747')],  # Cor de fundo da seleção
                                foreground=[('selected', 'white')]
                                )
        # Cor do texto da seleção
        self.photosAndIcons = {
            'pdf': self.image('assets/icon_pdf.png', (46, 46)),
            'informações': self.image('assets/icon_informacoes.png', (46, 46)),
            'random': self.image('assets/icon_random.png', (36, 36)),
            'image': self.image('assets/icon_imagem.png', (26, 26)),
            'costumer': self.image('assets/icon_no_picture.png', (76, 76)),
            'employee': self.image('assets/icon_no_picture.png', (76, 76)),
            'productUse': self.image('assets/icon_product.png', (76, 76)),
            'productSale': self.image('assets/icon_product.png', (76, 76)),
            'productUseUnusable': self.image('assets/icon_product.png', (76, 76)),
            'productSaleSold': self.image('assets/icon_product.png', (76, 76)),
            'barCode': self.image('assets/icon_barCode.png', (76, 76)),
        }
        self.mainTabview = ttk.Notebook(self.root)
        self.mainTabview.place(relx=0, rely=0.01, relwidth=1, relheight=1)

        # schedule ============================================================
        self.mainScheduleFrame = self.main_frame_notebook(self.mainTabview, ' Agenda ')
        self.scheduleManagementTabview = self.notebook(self.mainScheduleFrame)
        # schedule management ---------------------------------------------------
        self.scheduleFrame = self.main_frame_notebook(self.scheduleManagementTabview, ' Gerenciamento de agenda ')
        self.frame_schedule()

        # information ============================================================
        self.mainInformationFrame = self.main_frame_notebook(self.mainTabview, ' Cadastro & Informações ')
        self.informationsManagementTabview = self.notebook(self.mainInformationFrame)
        # costumers management ---------------------------------------------------
        self.costumersFrame = self.main_frame_notebook(self.informationsManagementTabview, ' Alunos ')
        self.frame_customers()
        # bar code management ---------------------------------------------------
        self.userFrame = self.main_frame_notebook(self.informationsManagementTabview, ' Usuários ')
        self.frame_users()

        # cash register ============================================================
        self.mainCashRegisterFrame = self.main_frame_notebook(self.mainTabview, ' Caixa ')
        self.cashManagementTabview = self.notebook(self.mainCashRegisterFrame)
        # cash management ---------------------------------------------------
        self.cashFrame = self.main_frame_notebook(self.cashManagementTabview, ' Gerenciamento de caixa ')
        self.frame_cash_register_management_day()

        # configuration ============================================================
        self.configurationFrame = self.main_frame_notebook(self.mainTabview, ' Configurações ')
        self.configurationTabview = self.notebook(self.configurationFrame)
        # costumization ---------------------------------------------------
        self.costumizationFrame = self.main_frame_notebook(self.configurationTabview, ' Customização ')
        # costimizators ===============================================
        self.frameForCostumizations = self.frame(self.costumizationFrame, 0, 0.01, 0.999, 0.95)
        self.frame_costumization_buttons()
        self.frame_costumization_frames()
        self.frame_costumization_tabview()
        self.frame_costumization_treeview()
        self.frame_costumization_entrys()
        self.frame_costumization_labels()
        self.save()
        # loadings configs ---------------------------
        self.load_configs()

        # filling in lists -----------------------------------------
        self.refresh_combobox_student()

        # keeping window ===========================================
        self.root.mainloop()

    # =================================  schedule configuration  ======================================
    def frame_schedule(self):
        # frame inputs ==========================================
        self.frameInputsSchedule = self.frame(self.scheduleFrame, 0.005, 0.01, 0.989, 0.43)

        # custom -------------
        labelCustom = self.labels(self.frameInputsSchedule, 'Aluno:', 0.02, 0.22, width=0.08)
        self.customScheduleEntry = self.entry(self.frameInputsSchedule, 0.12, 0.22, 0.2, 0.12, type_entry='list')

        # value -------------
        labelValue = self.labels(self.frameInputsSchedule, 'Valor:', 0.02, 0.36, width=0.15)
        self.valueScheduleEntry = self.entry(self.frameInputsSchedule, 0.12, 0.36, 0.2, 0.12, type_entry='entry')

        # method pay -------------
        labelMethodPay = self.labels(self.frameInputsSchedule, 'M/Pagamento:', 0.02, 0.50, width=0.15)
        self.methodPayScheduleEntry = self.entry(
            self.frameInputsSchedule, 0.155, 0.50, 0.165, 0.12, type_entry='list',
            value=['DINHEIRO', 'CARTÃO', 'TRANSFERÊNCIA', 'NOTA', 'SEM PAGAMENTO']
        )

        # date -------------
        labelDate = self.labels(self.frameInputsSchedule, 'Pagamento:', 0.34, 0.22, width=0.16)
        self.dateScheduleEntry = self.entry(self.frameInputsSchedule, 0.46, 0.22, 0.159, 0.12, type_entry='date')
        self.dateScheduleEntry.insert(0, datetime.today().strftime('%d/%m/%Y'))

        # marking ----------
        labelMarking = self.labels(self.frameInputsSchedule, 'Mensalidade:', 0.34, 0.36, width=0.12, custom='optional')
        self.markingScheduleEntry = self.entry(self.frameInputsSchedule, 0.46, 0.36, 0.159, 0.12, type_entry='date')

        # events bind of frame inputs ===========================
        self.dateScheduleEntry.bind('<<DateEntrySelected>>', lambda e: self.search_schedule(self.treeviewSchedule, entryPicker()[2]))
        self.customScheduleEntry.bind('<KeyPress>', lambda e: self.customScheduleEntry.configure(
            values=[name[1] for name in self.search_student(informations=self.searching_list(self.customScheduleEntry.get(), 12, 'nome'), save_seacrh=False, insert=False)]
        ))

        # delete informations -------------
        deleteInformationsInputs = self.button(
            self.frameInputsSchedule, 'apagar', 0.003, 0.87, 0.04, 0.12, function=lambda: self.insert_informations_entrys(entryPicker()[1], self.treeviewSchedule, False),
            photo=self.image('assets/clear_inputs.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # frame treeview ==================
        self.frameTreeviewSchedule = self.frame(self.scheduleFrame, 0.005, 0.45, 0.989, 0.53)

        # Treeview -----------------------------------------------------
        informationOfTable = ('ID', 'Aluno', 'Valor', 'Método de Pagamento', 'Data', 'pagamento')
        self.treeviewSchedule = self.treeview(self.frameTreeviewSchedule, informationOfTable)
        self.lineTreeviewColor['schedule'] = 0
        # event bind treeview ==========================================
        self.treeviewSchedule.bind("<Double-Button-1>", lambda e: self.insert_informations_entrys(entryPicker()[1], self.treeviewSchedule))

        # save last search schedule ===================================
        self.lastSearch['schedule'] = ''

        # buttons management ===========================================
        functions = {
            'register': lambda: self.register_scheduling(entryPicker()[0], self.treeviewSchedule, entryPicker()[1]),
            'search': lambda: self.search_schedule(self.treeviewSchedule, entryPicker()[0]),
            'order': lambda e: self.search_schedule(self.treeviewSchedule, entryPicker()[0]),
            'update': lambda: self.update_schedule(self.treeviewSchedule, entryPicker()[0], entryPicker()[1]),
            'delete': lambda: self.delete_schedule(self.treeviewSchedule),
            'pdf': lambda: self.create_pdf_schedule(self.treeviewSchedule),
            'informations': lambda: self.message_informations_schedule(self.treeviewSchedule)
        }
        self.orderBtnSchedule = self.tab_of_buttons(0.675, 0.02, 0.3, 0.9, self.frameInputsSchedule, functions, self.photosAndIcons, informationOfTable, type_btns='complete')

        # pick up entrys ===========================
        def entryPicker():
            entrysGet = []
            entrys = []
            for widget in self.frameInputsSchedule.winfo_children():
                if isinstance(widget, CTkComboBox) or isinstance(widget, DateEntry) or isinstance(widget, CTkEntry):
                    entrysGet.append(widget.get())
                    entrys.append(widget)
            entrysGet.append(self.orderBtnSchedule.get())
            return [entrysGet, entrys, ['', '', '', self.dateScheduleEntry.get(), '', self.orderBtnSchedule.get()]]

        # init search for day ===============================================
        self.search_schedule(self.treeviewSchedule, entryPicker()[0])

    # =================================  informations configuration  ======================================
    def frame_customers(self):
        # frame photo ==========================================
        self.framePhotoClient = self.frame(self.costumersFrame, 0.005, 0.01, 0.13, 0.3)

        # photo ----------
        self.labelClient = self.labels(self.framePhotoClient, '', 0.009, 0.01, width=0.98, height=0.98, photo=self.photosAndIcons['costumer'][0], position=CENTER)

        # observation --------------------
        self.observationClientEntry = self.text_box(self.costumersFrame, 0.005, 0.32, 0.13, 0.12)

        # frame inputs ==========================================
        self.frameInputsClient = self.frame(self.costumersFrame, 0.14, 0.01, 0.855, 0.43)

        # name -------------
        labelName = self.labels(self.frameInputsClient, 'Nome:', 0.02, 0.08, width=0.08)
        self.nameClientEntry = self.entry(self.frameInputsClient, 0.1, 0.08, 0.2, 0.12, type_entry='entry')

        # Age -------------
        labelAge = self.labels(self.frameInputsClient, 'Idade:', 0.02, 0.22, width=0.15)
        self.AgeStudentEntry = self.entry(self.frameInputsClient, 0.1, 0.22, 0.2, 0.12, type_entry='entry')

        # height -------------
        labelHeight = self.labels(self.frameInputsClient, 'Altura:', 0.02, 0.36, width=0.15)
        self.heightStudentEntry = self.entry(self.frameInputsClient, 0.1, 0.36, 0.20, 0.12, type_entry='entry')

        # width -------------
        labelWidth = self.labels(self.frameInputsClient, 'Peso:', 0.02, 0.50, width=0.15)
        self.widhtStudentEntry = self.entry(self.frameInputsClient, 0.1, 0.50, 0.20, 0.12, type_entry='entry')

        # belt -------------
        labelBelt = self.labels(self.frameInputsClient, 'Faixa:', 0.02, 0.64, width=0.20)
        self.beltEntry = self.entry(
            self.frameInputsClient, 0.1, 0.64, 0.165, 0.12, type_entry='list',
            value=['BRANCA', 'CINZA', 'AMARELA', 'LARANJA', 'VERDE', 'AZUL', 'ROXA', 'MARROM', 'PRETA']
        )

        # degree -------------
        labelDegree = self.labels(self.frameInputsClient, 'Grau:', 0.02, 0.78, width=0.15)
        self.DegreeEntry = self.entry(self.frameInputsClient, 0.1, 0.78, 0.20, 0.12, type_entry='entry')

        # health -------------
        labelHealth = self.labels(self.frameInputsClient, 'Saudável:', 0.32, 0.08, width=0.15)
        self.healthBtn = StringVar(value='')
        yesh = self.button(
            self.frameInputsClient, 'Sim', 0.44, 0.09, 0.12, 0.1, type_btn='radioButton',
            value='Sim', retur_variable=self.healthBtn
        )
        noh = self.button(
            self.frameInputsClient, 'Não', 0.51, 0.09, 0.12, 0.1, type_btn='radioButton',
            value='Não', retur_variable=self.healthBtn
        )

        # problem health -------------
        labelProblemHealth = self.labels(self.frameInputsClient, 'P/Saúde:', 0.32, 0.22, width=0.15)
        self.problemHealthClientEntry = self.entry(self.frameInputsClient, 0.44, 0.22, 0.2, 0.12, type_entry='entry')

        # limitation -------------
        labelLimitation = self.labels(self.frameInputsClient, 'limitação:', 0.32, 0.36, width=0.16)
        self.limitationBtn = StringVar(value='')
        yesl = self.button(
            self.frameInputsClient, 'Sim', 0.44, 0.36, 0.12, 0.1, type_btn='radioButton',
            value='Sim', retur_variable=self.limitationBtn
        )
        nol = self.button(
            self.frameInputsClient, 'Não', 0.51, 0.36, 0.12, 0.1, type_btn='radioButton',
            value='Não', retur_variable=self.limitationBtn
        )

        # which limitation -----------------
        labelWhichLimitation = self.labels(self.frameInputsClient, 'Q/Limitação:', 0.32, 0.50, width=0.16)
        self.whichLimitationClientEntry = self.entry(self.frameInputsClient, 0.44, 0.50, 0.2, 0.12, type_entry='entry')

        # phone -----------------
        labelPhone = self.labels(self.frameInputsClient, 'Telefone:', 0.32, 0.64, width=0.16)
        self.phoneEntry = self.entry(self.frameInputsClient, 0.44, 0.64, 0.2, 0.12, type_entry='entry')

        # RG ---------
        labelRG = self.labels(self.frameInputsClient, 'RG:', 0.32, 0.78, width=0.16)
        self.RGClientEntry = self.entry(self.frameInputsClient, 0.44, 0.78, 0.2, 0.12, type_entry='entry')

        # CPF -------------
        labelCPF = self.labels(self.frameInputsClient, 'CPF:', 0.66, 0.08, width=0.08)
        self.CPFClientEntry = self.entry(self.frameInputsClient, 0.76, 0.08, 0.2, 0.12, type_entry='entry')

        # adress -----------------
        labelAdress = self.labels(self.frameInputsClient, 'Endereço:', 0.66, 0.22, width=0.16)
        self.adressClientEntry = self.entry(self.frameInputsClient, 0.76, 0.22, 0.2, 0.12, type_entry='entry')

        # zip code -----------------
        labelZipCode = self.labels(self.frameInputsClient, 'CEP:', 0.66, 0.36, width=0.16)
        self.zipCodeClientEntry = self.entry(self.frameInputsClient, 0.76, 0.36, 0.125, 0.12, type_entry='entry')

        # district -----------------
        labelDistrict = self.labels(self.frameInputsClient, 'Bairro:', 0.66, 0.50, width=0.16)
        self.districtClientEntry = self.entry(self.frameInputsClient, 0.76, 0.50, 0.2, 0.12, type_entry='entry')

        # city -----------------
        labelCity = self.labels(self.frameInputsClient, 'Cidade:', 0.66, 0.64, width=0.16)
        self.cityClientEntry = self.entry(self.frameInputsClient, 0.76, 0.64, 0.2, 0.12, type_entry='entry')

        # state -----------------
        labelState = self.labels(self.frameInputsClient, 'Estado:', 0.66, 0.78, width=0.16)
        self.stateClientEntry = self.entry(self.frameInputsClient, 0.76, 0.78, 0.2, 0.12, type_entry='entry')

        # delete informations -------------
        deleteInformationsInputs = self.button(
            self.frameInputsClient, '', 0.003, 0.87, 0.04, 0.12, function=lambda: self.insert_informations_entrys(entryPicker()[1], self.treeviewStudent, False, type_insert='advanced', table='Clientes', photo='costumer'),
            photo=self.image('assets/clear_inputs.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # cash flow -------------
        cashFlow = self.button(
            self.frameInputsClient, '', 0.05, 0.875, 0.04, 0.10,
            function=lambda: self.active_monthly_payments(self.treeviewStudent),
            photo=self.image('assets/icon_cashFlow.png', (26, 27))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # document -------------
        document = self.button(
            self.frameInputsClient, '', 0.965, 0.875, 0.02, 0.11,
            function=lambda: self.create_record(self.selection_treeview(self.treeviewStudent)),
            photo=self.image('assets/documento-de-texto.png', (26, 27))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # events bind of frameInputs =========================
        noh.bind('<Button-1>', lambda e: [
                self.problemHealthClientEntry.configure(state='normal', fg_color='#ffffff'),
                self.problemHealthClientEntry.delete(0, END),
            ]
        )
        yesh.bind(
            '<Button-1>', lambda e: [
                self.problemHealthClientEntry.delete(0, END),
                self.problemHealthClientEntry.insert(0, 'NENHUM PROBLEMA'),
                self.problemHealthClientEntry.configure(state='disable', fg_color='#d8d8d8')
            ]
        )
        nol.bind(
            '<Button-1>', lambda e: [
                self.whichLimitationClientEntry.delete(0, END),
                self.whichLimitationClientEntry.insert(0, 'NENHUMA LIMITAÇÂO'),
                self.whichLimitationClientEntry.configure(state='disable', fg_color='#d8d8d8')
            ]
        )
        yesl.bind(
            '<Button-1>', lambda e: [
                self.whichLimitationClientEntry.configure(state='normal', fg_color='#ffffff'),
                self.whichLimitationClientEntry.delete(0, END)
            ]
        )
        self.phoneEntry.bind('<FocusOut>', lambda e: self.treating_numbers(info=self.phoneEntry, type_treating=9))
        self.labelClient.bind('<Double-Button-1>', lambda e: self.pick_picture(self.labelClient, 'costumer'))
        self.zipCodeClientEntry.bind(
            '<FocusOut>',
            lambda e: [
                self.request_adrees(self.zipCodeClientEntry.get(), [self.districtClientEntry, self.cityClientEntry, self.stateClientEntry]),
                self.treating_numbers(self.zipCodeClientEntry, type_treating=10)
            ]
        )
        self.CPFClientEntry.bind('<FocusOut>', lambda e: self.treating_numbers(self.CPFClientEntry, type_treating=10))
        self.RGClientEntry.bind('<FocusOut>', lambda e: self.treating_numbers(self.RGClientEntry, type_treating=11))

        # frame treeview ==================
        self.frameTreeviewStudent = self.frame(self.costumersFrame, 0.005, 0.45, 0.689, 0.53)

        # Treeview -----------------------------------------------------
        informationOfTable = ('ID', 'Nome', 'Idade', 'Altura', 'Peso', 'Faixa', 'Grau', 'Saudável', 'Problema de saíde', 'Limitação', 'Qual limitação', 'Telefone de emergência', 'RG', 'CPF', 'Endereço', 'CEP', 'Bairro', 'Cidade', 'Estado', 'Foto', 'Observações')
        self.treeviewStudent = self.treeview(self.frameTreeviewStudent, informationOfTable)
        self.lineTreeviewColor['student'] = 0
        # event bind treeview ==========================================
        self.treeviewStudent.bind("<Double-Button-1>", lambda e: self.insert_informations_entrys(entryPicker()[1], self.treeviewStudent, type_insert='advanced', table='Alunos', photo='costumer'))

        # save last search schedule ===================================
        self.lastSearch['student'] = ''

        # buttons management ============
        functions = {
            'register': lambda: self.register_student(entryPicker()[0], self.treeviewStudent),
            'search': lambda: self.search_student(self.treeviewStudent, entryPicker()[0]),
            'order': lambda e: self.search_student(self.treeviewStudent, entryPicker()[0]),
            'update': lambda: self.update_student(self.treeviewStudent, entryPicker()[0], entryPicker()[1]),
            'delete': lambda: self.delete_student(self.treeviewStudent),
            'pdf': lambda: self.create_pdf_student(self.treeviewStudent),
            'informations': lambda: self.message_informations_student(self.treeviewStudent)
        }
        self.orderBtnClient = self.tab_of_buttons(0.7, 0.48, 0.295, 0.4, self.costumersFrame, functions, self.photosAndIcons, informationOfTable[0:19])

        # pick up entrys ==========================
        def entryPicker():
            entrysGet = []
            entrys = []
            # entrys of frameInputs =============================
            for widget in self.frameInputsClient.winfo_children():
                if isinstance(widget, CTkComboBox) or isinstance(widget, DateEntry) or isinstance(widget, CTkEntry):
                    entrysGet.append(widget.get())
                    entrys.append(widget)

            # string var informations ======================
            entrysGet.insert(6, self.healthBtn.get())
            entrys.insert(6, self.healthBtn)
            entrysGet.insert(8, self.limitationBtn.get())
            entrys.insert(8, self.limitationBtn)

            # directory photo =======================
            entrysGet.append(self.photosAndIcons['costumer'][1].lower())

            # label photo =================================
            entrys.append(self.labelClient)

            # observations informations ====================
            entrysGet.append(self.observationClientEntry.get("1.0", "end-1c"))
            entrys.append(self.observationClientEntry)

            # order informations and ==========================
            entrysGet.append(self.orderBtnClient.get())
            return [entrysGet, entrys]

        # init search for day ===============================================
        self.search_student(self.treeviewStudent, entryPicker()[0])

    def frame_users(self):
        # frame inputs =========================================
        self.frameInputsUsers = self.frame(self.userFrame, 0.195, 0.01, 0.6, 0.43)

        # user --------------------
        labelUser = self.labels(self.frameInputsUsers, 'Usuário:', 0.07, 0.25, width=0.1)
        self.userEntry = self.entry(self.frameInputsUsers, 0.20, 0.25, 0.23, 0.12, type_entry='entry')

        # password -------------------
        labelPassword = self.labels(self.frameInputsUsers, 'Senha:', 0.07, 0.45, width=0.1)
        self.passwordEntry = self.entry(self.frameInputsUsers, 0.20, 0.45, 0.23, 0.12, type_entry='entry')

        # level -------------------
        labelLevel = self.labels(self.frameInputsUsers, 'Nivel:', 0.07, 0.65, width=0.1)
        self.levelEntry = self.entry(
            self.frameInputsUsers, 0.20, 0.65, 0.23, 0.12, type_entry='list',
            value=['ADMINISTRADOR', 'USUÁRIO']
        )

        # delete informations -------------
        deleteInformationsInputs = self.button(
            self.frameInputsUsers, 'apagar', 0.003, 0.87, 0.05, 0.12, function=lambda: self.insert_informations_entrys(entryPicker()[1], self.treeviewUsers, False, type_insert='advanced'),
            photo=self.image('assets/clear_inputs.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # frame treeview ==================
        self.frameTreeviewUsers = self.frame(self.userFrame, 0.195, 0.45, 0.6, 0.53)

        # Treeview -----------------------------------------------------
        informationOfTable = ('ID', 'Usuário', 'Senha', 'Nivel')
        self.treeviewUsers = self.treeview(self.frameTreeviewUsers, informationOfTable, max_width=380)
        self.lineTreeviewColor['users'] = 0
        # event bind treeview ==========================================
        self.treeviewUsers.bind("<Double-Button-1>", lambda e: self.insert_informations_entrys(entryPicker()[1], self.treeviewUsers))

        # save last search schedule ===================================
        self.lastSearch['users'] = ''

        # buttons management ============
        functions = {
            'register': lambda: self.password_window(self.register_users, {'treeview': self.treeviewUsers, 'informatons': entryPicker()[0]}),
            'search': lambda: self.search_users(self.treeviewUsers, entryPicker()[0]),
            'order': lambda e: self.search_users(self.treeviewUsers, entryPicker()[0]),
            'update': lambda: self.password_window(self.update_users, {'treeview': self.treeviewUsers, 'informatons': entryPicker()[0]}),
            'delete': lambda: self.password_window(self.delete_users, {'treeview': self.treeviewUsers})
        }
        self.buttons = self.tab_of_buttons(0.49, 0.02, 0.45, 0.9, self.frameInputsUsers, functions, self.photosAndIcons, informationOfTable, treeview='no')

        def entryPicker():
            entrysGet = []
            entrys = []
            # entrys of frameInputs =============================
            for widget in self.frameInputsUsers.winfo_children():
                if isinstance(widget, CTkComboBox) or isinstance(widget, CTkEntry):
                    entrysGet.append(widget.get())
                    entrys.append(widget)
            return [entrysGet, entrys]

    # ================================== cash register configuration ===============================

    def frame_cash_register_management_day(self):

        # frame inputs ==========================================
        self.frameInputsCashDay = self.frame(self.cashFrame, 0.14, 0.01, 0.855, 0.43)

        # observation --------------------
        self.observationCashDayEntry = self.text_box(self.cashFrame, 0.005, 0.01, 0.13, 0.43)

        # Custom -------------
        labelCustom = self.labels(self.frameInputsCashDay, 'T/Alunos:', 0.02, 0.08, width=0.12)
        self.customDayEntry = self.entry(self.frameInputsCashDay, 0.14, 0.08, 0.18, 0.12, type_entry='entry')

        # card -------------
        labelCard = self.labels(self.frameInputsCashDay, 'T/Cartão:', 0.02, 0.22, width=0.15)
        self.cardDayEntry = self.entry(self.frameInputsCashDay, 0.14, 0.22, 0.18, 0.12, type_entry='entry')

        # money -------------
        labelMoney = self.labels(self.frameInputsCashDay, 'T/Dinheiro:', 0.02, 0.36, width=0.15)
        self.moneyDayEntry = self.entry(self.frameInputsCashDay, 0.14, 0.36, 0.18, 0.12, type_entry='entry')

        # tranfer -------------
        labelTransfer = self.labels(self.frameInputsCashDay, 'T/Transferência:', 0.02, 0.50, width=0.15)
        self.transferDayEntry = self.entry(self.frameInputsCashDay, 0.17, 0.50, 0.15, 0.12, type_entry='entry')

        # note -------------
        labelNote = self.labels(self.frameInputsCashDay, 'T/Nota:', 0.02, 0.64, width=0.16)
        self.noteDayEntry = self.entry(self.frameInputsCashDay, 0.14, 0.64, 0.18, 0.12, type_entry='entry')

        # received -----------------
        labelReceived = self.labels(self.frameInputsCashDay, 'T/Recebido:', 0.02, 0.78, width=0.16)
        self.receivedDayEntry = self.entry(self.frameInputsCashDay, 0.14, 0.78, 0.19, 0.12, type_entry='entry')

        # date -----------------
        labelDate = self.labels(self.frameInputsCashDay, 'Data:', 0.34, 0.08, width=0.16)
        self.dateDayEntry = self.entry(self.frameInputsCashDay, 0.44, 0.08, 0.14, 0.12, type_entry='date', validity='yes')
        self.dateDayEntry.delete(0, 3)

        # status -----------------
        labelStatus = self.labels(self.frameInputsCashDay, 'Status:', 0.34, 0.22, width=0.16, custom='optional')
        self.statusDayEntry = self.entry(
            self.frameInputsCashDay, 0.44, 0.22, 0.2, 0.12, type_entry='list',
            value=['MÊS EM ANDAMENTO', 'MÊS FINALIZADO']
        )

        # exit -----------------
        labelExit = self.labels(self.frameInputsCashDay, 'Saida:', 0.34, 0.36, width=0.16, custom='optional')
        self.exitDayEntry = self.entry(self.frameInputsCashDay, 0.44, 0.36, 0.2, 0.12, type_entry='entry')

        # metody exit -----------------
        labelMetodyExit = self.labels(self.frameInputsCashDay, 'M/Saida:', 0.34, 0.50, width=0.16, custom='optional')
        self.MetodyExitDayEntry = self.entry(
            self.frameInputsCashDay, 0.44, 0.50, 0.2, 0.12, type_entry='list',
            value=['DINHEIRO', 'CARTÃO', 'TRANSFERÊNCIA', 'NOTA', 'SEM PAGAMENTO']
        )

        # delete informations -------------
        deleteInformationsInputs = self.button(
            self.frameInputsCashDay, '', 0.003, 0.87, 0.04, 0.12,
            function=lambda: self.insert_informations_entrys(entryPicker()[1], self.treeviewCashDay, False, type_insert='advanced'),
            photo=self.image('assets/clear_inputs.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # cash flow -------------
        cashFlow = self.button(
            self.frameInputsCashDay, '', 0.05, 0.875, 0.04, 0.10,
            function=lambda: self.password_window(self.pick_informations_for_cash, {'entrys': entryPicker()[1], 'date': self.dateDayEntry.get()}),
            photo=self.image('assets/icon_cashFlow.png', (26, 27))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # clearTreeview -------------
        clear = self.button(
            self.frameInputsCashDay, '', 0.1, 0.87, 0.04, 0.11,
            function=lambda: self.delete_informations_treeview(self.treeviewCashDay, self.lineTreeviewColor['cash']),
            photo=self.image('assets/clear_treeview.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # events bind ==========================
        self.dateDayEntry.bind('<FocusOut>', lambda e: self.dateDayEntry.delete(0, 3))
        self.dateDayEntry.bind("<<DateEntrySelected>>", lambda e: self.dateDayEntry.delete(0, 3))

        # frame treeview ==================
        self.frameTreeviewCashDay = self.frame(self.cashFrame, 0.005, 0.45, 0.989, 0.53)

        # Treeview -----------------------------------------------------
        informationOfTable = ('ID', 'T/Alunos', 'T/Cartão', 'T/Dinheiro', 'T/Transferência', 'T/nota', 'S/Cartão', 'S/Dinheiro', 'S/Transferência', 'S/Nota', 'T/Recebido', 'mês', 'Status')
        self.treeviewCashDay = self.treeview(self.frameTreeviewCashDay, informationOfTable)
        self.lineTreeviewColor['cash'] = 0
        # event bind treeview ==========================================
        self.treeviewCashDay.bind(
            "<Double-Button-1>", lambda e: self.insert_informations_entrys(entryPicker()[1], self.treeviewCashDay, type_insert='advanced', table='Gerenciamento_do_mês', data_base='cash')
        )
        # save last search schedule ===================================
        self.lastSearch['cash'] = ''

        # buttons management ============
        functions = {
            'register': lambda: self.password_window(
                self.register_cashManagement, {
                    'informations': entryPicker()[0],
                    'treeview': self.treeviewCashDay,
                }
            ),
            'search': lambda: self.password_window(
                self.search_cashManagement, {
                    'treeview': self.treeviewCashDay,
                    'informations': entryPicker()[0],
                }
            ),
            'order': lambda e: self.password_window(
                self.search_cashManagement, {
                    'treeview': self.treeviewCashDay,
                    'informations': entryPicker()[0],

                }
            ),
            'update': lambda: self.password_window(
                self.update_cashManagement, {
                    'treeview': self.treeviewCashDay,
                    'informations': entryPicker()[0],
                }
            ),
            'delete': lambda: self.password_window(
                self.delete_cashManagement, {
                    'treeview': self.treeviewCashDay,
                }
            ),
            'pdf': lambda: self.password_window(
                self.create_pdf_cashManagement, {
                    'treeview': self.treeviewCashDay,
                }
            ),
            'informations': lambda: self.password_window(
                self.message_informations_cashManagement, {
                    'treeview': self.treeviewCashDay,
                }
            ),
        }
        self.orderBtnDay = self.tab_of_buttons(0.675, 0.02, 0.3, 0.9, self.frameInputsCashDay, functions, self.photosAndIcons, informationOfTable)

        # pick up entrys ==========================
        def entryPicker():
            entrysGet = []
            entrys = []
            # entrys of frameInputs =============================
            for widget in self.frameInputsCashDay.winfo_children():
                if isinstance(widget, CTkComboBox) or isinstance(widget, DateEntry) or isinstance(widget, CTkEntry):
                    entrysGet.append(widget.get())
                    entrys.append(widget)

            # observations informations ====================
            entrysGet.append(self.observationCashDayEntry.get("1.0", "end-1c"))
            entrys.append(self.observationCashDayEntry)

            # order =============================================
            entrysGet.append(self.orderBtnDay.get())
            return [entrysGet, entrys]

        # init search =============================
        self.search_cashManagement(
            self.treeviewCashDay,
            self.searching_list('', 10, 'ID'),
            insert=False
        )

    # ================================== cash register configuration ===============================

    def frame_costumization_buttons(self):
        # buttons -------------------------
        self.frameForButtons = self.frame(self.frameForCostumizations, 0.02, 0.02, 0.2, 0.3, border_color='#d2d2d2', type_frame='labelFrame', text='Botões')
        # -> background
        background = self.labels(self.frameForButtons, 'Cor de fundo:', 0.03, 0.03, 0.5, 0.1, size=13)
        colorBgEntry = self.entry(self.frameForButtons, 0.4, 0.027, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerBg = self.button(
            self.frameForButtons, '', 0.7, 0.001, 0.15, 0.17,
            function=lambda: self.colorPicker(Btn, 'fg_color', colorBgEntry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )
        # -> text color
        textColor = self.labels(self.frameForButtons, 'Cor do texto:', 0.03, 0.2, 0.5, 0.1, size=13)
        colorFgEntry = self.entry(self.frameForButtons, 0.4, 0.2, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerFg = self.button(
            self.frameForButtons, '', 0.7, 0.17, 0.15, 0.17,
            function=lambda: self.colorPicker(Btn, 'text_color', colorFgEntry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )
        # -> text color
        borderColor = self.labels(self.frameForButtons, 'Cor da borda:', 0.03, 0.37, 0.5, 0.1, size=13)
        colorBdEntry = self.entry(self.frameForButtons, 0.4, 0.37, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerBd = self.button(
            self.frameForButtons, '', 0.7, 0.34, 0.15, 0.17,
            function=lambda: self.colorPicker(Btn, 'border_color', colorBdEntry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )
        # -> hover color
        hoverColor = self.labels(self.frameForButtons, 'Cor do hover:', 0.03, 0.54, 0.5, 0.1, size=13)
        colorHvEntry = self.entry(self.frameForButtons, 0.4, 0.54, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerHv = self.button(
            self.frameForButtons, '', 0.7, 0.51, 0.15, 0.17,
            function=lambda: self.colorPicker(Btn, 'hover_color', colorHvEntry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # events bind ==========================
        colorBgEntry.bind('<Return>', lambda e: self.colorPicker(Btn, 'fg_color', colorBgEntry, color_picker='no'))
        colorFgEntry.bind('<Return>', lambda e: self.colorPicker(Btn, 'text_color', colorFgEntry, color_picker='no'))
        colorBdEntry.bind('<Return>', lambda e: self.colorPicker(Btn, 'border_color', colorBdEntry, color_picker='no'))
        colorHvEntry.bind('<Return>', lambda e: self.colorPicker(Btn, 'hover_color', colorHvEntry, color_picker='no'))

        # line separator higher --------------------
        lineHigher = self.line_separator(self.frameForButtons, 0.03, 0.67)

        # demonstrative button ---------------------
        Btn = self.button(self.frameForButtons, 'Texto', 0.18, 0.78, 0.6, 0.2)

    def frame_costumization_frames(self):
        # buttons -------------------------
        self.frameForFrames = self.frame(self.frameForCostumizations, 0.02, 0.4, 0.2, 0.3, border_color='#d2d2d2', type_frame='labelFrame', text='Frames')

        # -> background
        background = self.labels(self.frameForFrames, 'Cor de fundo:', 0.03, 0.03, 0.5, 0.1, size=13)
        colorBgEntry = self.entry(self.frameForFrames, 0.4, 0.027, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerBg = self.button(
            self.frameForFrames, '', 0.7, 0.001, 0.15, 0.17,
            function=lambda: self.colorPicker(frame, 'fg_color', colorBgEntry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # -> border
        border = self.labels(self.frameForFrames, 'Cor da borda:', 0.03, 0.2, 0.5, 0.1, size=13)
        colorBdEntry = self.entry(self.frameForFrames, 0.4, 0.2, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerBd = self.button(
            self.frameForFrames, '', 0.7, 0.17, 0.15, 0.17,
            function=lambda: self.colorPicker(frame, 'border_color', colorBdEntry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # events bind ==========================
        colorBgEntry.bind('<Return>', lambda e: self.colorPicker(frame, 'fg_color', colorBgEntry, color_picker='no'))
        colorBdEntry.bind('<Return>', lambda e: self.colorPicker(frame, 'border_color', colorBdEntry, color_picker='no'))

        # line separator higher --------------------
        lineHigher = self.line_separator(self.frameForFrames, 0.03, 0.35)

        # demonstrative frame ---------------------
        frame = self.frame(self.frameForFrames, 0.14, 0.475, 0.67, 0.5)

    def frame_costumization_tabview(self):
        # buttons -------------------------
        self.frameForTabview = self.frame(self.frameForCostumizations, 0.38, 0.02, 0.2, 0.3, border_color='#d2d2d2', type_frame='labelFrame', text='Tabview')

        # -> background
        background = self.labels(self.frameForTabview, 'Cor de fundo:', 0.03, 0.03, 0.5, 0.1, size=13)
        colorBgEntry = self.entry(self.frameForTabview, 0.4, 0.027, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerBg = self.button(
            self.frameForTabview, '', 0.7, 0.001, 0.15, 0.17,
            function=lambda: self.colorPicker(tabview, 'fg_color', colorBgEntry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # -> border
        border = self.labels(self.frameForTabview, 'Cor da borda:', 0.03, 0.2, 0.5, 0.1, size=13)
        colorBdEntry = self.entry(self.frameForTabview, 0.4, 0.2, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerBd = self.button(
            self.frameForTabview, '', 0.7, 0.17, 0.15, 0.17,
            function=lambda: self.colorPicker(tabview, 'border_color', colorBdEntry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # events bind ==========================
        colorBgEntry.bind('<Return>', lambda e: self.colorPicker(tabview, 'fg_color', colorBgEntry, color_picker='no'))
        colorBdEntry.bind('<Return>', lambda e: self.colorPicker(tabview, 'border_color', colorBdEntry, color_picker='no'))

        # demonstrative tabview ---------------------
        tabview = self.tabview(self.frameForTabview, 0.14, 0.4, 0.67, 0.55)

        # line separator higher --------------------
        lineHigher = self.line_separator(self.frameForTabview, 0.03, 0.35)

    def frame_costumization_treeview(self):
        # buttons -------------------------
        self.frameForTreeview = self.frame(self.frameForCostumizations, 0.38, 0.35, 0.2, 0.4, border_color='#d2d2d2', type_frame='labelFrame', text='Tabela')

        # -> line1
        line1 = self.labels(self.frameForTreeview, 'Cor da linha 1:', 0.03, 0.03, 0.5, 0.06, size=13)
        colorL1Entry = self.entry(self.frameForTreeview, 0.4, 0.027, 0.3, 0.08, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerBg = self.button(
            self.frameForTreeview, '', 0.7, 0.001, 0.15, 0.13,
            function=lambda: self.colorPicker(treeview, 'tag1', colorL1Entry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # -> line2
        line2 = self.labels(self.frameForTreeview, 'Cor da linha 2:', 0.03, 0.15, 0.5, 0.06, size=13)
        colorL2Entry = self.entry(self.frameForTreeview, 0.4, 0.15, 0.3, 0.08, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerBd = self.button(
            self.frameForTreeview, '', 0.7, 0.12, 0.15, 0.13,
            function=lambda: self.colorPicker(treeview, 'tag2', colorL2Entry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # -> text color
        textColor = self.labels(self.frameForTreeview, 'Cor de texto:', 0.03, 0.27, 0.5, 0.06, size=13)
        colorFgEntry = self.entry(self.frameForTreeview, 0.4, 0.27, 0.3, 0.08, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerFg = self.button(
            self.frameForTreeview, '', 0.7, 0.24, 0.15, 0.13,
            function=lambda: self.colorPicker(treeview, 'text_color_treeview', colorFgEntry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # events bind ==========================
        colorL1Entry.bind('<Return>', lambda e: self.colorPicker(treeview, 'tag1', colorL1Entry, color_picker='no'))
        colorL2Entry.bind('<Return>', lambda e: self.colorPicker(treeview, 'tag2', colorL2Entry, color_picker='no'))
        colorFgEntry.bind('<Return>', lambda e: self.colorPicker(treeview, 'text_color_treeview', colorFgEntry, color_picker='no'))

        # demonstrative treeview ---------------------
        frameTreeview = self.frame(self.frameForTreeview, 0.02, 0.4, 0.97, 0.5, border_color='#d2d2d2')
        treeview = self.treeview(frameTreeview, ['informação 1'])
        self.lineTreeviewColor['demonstrative'] = 0
        self.insert_treeview_informations(treeview, ['Linha 1', 'linha2'], 'demonstrative')

    def frame_costumization_entrys(self):
        # buttons -------------------------
        self.frameForEntrys = self.frame(self.frameForCostumizations, 0.77, 0.02, 0.2, 0.3, border_color='#d2d2d2', type_frame='labelFrame', text='Entradas de texto')
        # -> background
        background = self.labels(self.frameForEntrys, 'Cor de fundo:', 0.03, 0.03, 0.5, 0.1, size=13)
        colorBgEntry = self.entry(self.frameForEntrys, 0.4, 0.027, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerBg = self.button(
            self.frameForEntrys, '', 0.7, 0.001, 0.15, 0.17,
            function=lambda: self.colorPicker(entry, 'fg_color', colorBgEntry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )
        # -> text color
        textColor = self.labels(self.frameForEntrys, 'Cor do texto:', 0.03, 0.2, 0.5, 0.1, size=13)
        colorFgEntry = self.entry(self.frameForEntrys, 0.4, 0.2, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerFg = self.button(
            self.frameForEntrys, '', 0.7, 0.17, 0.15, 0.17,
            function=lambda: self.colorPicker(entry, 'text_color', colorFgEntry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )
        # -> text color
        borderColor = self.labels(self.frameForEntrys, 'Cor da borda:', 0.03, 0.37, 0.5, 0.1, size=13)
        colorBdEntry = self.entry(self.frameForEntrys, 0.4, 0.37, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerBd = self.button(
            self.frameForEntrys, '', 0.7, 0.34, 0.15, 0.17,
            function=lambda: self.colorPicker(entry, 'border_color', colorBdEntry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # events bind ==========================
        colorBgEntry.bind('<Return>', lambda e: self.colorPicker(entry, 'fg_color', colorBgEntry, color_picker='no'))
        colorFgEntry.bind('<Return>', lambda e: self.colorPicker(entry, 'text_color', colorFgEntry, color_picker='no'))
        colorBdEntry.bind('<Return>', lambda e: self.colorPicker(entry, 'border_color', colorBdEntry, color_picker='no'))

        # line separator higher --------------------
        lineHigher = self.line_separator(self.frameForEntrys, 0.03, 0.54)

        # demonstrative button ---------------------
        entry = self.entry(self.frameForEntrys, 0.18, 0.70, 0.6, 0.2, type_entry='entry')
        entry.insert(0, 'Texto')

    def frame_costumization_labels(self):
        # buttons -------------------------
        self.frameForLabels = self.frame(self.frameForCostumizations, 0.77, 0.4, 0.2, 0.3, border_color='#d2d2d2', type_frame='labelFrame', text='Textos')

        # -> text color
        text1 = self.labels(self.frameForLabels, 'Cor de texto 1:', 0.03, 0.03, 0.5, 0.1, size=13)
        colorFg1Entry = self.entry(self.frameForLabels, 0.4, 0.027, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerFg1 = self.button(
            self.frameForLabels, '', 0.7, 0.001, 0.15, 0.17,
            function=lambda: self.colorPicker(text1, 'text_color', colorFg1Entry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        text2 = self.labels(self.frameForLabels, 'Cor de texto 2:', 0.03, 0.2, 0.5, 0.1, size=13)
        colorFg2Entry = self.entry(self.frameForLabels, 0.4, 0.2, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerFg2 = self.button(
            self.frameForLabels, '', 0.7, 0.17, 0.15, 0.17,
            function=lambda: self.colorPicker(text2, 'text_color', colorFg2Entry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # events bind ==========================
        colorFg1Entry.bind('<Return>', lambda e: self.colorPicker(text1, 'text_color', colorFg1Entry, color_picker='no'))
        colorFg2Entry.bind('<Return>', lambda e: self.colorPicker(text2, 'text_color', colorFg2Entry, color_picker='no'))

        # line separator higher --------------------
        lineHigher = self.line_separator(self.frameForLabels, 0.03, 0.35)

        # demonstrative labels ---------------------
        text1 = self.labels(self.frameForLabels, 'Texto 1', 0.33, 0.5, 0.3, 0.2)
        text2 = self.labels(self.frameForLabels, 'Texto 2', 0.33, 0.75, 0.3, 0.2, custom='optional')

    def save(self):
        # line separator higher --------------------
        lineHigher = self.line_separator(self.frameForCostumizations, 0.02, 0.8, width=0.95)

        # demonstrative labels ---------------------
        text1 = self.button(self.frameForCostumizations, 'Salvar', 0.75, 0.86, 0.2, 0.1, function=lambda: self.save_configs())


if __name__ == '__main__':
    app = Aplication()
