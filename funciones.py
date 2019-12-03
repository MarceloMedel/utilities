import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#mejorar manejo de carpetas
#mejorar gráficos


def check_data(data, null_col=False, msg=True):
    rows = data.shape[0]
    cols = data.shape[1]
    col_name = data.columns
    if null_col is True:
        dict_col_null = check_col_null(data,col_name,msg=msg)
    return rows, cols, dict_col_null

def check_col_null(data, header, save_plt=False,dir_name=None, msg=False):  
    ''' Esta funcion muestra (default:msg=False) en pantalla la cantidad de datos nulos para las columnas específicas de un dataframe y guarda plots para las 
        columnas (default:save_plt=False)
        Recibe como input el dataframe y las columnas a evaluar.
    '''
    #header = [a for a in list(data) if a in data]
    null_values_col = []
    non_null_col = []
    dict_col_null = {}
    i = 0
    for col in header:
        i += 1
        col_type = data[col].dtype
        na_values = data[col].isnull().sum()
        q_values = data[col].count()
        p_null = (na_values/(na_values+q_values))*100
        if p_null>0:
            if msg is True:
                print('Columna {} tiene {:.2f}% ({:d}) de valores nulos'.format(col,p_null,na_values))
            null_values_col.append(col)
            dict_col_null.update({col:[na_values,q_values,p_null]})
            #print(dict_col_null)
        else:
            non_null_col.append(col)
            if msg is True:
                print('Columna {} no tiene valores nulos, tipo de columna= {}'.format(col,col_type))
    if save_plt== True:           
        save_plot(data,null_values_col)
        save_plot(data,non_null_col)
    return dict_col_null

def save_plot(data,values_col, type, dir_name='/Plots',show=False):
#Falta agregar el diccionario
    ''' Funcion que genera plots de los datos dependiendo del tipo de datos
        para columnas object genera un countplot y lo guarda con el nombre col_name_countplot
        para columnas numéricas genera un distplot y lo guarda con el nombre col_name_distplot.
        Recibe como parámetros el dataframe y los nombres de columnas para genera plots
        '''
    i = 0
    wd = os.getcwd()
    dir_img = []
    #dir_img = {}
    for col in values_col:
        i += 1
        fig = plt.figure()
        sns.set(style="whitegrid", rc={'figure.figsize':(5,4)})
        if data[col].dtype == 'object':
            sns.countplot(x=col,data=data, palette='RdBu_r')
            dir_plt = wd+dir_name+'/'+str(i)+'-'+col+ '_countplot'
            plt.savefig(dir_plt)
            dir_img.append(dir_plt)
            if show is True:
                plt.show()
            plt.close()
        elif data[col].dtype in ('int64','float64'):
            sns.distplot(data[data[col].notnull()][col])#,fit=stats.norm)
            dir_plt = wd+dir_name+'/'+str(i)+'-'+col+'_distplot'
            dir_img.append(dir_plt)
            plt.savefig(dir_plt)
            if show is True:
                plt.show()
            plt.close(fig)
    return dir_img