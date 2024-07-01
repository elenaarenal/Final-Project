import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
from datetime import datetime
import folium
import time


#st.snow()



new_title = '<p style="font-family:Francois One; color:#0077b6; font-size: 38px;">Polar Ice melting & sea level rise analysis</p>'
st.markdown(new_title, unsafe_allow_html=True)



# Cargar datos
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)


sea_level_path = 'C:/Users/arena/Mi unidad/IRONHACK/KAGLE_FINAL PROJECT/1.GlobalSeaLevel/sealevel.csv'
sea_level_path2= 'C:/Users/arena/Mi unidad/IRONHACK/KAGLE_FINAL PROjECT/2.Global sea level rise/Global_sea_level_rise.csv'
ice_path='C:/Users/arena/Mi unidad/IRONHACK/KAGLE_FINAL PROjECT/4.SeaIceIndex/monthly_sea_ice_index.csv'
#predicted_ice_data = load_data('path_to_your_predicted_ice_data.csv')
#predicted_sea_level_data = load_data('path_to_your_predicted_sea_level_data.csv')


sea_data=load_data(sea_level_path)
sea_data2=load_data(sea_level_path2)
ice_data= load_data(ice_path)
#df_ice(tratando ice_data)
df_ice = pd.read_csv(ice_path)
df_ice=df_ice.drop('data-type', axis=1)
df_ice=df_ice.drop(df_ice[df_ice['extent']<0].index)
df_ice=df_ice.drop(df_ice[df_ice['area']<0].index)
ice_N=df_ice[df_ice['region']=='N']
ice_S=df_ice[df_ice['region']=='S']
# Barra lateral con opciones de navegación
st.sidebar.title("Data explorer")
st.sidebar.image("map.jpg")
opcion = st.sidebar.selectbox("Choose an option:", ["Historical Data", "Prediction", "Webcams",  "Risk Map","Download&suscribe"])


       
        
    

if opcion == "Webcams":
    st.snow()
    #submenu = st.sidebar.selectbox("Select which cam you want to see :", ["South", "North"])
    submenu= st.radio (     "Which camera do you want to see",
    ["South", "North"],
    index=None,
)

    st.write("You selected:", submenu)
       #  Webcams
    
    if submenu=='South':
        st.header('Real Time Monitoring')
        st.subheader('Antartic')
       
        antartic_webcam_url ='https://webcams.windy.com/webcams/public/embed/player/1698667378/day#'
        st.markdown(f'<iframe src="{antartic_webcam_url}" width="700" height="480"></iframe>', unsafe_allow_html=True)
    if submenu=='North':
 
        st.header('Real Time Monitoring')
        st.subheader('Artic')
        arctic_webcam_url = 'https://www.metcam.navcanada.ca/hb/player.jsp?id=157&cam=352&lang=e'
        st.markdown(f'<iframe src="{arctic_webcam_url}" width="800" height="480"></iframe>', unsafe_allow_html=True)
