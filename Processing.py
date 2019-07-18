# ### CSV Processing
#
# - Input: path of raw CSV files.
# - Output: CSV (single sheet)/XLSX (multiple sheets) files with improved readability.

import pandas as pd
import os
import glob
from pathlib import Path


def http_https (x):
    if x[0:7] == 'http://':
        x = x.replace('http://', 'https://', 1)
    return x

def prod_str (df):
    '''
    df: pandas dataframe that needs product string parsing.
    output: product string to text file (type:str)
    '''

    import pandas as pd
    import os
    
    # Delimiters for product string in order is: (1) ',' (2) ';'
    products = df.loc['Products'][0].strip()
    products = products.split(',') # First delimiter
    prostr = '\n'

    # Dictionary of categories for product string.
    dictProducts = {0: 'Category : ',
                    1: 'Product  : ',
                    2: 'Quantity : ',
                    3: 'Price    : ',
                    4: 'Events   : ',
                    5: 'eVars    : '}

    prodDict = []

    for count,i in enumerate(products):
        # Add a new line to the string if it isn't the first item of the product.
        item = i.split(';') # Second delimiter
        for countj,j in enumerate(item):
            if (countj % 4 == 0 or countj % 5 == 0) and countj != 0 and j != '':
                j = j.split('|') # Delimiter for events/evars
                for e in j:
                    if countj % 4 == 0:
                        prodDict.append(e[0:7] + '  : ' + e[8:])
                    else:
                        prodDict.append(e[0:6] + '   : ' + e[7:])
            else:
                # Map dictionary to product string components.
                prodDict.append(((dictProducts[countj]) if countj<=5 else '    ')+j)

    l = []
    d = {}
    
    # String to list of dictionaries
    for i in range(len(prodDict)):
        d[prodDict[i][0:9]] = prodDict[i][11:]
        if i == (len(prodDict)-1) or ('Category' in prodDict[i+1]):
            l.append(d)
            d = {}
            
    ps = pd.DataFrame(l)
    ps.set_index('Category ')
    
    return ps.transpose()

def csv_prettifier(path, endpoints, outfile, forms = False):

    """
    This function takes the raw csv files from the adobe debugger chrome extension and makes them more readable.
    
    Parameters
    ----------
    path : system file path to folder with raw csv files (type: string).
    endpoints : name of endpoints file from pageloads or link clicks (type: string).
    outfile : name of output .xlsx file with summary page and individual pages (type: string).
    forms : if the function needs to perform form filling or not, False by default (type: bool).
    """

    import pandas as pd
    import os
    import glob
    from pathlib import Path

    # Read all csv files in specified path.
    all_files = glob.glob1(path, "*csv")

    # If forms is set to False, open endpoints and set all links to 'FAILED' status.
    if not forms:
        ep = pd.read_csv(str(Path(path + '/' + endpoints)), names=['Endpoints'])
        dup_ep = ep
        ep['Endpoints'] = ep['Endpoints'].apply(lambda x: http_https(x))
        dup_ep['Result'] = 'FAILURE/REDIRECTED'

    # Remove any csv files that aren't part of analytics output from the list (doesn't delete files).
    for file in all_files:
        if file[0:24] != 'adobe-analytics-data-raw':
            all_files.remove(file)
            
    li = []
    di = {}
    li_prod = []

    # Read csv files to pandas and append to `li` for summary page and `di` for individual sheets.
    for filename in all_files:
        x = str(Path(path + '/' + filename))
        df = pd.read_csv(x, index_col=None, header=0, sep='~~', engine='python')
        df['Report Suite ID    '] = df['Report Suite ID    '].apply(lambda x: x.strip())
        df.set_index('Report Suite ID    ', inplace=True)

        # Checks if 'Products' index exists and prints to a text file (keeps appending).
        if 'Products' in df.index:
            ps = prod_str(df)
            li_prod.append(ps)

        li.append(df)

        # If we aren't form filling, then compare current URL to endpoints URLs.
        if not forms:
            # If URL is isn't in the endpoints file, FAILED.
            url = df.loc['Current URL'][0].strip()
            if url[-1] == '/':
                url = url[:-1]

            if url in list(ep['Endpoints']):
                i = ep[ep['Endpoints'] == url].index
                dup_ep['Result'][i] = 'SUCCESS'

        # Setting the name of each sheet to the webpage name.
        if (':' in df.iloc[0][0]) or ('/' in df.iloc[0][0]) :
            di.update({'home': df})
        elif len(df.iloc[0][0]) <= 31:
            di.update({df.iloc[0][0]: df})
        elif len(df.iloc[0][0]) > 31:
            di.update({df.iloc[0][0][0:30]: df})

        # Delete raw csv file after use.
        os.remove(x)

    # Concat list of dataframes to generate summary page.
    frame = pd.concat(li, axis=1, sort='False')
    di.update({'Summary': frame})

    writer = pd.ExcelWriter(str(Path(path + '/' + outfile)), engine='xlsxwriter')

    # Write each sheet to .xlsx file.
    for sheet in di.keys():
        di[sheet].to_excel(writer, sheet_name=sheet, index=True)
    if not forms:
        dup_ep.to_csv(str(Path(path + '/' + endpoints)), index=False)
    elif forms:
        # Product Strings concat
        frame_prod = pd.concat(li_prod, axis=0, sort='False')
        frame_prod.to_csv(str(Path(path + '/' + 'product-strings.csv')), mode='a')
        
    writer.save()
