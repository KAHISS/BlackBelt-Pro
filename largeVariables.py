from databaseConnection import DataBase

config = DataBase('resources/config.db')
header = config.searchDatabase('SELECT * FROM Botões')[0]

# sql comands general==========================================
searchAll = 'SELECT * FROM {}'
deleteInformation = 'DELETE FROM {} WHERE ID = {}'

# style of tables general ===============================================
styleTableInformationsTreeview = [
    ('BACKGROUND', (0, 1), (-1, 1), f'{header[0]}'),
    ('BACKGROUND', (0, 2), (-1, -1), f'#ffffff'),
    ('TEXTCOLOR', (0, 1), (-1, 1), f'{header[1]}'),
    ('TEXTCOLOR', (0, 2), (-1, -1), f'#000000'),
    ('FONTSIZE', (0, 1), (-1, 1), 12),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('BOX', (0, 1), (-1, -1), 0.25, '#000000'),
    ('INNERGRID', (0, 1), (-1, -1), 0.25, '#000000')
]
styleTableInformationsComplementary = [
    ('BACKGROUND', (0, 1), (-1, 1), f'{header[2]}'),
    ('BACKGROUND', (0, 2), (-1, -1), f'#ffffff'),
    ('TEXTCOLOR', (0, 1), (-1, 1), f'{header[1]}'),
    ('TEXTCOLOR', (0, 2), (-1, -1), f'#000000'),
    ('FONTSIZE', (0, 1), (-1, 1), 12),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('BOX', (0, 1), (-1, -1), 0.25, '#000000'),
    ('INNERGRID', (0, 1), (-1, -1), 0.25, '#000000')]

# sql comands for scheduling ===================================
registerScheduling = (
    'INSERT INTO Agenda (aluno, valor, método_de_pagamento, data, pagamento)'
    'VALUES ("{}", "{}", "{}", "{}", "{}")'
)
searchSchedule = '''SELECT * 
                  FROM Agenda
                  WHERE {} LIKE "%{}%"
                  and valor LIKE "%{}%"
                  and método_de_pagamento LIKE "%{}%"
                  and data LIKE "%{}%"
                  and pagamento LIKE "%{}%" ORDER BY {} ASC'''

updateSchedule = '''UPDATE Agenda
                      SET aluno = "{}",
                          valor = "{}",
                          método_de_pagamento = "{}",         
                          data = "{}",
                          pagamento = "{}"
                      WHERE ID = {}'''

# tables for schedule informations =================================
tableWithInformationsScheduleTreeview = [['', '', '', '', ''], ['    ID    ', '    Aluno    ', '    valor    ', '    M/Pagamento   ', '    data    ', '    pagamento    ']]
tableWithInformationsComplementarySchedule = [['', '', '', '', '', '', ''], ['Total de Alunos', 'T/Cartão', 'T/Dinheiro', 'T/Tranferência', 'T/Nota', 'T/Não pago', 'T/Recebido']]

# sql comands for clients informations ==============================
registerStudent = (
    'INSERT INTO Alunos (nome, idade, altura, peso, faixa, grau, saúde, problema_de_saúde, limitação, qual_limitação, telefone, rg, cpf, endereço, cep, bairro, cidade, estado, foto, observação)'
    'VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'
)
searchStudent = '''SELECT * 
                  FROM Alunos
                  WHERE {} LIKE "%{}%"
                  and idade LIKE "%{}%"
                  and altura LIKE "%{}%"
                  and peso LIKE "%{}%"
                  and faixa LIKE "%{}%"
                  and grau LIKE "%{}%"
                  and saúde LIKE "%{}%"
                  and problema_de_saúde LIKE "%{}%"
                  and limitação LIKE "%{}%"
                  and qual_limitação LIKE "%{}%"
                  and telefone LIKE "%{}%"
                  and rg LIKE "%{}%"
                  and cpf LIKE "%{}%"
                  and endereço LIKE "%{}%"
                  and cep LIKE "%{}%"
                  and bairro LIKE "%{}%"
                  and cidade LIKE "%{}%"
                  and estado LIKE "%{}%" ORDER BY {} ASC'''
updateStudent = '''UPDATE Alunos
                      SET nome = "{}",
                          idade = "{}",
                          altura = "{}",
                          peso = "{}",
                          faixa = "{}",
                          grau = "{}",
                          saúde = "{}",
                          problema_de_saúde = "{}",
                          limitação = "{}",
                          qual_limitação = "{}",
                          telefone = "{}",
                          rg = "{}",
                          cpf = "{}",
                          endereço = "{}",
                          cep = "{}",
                          bairro = "{}",
                          cidade = "{}",
                          estado = "{}",
                          foto = "{}"
                      WHERE ID = {}'''

