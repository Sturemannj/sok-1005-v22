{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "054a06fc",
   "metadata": {},
   "outputs": [],
   "source": [
    "from bs4 import BeautifulSoup\n",
    "import requests\n",
    "import  pandas  as  pd \n",
    "import  matplotlib.pyplot  as  plt\n",
    "from  statsmodels.regression.linear_model  import  OLS\n",
    "import numpy as np\n",
    "\n",
    "\n",
    "\n",
    "# create data\n",
    "def fetch_html_tables(url):\n",
    "    \"Returnerer en liste over tabeller i html-en til url\"\n",
    "    page = requests.get(url)\n",
    "    bs=BeautifulSoup(page.content)\n",
    "    tables=bs.find_all('table')\n",
    "    return tables\n",
    "\n",
    "tables=fetch_html_tables('https://www.norskfamilie.no/barometre/rentebarometer/')\n",
    "table_html=tables[0]\n",
    "\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "b221c448",
   "metadata": {},
   "source": [
    "# Skrap dataene fra nettstedet og lagre numeriske verdier"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "1d856e07",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[['', 'Bank', '', 'Navn', 'Nominell', 'Sikkerhetsgebyr', 'Etableringsgebyr', 'Termin', 'Effektiv'], ['1', 'Statens pensjonskasse', '', 'Boliglån inntil 80 %', '1,69', '0', '0', '50', '1,76'], ['2', 'Bulder Bank (Sparebanken Vest)', '', 'Boliglån innenfor 50 %', '1,78', '0', '0', '0', '1,79'], ['3', 'Etne Sparebank', '', '\"Him te Etne\" - lånet', '1,75', '0', '0', '50', '1,83'], ['4', 'Nybygger.no (Sparebanken Øst)', '', 'Boliglån 75%', '1,81', '0', '0', '0', '1,83'], ['5', 'SpareBank 1 Nordmøre', '', 'Grønt førstehjemslån', '1,75', '1200', '0', '75', '1,86'], ['6', 'NORDirekte (Skagerrak Sparebank)', '', 'Boliglån inntil 50%', '1,80', '0', '0', '40', '1,86'], ['7', 'Bulder Bank (Sparebanken Vest)', '', 'Boliglån innenfor 55 %', '1,86', '0', '0', '0', '1,88'], ['8', 'Sunndal Sparebank', '', 'Grønt boliglån', '1,80', '1000', '0', '65', '1,89'], ['9', 'Landkreditt Bank AS', '', 'Grønt Boliglån 50%', '1,89', '500', '0', '0', '1,91'], ['10', 'SpareBank 1 SMN', '', 'Grønt førstehjemslån', '1,\n"
     ]
    }
   ],
   "source": [
    "def html_to_table(html):\n",
    "    \"Returnerer tabellen definert i html som en liste\"\n",
    "    #defining the table:\n",
    "    table=[]\n",
    "    #iterating over all rows\n",
    "    for row in html.find_all('tr'):\n",
    "        r=[]\n",
    "        #finding all cells in each row:\n",
    "        cells=row.find_all('td')\n",
    "        \n",
    "        #if no cells are found, look for headings\n",
    "        if len(cells)==0:\n",
    "            cells=row.find_all('th')\n",
    "            \n",
    "        #iterate over cells:\n",
    "        for cell in cells:\n",
    "            cell=format(cell)\n",
    "            r.append(cell)\n",
    "        \n",
    "        #append the row to t:\n",
    "        table.append(r)\n",
    "    return table\n",
    "\n",
    "def format(cell):\n",
    "    \"Returnerer en streng etter konvertering av bs4-objektcelle til ren tekst\"\n",
    "    if cell.content is None:\n",
    "        s=cell.text\n",
    "    elif len(cell.content)==0:\n",
    "        return ''\n",
    "    else:\n",
    "        s=' '.join([str(c) for c in cell.content])\n",
    "        \n",
    "    #her kan du legge til flere tegn/strenger du vil \n",
    "    #fjern, endre tegnsetting eller formater strengen i andre\n",
    "    #ways:\n",
    "    s=s.replace('\\xa0','')\n",
    "    s=s.replace('\\n','')\n",
    "    return s\n",
    "\n",
    "table=html_to_table(table_html)\n",
    "\n",
    "#printing top\n",
    "print(str(table)[:1000])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "43f4857f",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "  Nominal Security fee Establishment fee Term Efficient\n",
      "0    1.69            0                 0   50      1.76\n",
      "1    1.78            0                 0    0      1.79\n",
      "2    1.75            0                 0   50      1.83\n",
      "3    1.81            0                 0    0      1.83\n",
      "4    1.75         1200                 0   75      1.86\n"
     ]
    }
   ],
   "source": [
    "def  save_data_to_csv ( file_name , table ): \n",
    "    \"\"\"\n",
    "    Lagrer numeriske data fra tabellen som csv atskilt med komma\n",
    "    \n",
    "    \"\"\"\n",
    "     \n",
    "    #initialize all table columns with numerical values\n",
    "    numeric_colums = [\"Nominal\",\"Security fee\",\"Establishment fee\",\"Term\",\"Efficient\"]\n",
    "    \n",
    "    df = pd.DataFrame([row[-5:] for row in table[1:]], columns=numeric_colums)\n",
    "    \n",
    "    #replace the commas in numeric data with \".\"\n",
    "    df[\"Nominal\"] = df[\"Nominal\"].apply(lambda w: w.replace(\",\",\".\"))\n",
    "    df[\"Efficient\"] = df[\"Efficient\"].apply(lambda w: w.replace(\",\",\".\"))\n",
    "    \n",
    "    print(df.head())\n",
    "    \n",
    "    #save the data to csv file\n",
    "    df.to_csv(file_name)\n",
    "\n",
    "         \n",
    "    \n",
    "save_data_to_csv( 'data.csv' , table )"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "499a17f0",
   "metadata": {},
   "source": [
    "# Regresjon\n",
    "    Jeg brukte regresjon for å analysere forholdet mellom nominelle og effektive variabler fra de skrapte dataene\n",
    "\n",
    "Et skjevhetsledd som er en variabel \"avskjæringspunkt\" lik én legges til x variabel.\n",
    "\n",
    "      y = α+β⋅x\n",
    " \n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "2cb7e110",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Unnamed: 0</th>\n",
       "      <th>Nominal</th>\n",
       "      <th>Security fee</th>\n",
       "      <th>Establishment fee</th>\n",
       "      <th>Term</th>\n",
       "      <th>Efficient</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>0</td>\n",
       "      <td>1.69</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>50</td>\n",
       "      <td>1.76</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>1</td>\n",
       "      <td>1.78</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>1.79</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>2</td>\n",
       "      <td>1.75</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>50</td>\n",
       "      <td>1.83</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>3</td>\n",
       "      <td>1.81</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>1.83</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>4</td>\n",
       "      <td>1.75</td>\n",
       "      <td>1200</td>\n",
       "      <td>0</td>\n",
       "      <td>75</td>\n",
       "      <td>1.86</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   Unnamed: 0  Nominal  Security fee  Establishment fee  Term  Efficient\n",
       "0           0     1.69             0                  0    50       1.76\n",
       "1           1     1.78             0                  0     0       1.79\n",
       "2           2     1.75             0                  0    50       1.83\n",
       "3           3     1.81             0                  0     0       1.83\n",
       "4           4     1.75          1200                  0    75       1.86"
      ]
     },
     "execution_count": 4,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#les dataene inn i pandas dataramme\n",
    "data = pd.read_csv('data.csv')\n",
    "data.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "6aaccb4f",
   "metadata": {},
   "source": [
    "### Scatter plot of \"Nominal\" against \"Efficient\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "f561f138",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<matplotlib.legend.Legend at 0x7f2461c47f70>"
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "fig,ax = plt.subplots()\n",
    "\n",
    "#legge til akseetiketter: \n",
    "ax.set_ylabel ('Nominal') \n",
    "ax.set_xlabel ('Efficient')\n",
    "\n",
    "#plotte funksjonen: \n",
    "ax.scatter( data[ 'Nominal' ],  data['Efficient'],   label = 'Observations' ) \n",
    "ax.legend ( loc = 'lower right' , frameon = False )"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "c9813f38",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Efficient</th>\n",
       "      <th>intercept</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>1.76</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>1.79</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>1.83</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>1.83</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>1.86</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   Efficient  intercept\n",
       "0       1.76          1\n",
       "1       1.79          1\n",
       "2       1.83          1\n",
       "3       1.83          1\n",
       "4       1.86          1"
      ]
     },
     "execution_count": 6,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "y = data[\"Nominal\"]\n",
    "\n",
    "x = pd.DataFrame(data[\"Efficient\"] )\n",
    "x['intercept'] = 1 \n",
    "x.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "3bd23ce8",
   "metadata": {},
   "source": [
    "### Estimat \n",
    "Anslå koeffisienter \n",
    "α\n",
    " og \n",
    "β\n",
    " som passer best til dataene. Så bruker vi OLS fra statsmodeller og setter inn y og x:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "8681e0c8",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "                            OLS Regression Results                            \n",
      "==============================================================================\n",
      "Dep. Variable:                Nominal   R-squared:                       0.999\n",
      "Model:                            OLS   Adj. R-squared:                  0.999\n",
      "Method:                 Least Squares   F-statistic:                 3.957e+05\n",
      "Date:                Tue, 03 May 2022   Prob (F-statistic):               0.00\n",
      "Time:                        01:24:15   Log-Likelihood:                 892.12\n",
      "No. Observations:                 361   AIC:                            -1780.\n",
      "Df Residuals:                     359   BIC:                            -1772.\n",
      "Df Model:                           1                                         \n",
      "Covariance Type:            nonrobust                                         \n",
      "==============================================================================\n",
      "                 coef    std err          t      P>|t|      [0.025      0.975]\n",
      "------------------------------------------------------------------------------\n",
      "Efficient      0.9599      0.002    629.055      0.000       0.957       0.963\n",
      "intercept      0.0091      0.004      2.170      0.031       0.001       0.017\n",
      "==============================================================================\n",
      "Omnibus:                       87.453   Durbin-Watson:                   1.402\n",
      "Prob(Omnibus):                  0.000   Jarque-Bera (JB):              177.242\n",
      "Skew:                           1.272   Prob(JB):                     3.25e-39\n",
      "Kurtosis:                       5.304   Cond. No.                         12.0\n",
      "==============================================================================\n",
      "\n",
      "Notes:\n",
      "[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.\n"
     ]
    }
   ],
   "source": [
    "model =OLS(y,x ).fit ()\n",
    "\n",
    "print (model.summary ())"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "f6599d1b",
   "metadata": {},
   "source": [
    "### Plot regression line"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "edc2f7f4",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAAXgAAAEGCAYAAABvtY4XAAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjMuNCwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy8QVMy6AAAACXBIWXMAAAsTAAALEwEAmpwYAAAqfElEQVR4nO3deZzO5f7H8dfHGAyRFhVKHJXQZGkqpVIkFUlKq044vxwtIktIkTY62o/qJNGmUpZJq0goFRm7pFKKUdHJGjIzrt8f1z0OmuWee+7v3DP3vJ+Pxzxm5t6+n9s58+66r+/ne13mnENEROJPmVgXICIiwVDAi4jEKQW8iEicUsCLiMQpBbyISJwqG+sC9nX44Ye72rVrx7oMEZESIy0t7TfnXLWc7itWAV+7dm0WLFgQ6zJEREoMM/sxt/s0RSMiEqcCDXgzu93MVpjZcjN7zcwqBHk8ERH5n8AC3sxqArcBKc65k4AE4OqgjiciIvsLeoqmLJBkZmWBisD6gI8nIiIhgQW8cy4deBj4CfgZ2OKc+/DAx5lZdzNbYGYLNm7cGFQ5IiKlTpBTNIcAlwJ1gBpAJTPrfODjnHOjnXMpzrmUatVy7PQREYlLqYvSaT5iJnUGvkvzETNJXZQe1dcPcormfOAH59xG51wGMBk4M8DjiYiUGKmL0hk0eRnpm3figPTNOxk0eVlUQz7IgP8JaGZmFc3MgFbAygCPJyJSYoyctoqdGVn73bYzI4uR01ZF7RhBzsHPAyYCC4FloWONDup4IiIlyfrNOwt0eyQCvZLVOTcUGBrkMURESqIaVZNIzyHMa1RNitoxdCWriEgM9G9Tj6TEhP1uS0pMoH+belE7RrFai0ZEpLTo0KQm4Ofi12/eSY2qSfRvU2/v7dGggBcRiZEOTWpGNdAPpCkaEZE4pYAXEYlTCngRkTilgBcRiVMKeBGROKWAFxGJUwp4EZE4pYAXEYlTCngRkTilgBcRiVMKeBGROKW1aERE8DssBbnwVywo4EWk1MvePi97h6Xs7fOAEh3ymqIRkVKvKLbPiwUFvIiUekWxfV6esrLyf0wEFPAiUurltk1eNLfPy9GWLdCnD7RqBc5F/eUV8CJS6hXF9nn7ycqCMWPg+OPh8cfhhBNg166oH0YnWUWk1CuK7fP2mjsXbrsNFi6E5s3hgw+gadPoHwcFvIgIEPz2eaxbBwMGwKuvQs2a/vvVV4NZYIcMbIrGzOqZ2eJ9vraaWe+gjiciUizt2gX33w/16sGkSXDXXbBqFVxzTaDhDgGO4J1zq4DGAGaWAKQDU4I6nohIseIcTJkCffvCmjVw+eUwciTUqVNkJRTVSdZWwGrn3I9FdDwRkdhZvhzOP9+H+kEHwUcfwcSJRRruUHQBfzXwWhEdS0QkNn7/HXr2hMaNYdEiGDXKf2/ZMiblBB7wZlYOaA+8mcv93c1sgZkt2LhxY9DliIhEX2YmPP20b3t8+mn45z/h22/hllugbOx6WYpiBH8RsNA592tOdzrnRjvnUpxzKdWqVSuCckREomjWLN/meMstcPLJfsT+1FNw2GGxrqxIAv4aND0jIvFmzRro1AnOOw+2bvVz7DNn+pAvJgINeDOrCLQGJgd5HBGRIrNjBwwZAvXrw7vvwr33wsqV/oRqwG2PBRXo5JBzbgcQ+88pIiKF5RxMmAD9+/uLlq65Bh56CI45JtaV5Upr0YiI5GfRImjRwod6tWrwySf+StRiHO6gpQpEpJiL6U5LGzf6K0+fe86fNB09Grp1g4SE/J9bDCjgRaTYitlOSxkZvhPmnntg+3bo1QuGDoWqVYM7ZgA0RSMixVZMdlr68ENo1Ahuvx1OPx2WLYPHHitx4Q4KeBEpxop0p6XVq+HSS6FNG9i9G6ZO9Uv51q8f/WMVEQW8iBRbRbLT0rZtMGgQNGjg+9hHjIAVK+CSS4pd22NBKeBFpNgKdKelPXvg5Zf9Mr4jRvi12Vet8mu2ly9f+NcvBnSSVUSKrcB2Wpo/3584/eILOPVUmDwZmjWLQsXFiwJeRIq1qO609MsvfjrmhRfgyCNh3Dj4+9+hTHxOZijgRST+/fknPPEE3Hef//mOO2DwYKhSJdaVBUoBLyLxyzm/XkyfPn753nbt4NFH/bK+pUB8fi4REVm1Ci6+2HfDJCTA++/D22+XmnAHBbyIxJstW6BfPzjpJPjsMz9iX7oULrww1pUVOU3RiEh8yMryJ0/vvNOvIdOtGzz4IBxxRKwrixkFvIiUfHPn+rbHtDRo3hzeew9OOSXWVcWcpmhEpORKT4frroOzzvItkOPH+6V8Fe6ARvAiUhLt2gWPPOKnYLKy/JK+AwdCpUqxrqxYUcCLSKEU6XrtzkFqKvTtCz/8AB07wsMPQ506wRyvhFPAi0jEinS99uXLoXdv+Ogj3yHz0UfQsmV0jxFnNAcvIhErkvXaf/8devaExo1h4UIYNcpvoadwz5dG8CISsUDXa8/K8lvk3X03bNoE//ynX2rgsMMK/9qlhEbwIhKxwNZrnz0bmjaFm2+G5GQ/Yn/6aYV7ASngRSRiUV+v/ccf4cor4dxz/RWpb7zhN+E4+eTCF1sKBRrwZlbVzCaa2ddmttLMzgjyeCJStDo0qcnwjsnUrJqEATWrJjG8Y3LBT7Du2OE3tT7xRHjnHRg2DFauhE6dSvyuSrEU9Bz8E8AHzrkrzKwcUDHg44lIhCJtdyzUeu3O+VF6//6wdq3fVemhh6BWrcheT/YTWMCbWRXgHKALgHNuN7A7qOOJSOSKtN0x2+LFfnmBOXN8h8z48XD22cEcq5QKcormb8BGYJyZLTKzMWb2l8vMzKy7mS0wswUbN24MsBwRyc2wt1cE3+6Y7bffoEcPv5zAV1/Bs8/CggUK9wAEGfBlgabAM865JsAfwMADH+ScG+2cS3HOpVSrVi3AckQkJ6mL0tm0IyPH+6LS7pgtI8PvqnT88TBmjO9t/+Yb6N7dr9cuURdkwK8D1jnn5oV+n4gPfBEpRvIapRe63THb9Ol+GqZ3b7/J9dKl8PjjcMgh0Xl9yVFgAe+c+wVYa2bZ/VKtgK+COp6IRCavUXrE7Y7ZVq+GDh3gggv8AmFvvQXTpkGDBoV7XQlL0F00PYHxoQ6a74GuAR9PRAqoRtUk0nMI+apJiZGfYN2+3a/0+MgjkJgIw4fD7bdD+fKFrFYKItA+eOfc4tD8+snOuQ7OuU1BHk9ECi63i5Xuad+w4C/mHLzyCtSr50P9qqv8PPvAgQr3GNBaNCKlXPYovdBL/n75pW97/PxzSEmBSZOgWbMAKpZwKeBFpHAXK/3yi98Hddw4OPJIGDsWbrgBymgllFhTwItIZHbvhiefhHvv9SdQ+/f3OytVqRLryiREAS8iBffee/6k6TffQNu28OijcMIJsa5KDqDPUCISvlWr4OKLfaiDD/p33lG4F1MKeBHJ35Yt0K+f3ypv7ly/D+qyZXDRRbGuTPKgKRoRyd2ePf7k6Z13wsaN0LWr728/8shYVyZhUMCLSM4++wxuuw3S0uDMM+Hdd337o5QYmqIRkf2lp0PnztC8uW+BHD8ePv1U4V4CaQQvUkJEuiFH2Hbt8t0wDz4ImZkweLC/AvWgg6J3DClSCniREiDQDTmc84uA9e0L338Pl13mT6L+7W+FLVtiTFM0IiXAyGmrgtmQ46uv/EqPl10GSUkwYwZMnqxwjxMKeJESILclfSPekGPTJr9uzMkn+5Oo//6330KvVavIi5RiRwEvUgLktvFGgTfkyMryW+QdfzyMGuV3U/rmG7j1ViirGdt4o4AXKQFyW9K3QBtyzJ7t90Ht0cNfsLRwITz9NBx+eJSrleJCAS9SAnRoUpPhHZOpWTUJA2pWTWJ4x+TwTrD++CNceSWce66fmnnjDfj4Y2jUKOiyJcb0mUykhCjwkr47dsC//gUPPQRmcM89fsXHihUDq1GKlzwD3sz65HW/c+7R6JYjIoXmHLz5pl87Zu1av6vSv/4FtWrFujIpYvmN4CsXSRUiEh1LlvjlBebMgcaN/fZ555wT66okRvIMeOfcsKIqREQK4bff4O67YfRoOPRQ3ynzj39AQkL+z5W4FdYcvJlVAP4BNAQqZN/unOsWUF0iEo6MDHjmGRg6FLZt8+2O99wDhxwS68qkGAi3i+Zl4CigDTAbOBrYFlRRIhKGGTP8NEyvXn4hsCVL4IknFO6yV7gBf5xz7m7gD+fci0BbIDm4skQkV9nrxbRu7RcIS02FDz+Ehg1jXZkUM+G2SWaEvm82s5OAX4Da+T3JzNbgR/pZQKZzTuuNikRq+3a/0uMjj0Biov/59tuhQoX8nyulUrgBP9rMDgHuBqYCBwFDwnzuec653yIpTkTwbY/jx8OAAbB+vV+rfcQIqBnFpYIlLoUV8M65MaEfZwNaZk6kqCxY4NseP//cz7NPnAhnnBHrqqSECLeLpjxwOX5aZu9znHP35vNUB3xoZg541jk3OofX7g50B6ilCzFEvF9/9fugjhsHRxwBY8fCDTdAGa0uIuELd4rmLWALkAb8WYDXb+6cW29mRwDTzexr59ycfR8QCv3RACkpKa4Ary0Sf3bv9kv33nsv7NwJffrAkCFQpUqsK5MSKNyAP9o5d2FBX9w5tz70fYOZTQFOA+bk/SyRUur996F3b79878UXw2OPwQknxLoqKcHC/bz3mZkVqC3SzCqZWeXsn4ELgOUFrE8k/n3zDbRt60Md4N13/ZfCXQop3BH8WUAXM/sBP0VjgHPOnZzHc44EpphZ9nFedc59UJhiReLK1q1w333+4qQKFfw+qD17Qrlysa5M4kS4AX9RQV/YOfc9oAWnRQ60Zw+8+CIMGgQbNkDXrr6n/cgjY12ZxJn8lguu4pzbipYlEImOzz/3bY8LFvh2x3fe8e2PIgHIbwT/KtAO3z3j8FMz2RzqiRcJz/r1/kKlV16B6tXh5Zfhuuv8RhwiAclvueB2oe91iqYckTizaxc8+qifgsnI8NMyd94JBx0U68qkFAh7yz4zO5m/Xug0OYCaREo+52DqVN/H/v33cOmlfg2ZunVjXZmUIuFeyToWOBlYAewJ3ewABbzIgb76yvezT58ODRr4lR5bt451VVIKhTuCb+acaxBoJSJFKHVROiOnrWL95p3UqJpE/zb1CrahdU42bfKbbTz1FFSuDE8+CT16+JUfRWIg3ID/3MwaOOe+CrQakSKQuiidQZOXsTMjC4D0zTsZNHkZQGQhn5UFY8bA4ME+5Lt39/3thx8ezbJFCizcK1lfxIf8KjNbambLzGxpkIWJBGXktFV7wz3bzowsRk5bVfAXmzPHtzn26OE33EhL81voKdylGAh3BD8WuB5Yxv/m4EVKhAOnY9I378zxcetzuT1HP/0Ed9wBEybAMcf47506qe1RipVwA/4n59zUQCsRCUBO0zGG7xA4UI2qSfm/4I4dMHIkPPSQ75QZOtQHfcWKUa1bJBrCDfivzexV4G32WS5YbZJSXGWP2nMarWdfsbdvyCclJtC/Tb3cX9A5v9lGv35+9H7llT7otYeBFGPhBnwSPtgv2Oc2tUlKsXTgqD0nDqhZNSm8LpqlS/3yArNnQ6NG8NJL0KJFMMWLRFG4W/Z1DboQkcLKa9R+oJpVk5g7sGXeD/rvf+Huu+HZZ+GQQ/zJ0xtvhISEKFUsEqywumjM7Ggzm2JmG8zsVzObZGZHB12cSLiyR+3hhHu+0zGZmX5XpeOPh9Gj4ZZb4NtvfaeMwl1KkHDbJMcBU4EaQE38XPy4oIoSKaicWh9zUrNqEsM7Juc+HfPRR9C4sZ+SOeUUWLLEX7B0yCHRLVikCIQ7B1/NObdvoL9gZr0DqEckIvm1OCYlJuQd7D/8AH37wpQpUKeO/37ppWp7lBIt3BH8b2bW2cwSQl+dgf8GWZhIQeTV4pjnqH37dn8Fav36fs2YBx7wa8l06KBwlxIv3BF8N2AU8Bi+AeGz0G0ixUL/NvX+0jmT56jdOXj1Vd/Dvn69X5v9oYegZiHXoxEpRsLtovkJaB9wLSIRyw7xsBYQS0uDXr1g7lw/z/7mm3DmmUVcsUjw8tuyb0gedzvn3H1RrkckYh2a1Mx7sbANG/xmG2PHQrVq8Pzz0KULlAl3plKkZMlvBP9HDrdVAv4BHAYo4KX4270bRo2CYcP8UgN9+vj+9oMPjnVlIoHKb8u+R7J/NrPKQC+gK/A68EhuzxMpNt5/H26/HVatgosv9tvn1cujB14kjuT72dTMDjWz+4Gl+P8gNHXODXDObQi8OpFIffsttGvnQ33PHnj3Xf+lcJdSJL85+JFAR2A0kOyc217QA5hZArAASM/exFtkX1HdXWnrVrj/fnj8cahQwS8IdtttUK5cVGsWKQnym4Pvi19k7C5gsP2vL9jwJ1mrhHGMXsBKIJzHSikTtd2V9uyBF1+EQYPg11+ha1d48EE46qggyhYpEfKconHOlXHOJTnnKjvnquzzVTmccA+tV9MWGBOtgiW+RGV3pS++gGbNoFs3fxXq/Pm+U0bhLqVc0P1hjwN3kMcuUGbW3cwWmNmCjRs3BlyOFDe5LTEQ1u5K69fD9dfDGWfAunXw8su+t/3UU6NcpUjJFO6VrAVmZu2ADc65NDM7N7fHOedG4+f4SUlJyWmjHYkjd6Uu47V5a8lyjgQzKpZL4I/df10kLM/dlXbt8nPs998PGRkwcKDvb69cObjCRUqgwAIeaA60N7OLgQpAFTN7xTnXOcBjSjF2V+oyXvnip72/ZznHH7uzSChjZO3533/bc13O1zmYOtX3sX//vV8v5uGHoW7dIqhepOQJLOCdc4OAQQChEXw/hXvpkVNnzGvz1ub42D17XP67K331FfTuDdOnQ4MGfmGw1q2DfyMiJViQI3gppVIXpdN/4hIysvyoPH3zTvpPXEKWy3kGzkHuuytt2uSvQB01yk/BPPEE3HQTJCYGVL1I/CiSgHfOzQJmFcWxJPaGvb1ib7hnO/D3fSXktCxvVhaMGQN33eW3zuveHe67z68hIyJh0SpLEnWbdmQU6PHXnH7M/jd88gmkpPgt8urXh4UL4T//UbiLFJACXopU52a19o7YE8zo3KwW93dI9neuXQtXXw3nnONH7a+/DrNn+y30RKTANAcvEcttiYGqSYls3vnXUXzVpETu75D8v0DPtnOnX1JgxAjfKTNkCAwYABUrFtE7EYlPCniJSF5LDNzTviH931xCxj6tj4lljHvaN9z/RZyDSZOgXz/48Ue44grf9njssUX2PkTimaZoJCJ5LTHQoUlNRnZqRM2qSRh+T9SRnRrt3/q4dCm0bAmdOvl12T/+2O+spHAXiRqN4CUi+S0xkOvuSv/9r99s49lnoWpVePppuPFGKKv/K4pEm/6qJF/XPfc5c1f/vvf35nUPpUbVJNJzCPlclxjIzPSdMEOG+CV9b77Z97cfemhQZYuUepqikTwdGO4Ac1f/TsVyZUhKTNjv9lyXGJg5E5o0gZ49oWlTWLwY/v1vhbtIwBTwkqvURel/Cfds3274g+Edk/ebZx/eMXn/aZkffoDLL4dWrWD7dpg82S81cNJJRfMGREo5TdFIjrK7ZPKS6zz7H3/A8OG+IyYhwa/62Lev32FJRIqMAl5ylFOXTL6cg9degzvugPR0uPZaeOghOProYIoUkTxpikZylN+GG83rHjB/vnAhnH02XHcdHHkkfPopjB+vcBeJIY3gS7G8NrvOrUsGfLiPv/EM/8uGDTB4MDz/vF8r5rnn/H6oCQk5PldEio4CvpTJDvX0zTv9zumh2w/c7Lp/m3r7XakKvktm74nUjAy/hO+wYX7O/fbbfQvkwQcX/ZsSkRxpiqYUSV2Uzu0TFu8dmR+4gO++m113aFIz9y6ZDz6A5GS/s9KZZ8Ly5fDIIwp3kWJGI/hSInVROr0nLM73cfvOvf+lS+bbb+GSS+Cdd+D44/33tm0DqFZEokEBXwq0fnQW3274I6zH5ngl6tatvtXx8cehfHnfGdO7N5QrF9U6RSS6FPBx7MBNrvPzlytR9+yBl16CQYPgl1+gSxff337UUdEvVkSiTgEfZ3JaWiAcNQ/c7HrePLjtNpg/H5o1g6lT4dRTo1ytiARJAR9HIg3344+oxPQ+5/pf1q+HgQPh5ZehenU/gr/uOiij8/EiJY0CPk7clbqscOH+55/w2GPwwAOwe7cP+TvvhMqVo1+siBQJBXwcKMhJ1H01r3so4/+vGbz9tu9jX70a2rf3LY/HHRdApSJSlAILeDOrAMwByoeOM9E5NzSo45VGpz8wnV+37Y7ouc3rHsr4s6rCRRfBtGlQv77/fsEF0S1SRGImyBH8n0BL59x2M0sEPjWz951zXwR4zFIh3J72A5UBHr2qMR3qVPJXoN48CipV8lMzt9wCiYlRr1VEYiewgHfOOWB76NfE0NeBF09KAUUa7jWrJtH//OPo8OW7cMFgv3XejTf6/vZq1aJfqIjEXKBz8GaWAKQBxwFPOefm5fCY7kB3gFq1agVZTolVmKmYKuUTWDrsQr+6Y/cOsGgRnHUWPPmk32VJROJWoL1vzrks51xj4GjgNDP7y1Y+zrnRzrkU51xKNY0k/6Iw4X5k5XIs/b+GcM01finfjRv9eu1z5ijcRUqBIumicc5tNrNZwIXA8qI4ZjyoPfDdiJ9bq4Jjzp4v4MQO/orUu++GAQP8nLuIlApBdtFUAzJC4Z4EnA88FNTx4kXqonTumbqCzTszCvzcIyuXY96d58OkSdCvH/z4o98T9eGHoXbt6BcrIsVakCP46sCLoXn4MsAbzrl3AjxeiZe9nG8kZ6LLGsy75Eho2RJmzfLL+c6cCeedF+0yRaSECLKLZimgid4wnTj4PXZlRdZkdPiurSzI+BSa/AeqVoWnn/YdMmV1HZtIaaYEiKG7Upfx2ry1ZLnIgv2Jy0/i0vnv+Pn1rVvh5pt9f/uhh+b/ZBGJewr4GCnoUr77qphYhtHHbOOsbu38bkotW8ITT8BJf2lSEpFSTAEfA4VpfexZpwx9PxwD90/2J04nTYLLLgOz6BYpIiWeAr6IRdr6mLR7F0+v+5DzHn8REhL8Fah9+kBSDjswiYiggC8Ska7TDoBztF85hycXvQbr1sG11/ot844+OrpFikjcUcAHLNKlfAEa/vIdw2Y+R8raFdC0Kbz+OjRvHuUKRSReKeADlLooPaJwP3THFvrNeYmrl35IRtVD4bnnoGtXPzUjIhImBXyUpS5Kp+8bi4mkpb1sViZDf5zJ9R++CH/8Ab17U37IEN/bLiJSQAr4KIp0KV+Ac75PY/gnY6n5y4/Qpo1fo71+/egWKCKligI+So4b9C6ZEYzaj920nrtmjqH1d/P9Nnlvvw1t26rtUUQKTQFfSJGO2iv9uYNbP3+Dfyx4CytfznfG9OoF5ctHv0gRKZUU8IUQydWo5vbQcfnHPDB/PBV+2wA33ADDh0P16gFVKSKllQI+ApFOxzRev4qhM0bT5OdVcNpp8M5UOP306BcoIoICvsDqDHy3wMv5Vtv+OwNmv8gVyz9iQ6VD4IUX4PrroUygG2qJSCmngA9TJKP2cpkZdE17i56fTSAxK4NnTr+Cjb36MuSaZsEUKSKyDwV8PiJaZsA5Wq2ez10zx1Bn089MP+50hrf6P8688HTu75AcTKEiIgdQwOchknCv+9+1DPnoOVr8sJA11Wrx2ahXaH3LdbQOqEYRkdwo4HMQye5KVXZt57a5r3HDwnfYmViBf13QnTveGUXtxMSAqhQRyZsCPiR1UTp3Tl7Kjow9BXpemT1ZXLl0Ov0+eZlDd2zl9UYXMPr8Lsx6+OqAKhURCY8Cnsh3V0pZt4KhM0aT/OtqOOsseOIJrm3alGsDqFFEpKBKfcBHsgHHUVt/Y9CscVy6cjY7jzgKXnsNrrpKywuISLFSqgO+oOFePuNPbvxyCjd/8SaJOLj7bpIGDIBKlQKqUEQkcqUy4Au8CYdzXPjNZwz+eCzHbPmV9084k4s+eAXq1AmuSBGRQgos4M3sGOAl4ChgDzDaOfdEUMcLR+qidPpMWExBTqPW27iGoTNGc+ZPS/n68GO55uoHqHvVJVykcBeRYi7IEXwm0Nc5t9DMKgNpZjbdOfdVgMfMVUFPpB68cxt9Pn2FzoveZ2v5StzdugcTmlzMlWfU1sVKIlIiBBbwzrmfgZ9DP28zs5VATaBIAz51UTr3TF3B5p0ZYT0+YU8W1yz+gL6fvEKVP//glSYXMeqczgz++9nc16RmwNWKiERPkczBm1ltoAkwL4f7ugPdAWrVqhXV46YuSmfQ5GXszMgK6/HNflrK0Bmjqb9xDZ/VOplh53dnTfW/8dDlJ9NB4S4iJUzgAW9mBwGTgN7Oua0H3u+cGw2MBkhJSYlgEd6c+b1Rl5Dl8n/Jo7f8yqCPx9J21VzWVTmCHh0G8WG9M7m22bFM03SMiJRQgQa8mSXiw328c25ykMcCH+ojp60iffPOsB6ftHsXPeZN5J/zJ+MwHjnrOkaf1pGUE6vz/Y1nBFytiEiwguyiMeB5YKVz7tGgjpMtdVE6/ScuISOcNWSc45KVcxg0axw1tv3GW/VbMOLcLvxSpRrXNaulk6giEheC3HGiOXA90NLMFoe+Lg7qYMPeXhFWuDf8dTUTXh3Iv98eye8VD+aK6x6iz6V30OqCU/hhRFuFu0gxsm7dOi699FKOP/546tatS69evdi9ezcvvPACt956a6zLIzU1la+++l/fyJAhQ5gxY0YMK9pfkF00nwKBX7ufPS2zaUfeXTKH7thCvzkvc/WSaWxKqsygNrdy+v39mZgS3RO7IqVV9t/i+s07qVE1if5t6hWqOcE5R8eOHbnpppt46623yMrKonv37gwePJiGDRtGsXIvMzOTsmULFompqam0a9eOBg0aAHDvvfdGva7CKNF7xmV3yeQ15142K5NuX77FrNHd6bRsOuNS2nNe99Ek9OhOB4W7SFTs+7fogPTNOxk0eRmpi9Ijfs2ZM2dSoUIFunbtCkBCQgKPPfYYY8eOZceOHaxdu5YLL7yQevXqMWzYMAD++OMP2rZtS6NGjTjppJOYMGECAGlpabRo0YJTTjmFNm3a8PPPPwNw7rnncuedd9KiRQseeOABateuzZ49/lLIHTt2cMwxx5CRkcFzzz3HqaeeSqNGjbj88svZsWMHn332GVOnTqV///40btyY1atX06VLFyZOnAjARx99RJMmTUhOTqZbt278+eefANSuXZuhQ4fStGlTkpOT+frrrwGYPXs2jRs3pnHjxjRp0oRt27ZF/G+XrUQH/Mhpq/JsgTz7h4W8P64nQ2Y+x+LqJ3Bh11GMvfw27r3hLE3FiERRTn+LOzOyGDltVcSvuWLFCk455ZT9bqtSpQq1atUiMzOT+fPnM378eBYvXsybb77JggUL+OCDD6hRowZLlixh+fLlXHjhhWRkZNCzZ08mTpxIWloa3bp1Y/DgwXtfc/PmzcyePZuhQ4fSqFEjZs+eDcDbb79NmzZtSExMpGPHjnz55ZcsWbKE+vXr8/zzz3PmmWfSvn17Ro4cyeLFi6lbt+7e19y1axddunRhwoQJLFu2jMzMTJ555pm99x9++OEsXLiQm266iYcffhiAhx9+mKeeeorFixfzySefkJSUFPG/XbYSHfDrcxm5H7tpPc9Nuo+X3xhCYlYm/7j8bv5+5b30vOUS5g5sqZ52kSjL7W8xt9vD4ZzDclihNfv21q1bc9hhh5GUlETHjh359NNPSU5OZsaMGQwYMIBPPvmEgw8+mFWrVrF8+XJat25N48aNuf/++1m3bt3e17vqqqv2+zl71P/666/vvW/58uWcffbZJCcnM378eFasWJFn7atWraJOnTqccMIJANxwww3MmTNn7/0dO3YE4JRTTmHNmjUANG/enD59+vDkk0+yefPmAk8X5aRELzZWo2rSftMzlf7cwa2fv0G3BalkJCQyokUXxqZcSkbZRDo3q6VgFwnIgX+L+94eqYYNGzJp0qT9btu6dStr164lISHhL+FvZpxwwgmkpaXx3nvvMWjQIC644AIuu+wyGjZsyOeff57jcSrtsxps+/btGTRoEL///jtpaWm0bNkSgC5dupCamkqjRo144YUXmDVrVp61u3yuvylfvjzgp50yMzMBGDhwIG3btuW9996jWbNmzJgxgxNPPDHP18lPiR7B929Tj6TEBMztoePyj5g5pgc3zZvIV2dfxHV9X+DZZldQ7fAqPHZVY03JiAQo+29xX0mJCfRvUy/i12zVqhU7duzgpZdeAiArK4u+ffvSpUsXKlasyPTp0/n999/ZuXMnqampNG/enPXr11OxYkU6d+5Mv379WLhwIfXq1WPjxo17Az4jIyPXEfhBBx3EaaedRq9evWjXrh0JCf49bdu2jerVq5ORkcH48eP3Pr5y5co5zpWfeOKJrFmzhu+++w6Al19+mRYtWuT5flevXk1ycjIDBgwgJSVl79x8YZToEXyHJjVJ3LaF2p2voOHalaw4+kS+HjWOFje0561YFydSimR/Oo5mF42ZMWXKFG6++Wbuu+8+9uzZw8UXX8yDDz7Ia6+9xllnncX111/Pd999x7XXXktKSgrTpk2jf//+lClThsTERJ555hnKlSvHxIkTue2229iyZQuZmZn07t07106cq666ik6dOu03Sr/vvvs4/fTTOfbYY0lOTt4b6ldffTU33ngjTz755N6TqwAVKlRg3LhxdOrUiczMTE499VR69OiR5/t9/PHH+fjjj0lISKBBgwZcdNFFEf/b7f03zO+jRFFKSUlxCxYsKNiTnIPrr4fWrf33MiX6Q4mISIGYWZpzLiWn+0r0CB7w2+S98kqsqxARKXY03BURiVMKeBGROKWAFxGJUwp4EZE4pYAXEYlTCngRkTilgBcRiVMKeBGROFWsrmQ1s43AjzE6/OHAbzE6dhDi7f1A/L2neHs/EH/vqSS8n2Odc9VyuqNYBXwsmdmC3C73LYni7f1A/L2neHs/EH/vqaS/H03RiIjEKQW8iEicUsD/z+hYFxBl8fZ+IP7eU7y9H4i/91Si34/m4EVE4pRG8CIicUoBLyISp0p9wJvZMWb2sZmtNLMVZtYr1jUVhplVMLP5ZrYk9H6GxbqmaDCzBDNbZGbvxLqWaDCzNWa2zMwWm1kBtzErfsysqplNNLOvQ39LZ8S6psIws3qh/22yv7aaWe9Y11VQpX4O3syqA9WdcwvNrDKQBnRwzn0V49IiYn6r+UrOue1mlgh8CvRyzn0R49IKxcz6AClAFedcu1jXU1hmtgZIcc4V94towmJmLwKfOOfGmFk5oKJzbnOMy4oKM0sA0oHTnXOxuhAzIqV+BO+c+9k5tzD08zZgJRD5TsEx5rztoV8TQ18l+r/iZnY00BYYE+ta5K/MrApwDvA8gHNud7yEe0grYHVJC3dQwO/HzGoDTYB5MS6lUELTGYuBDcB051yJfj/A48AdwJ4Y1xFNDvjQzNLMrHusiymkvwEbgXGhabQxZlYp1kVF0dXAa7EuIhIK+BAzOwiYBPR2zm2NdT2F4ZzLcs41Bo4GTjOzk2JcUsTMrB2wwTmXFutaoqy5c64pcBFwi5mdE+uCCqEs0BR4xjnXBPgDGBjbkqIjNN3UHngz1rVEQgEPhOaqJwHjnXOTY11PtIQ+Js8CLoxtJYXSHGgfmrN+HWhpZq/EtqTCc86tD33fAEwBTottRYWyDli3zyfFifjAjwcXAQudc7/GupBIlPqAD52UfB5Y6Zx7NNb1FJaZVTOzqqGfk4Dzga9jWlQhOOcGOeeOds7Vxn9Unumc6xzjsgrFzCqFTugTmsq4AFge26oi55z7BVhrZvVCN7UCSmSTQg6uoYROz4D/aFXaNQeuB5aF5q0B7nTOvRe7kgqlOvBi6Mx/GeAN51xctBbGkSOBKX5sQVngVefcB7EtqdB6AuNDUxrfA11jXE+hmVlFoDXwz1jXEqlS3yYpIhKvSv0UjYhIvFLAi4jEKQW8iEicUsCLiMQpBbyISJxSwEtcMrOsA1YDHBi6/ezQKpuLzSzJzEaGfh9pZj3M7O95vGYNM5tYiJp6h1rvRIqE2iQlLpnZdufcQTnc/h9gnnNuXOj3rUA159yfRVDTGuJoBUkp/nShk5QaZvZ/wJVAGzM7H6gMVALmmdlwoD6w3Tn3sJkdB/wHqAZkAZ1C399xzp0UupBsBHAuUB54yjn3rJmdC9wD/AachF9+ujP+QqAawMdm9ptz7rwiedNSqingJV4l7XNlMsDw0FrlZ+FDeiLsHek3Dv18zz6PHw+McM5NMbMK+OnMI/a5/x/AFufcqWZWHphrZh+G7msCNATWA3PxC4s9GVrT/jyN4KWoKOAlXu3MDu6CCq0TU9M5NwXAObcrdPu+D7sAONnMrgj9fjBwPLAbmO+cWxd6zmKgNn7jFZEipYAX+SvL/yEY0NM5N22/G/0Uzb7z+Vno70xiRF00IgcI7Qewzsw6AJhZ+Ry6X6YBN4WWmsbMTghjk4tt+Hl/kSKhgJd4lXRAm+SIAj7/euA2M1sKfAYcdcD9Y/BL4i40s+XAs+Q/Uh8NvG9mHxewFpGIqE1SRCROaQQvIhKnFPAiInFKAS8iEqcU8CIicUoBLyISpxTwIiJxSgEvIhKn/h9WigS3iM4nwgAAAABJRU5ErkJggg==\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "execution_count": 8,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "x=np.linspace(min(data[\"Nominal\"]),  max (data[\"Nominal\"]),  100 )\n",
    "\n",
    "regression_line = model.params ['intercept'] + model.params ['Efficient'] * x\n",
    "\n",
    "ax.plot(x,regression_line , color = 'red' ) \n",
    "fig"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "6e77e344",
   "metadata": {},
   "source": [
    "### Result\n",
    "The results of the regression above, Shows that:\n",
    "\n",
    "    α = 0.009\n",
    "    β = 0.9599\n",
    "\n",
    "    The regression line fits the data well.This line represent the least distance on average to the the points\n",
    " in the our data. The distance is measured as square of the vertical difference.writen as:\n",
    "    \n",
    "    y = α+β⋅x\n",
    "    \n",
    "Which is an equation of a straight line with a +ve gradient.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "caae3ec6",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.8"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}