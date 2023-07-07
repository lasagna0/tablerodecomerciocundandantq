import streamlit as st  
import pandas as pd 
#plotly expess
import plotly.express as px
#aggrid para streamlit
from st_aggrid import AgGrid

#wide
st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    importacionesantpath="datos requeridos\dfimportacionesantfiltered.parquet"
    exportacionesantpath="datos requeridos\dfexportacionesantfiltered.parquet"
    importacionescundpath="datos requeridos\dfimportacionescundfiltered.parquet"
    exportacionescundpath="datos requeridos\dfexportacionescundfiltered.parquet"
    importacionesant=pd.read_parquet(importacionesantpath)
    exportacionesant=pd.read_parquet(exportacionesantpath)
    importacionescund=pd.read_parquet(importacionescundpath)
    exportacionescund=pd.read_parquet(exportacionescundpath)
    return importacionesant,exportacionesant,importacionescund,exportacionescund

importacionesant,exportacionesant,importacionescund,exportacionescund=load_data()


st.sidebar.title('Filtros')
st.sidebar.subheader('Seleccione el departamento')
departamento=st.sidebar.selectbox('Departamento',('Antioquia','Cundinamarca'))
st.sidebar.subheader('Seleccione el tipo de comercio')
tipo=st.sidebar.selectbox('Tipo de comercio',('Importaciones','Exportaciones'))
# """
# COLUMNAS DE IMPORTACIONES 
# Index(['NOMBRE_IMPORTADOR', 'NIT_IMPORTADOR', 'DIRECCION_IMPORTADOR',
#        'NOMBRE_EXPORTADOR', 'DIRECCION_EXPORTADOR', 'PAIS_PROCEDENCIA',
#        'SUBPARTIDA_ARANCELARIA', 'VALOR_FOB_USD', 'PAIS_ORIGEN',
#        'DEPARTAMENTO_IMPORTADOR', 'year', 'month', 'Subpartida Arancelaria',
#        'CIIU Rev. 4 A.C (2021)', 'Clase', 'Descripción'],
#       dtype='object')
# """
# """
# COLUMNAS DE EXPORTACIONES
# Index(['NIT_EXPORTADOR', 'PAIS_DESTINO_FINAL', 'REGION_PROCEDENCIA',
#        'SUBPARTIDA', 'REGION_DE_ORIGEN', 'VALOR_FOB_USD',
#        'RAZON_SOCIAL_EXPORTADOR', 'DIREC_EXPORTADOR', 'year', 'month',
#        'Subpartida Arancelaria', 'CIIU Rev. 4 A.C (2021)', 'Clase',
#        'Descripción'],
# """

if departamento=='Antioquia':
    if tipo=='Importaciones':
        datosactivos=importacionesant
    else:
        datosactivos=exportacionesant
else:
    if tipo=='Importaciones':
        datosactivos=importacionescund
    else:
        datosactivos=exportacionescund

st.write("Para cualquiera de las tablas presentadas, se puede descarga un archivo XLSX con sus datos, para ello presiona click derecho sobre la tabla deseada")