elif opcion=='Prediction':
        #st.image('map.jpg', caption='A: Antartic B: Artic')
        
        tab1, tab2, tab3 = st.tabs(["Level Rise", "Antartic Ice", "Artic Ice"])

        with tab1:
            options = st.multiselect(
             "Which visualization fo you want to see",
            ["Interactive(level rise)", "Global(level rise)", "Trend(level rise)", "Yearly(level rise)"])
            

            st.write("You selected:", options)
            st.header("Level Rise")

            df2=pd.read_csv(sea_level_path2)
            df2_pred=df2.drop('year', axis=1)
            df2_pred['date'] = pd.to_datetime(df2_pred['date'], format='%m/%d/%Y')
            df2_pred=df2_pred.rename(columns={'date': 'ds', 'mmfrom1993-2008average': 'y'}) 
                    
            m=Prophet()
            m.fit(df2_pred)
            future = m.make_future_dataframe(periods=3653) #predicción a 10 años
            forecast = m.predict(future)
           # st.table(forecast)

            fig1 = m.plot(forecast)
          
            fig2=m.plot_components(forecast)
      
            fig3=plot_plotly(m, forecast)
            st.plotly_chart(fig3,use_container_width=True)
            st.pyplot(fig1)
            st.pyplot(fig2)


                     
    
        with tab2:
            st.header("Antartic Ice")
            options = st.multiselect(
            "Which visualization fo you want to see",
            ["Interactive(Antartic Ice)", "Global(Antartic Ice)", "Trends(Antartic Ice)", "Yearly(Antartic Ice)"])
            st.write("You selected:", options)
            ice_S=df_ice[df_ice['region']=='S']
            ice_S=ice_S.drop('region', axis=1)
            ice_S['day'] = 1

            ice_S = ice_S.rename(columns={'year': 'year', 'mo': 'month'})
            ice_S['timestamp'] = pd.to_datetime(ice_S[['year', 'month','day']])
            #south extent

            ice_S_pro=ice_S.drop('year', axis=1)
            ice_S_pro=ice_S.drop('month', axis=1)
            ice_S_pro=ice_S.drop('day', axis=1)
            ice_S_pro=ice_S.drop('area',axis=1)

            ice_S_pro_area=ice_S = ice_S[['timestamp', 'extent']]

            ice_S_pro = ice_S.rename(columns={'timestamp': 'ds', 'extent': 'y'})
            m_S=Prophet()
            m_S.fit(ice_S_pro)
            future = m_S.make_future_dataframe(periods=1825) #predicción a 5 años
            forecast = m_S.predict(future)
            fig_SN= m_S.plot(forecast)
            fig_S2 = m_S.plot_components(forecast)
            axes = fig_S2.get_axes()
            axes[0].set_ylim([8, 16])
            fig_S3=plot_plotly(m_S, forecast)
            st.plotly_chart(fig_S3,use_container_width=True)
            st.pyplot(fig_S2)

               
               
               
        with tab3:
                options = st.multiselect(
                "Which visualization fo you want to see",
                ["Interactive(Artic Ice)", "Global(Artic Ice)", "Trends(Artic Ice)", "Yearly(Artic Ice)"])
                st.write("You selected:", options)
                st.header("Artic Ice")
                ice_N=df_ice[df_ice['region']=='N']
                ice_N=ice_N.drop('region', axis=1)
                ice_N['day'] = 1

                ice_N = ice_N.rename(columns={'year': 'year', 'mo': 'month'})
                ice_N['timestamp'] = pd.to_datetime(ice_N[['year', 'month','day']])
      #north extent

                ice_N_pro=ice_N.drop('year', axis=1)
                ice_N_pro=ice_N.drop('month', axis=1)
                ice_N_pro=ice_N.drop('day', axis=1)
                ice_N_pro=ice_N.drop('area',axis=1)

                ice_N_pro_area=ice_N = ice_N[['timestamp', 'extent']]

                ice_N_pro = ice_N.rename(columns={'timestamp': 'ds', 'extent': 'y'})
                m_N=Prophet()
                m_N.fit(ice_N_pro)
                future = m_N.make_future_dataframe(periods=1825) #predicción a 5 años
                forecast = m_N.predict(future)
                fig_N= m_N.plot(forecast)
                fig_N2 = m_N.plot_components(forecast)
                axes = fig_N2.get_axes()
                axes[0].set_ylim([8, 16])
                fig_N3=plot_plotly(m_N, forecast)
                st.plotly_chart(fig_N3,use_container_width=True)
                st.pyplot(fig_N)
                st.pyplot(fig_N2)

                
        
        
        
        
        
