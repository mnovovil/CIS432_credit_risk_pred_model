import streamlit as st
import pickle
import pandas as pd
import numpy as np

from scipy import stats

def page():

	st.markdown(
		"""
		<style>
		.img{
			width:50px;
			height:50px;
		}
		</style>
		""",
		unsafe_allow_html=True
	)

	st.markdown(
		f"""
		<div>
			<h1><img class="img" src="https://cdn-icons-png.flaticon.com/512/2891/2891711.png" alt="logo"/> Application Form</h1>
		</div>
		""",
		unsafe_allow_html=True
	)
	
	with open('logistic_regression_model.p', 'rb') as f:
		model = pickle.load(f)

	df = pd.read_csv("heloc_dataset_v1.csv")

	with st.form("Application"):
		c1, c2 = st.columns(2)
		with c1:
			ExternalRiskEstimate = st.number_input('External Risk Estimate', step = 1)
			MSinceOldestTradeOpen = st.number_input('Months Since Oldest Trade Open', step = 1)
			MSinceMostRecentTradeOpen = st.number_input('Months Since Recent Trade Open', step=1)
			AverageMInFile = st.number_input('Average Months in File', step = 1)
			NumSatisfactoryTrades = st.number_input('Number Satisfactory Trades', step = 1)
			NumTrades60Ever2DerogPubRec = st.number_input('Number Trades 60+ Ever', step = 1)
			NumTrades90Ever2DerogPubRec = st.number_input('Number Trades 90+ Ever', step = 1)
			PercentTradesNeverDelq = st.number_input('Percent Trades Never Delinquent', step = 1)
			MSinceMostRecentDelq = st.number_input('Months Since Most Recent Delinquency', step = 1)
			MaxDelq2PublicRecLast12M = st.number_input('Max Delinquency/Public Records Last 12 Months', step = 1)
			MaxDelqEver = st.number_input('Max Delinquency Ever', step = 1)
			NumTotalTrades = st.number_input('Number of Total Trades (total number of credit accounts)', step = 1)
		with c2:
			NumTradesOpeninLast12M = st.number_input('Number of Trades Open in Last 12 Months', step = 1)
			PercentInstallTrades = st.number_input('Percent Installment Trades', step = 1)
			MSinceMostRecentInqexcl7days = st.number_input('Months Since Most Recent inquiries excluding last 7 days', step = 1)
			NumInqLast6M = st.number_input('Number of inquiries Last 6 Months', step = 1)
			NumInqLast6Mexcl7days = st.number_input('Number of inquiries Last 6 Months excluding the last 7 days. Excluding the last 7 days removes inquiries that are likely due to price comparision shopping.', step = 1)
			NetFractionRevolvingBurden = st.number_input('Net Fraction Revolving Burden. This is revolving balance divided by credit limit', step = 1)
			NetFractionInstallBurden = st.number_input('Net Fraction Installment Burden. This is installment balance divided by original loan amount', step = 1)
			NumRevolvingTradesWBalance = st.number_input('Number Revolving Trades with Balance', step = 1)
			NumInstallTradesWBalance = st.number_input('Number Installment Trades with Balance', step = 1)
			NumBank2NatlTradesWHighUtilization = st.number_input('Number Bank/Natl Trades w high utilization ratio', step = 1)
			PercentTradesWBalance = st.number_input('Percent Trades with Balance', step = 1)

		submit = st.form_submit_button("Submit")

	if submit:
		new_application = [ExternalRiskEstimate, MSinceOldestTradeOpen, MSinceMostRecentTradeOpen, AverageMInFile, NumSatisfactoryTrades,
									NumTrades60Ever2DerogPubRec, NumTrades90Ever2DerogPubRec, PercentTradesNeverDelq,
									MSinceMostRecentDelq, MaxDelq2PublicRecLast12M, MaxDelqEver, NumTotalTrades, 
									NumTradesOpeninLast12M, PercentInstallTrades, MSinceMostRecentInqexcl7days, NumInqLast6M,
									NumInqLast6Mexcl7days, NetFractionRevolvingBurden, NetFractionInstallBurden, 
									NumRevolvingTradesWBalance, NumInstallTradesWBalance,
									NumBank2NatlTradesWHighUtilization, PercentTradesWBalance]

		prediction = model.predict([new_application])

	
		if prediction == 0:
			st.success("This application should be accepted.")
		else:
			st.error("This application should be rejected.")
		benchmarks_df = get_benchmarks(new_application, df)

		st.write("")
		st.write("Application Evaluation: ")
		st.write(benchmarks_df)



def get_benchmarks(row, base_df):
    # Get DataFrames of Good and Bad RiskPerformance
    df_good = base_df[base_df['RiskPerformance'] == 'Good']
    df_bad = base_df[base_df['RiskPerformance'] == 'Bad']

    # Get descriptors of all DataFrames
    df_good_desc = df_good.describe()
    df_bad_desc = df_bad.describe()
    df_desc = base_df.describe()


    all_insights = {'ColName': [], 'Insight': [], 'Percentile': []}
    for col_num in range(len(df_desc.columns)):
        percentile = stats.percentileofscore(base_df[df_desc.columns[col_num]], row[col_num])
        all_insights['ColName'].append(df_desc.columns[col_num])
        all_insights['Percentile'].append(percentile)
        if df_good_desc[df_desc.columns[col_num]]['mean'] >= df_bad_desc[df_desc.columns[col_num]]['mean']:
            if percentile > 80:
                all_insights['Insight'].append('Very Good')
            elif percentile > 40:
                all_insights['Insight'].append('Good')
            elif percentile > 30:
                all_insights['Insight'].append('Fair')
            elif percentile > 20:
                all_insights['Insight'].append('Poor')
            else:
                all_insights['Insight'].append('Very Poor')
        else:
            if percentile < 20:
                all_insights['Insight'].append('Very Good')
            elif percentile < 30:
                all_insights['Insight'].append('Good')
            elif percentile < 40:
                all_insights['Insight'].append('Fair')
            elif percentile < 80:
                all_insights['Insight'].append('Poor')
            else:
                all_insights['Insight'].append('Very Poor')

    insights_df = pd.DataFrame(all_insights)
    insights_df = insights_df.set_index('ColName')
    new_insights_df = insights_df.drop(['MaxDelqEver', 'AverageMInFile', 'NumSatisfactoryTrades', 'PercentTradesNeverDelq',
					  'MSinceMostRecentDelq', 'PercentTradesWBalance', 'NumInstallTradesWBalance', 'NumTotalTrades',
					  'MSinceOldestTradeOpen', 'NetFractionInstallBurden', 'MSinceMostRecentTradeOpen',
					  'NetFractionRevolvingBurden', 'NumTradesOpeninLast12M', 'PercentInstallTrades'], axis=0)


    return new_insights_df
