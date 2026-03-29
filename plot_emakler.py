import pandas as pd
import matplotlib.pyplot as plt
import re
import matplotlib
# Ścieżka do pliku CSV
file_path = 'eMAKLER_portfel_wyceny_historyczne.Csv'

#matplotlib.use("GTK4Agg")   # albo Qt5Agg jeśli masz Qt

# Funkcja parsująca pojedynczy blok danych
def parse_block(block):
    lines = block.splitlines()
    date_str, _ = lines[0].split(';')
    date = pd.to_datetime(date_str.strip(), dayfirst=True)
    holdings_data = lines[2:]
    columns = ['Papier', 'Giełda', 'Liczba', 'Blokada', 'Udział %', 'Wartość', 'Waluta']
    rows = [line.split(';') for line in holdings_data if line]
    df = pd.DataFrame(rows, columns=columns)
    df['Wartość'] = pd.to_numeric(df['Wartość'], errors='coerce')
    df['Liczba'] = pd.to_numeric(df['Liczba'], errors='coerce')
    return date, df

# Wczytanie i rozdzielenie bloków danych
with open(file_path, 'r', encoding='cp1250') as f:
    raw_text = f.read()

blocks = re.split(r'\nData;Wycena\n', raw_text)[1:]

# Parsowanie wszystkich bloków do jednej ramki danych
all_data = []
for block in blocks:
    date, df = parse_block(block)
    df['Date'] = date
    all_data.append(df[['Date', 'Papier', 'Liczba', 'Wartość']])

portfolio_df = pd.concat(all_data)

# Obliczenie wartości jednostkowej (wartość / ilość)
portfolio_df['Wartość_jednostkowa'] = portfolio_df['Wartość'] / portfolio_df['Liczba']

# Pivot do szerokiego formatu
pivot_value_per_unit = portfolio_df.pivot(index='Date', columns='Papier', values='Wartość_jednostkowa').fillna(0)
pivot_quantity = portfolio_df.pivot(index='Date', columns='Papier', values='Liczba').fillna(0)
pivot_value_total = portfolio_df.pivot(index='Date', columns='Papier', values='Wartość').fillna(0)
pivot_value_total['Total'] = pivot_value_total.sum(axis=1)

# Tworzenie wykresów
fig1, ax1 = plt.subplots(figsize=(14, 7))
pivot_value_total.drop(columns=['Total']).plot.area(stacked=True, ax=ax1)
ax1.set_title('Segmentacja wartości portfela wg pozycji (skumulowana)')
ax1.set_ylabel('Wartość w PLN')
ax1.set_xlabel('Data')
ax1.legend(loc='upper left')
fig1.tight_layout()
plt.show()

fig2, ax2 = plt.subplots(figsize=(14, 7))
pivot_value_per_unit.plot(ax=ax2)
ax2.set_title('Wartość jednostkowa (wartość/ilość) dla każdej pozycji')
ax2.set_ylabel('Wartość jednostkowa (PLN)')
ax2.set_xlabel('Data')
ax2.legend(loc='upper left')
fig2.tight_layout()
plt.show()