elif opcion == 'Historical Data':
    tab1, tab2, tab3,tab4 = st.tabs(["Level Rise", "Antartic Ice", "Artic Ice", "Global visualization"])
    
    with tab1:
        st.header("Level Rise")
        
       
        df = pd.read_csv(sea_level_path)
        df = df.groupby('Year').mean().reset_index()
        
        fig_level = px.line(df, x='Year', y=['GMSL_noGIA'], title='Global Sea Level')
        fig_level.update_layout(xaxis_title="Year", yaxis_title="Sea Level (mm)")
        fig_level.update_xaxes(dtick=1)
        
        st.plotly_chart(fig_level)
        st.write("The graphic shows the sea level height in mm from 1980 to 2023. The data shown in the plot does not include the glacial isostatic adjustment (GIA).")
        
        df2=pd.read_csv(sea_level_path2)
     
    #  Matplotlib
        fig, ax = plt.subplots(figsize=(11, 5))
        ax.scatter(df2['year'], df2['mmfrom1993-2008average'])
        ax.set_xlabel('Year')
        ax.set_ylabel('mm from 1993-2008 average')
        ax.set_title('Scatter Plot of Sea Level Rise')

    # Mostrar el gráfico en Streamlit
        st.pyplot(fig)
        

    with tab2:
        st.header("Antarctic Ice")
       
        ice_S=df_ice[df_ice['region']=='S']
        ice_S_y=ice_S[ice_S['year']>1979]
        ice_S_y=ice_S_y.groupby('year').sum().reset_index()
        figure, ax = plt.subplots(figsize=(11, 5))
        ax.plot(ice_S_y['year'], ice_S_y['extent'], marker='o', linestyle='-')
        ax.set_xlabel('Year')
        ax.set_ylabel('Extent')
        ax.set_title('Ice Extent Over Years (excluding 1979)')
        ax.grid(True)
        st.pyplot(figure)
        st.caption(' 1979 has been removed due the lack of information ')
        


    with tab3:
        st.header(" Artic Ice")
        ice_N=df_ice[df_ice['region']=='N']
        ice_N_y=ice_N[ice_N['year']>1979]
        ice_N_y=ice_N_y.groupby('year').sum().reset_index()
        figure, ax = plt.subplots(figsize=(11, 5))
        ax.plot(ice_N_y['year'], ice_N_y['extent'], marker='o', linestyle='-')
        ax.set_xlabel('Year')
        ax.set_ylabel('Extent')
        ax.set_title('Ice Extent Over Years (excluding 1979)')
        ax.grid(True)
   
        st.pyplot(figure)
        st.caption(' 1979 has been removed due the lack of information ')
         
    with  tab4:  
        st.header(" Global visualization")
        df_ice = pd.read_csv(ice_path)
        df_ice=df_ice.drop('data-type', axis=1)
        df_ice=df_ice.drop(df_ice[df_ice['extent']<0].index)
        df_ice=df_ice.drop(df_ice[df_ice['area']<0].index)
       
        ice_N=df_ice[df_ice['region']=='N']
        ice_N=ice_N.drop('region', axis=1)

        ice_N=ice_N.groupby('year').mean().reset_index()
        
        ice_S=df_ice[df_ice['region']=='S']
        ice_S=ice_S.drop('region', axis=1)

        ice_S=ice_S.groupby('year').mean().reset_index()
        
        fig, ax = plt.subplots(figsize=(11, 5))


        ax.plot(ice_N['year'], ice_N['area'], label='Ice_North Area', color='g')
        ax.plot(ice_N['year'], ice_N['extent'], label='Ice_North extent', color='g', linestyle='--')
        #st.pyplot(fig)

        ax.plot(ice_S['year'], ice_S['area'], label='Ice_South Area', color='r')
        ax.plot(ice_S['year'], ice_S['extent'], label='Ice_South extent', color='r', linestyle='--')
        
        
        ax.set_ylabel('millions of square kilometers')
        ax.set_xlabel('Year')
        ax.set_title('Area and extent over Years for North and South Pole')
        ax.legend()
       
        st.pyplot(fig)

elif opcion == 'Risk Map': 
    city_path = 'C:/Users/arena/Mi unidad/IRONHACK/KAGLE_FINAL PROJECT/city.csv'  
    city_data=load_data(city_path)
    df_city=pd.read_csv(city_path)
    df_city = df_city.rename(columns={'Número de Habitantes (aprox.)': 'Population'})
    
    

    st.title('Cities at risk and its population')
    texto = 'This is interactive map allows you to filter by population range and shows the cities at risk by sea level rise as a consquence of climatic change. When you click in the marked point, you will be able to see the name of the city and its population'
    


    def stream_data():
        for word in texto.split(" "):
            yield word + " "
            time.sleep(0.05)

    

        for word in texto.split(" "):
            yield word + " "
            time.sleep(0.05)


    if st.button("Explanation"):
        st.write_stream(stream_data)
    
     # Slider para filtrar por población

    min_pop = int(df_city['Population'].min())
    max_pop = int(df_city['Population'].max())
    selected_population = st.slider('Select population range', min_value=min_pop, max_value=max_pop, value=(min_pop, max_pop))
    filtered_cities = df_city[(df_city['Population'] >= selected_population[0]) & (df_city['Population'] <= selected_population[1])]

    map_folium = folium.Map(location=[df_city['Latitud'].iloc[0], df_city['Longitud'].iloc[0]], zoom_start=2,tiles='OpenStreetMap')
    for index, row in filtered_cities.iterrows():
        popup_text = f"{row['Ciudad']} - Population: {row['Population']:,}"
        folium.Marker([row['Latitud'], row['Longitud']], popup=popup_text).add_to(map_folium)
    map_html = map_folium._repr_html_()
    st.components.v1.html(map_html, width=800, height=600)

      