st.subheader('Tipo de Identificación')
st.selectbox('IDENTIFICACION TOP CIIU, IDENTIFICACION POR CIIU, IDENTIFICACION POR EMPRESA',('IDENTIFICACION TOP CIIU','IDENTIFICACION POR CIIU','IDENTIFICACION POR EMPRESA'),key='modalidad')
if st.session_state.modalidad=='IDENTIFICACION POR EMPRESA':
    st.write('Seleccione la empresa que desea consultar')
    if tipo=="Importaciones":
        empresa=st.selectbox('EMPRESA',datosactivos['NOMBRE_IMPORTADOR'].unique())
        st.write('A continuación se presenta por cada CIIU cual es el valor de ' + tipo.lower() + ' en el departamento de ' + departamento.lower())
        targetdata=datosactivos[datosactivos['NOMBRE_IMPORTADOR']==empresa]
        # Group the data by importer and country and sum the FOB value
        grouped_data = targetdata.groupby(['Descripción', 'PAIS_ORIGEN'])['VALOR_FOB_USD'].sum()
        # Sort the data by the FOB value
        grouped_data = grouped_data.sort_values(ascending=False)
        # Reset the index to make the importer and country columns
        col1, col2=st.columns(2)
        grouped_data = grouped_data.reset_index()
        with col1:
            #creeate a histogram with target data to show how much are the values of the company 
            fig = px.histogram(targetdata, x='VALOR_FOB_USD', title='Histogram of Import Values for ' + empresa)
            #resize fig2 biggger
            fig.update_layout(
                autosize=False,
                width=450,
                height=600,)
            st.plotly_chart(fig)
        with col2:
            monthdata=targetdata.groupby(['month', 'PAIS_ORIGEN'])['VALOR_FOB_USD'].sum().reset_index() 
            #line chart by month
            fig2 = px.line(monthdata, x='month', y='VALOR_FOB_USD', color='PAIS_ORIGEN', title='Import Values by Month for ' + empresa)
            #resize fig2 biggger
            fig2.update_layout(
                autosize=False,
                width=450,
                height=600,)
            st.plotly_chart(fig2)

            #create table with grouped data
        AgGrid(grouped_data)
        #SHOW BAR GRAPH SHOWING CIIU AND VALUE
        ciiusandvalues=targetdata.groupby(['Descripción'])['VALOR_FOB_USD'].sum().reset_index()
        fig3 = px.bar(ciiusandvalues, x='Descripción', y='VALOR_FOB_USD', title='Import Values by CIIU for ' + empresa)
        #resize fig2 biggger
        fig3.update_layout(
            autosize=False,
            width=900,
            height=600,)
        st.plotly_chart(fig3)
    elif tipo=='Exportaciones':
        empresa=st.selectbox('EMPRESA',datosactivos['RAZON_SOCIAL_EXPORTADOR'].unique())
        st.write('A continuación se presenta por cada CIIU cual es el valor de ' + tipo.lower() + ' en el departamento de ' + departamento.lower())
        targetdata=datosactivos[datosactivos['RAZON_SOCIAL_EXPORTADOR']==empresa]
        # Group the data by exporter and country and sum the FOB value
        grouped_data = targetdata.groupby(['Descripción', 'PAIS_DESTINO_FINAL'])['VALOR_FOB_USD'].sum()
        # Sort the data by the FOB value
        grouped_data = grouped_data.sort_values(ascending=False)
        # Reset the index to make the exporter and country columns
        grouped_data = grouped_data.reset_index()
        col1, col2=st.columns(2)
        with col1:
            #creeate a histogram with target data to show how much are the values of the company 
            fig = px.histogram(targetdata, x='VALOR_FOB_USD', title='Histogram of Export Values for ' + empresa)
            #resize fig2 biggger
            fig.update_layout(
                autosize=False,
                width=450,
                height=600,)
            st.plotly_chart(fig)
        with col2:
            monthdata=targetdata.groupby(['month', 'PAIS_DESTINO_FINAL'])['VALOR_FOB_USD'].sum().reset_index()
            #line chart by month
            fig2 = px.line(monthdata, x='month', y='VALOR_FOB_USD', color='PAIS_DESTINO_FINAL', title='Export Values by Month for ' + empresa)
            #resize fig2 biggger
            fig2.update_layout(
                autosize=False,
                width=450,
                height=600,)
            st.plotly_chart(fig2)
            
            #create table with grouped data
        AgGrid(grouped_data)
        #SHOW BAR GRAPH SHOWING CIIU AND VALUE
        ciiusandvalues=targetdata.groupby(['Descripción'])['VALOR_FOB_USD'].sum().reset_index()
        fig3 = px.bar(ciiusandvalues, x='Descripción', y='VALOR_FOB_USD', title='Export Values by CIIU for ' + empresa)
        #resize fig2 biggger
        fig3.update_layout(
            autosize=False,
            width=900,
            height=600,)
        st.plotly_chart(fig3)
        
        