# tables for client informations =================================
tableWithInformationsStudentTreeview1 = [['', '', '', '', '', ''], ['    ID    ', '    Nome    ', '    Idade    ', '    Altura   ', ' Peso ', 'Faixa']]
tableWithInformationsStudentTreeview2 = [['', '', '', '', '', ''], ['Grau ', ' Saúde ', ' P/Saúde ', ' Limitação ', ' Q/limitação ', ' Telefone ']]
tableWithInformationsStudentTreeview3 = [['', '', '', '', '', '', ''], ['RG ', ' CPF ', ' Endereço ', ' CEP ', ' Bairro ', ' Cidade ', 'Estado']]
tableWithInformationsComplementaryStudent = [['', '', '', '', ''], ['Total de Alunos', 'Maior', 'Menor', 'M/Pesado', 'M/Leve']]

# sql comands for cash ==============================
registerCashManagement = (
    'INSERT INTO Gerenciamento_do_mês (t_alunos, t_cartão, t_dinheiro, t_transferência, t_nota, s_cartão, s_dinheiro, s_transferência, s_nota, t_recebido, mês, status, observação)'
    'VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'
)
searchCashManagement = '''SELECT *
                  FROM Gerenciamento_do_mês
                  WHERE t_alunos LIKE "%{}%"
                  and t_cartão LIKE "%{}%"
                  and t_dinheiro LIKE "%{}%"
                  and t_transferência LIKE "%{}%"
                  and t_nota LIKE "%{}%"
                  and {} LIKE "%{}%"
                  and t_recebido LIKE "%{}%"
                  and mês LIKE "%{}%"
                  and status LIKE "%{}%"
                  and observação LIKE "%{}%" ORDER BY {} ASC'''

updateCashManagement = '''UPDATE Gerenciamento_do_mês
                      SET t_alunos = "{}",
                          t_cartão = "{}",
                          t_dinheiro = "{}",
                          t_transferência = "{}",
                          t_nota = "{}",
                          {} = "{}",
                          t_recebido = "{}",
                          mês = "{}",
                          status = "{}",
                          observação = "{}"
                      WHERE ID = {}'''

# tables for client informations =================================
tableWithInformationsCashManagementTreeview1 = [['', '', '', '', '', '', ''], ['ID', 'T/Alunos', 'T/Cartão', 'T/Dinheiro', 'T/Transferência', 'T/Nota', 'S/Cartão']]
tableWithInformationsCashManagementTreeview2 = [['', '', '', '', '', ''], ['S/Dinheiro', 'S/Transferência', 'S/Nota', 'T/Recebido', 'mês', 'Status']]
tableWithInformationsComplementaryCashManagement = [['', '', ''], ['T/Clientes', 'T/Recebido', 'T/Saída']]
# message informations cash day ===============================
messageCashManagement = ('Total de Alunos = {}\n'
                         'Total recebido = {}\n'
                         'Total de Saida = {}')

# sql comands for users ==============================
registerUsers = (
    'INSERT INTO Usuários (nome, senha, nivel)'
    'VALUES ("{}", "{}", "{}")'
)
searchUsers = '''SELECT *
                  FROM Usuários
                  WHERE nome LIKE "%{}%"
                  and nivel LIKE "%{}%"'''
updateUsers = '''UPDATE Usuários
                      SET nome = "{}",
                          senha = "{}",
                          nivel = "{}"
                      WHERE ID = {}'''

date_pattern = r'\b\d{2}[/-]\d{4}\b'

# set references for replacement
references = {
    'nnn': '',  # Nome
    'iii': '',  # Idade
    'aaa': '',  # Altura
    'ppp': '',  # Peso
    'fff': '',  # Faixa
    'ggg': '',  # Grau
    'sss': '',  # Saúde
    'pspsps': '',
    'lll': '',  # Limitação
    'qqq': '',
    'ttt': '',  # Telefone
    'rrr': '',  # RG
    'cpcpcp': '', # CPF
    'eee': '',  # Endereço
    'ccc': '',  # CEP
    'bbb': '',  # Bairro
    'cicici': '', # Cidade
    'eseses': ''  # Estado
}