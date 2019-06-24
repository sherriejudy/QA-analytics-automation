# ### CSV Prettifier
#
# - Input: path of raw CSV files.
# - Output: CSV (single sheet)/XLSX (multiple sheets) files with improved readability.

# In[4]:


def CSV_prettifier(path):

    """
    Input: path of raw .csv files from adobe debugger extension.
    (i.e. path = '/Users/[username]/Downloads')
    Output: .xlsx file with individual sheets for every hit + summary sheet.
    """

    import pandas as pd
    import os
    import glob
    from pathlib import Path, PureWindowsPath

    # Read all csv files in specified path.
    all_files = glob.glob1(path,"*csv")

    ep = pd.read_csv(str(Path(path+ '/Endpoints.csv')), names=['Endpoints'])
    dup_ep = ep
    dup_ep['Result'] = 'FAILURE/REDIRECTED'

    # Remove any csv files that aren't part of analytics output.
    for file in all_files:
        if file[0:24] == 'adobe-analytics-data-raw':
            pass
        else:
            all_files.remove(file)

    li = []
    di = {}
    #failure = []
    #success = []

    # Read csv files to pandas and append to `li` for summary page and `di` for indiv sheets.
    for filename in all_files:
        x = path+ '/' +filename
        df = pd.read_csv(x, index_col=None, header=0, sep='~~', engine='python')
        df.set_index('Report Suite ID    ', inplace=True)
        li.append(df)

        # If URL is isn't in the endpoints file, FAILED.
        url = df.loc['Current URL        '][0].strip()
        if url[-1] == '/':
            url = url[:-1]

        if url in list(ep['Endpoints']):
            i = ep[ep['Endpoints'] == url].index
            dup_ep['Result'][i] = 'SUCCESS'


        # Setting the name of each sheet to the webpage name.
        if len(df.iloc[0][0]) <= 31:
            di.update({ df.iloc[0][0] : df})
        elif len(df.iloc[0][0]) > 31:
            di.update({ 'home' : df})

        # Delete raw csv file after use.
        os.remove(x)

    # Concat list of dataframes to generate summary page.
    frame = pd.concat(li, axis=1, sort='False')
    di.update({'Summary' : frame})

    writer = pd.ExcelWriter(str(Path(path+ '/Shaw-pageloads.xlsx')), engine='xlsxwriter')

    # Write each sheet to .xlsx file.
    for sheet in di.keys():
        di[sheet].to_excel(writer, sheet_name=sheet, index=True)

    #dup_ep.fillna('FAILURE/REDIRECTED')
    dup_ep.to_csv(str(Path(path+ '/Endpoints-final.csv')),index=False)
    writer.save()