if st.session_state.modalidad=='IDENTIFICACION POR CIIU':
    st.write('Seleccione el CIIU que desea consultar')
    ciiu=st.selectbox('CIIU',datosactivos['Descripción'].unique())
    st.write('A continuación se presenta por cada empresa cual es el valor de ' + tipo.lower() + ' en el departamento de ' + departamento.lower())
    if tipo=='Importaciones':
        targetdata=datosactivos[datosactivos['Descripción']==ciiu]
        # Group the data by importer and sum the FOB value
        grouped_data = targetdata.groupby('NOMBRE_IMPORTADOR')['VALOR_FOB_USD'].sum()
        # Sort the data by the FOB value
        grouped_data = grouped_data.sort_values(ascending=False)
        # Reset the index to make the importer a column
        grouped_data = grouped_data.reset_index()
        #show the data
        col1, col2 = st.columns(2)
        with col1:
            AgGrid(grouped_data)
        with col2:
            # Create a bar chart showing the top 10 importers
            fig = px.bar(grouped_data.head(10), x='NOMBRE_IMPORTADOR', y='VALOR_FOB_USD', title='Top 10 Importers in' + departamento)
            #resize fig2 biggger
            fig.update_layout(
                autosize=False,
                width=450,
                height=600,)
            st.plotly_chart(fig)
            

    elif tipo=='Exportaciones':
        targetdata=datosactivos[datosactivos['Descripción']==ciiu]
        # Group the data by importer and sum the FOB value
        grouped_data = targetdata.groupby('RAZON_SOCIAL_EXPORTADOR')['VALOR_FOB_USD'].sum()
        # Sort the data by the FOB value
        grouped_data = grouped_data.sort_values(ascending=False)
        # Reset the index to make the importer a column
        grouped_data = grouped_data.reset_index()
        #show the data
        col1, col2 = st.columns(2)
        with col1:
            AgGrid(grouped_data)
        with col2:
            # Create a bar chart showing the top 10 importers
            fig = px.bar(grouped_data.head(10), x='RAZON_SOCIAL_EXPORTADOR', y='VALOR_FOB_USD', title='Top 10 Exporters in' + departamento)
            #resize fig2 biggger
            fig.update_layout(
                autosize=False,
                width=450,
                height=600,)
            st.plotly_chart(fig)
            #create a map with the data cloropeth
            datawithcountry=datosactivos[datosactivos['Descripción']==ciiu]
            countrycode=pd.read_csv('https://gist.githubusercontent.com/brenes/1095110/raw/c8f208b03485ba28f97c500ab7271e8bce43b9c6/paises.csv')
            countrycode["nombre"] = countrycode["nombre"].str.upper()
            #nombre, name, nom, iso2, iso3, phone_code

            countrycode.columns=['nombre', 'name', 'nom', 'iso2', 'iso3', 'phone_code']
            datawithcountry=datawithcountry.merge(countrycode, left_on='PAIS_DESTINO_FINAL', right_on='nombre')
            #iso2 is the code for the map
            fig2 = px.choropleth(datawithcountry, locations="iso3", color="VALOR_FOB_USD", hover_name="PAIS_DESTINO_FINAL", color_continuous_scale=px.colors.sequential.Plasma)
            fig2.update_layout(showlegend=False)
            #resize fig2 biggger
            fig2.update_layout(
                autosize=False,
                width=450,
                height=600,)
            


            
