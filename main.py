import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt


st.markdown('# Medical Cost Personal Dataset')
df = pd.read_csv('/Users/vladislavazhilenko/Desktop/insurance.csv')
app = st.sidebar.selectbox('Steps', ['Analyse', 'Statistics&Clean_Up', 'Links'])
if app == 'Analyse':
    table1, table2, table3 = st.tabs(['Simple Charts', 'Analysis for an insurance company', 'Conclusion'])
    with table1:
        st.header('Simple Charts')
        st.write('First graph shows the number of smokers')
        st.write('Second graph indicates the frequently '
                'encountered number of children in families')

        st.title('The number of smokers')
        result1 = st.button('Smokers', key=True)
        st.write(result1)
        if result1:
            fig, ax = plt.subplots()
            df["smoker"].value_counts().plot.pie()
            plt.legend()
            st.pyplot(fig)

        st.title('The frequently encountered number of children')
        result2 = st.button('Children')
        st.write(result2)
        if result2:
            fig, ax = plt.subplots()
            plt.hist(df['children'], bins=5)
            st.pyplot(fig)

    with table2:
        st.header('Analysis for an insurance company')
        st.write(' Lets say we are a new insurance company that wants to indicate '
                'which group of the population living in which area is most '
                'unprofitable.')
        group1, group2 = st.tabs(['First part', 'Second part'])
        with group1:
            name0fChart = st.selectbox('charts', (['Region', 'Age', 'Complex graph']))
            if name0fChart == 'Region':
                fig, ax = plt.subplots()


                def sumOfRegion(reg):
                    curReg = df[df['region'] == reg]
                    sumOfCur = curReg['charges'].sum()
                    return sumOfCur


                regions = df['region'].unique()
                values = []
                for reg in regions:
                    values.append(sumOfRegion(reg))

                plt.pie(values, labels=regions, autopct='%1.1f%%')
                st.pyplot(fig)
                st.markdown('_From this pie chart, we can '
                            'indicate that the southeastern district'
                            ' has the largest number of charges._')
            if name0fChart == 'Age':
                fig, ax = plt.subplots()
                targetReg = df[df['region'] == 'southeast']
                targetReg['age'].plot.hist(width=4)
                plt.legend()
                st.pyplot(fig)
                st.markdown('_Looking at just ages of region we cant'
                            ' really see the whole picture so lets look at '
                            'means between ages and figure out which audience '
                            'is most unprofitable._')
            if name0fChart == 'Complex graph':
                fig, ax = plt.subplots()
                targetReg = df[df['region'] == 'southeast']
                ages = targetReg['age'].unique()

                means = {}

                for a in ages:
                    ageSplit = targetReg[targetReg['age'] == a]
                    means[a] = ageSplit['charges'].mean()

                ind = means.keys()
                val = means.values()

                plt.title('Correlation between age and average cost healthcare')
                plt.xlabel('Age')
                plt.ylabel('Charges')
                plt.bar(ind, val, label='Data', color="g")
                plt.axhline(df['charges'].mean(), color="red", label='Mean', linestyle='--')
                plt.legend()
                st.pyplot(fig)
                st.markdown('_From this graph we can indicate that it is '
                            'an audience of young people._')

        with group2:
            name0fChart = st.selectbox('charts', (['Male&Female', 'Complex graph']))
            if name0fChart == 'Male&Female':
                fig, ax = plt.subplots()
                targetReg = df[df['region'] == 'southeast']
                num0 = targetReg['sex'].value_counts()
                values = num0.values
                plt.pie(values, labels=num0.index, autopct='%1.1f%%', startangle=180)
                plt.legend()
                st.pyplot(fig)
                st.markdown('_This pie chart shows that the number of men and women '
                            'is approximately equal._')
            if name0fChart == 'Complex graph':
                fig, ax = plt.subplots()
                targetReg = df[df['region'] == 'southeast']
                targetYoung = targetReg[targetReg['age'] <= 25]
                pl = sns.lmplot(data=targetYoung, x="bmi", y="charges", hue="sex", aspect=2)
                st.pyplot(pl)
                st.markdown('_With the growth of the body mass index, the largest amount of '
                            'insurance charges is provided to men at a young age_')
    with table3:
        st.header('Conclusion')
        st.markdown(
            '##### _Our goal was to indicate the target audience and their living area which is most unprofitable._')
        st.markdown('_First of all, we notice that the number of smokers is really small, therefore, we do not take into'
                    ' account the dependence of payments on smoking, since a larger percentage of respondents do not smoke._')
        st.markdown('_Moreover, we note that most do not have children, so we will also not focus on this parameter._')
        st.markdown('_Starting the analysis by identifying the area to which the insurance company pays the most money, '
                'we came to the conclusion that this is the southeast district._')
        st.markdown('_Next, considering only residents of the southeastern district, the graph showed that young people'
                ' receive more insurance payments than older people in comparison with the median value._')
        st.markdown('_Finally, having determined on a simple graph that the number of men and women is about the same, '
                    'we analyzed the relationship of the body mass index with the number of charges by gender. The increase '
                    'in payments with an increase in body mass index among men is more dramatic._')
        st.markdown(
            '##### _To summarize, цe determined that the insurance company deducts the largest number of payments in '
            'the southeastern region to young men with an increased body mass index._')

if app == 'Statistics&Clean_Up':
    t1, t2 = st.tabs(['Statistics', 'Clean Up'])
    with t1:
        st.header('Statistics')
        data = df.describe()
        drop_l = ['25%', "75%", "count"]
        for i in drop_l:
            data = data.drop(i)
        data = data.reindex(["mean", "50%", "std", "max", "min"])
        data.index = ["mean", "median", "standard deviation", "max", "min"]
        data
    with t2:
        st.header('Clean Up')
        st.table(pd.DataFrame.from_dict({'Problem': ['No NaN values', 'All data types correct'],  'Validity': [True, True]}))
        st.write('Data Frame is correct')
        st.write(df.isnull().values.any())
if app == 'Links':
    st.write('[Dataset](https://www.kaggle.com/datasets/mirichoi0218/insurance)')
    with open('Medical Cost Personal Dataset.ipynb', 'rb') as file:
        st.download_button(
            label='Download Jupyter',
            data=file,
            file_name='Medical Cost Personal Dataset.ipynb',
            mime="application/x-ipynb+json"
        )