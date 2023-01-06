import plotly.express as px
import streamlit as st
import pandas as pd
import bar_chart_race as bcr

st.markdown("""<style>
               .main 
                </style>
                """,
                unsafe_allow_html = True)

background_color= '#F5F5F5'
st.title("Covid data-India")
st.text("Covid data is between march 2020 to june 2022.")
st.text("Vaccination data is between jan 2021 to dec 2022.")
st.text("17.77% of people in the world lives in India.")
st.text("The population of india in 2022 was 1417173173.")
st.image("data//images.jpg")

navigate = st.sidebar.radio("Which data you need",["Home.","Confirmed cases.","Active cases.","Cured cases.","Deaths.","Vaccinations."])

df = pd.read_csv("data//covid_data.csv")
df["date"]=pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

vac_df = pd.read_csv("data//weekly_data.csv")
vac_df["startdate"] = pd.to_datetime(vac_df["startdate"]).dt.strftime("%Y-%m-%d")

pop_df = pd.read_csv("data//world_population.csv")

df['Country'] = "India"
merged_df = df.merge(pop_df,on='Country')
new_df = merged_df[["date","region","confirmed","active","cured","deaths","Country","2022 Population","World Population Percentage"]]

vac_df['Country'] = "India"
merged_vac_df = vac_df.merge(pop_df,on='Country')
new_vac_df = merged_vac_df[["startdate","total","dose_one","dose_two","dose_precaution","children","teens","adults","middle_aged","senior"]] 

if navigate == "Home.":
    if st.checkbox("Show covid data."):
        st.write(new_df)
    if st.checkbox("Show vaccination data"):    
        st.write(new_vac_df)

if navigate == "Confirmed cases.":
    st.subheader("Confirmed cases")
    total_confirmed = round(sum(new_df.groupby('region')["confirmed"].max()))
    per_r_confirmed =round(sum(new_df.groupby('region')["confirmed"].max())/1417173173 * 100)
    st.write(f"Total confirmed cases in india: {total_confirmed}.")
    st.write(f"Percentage of confirmed cases in india : {per_r_confirmed}%.") 
   
    region_options = df["region"].unique().tolist()
    date_options = df["date"].unique().tolist()
    dat = st.selectbox("**Which date would you like to see?**.",date_options)
    reg = st.multiselect("**Which region would you like to see?**.",region_options,["Goa","Assam"])
    st.text("You can select multiple region.")
    df = df[df["region"].isin(reg)]
    df = df[df["date"] == dat]
    fig =px.bar(df, x="region",y="confirmed",color="region")
    fig.update_layout(width=800,hovermode='x',title='Bar chart of Confirmed cases')
    st.write(fig)

if navigate == "Active cases.":
    st.subheader("Active cases")
    total_active = round(sum(new_df.groupby('region')["active"].max()))
    st.write(f"Total active cases in india: {total_active}.")
    
    date_options1 = df["date"].unique().tolist()
    region_options1 = df["region"].unique().tolist()
    date = st.select_slider("**Which date would you like to see?**.",date_options1)
    region = st.multiselect("**Which region would you like to see?**.",region_options1,["Goa","Kerala"])
    st.text("You can select multiple region.")
    df = df[df["region"].isin(region)]
    df = df[df["date"] == date]
    fig1 =px.bar(df, x="region",y="active",color="region",title='Bar chart of Active cases')
    #fig1.update_geos(projection_type='equirectangular',visible=True,resolution = 110)
    fig1.update_layout(width=800)
    st.write(fig1)

if navigate == "Cured cases.":
    st.subheader("Cured cases")
    total_cured = round(sum(new_df.groupby('region')["cured"].max()))
    per_cured =round(sum(new_df.groupby('region')["cured"].max())/ sum(new_df.groupby('region')["confirmed"].max()) * 100)
    st.write(f"Total cured cases in india: {total_cured}.")
    st.write(f"Percentage of cured cases in india : {per_cured}%.") 
   
    cured_region_options = df["region"].unique().tolist()
    cured_date_options = df["date"].unique().tolist()
    cured_date = st.selectbox("**Which date would you like to see?**.",cured_date_options)
    cured_region = st.multiselect("**Which region would you like to see?**.",cured_region_options,["Goa","Tamil Nadu"])
    st.text("You can select multiple region.")
    df = df[df["region"].isin(cured_region)]
    #df = df[df["date"] == cured_date]
    fig2 =px.bar(df, x="region",y="cured",color="region",animation_frame="date",animation_group="region",title='Bar chart of Cured cases')
    fig2.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 30
    fig2.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 5
    fig2.update_layout(width=800)
    st.write(fig2)
    
