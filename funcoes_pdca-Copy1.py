import pandas as pd
import numpy as np

###FUNÇÕES DE PROCESSAMENTO GERAL

def read_sheets():
    #dir_dba = r'E:\MEGA\PMMG\MySql\10 - Tbl_dimensao\pdca\tbl_base_PDCA_2020.xls'#Home
    dir_dba = r'C:\Users\Geo\Documents\MEGAsync\MySql\10 - Tbl_dimensao\pdca\tbl_base_PDCA_2020.xls'#Office
    df_ocorrencias = pd.read_excel(dir_dba, sheet_name='tbl_ocorrencias')
    df_armas_fgo = pd.read_excel(dir_dba, sheet_name='tbl_armas_fgo')
    df_envolvidos = pd.read_excel(dir_dba, sheet_name='tbl_envolvidos')
    df_veiculos = pd.read_excel(dir_dba, sheet_name='tbl_veiculos')
    df_materiais = pd.read_excel(dir_dba, sheet_name='tbl_materiais')
    df_infracoes = pd.read_excel(dir_dba, sheet_name='tbl_infracoes')
    df_integrantes = pd.read_excel(dir_dba, sheet_name='tbl_integrantes')
    return [df_ocorrencias,df_armas_fgo,df_envolvidos,df_veiculos,df_materiais,df_infracoes,df_integrantes]

def columns():
    for df in [df_ocorrencias,df_armas_fgo,df_envolvidos,df_veiculos,df_materiais,df_infracoes,df_integrantes]:
        df.columns = df.columns.str.replace(' ', '_')
        df.columns = df.columns.str.upper()
    return df

def index_nreds():
    for df in [df_ocorrencias,df_armas_fgo,df_envolvidos,df_veiculos,df_materiais,df_infracoes,df_integrantes]:
        df.set_index('NÚMERO_REDS', inplace=True)
    return df


def class_diao(row):
    nat = row['CÓDIGO_SUBCLASSE_NAT_PRINCIPAL']
    if nat == ('B01121'):
        return 'HOMICIDIO'
    elif nat  == ('C01155'):
        return 'FURTO'
    elif nat == ('C01157'):
        return 'ROUBO'
    elif nat == ('I04033'):
        return 'TRAFICO'
    else:
        return 'OUTRAS'
    
    

def create_municoes_column(df_mat):    

    tipo_mat = ('APETRECHOS, EQUIPAMENTOS, ACESSORIOS, PECAS, CARTUCHOS VAZIOS, SEMI-CARREGADOS OU CARREGADOS E CHUMBO GRANULADO, DESTINADOS A FABRICACAO DE MUNICAO E/OU ARMA DE FOGO DE USO RESTRITO E/OU PROIBIDO',
            'CARTUCHO INTACTO (MUNICAO) DE ARMA DE FOGO DE USO PERMITIDO', 'CARTUCHO INTACTO (MUNICAO) DE CALIBRE RESTRITO', 'CARTUCHO VAZIO DE MUNICAO DE USO RESTRITO',
            'MUNICAO - DEMAIS SUBSTANCIAS, PRODUTOS SUJEITOS AO CONTROLE DO R-105', 'MUNICOES OU DISPOSITIVOS COM EFEITOS PIROTECNICOS, OU DISPOSITIVOS SIMILARES CAPAZES DE PROVOCAR INCENDIO OU EXPLOSOES(SINALIZADORES) (RESTRITO)',
            'OUTROS  - EXPLOSIVOS / MUNICOES / TIRO ESPORTIVO')

    is_mun = [
                (df_mat['SITUAÇÃO_MATERIAL'].isin(['APREENDIDO', 'RECUPERADO'])) &
                (df_mat['DESCRIÇÃO_LONGA_TIPO_MATERIAL'].isin(tipo_mat))
               ]

    df_mat['MUNICOES_UN'] = np.select(is_mun, [df_mat['QTDE_MATERIAIS']*df_mat['QTDE/VOLUME_MATERIAL']], default=0)
    
### UNIVERSO OCORRÊNCIAS

    #insere a coluna UEOP   
