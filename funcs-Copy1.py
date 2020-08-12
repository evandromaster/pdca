import pandas as pd
import numpy as np

def read_sheets():
    dir_dba = r'E:\MEGA\PMMG\MySql\10 - Tbl_dimensao\pdca\tbl_base_PDCA_2020.xls'#Home
    #dir_dba = r'C:\Users\Geo\Documents\MEGAsync\MySql\10 - Tbl_dimensao\pdca\tbl_base_PDCA_2020.xls'#Office
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
    

