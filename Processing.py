# ### CSV Processing
#
# - Input: path of raw CSV files.
# - Output: CSV (single sheet)/XLSX (multiple sheets) files with improved readability.

def prodStr(df):
    '''
    df: pandas dataframe that needs product string parsing.
    output: product string (type:str)
    '''
    
    # Delimiters for product string in order is: (1) ',' (2) ';'
    products = df.loc['Products'][0].strip()
    products = products.split(',')
    prostr = '\n'

    # Dictionary of categories for product string.
    dictProducts = {0: 'Category : ',
                    1: 'Product  : ',
                    2: 'Quantity : ',
                    3: 'Price    : ',
                    4: 'Events   : ',
                    5: 'eVars    : '}

    count = 0
    for i in products:
        # Add a new line to the string if it isn't the first item of the product.
        prostr = prostr + ('' if (i == 0) else '\n') + '    #'+ (str(count+1)) + '\n'
        item = i.split(';')

        countj = 0
        for j in item:
            # Map dictionary to product string components.
            prostr = prostr + (('    ' + dictProducts[countj]) if countj<=5 else '    ')
            prostr = prostr + j + '\n'
            countj = countj + 1
        count = count + 1
    return prostr

def CSVProcessing(path, endpoints, outfile, forms = False):

    """
    Input: path of raw .csv files from adobe debugger extension.
    (i.e. path = '/Users/[username]/Downloads')
    Output: .xlsx file with individual sheets for every hit + summary sheet.
    """

    import pandas as pd
    import os
    import glob
    from pathlib import Path

    # Read all csv files in specified path.
    all_files = glob.glob1(path, "*csv")

    # If forms is set to False, open endpoints and set all links to 'FAILED' status.
    if not forms:
        ep = pd.read_csv(str(Path(path + '/Endpoints.csv')), names=['Endpoints'])
        dup_ep = ep
        dup_ep['Result'] = 'FAILURE/REDIRECTED'

    # Remove any csv files that aren't part of analytics output from the list (doesn't delete files).
    for file in all_files:
        if file[0:24] == 'adobe-analytics-data-raw':
            pass
        else:
            all_files.remove(file)

    li = []
    di = {}

    # Read csv files to pandas and append to `li` for summary page and `di` for individual sheets.
    for filename in all_files:
        x = str(Path(path + '/' + filename))
        df = pd.read_csv(x, index_col=None, header=0, sep='~~', engine='python')
        df['Report Suite ID    '] = df['Report Suite ID    '].apply(lambda x: x.strip())
        df.set_index('Report Suite ID    ', inplace=True)

        # Checks if 'Products' index exists and prints to a text file (keeps appending).
        if 'Products' in df.index:
            product_str = prodStr(df)
            df.loc['Products'][0] = product_str
            with open(str(Path(path + '/' + 'product-strings.txt')), "a") as text_file:
                print(product_str, file=text_file)
            text_file.close()

        li.append(df)

        # If we aren't form filling, then compare current URL to endpoints URLs.
        if not forms:
            # If URL is isn't in the endpoints file, FAILED.
            url = df.loc['Current URL        '][0].strip()
            if url[-1] == '/':
                url = url[:-1]

            if url in list(ep['Endpoints']):
                i = ep[ep['Endpoints'] == url].index
                dup_ep['Result'][i] = 'SUCCESS'

            dup_ep.to_csv(str(Path(path + '/' + endpoints)), index=False)
            writer.save()

            os.remove(str(Path(path + '/Endpoints.csv')))

        # Setting the name of each sheet to the webpage name.
        if len(df.iloc[0][0]) <= 31:
            di.update({df.iloc[0][0]: df})
        elif len(df.iloc[0][0]) > 31:
            di.update({'home': df})

        # Delete raw csv file after use.
        os.remove(x)

    # Concat list of dataframes to generate summary page.
    frame = pd.concat(li, axis=1, sort='False')
    di.update({'Summary': frame})

    writer = pd.ExcelWriter(str(Path(path + '/' + outfile)), engine='xlsxwriter')

    # Write each sheet to .xlsx file.
    for sheet in di.keys():
        di[sheet].to_excel(writer, sheet_name=sheet, index=True)
