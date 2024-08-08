from edgar import (
    get_user_agent_string, 
    get_cik_ticker_map, 
    get_cik_from_ticker, 
    get_company_data, 
    organize_by_tag,
    get_dict,
    plot
)

first_name = "Ingimar"
last_name = "Tomasson"
email = "ingitom99@gmail.com"
user_agent_string = get_user_agent_string(first_name, last_name, email)

# Get CIK mapping
cik_map = get_cik_ticker_map(user_agent_string)

# Choose a company (e.g., Apple)
ticker = "AAPL"
cik = get_cik_from_ticker(ticker, cik_map)

# Define tags to fetch
# tags_dict = get_dict('data/tags.json')

tags_dict = {
    "AccountsPayable": "Carrying value as of the balance sheet date of liabilities incurred (and for which invoices have typically been received) and payable to vendors for goods and services received that are used in an entity's business. For classified balance sheets, used to reflect the current portion of the liabilities (due within one year or within the normal operating cycle if longer); for unclassified balance sheets, used to reflect the total liabilities (regardless of due date).",
    "AccountsPayableCurrent": "Carrying value as of the balance sheet date of liabilities incurred (and for which invoices have typically been received) and payable to vendors for goods and services received that are used in an entity's business. Used to reflect the current portion of the liabilities (due within one year or within the normal operating cycle if longer).",
    "AccountsReceivableNetCurrent": "Amount, after allowance for credit loss, of right to consideration from customer for product sold and service rendered in normal course of business, classified as current.",
    "AccruedIncomeTaxesCurrent": "Carrying amount as of the balance sheet date of the unpaid sum of the known and estimated amounts payable to satisfy all currently due domestic and foreign income tax obligations.",
    "AccruedIncomeTaxesNoncurrent": "Carrying amount as of the balance sheet date of the unpaid sum of the known and estimated amounts payable to satisfy all domestic and foreign income tax obligations due beyond one year or the operating cycle, whichever is longer. Alternate captions include income taxes payable, noncurrent.",
}

# Fetch company data
company_data = get_company_data(user_agent_string, cik, tags_dict)

accounts_payable = organize_by_tag(company_data, "AccountsPayable")

# Plot data for each tag
for tag in tags_dict.keys():
    organized_data = organize_by_tag(company_data, tag)
    plot(organized_data, f"{ticker} - {tag}", f"./plots/{ticker}_{tag}.png")

print(f"Data fetched and plotted for {ticker}. Check the generated PNG files.")