if st.session_state.modalidad=='IDENTIFICACION TOP CIIU':
    st.write('A continuación se presenta por cada CIIU cual es la empresa con mayor número de ' + tipo.lower() + ' en el departamento de ' + departamento.lower())
    if tipo=='Importaciones':
    # BEGIN: 5z9j7f8d2z9d
    # Define a function to get the top company for a given CIIU
        def get_top_company(df):
            # Group by importer and sum the FOB value
            importer_group = df.groupby('NOMBRE_IMPORTADOR')['VALOR_FOB_USD'].sum()
            # Get the importer with the highest FOB value
            top_importer = importer_group.idxmax()
            # Get the top importer's data
            top_importer_data = df[df['NOMBRE_IMPORTADOR'] == top_importer]
            # Group by country and sum the FOB value
            country_group = top_importer_data.groupby('PAIS_ORIGEN')['VALOR_FOB_USD'].sum()
            # Get the country with the highest FOB value
            top_country = country_group.idxmax()
            # Get the total import value
            total_import_value = df['VALOR_FOB_USD'].sum()
            # Get the import value to the top country
            import_value_to_top_country = top_importer_data[top_importer_data['PAIS_ORIGEN'] == top_country]['VALOR_FOB_USD'].sum()
            # Return a dictionary with the required data
            return {'CIIU': df['Descripción'].iloc[0], 'Top Importer': top_importer, 'Top Country': top_country, 'Total Import Value': total_import_value, 'Import Value to Top Country': import_value_to_top_country}

        # Create an empty list to store the data
        top_data = []
        # Loop through each CIIU in datosactivos
        for ciiu in datosactivos['Descripción'].unique():
            # Get the data for the current CIIU
            ciiu_data = datosactivos[datosactivos['Descripción'] == ciiu]
            # Get the top company for the current CIIU
            top_company = get_top_company(ciiu_data)
            # Append the data to the list
            top_data.append(top_company)

        # Create a DataFrame from the list of data
        
    else:
        def get_top_company(df):
            # Group by importer and sum the FOB value
            exporter_group = df.groupby('RAZON_SOCIAL_EXPORTADOR')['VALOR_FOB_USD'].sum()
            # Get the importer with the highest FOB value
            top_exporter = exporter_group.idxmax()
            # Get the top importer's data
            top_exporter_data = df[df['RAZON_SOCIAL_EXPORTADOR'] == top_exporter]
            # Group by country and sum the FOB value
            country_group = top_exporter_data.groupby('PAIS_DESTINO_FINAL')['VALOR_FOB_USD'].sum()
            # Get the country with the highest FOB value
            top_country = country_group.idxmax()
            # Get the total import value
            total_export_value = df['VALOR_FOB_USD'].sum()
            # Get the import value to the top country
            export_value_to_top_country = top_exporter_data[top_exporter_data['PAIS_DESTINO_FINAL'] == top_country]['VALOR_FOB_USD'].sum()
            # Return a dictionary with the required data
            return {'CIIU': df['Descripción'].iloc[0], 'Top Exporter': top_exporter, 'Top Country': top_country, 'Total Export Value': total_export_value, 'Export Value to Top Country': export_value_to_top_country}

        # Create an empty list to store the data
        top_data = []
        # Loop through each CIIU in datosactivos
        for ciiu in datosactivos['Descripción'].unique():
            # Get the data for the current CIIU
            ciiu_data = datosactivos[datosactivos['Descripción'] == ciiu]
            # Get the top company for the current CIIU
            top_company = get_top_company(ciiu_data)
            # Append the data to the list
            top_data.append(top_company)

        # Create a DataFrame from the list of data
    col1,col2=st.columns(2)
    if tipo=='Importaciones':
        with col1:
            top = pd.DataFrame(top_data)
            AgGrid(top)
            if tipo=='Importaciones':
                # Create a bar chart showing the top 10 importers
                fig2 = px.bar(top.sort_values('Total Import Value', ascending=False).head(10), x='Top Importer', y='Total Import Value', color='CIIU', title='Top 10 Importers in' + departamento)
                #resize fig2 biggger
                fig2.update_layout(
                    autosize=False,
                    width=1000,
                    height=600,)

                # Group the data by CIIU and get the count of unique companies and the sum of USD FOB
                grouped_data = datosactivos.groupby('Descripción').agg({'NOMBRE_IMPORTADOR': 'nunique', 'VALOR_FOB_USD': 'sum'})

                # Rename the columns
                grouped_data = grouped_data.rename(columns={'NOMBRE_IMPORTADOR': 'Number of Companies', 'VALOR_FOB_USD': 'USD FOB'})

                # Reset the index to make the CIIU a column
                grouped_data = grouped_data.reset_index()

                # Create the bubble chart
                fig = px.scatter(grouped_data, x='Number of Companies', y='USD FOB', size='USD FOB', color='Descripción', hover_name='Descripción', log_x=True, size_max=60)
                fig.update_layout(showlegend=False)
                #RESIZE THE CHART TO BE SMALLER AND FIT IN THE PAGE
                fig.update_layout(
                    autosize=False,
                    width=500,
                    height=600,)
            with col2:
            
                st.plotly_chart(fig)

            st.plotly_chart(fig2)
    elif tipo=='Exportaciones':
        with col1:
            top = pd.DataFrame(top_data)
            AgGrid(top)
            if tipo=='Exportaciones':
                # Create a bar chart showing the top 10 importers
                fig2 = px.bar(top.sort_values('Total Export Value', ascending=False).head(10), x='Top Exporter', y='Total Export Value', color='CIIU', title='Top 10 Exporters in' + departamento)
                #resize fig2 biggger
                fig2.update_layout(
                    autosize=False,
                    width=1000,
                    height=600,)

                # Group the data by CIIU and get the count of unique companies and the sum of USD FOB
                grouped_data = datosactivos.groupby('Descripción').agg({'RAZON_SOCIAL_EXPORTADOR': 'nunique', 'VALOR_FOB_USD': 'sum'})

                # Rename the columns
                grouped_data = grouped_data.rename(columns={'RAZON_SOCIAL_EXPORTADOR': 'Number of Companies', 'VALOR_FOB_USD': 'USD FOB'})

                # Reset the index to make the CIIU a column
                grouped_data = grouped_data.reset_index()

                # Create the bubble chart
                fig = px.scatter(grouped_data, x='Number of Companies', y='USD FOB', size='USD FOB', color='Descripción', hover_name='Descripción', log_x=True, size_max=60)
                fig.update_layout(showlegend=False)
                #RESIZE THE CHART TO BE SMALLER AND FIT IN THE PAGE
                fig.update_layout(
                    autosize=False,
                    width=500,
                    height=600,)
            with col2:
            
                st.plotly_chart(fig)

            st.plotly_chart(fig2)
    

# """
# CODIGO CREADO POR DAVID ALEJANDRO SANCHEZ POLO PARA PROBARRANQUILLA
# SU USO ES LIBRE, SIEMPRE Y CUANDO SE MANTENGA ESTE COMENTARIO
# PROBARRANQUILLA 2023
# """