if navigate == "Deaths.":    
    st.subheader("Deaths")
    total_death = round(sum(new_df.groupby('region')["deaths"].max()))
    per_death =round(sum(new_df.groupby('region')["deaths"].max())/ sum(new_df.groupby('region')["confirmed"].max()) * 100)
    st.write(f"Total deaths in india: {total_death}.")
    st.write(f"Percentage of death rates in india : {per_death}%.") 
   
    death_region_options = df["region"].unique().tolist()
    death_date_options = df["date"].unique().tolist()
    death_date = st.selectbox("**Which date would you like to see?**.",death_date_options)
    death_region = st.multiselect("**Which region would you like to see?**.",death_region_options,["Tamil Nadu","Delhi"])
    st.text("You can select multiple region.")
    df = df[df["region"].isin(death_region)]
    df = df[df["date"] == death_date]
    fig3 =px.bar(df, x="region",y="deaths",color="region",title='Bar chart of deaths')
    fig3.update_layout(width=800)
    st.write(fig3)   

if navigate == "Vaccinations.":   
    st.subheader("Vaccinations")
    N = st.radio("Vaccinations data",["Total vaccinations.","Dose one.","Dose two.","Dose precaution."])

    if N == "Total vaccinations.":
        st.write("Total number of vaccinations is ", vac_df["total"].sum())
        st.subheader("Vaccination by age")
        fig7 = px.line(vac_df,x='startdate')
        fig7.add_scatter(x=vac_df['startdate'],y=vac_df['children'],mode='lines',name='Childrens (below 13)')  
        fig7.add_scatter(x=vac_df['startdate'],y=vac_df['teens'],mode='lines',name='Teens (13 - 18)') 
        fig7.add_scatter(x=vac_df['startdate'],y=vac_df['adults'],mode='lines',name='Adults (18 - 45)') 
        fig7.add_scatter(x=vac_df['startdate'],y=vac_df['middle_aged'],mode='lines',name='Middle aged (45 - 60)') 
        fig7.add_scatter(x=vac_df['startdate'],y=vac_df['senior'],mode='lines',name='Seniors (above 60')      
        fig7.update_layout(width=800,showlegend=True,hovermode='x',yaxis_title='vaccination counts',title='Dose one vaccination')
        st.write(fig7)

        st.subheader("Total vaccination by age")
        st.write("Total number of childrens vaccination is ", vac_df["children"].sum())
        st.write("Total number of teens vaccinations is ", vac_df["teens"].sum())
        st.write("Total number of adults vaccinations is ", vac_df["adults"].sum())
        st.write("Total number of middle aged people vaccinations is ", vac_df["middle_aged"].sum())
        st.write("Total number of senior people vaccinations is ", vac_df["senior"].sum())

    if N == "Dose one.":
        st.subheader("Dose one vaccination")
        st.write("Total number of dose one vaccinations is", vac_df["dose_one"].sum()) 
        per_dose_one = round(vac_df["dose_one"].sum() / 1417173173 * 100)
        st.write(f"{per_dose_one}% of people in india vaccinated dose one.")  
        fig5 = px.line(vac_df,x='startdate')
        fig5.add_scatter(x=vac_df['startdate'],y=vac_df['dose_one'],mode='lines',name='Dose one')       
        fig5.update_layout(width=800,showlegend=False,hovermode='x',yaxis_title='vaccination counts',title='Dose one vaccination')
        st.write(fig5)
        
    if N == "Dose two.":
        st.subheader("Dose two vaccination")
        st.write("Total number of dose two vaccinations is",vac_df["dose_two"].sum())
        per_dose_two = round(vac_df["dose_two"].sum() / 1417173173 * 100)
        st.write(f"{per_dose_two}% of people in india vaccinated dose two.")
        fig6 = px.line(vac_df,x='startdate')
        fig6.add_scatter(x=vac_df['startdate'],y=vac_df['dose_two'],mode='lines',name='Dose two')       
        fig6.update_layout(width=800,showlegend=False,hovermode='x',yaxis_title='vaccination counts',title='Dose two vaccination')
        st.write(fig6)

    if N == "Dose precaution.":
        st.subheader("Precaution dose vaccination")
        st.write("Total number of dose precaution is ", vac_df["dose_precaution"].sum()) 
        per_dose_precaution = round(vac_df["dose_precaution"].sum() / 1417173173 * 100)
        st.write(f"{per_dose_precaution}% of people in india precaution dose vaccinated.")
        fig7 = px.line(vac_df,x='startdate')
        fig7.add_scatter(x=vac_df['startdate'],y=vac_df['dose_precaution'],mode='lines',name='Dose one')       
        fig7.update_layout(width=800,showlegend=False,hovermode='x',yaxis_title='vaccination counts',title='Dose precaution')
        st.write(fig7)       