def ueop(df_ocor):   
    conds=[
        df_ocor['MUNICÍPIO'].isin(['ABAETE','BIQUINHAS','BOM DESPACHO','CEDRO DO ABAETE','CORREGO DANTA',
            'DORES DO INDAIA','ESTRELA DO INDAIA','JAPARAIBA','LAGOA DA PRATA','LUZ','MARTINHO CAMPOS','MOEMA',
            'MORADA NOVA DE MINAS','PAINEIRAS','PEDRA DO INDAIA','POMPEU','QUARTEL GERAL','SANTO ANTONIO DO MONTE',
            'SERRA DA SAUDADE']),
        df_ocor['MUNICÍPIO'].isin(['CARMO DO CAJURU','CLAUDIO','DIVINOPOLIS','ITATIAIUCU','ITAUNA','SAO GONCALO DO PARA']),
        df_ocor['MUNICÍPIO'].isin(['ARAUJOS','CONCEICAO DO PARA','LEANDRO FERREIRA','NOVA SERRANA','PERDIGAO','PITANGUI']),
        df_ocor['MUNICÍPIO'].isin(['ARCOS','BAMBUI','CAMACHO','CORREGO FUNDO','FORMIGA','IGUATAMA','ITAPECERICA','MEDEIROS','PAINS','PIMENTA','SAO SEBASTIAO DO OESTE','TAPIRAI']),
        df_ocor['MUNICÍPIO'].isin(['IGARATINGA','MARAVILHAS','ONCA DO PITANGUI','PAPAGAIOS','PARA DE MINAS','PEQUI','SAO JOSE DA VARGINHA']),
    ]
    res=['07º BPM','23º BPM','60º BPM','63º BPM','19ª CIA PM IND']

    df_ocor['UEOP'] = np.select(conds,res,default='other')

    #insere a coluna companhia   
def cia(df_ocor):
    cia = df_ocor['UNID_REGISTRO_NÍVEL_6'].str.split("/", n = 1, expand = True)
    df_ocor['CIA'] = cia[0]

### UNIVERSO MATERIAIS     

    #insere a coluna dos materiais apreendidos e  computados no PDCA

   
def mat_group(row):
    
    if row['SITUAÇÃO_MATERIAL'] in ('APREENDIDO', 'RECUPERADO') and row['DESCRIÇÃO_LONGA_TIPO_MATERIAL'] in ('SIMULACRO DE ARMA DE FOGO (USO RESTRITO)'):
        return 'SIMULACRO'
    
    elif row['SITUAÇÃO_MATERIAL'] == ('APREENDIDO') and row['DESCRIÇÃO_LONGA_TIPO_MATERIAL'] in ('OUTROS - INSTRUMENTO PERFURANTE, CORTANTE OU CONTUNDENTE'):
        return 'ARMA_BR'
    
    elif row['SITUAÇÃO_MATERIAL'] == ('APREENDIDO', 'RECUPERADO') and row['DESCRIÇÃO_LONGA_TIPO_MATERIAL'] in ('MICRO COMPUTADOR'):
        return 'COMPUTADOR'
    
    elif row['SITUAÇÃO_MATERIAL'] == ('APREENDIDO', 'RECUPERADO') and row['DESCRIÇÃO_LONGA_TIPO_MATERIAL'] in ('TELEFONE CELULAR'):
        return 'CELULAR_RECUP_APREEND'
    
    elif row['SITUAÇÃO_MATERIAL'] == ('APREENDIDO', 'RECUPERADO') and row['DESCRIÇÃO_LONGA_TIPO_MATERIAL'] in ('MOEDA NACIONAL (REAL)', 'MOEDA ESTRANGEIRA', 'OUTROS - TIPOS DE MOEDAS'):
        return 'DINHEIRO'
    
    elif row['SITUAÇÃO_MATERIAL'] == ('APREENDIDO') and row['DESCRIÇÃO_LONGA_TIPO_MATERIAL'] in ('CRACK EM PEDRAS'):
        return 'CRACK_PEDRAS'
    
    elif row['SITUAÇÃO_MATERIAL'] == ('APREENDIDO') and row['DESCRIÇÃO_LONGA_TIPO_MATERIAL'] in ('CRACK EM QUILOGRAMAS', 'OUTROS - CRACK'):
        return 'CRACK_GR'
    
    elif row['SITUAÇÃO_MATERIAL'] == ('APREENDIDO') and row['DESCRIÇÃO_LONGA_TIPO_MATERIAL'] in ('MACONHA PRENSADA (BARRA / TABLETE)'):
        return 'MACONHA_TABLT'
    
    elif row['SITUAÇÃO_MATERIAL'] == ('APREENDIDO') and row['DESCRIÇÃO_LONGA_TIPO_MATERIAL'] in ('BUCHA DE MACONHA', 'CIGARRO DE MACONHA', 'OUTROS - MACONHA'):
        return 'CIG_BUCHA_MACONHA'
    
    elif row['SITUAÇÃO_MATERIAL'] == ('APREENDIDO') and row['DESCRIÇÃO_LONGA_TIPO_MATERIAL'] in ('PLANTACAO (PE) DE MACONHA', 'SEMENTE DE MACONHA'):
        return 'MACONHA_PES_SEM'
    
    elif row['SITUAÇÃO_MATERIAL'] == ('APREENDIDO') and row['DESCRIÇÃO_LONGA_TIPO_MATERIAL'] in ('PAPELOTES DE COCAINA'):
        return 'COCAINA_PAPELOTE'
    
    elif row['SITUAÇÃO_MATERIAL'] == ('APREENDIDO') and row['DESCRIÇÃO_LONGA_TIPO_MATERIAL'] in ('PASTA DE COCAINA', 'OUTROS - COCAINA', 'COCAINA EM PO'):
        return 'COCAINA_OUTROS'
    
    elif row['SITUAÇÃO_MATERIAL'] == ('APREENDIDO') and row['DESCRIÇÃO_LONGA_TIPO_MATERIAL'] in ('HAXIXE EM BOLA', 'OUTROS - HAXIXE'):
        return 'HAXIXE_BOLA'
    
    elif row['SITUAÇÃO_MATERIAL'] == ('APREENDIDO') and row['DESCRIÇÃO_LONGA_TIPO_MATERIAL'] in ('HAXIXE EM BOLA', 'OUTROS - HAXIXE'):
        return 'HAXIXE_KG'
    
    elif row['SITUAÇÃO_MATERIAL'] == ('APREENDIDO') and row['DESCRIÇÃO_LONGA_TIPO_MATERIAL'] in ('ECSTASY / MDMA'):
        return 'ECSTASY'
    
    elif row['SITUAÇÃO_MATERIAL'] == ('APREENDIDO') and row['DESCRIÇÃO_LONGA_TIPO_MATERIAL'] in ('OUTROS - LSD'):
        return 'LSD'
    
    elif row['SITUAÇÃO_MATERIAL'] == ('APREENDIDO', 'RECUPERADO') and row['DESCRIÇÃO_LONGA_TIPO_MATERIAL'] in ('ARTANE', 'DIAZEPAN', 'DIEMPAX', 'INIBEX', 'ROHYPNOL', 'XAROPE', 'OUTROS - MEDICAMENTOS / SINTETICOS', 'CARGA DE MEDICAMENTOS'):
        return 'MEDICAMENTOS'
    
    elif row['SITUAÇÃO_MATERIAL'] == ('APREENDIDO') and row['DESCRIÇÃO_LONGA_TIPO_MATERIAL'] in ('OUTROS - EQUIPAMENTOS PARA DROGAS / NARCOTICOS'):
        return 'EQUIP_NARCOTICO'
    
    else:
        return 'OUTROS'
    
### UNIVERSO ENVOLVIDOS
    
    # Cria coluna com o tipo  de cada prisao especificada para computo do PDCA
def prisoes(row):
    
    presos = ('FLAGRANTE DE CRIME / CONTRAVENCAO','OUTRAS - PRISAO / APREENSAO', 'RECAPTURA', 'FLAGRANTE DE ATO INFRACIONAL', 'MANDADO JUDICIAL')
    
    if row['PRISÃO_/_APREENSÃO'] in (presos) and row['CÓDIGO_SUBCLASSE_NAT_PRINCIPAL'] == ('C01155'):
        return 'PRESO_FURTO'
    
    elif row['PRISÃO_/_APREENSÃO'] in (presos) and row['CÓDIGO_SUBCLASSE_NAT_PRINCIPAL'] == ('C01157'):
        return 'PRESO_ROUBO'
    
    elif row['PRISÃO_/_APREENSÃO'] in (presos) and row['CÓDIGO_SUBCLASSE_NAT_PRINCIPAL'] in ('D01213','D01213'):
        return 'PRESO_ESTUPRO'
    
    elif row['PRISÃO_/_APREENSÃO'] in (presos) and row['CÓDIGO_SUBCLASSE_NAT_PRINCIPAL'] in ('I04033'):
        return 'PRESO_TRAFICO'
    
    elif row['PRISÃO_/_APREENSÃO'] in (presos) and row['CÓDIGO_SUBCLASSE_NAT_PRINCIPAL'] in ('B01121'):
        return 'PRESO_HOMICIDIO'
    
    elif row['PRISÃO_/_APREENSÃO'] in (presos):
        return 'PRESOS_OUTRAS'
 
    else:
        return 'ENVOLVIDOS'

 