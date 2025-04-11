import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

def ema_macd(data, N, current_date):
   
    filtered_data = data.loc[data['Data'] <= current_date].tail(N + 1)
    
    zamkniecie_values = filtered_data['Zamkniecie'].tolist()[::-1]
    
    alpha = 2 / (N + 1)
    ema = zamkniecie_values[0]  
    denominator = sum([(1 - alpha)**i for i in range(N + 1)])
    for i, value in enumerate(zamkniecie_values[1:], start=1):
        ema += (1 - alpha)**i * value
    
    ema /= denominator
    
    return ema
  
def ema_signal(macd, N, cur_index):
    alpha = 2 / (N + 1)
    macd_values = macd[cur_index - N:cur_index][::-1]
    signal = macd_values[0]
    denominator = sum([(1 - alpha)**i for i in range(N)])
    for i, value in enumerate(macd_values[1:], start=1):
        signal += (1 - alpha)**i * value
    signal /= denominator
    return signal
    



plt.rcParams.update({'font.size':16})

df = pd.read_csv('wig_d.csv')
df['Data'] = pd.to_datetime(df['Data'])
df = df.tail(1000)

plt.figure(figsize=(10, 4.5))
plt.plot(df['Data'], df['Zamkniecie'], linewidth=1)
plt.xlabel('Rok')
plt.ylabel('Wartość')
plt.title('Notowania indeksu WIG na przestrzeni lat')
date_form = DateFormatter("%Y")
plt.gca().xaxis.set_major_formatter(date_form)
plt.show()
                                                 
cur_index = 26
current_date = df['Data'].iloc[cur_index]
macd = []
signal = []
for i in range(9):
    macd.append(ema_macd(df, 12, current_date) - ema_macd(df, 26, current_date))
    cur_index += 1
    current_date = df['Data'].iloc[cur_index]
    
for i in range(cur_index, len(df) - 1):
    macd.append(ema_macd(df, 12, current_date) - ema_macd(df, 26, current_date))
    signal.append(ema_signal(macd, 9, cur_index-26))
    cur_index += 1
    current_date = df['Data'].iloc[cur_index]




plt.plot(df['Data'].iloc[36:], macd[9:], label='MACD', color='blue', linewidth=1)  
plt.plot(df['Data'].iloc[36:], signal, label='SIGNAL', color='red', linewidth=1)   


buy_signal_dates = []
buy_signal_values = []
sell_signal_dates = []
sell_signal_values = []
for i in range(0, len(signal)):
    if macd[i+9] > signal[i] and macd[i+9 - 1] <= signal[i - 1]:
        # Buy signal: MACD crosses Signal from below
        buy_signal_dates.append(df['Data'].iloc[i+36])
        buy_signal_values.append(signal[i])
    elif macd[i+9] < signal[i] and macd[i+9 - 1] >= signal[i - 1]:
        # Sell signal: MACD crosses Signal from above
        sell_signal_dates.append(df['Data'].iloc[i+36])
        sell_signal_values.append(signal[i])

plt.scatter(buy_signal_dates, buy_signal_values, color='green', marker='o', label='Kupuj', s=20)
plt.scatter(sell_signal_dates, sell_signal_values, color='purple', marker='o', label='Sprzedaj',s=20)

plt.legend(handles=[plt.Line2D([], [], color='blue', linestyle='-', label='MACD'),
                    plt.Line2D([], [], color='red', linestyle='-', label='SIGNAL'),
                    plt.Line2D([], [], color='green', marker='o', linestyle='None', label='Kupuj'),
                    plt.Line2D([], [], color='purple', marker='o', linestyle='None', label='Sprzedaj')])

plt.xlabel('Rok')
plt.ylabel('')
plt.title('Wykres wskaźnika MACD')
plt.gca().xaxis.set_major_formatter(date_form)
plt.show()


portfolio_values = []
shares_values = []
initial_portfolio = 100000
portfolio = initial_portfolio 
shares = 0

baf_values = []
buy_and_forget = initial_portfolio
shares_baf = initial_portfolio // df['Zamkniecie'].iloc[36]
buy_and_forget -= shares_baf * df['Zamkniecie'].iloc[36]


for i in range(36, len(signal)):
    if df['Data'].iloc[i] in buy_signal_dates:
        shares = portfolio // df['Zamkniecie'].iloc[i]
        portfolio = portfolio % df['Zamkniecie'].iloc[i]
    elif df['Data'].iloc[i] in sell_signal_dates:
        portfolio += shares * df['Zamkniecie'].iloc[i]
        shares = 0
    
    
    shares_value = shares * df['Zamkniecie'].iloc[i]
    baf_value = buy_and_forget + shares_baf * df['Zamkniecie'].iloc[i] 
    
    

    portfolio_values.append(portfolio+shares_value)
    shares_values.append(shares_value)
    baf_values.append(baf_value)
    
print('MACD')
print(f'Początkowa wartość: {initial_portfolio:.2f}')
print(f'Końcowa wartość:', portfolio_values[-1].round(2))
print('Zysk:', (portfolio_values[-1] - initial_portfolio).round(2))

print('\nKup i Zapomnij')
print(f'Początkowa wartość: {initial_portfolio:.2f}')
print(f'Końcowa wartość:', baf_values[-1].round(2))
print('Zysk:', (baf_values[-1] - initial_portfolio).round(2))


plt.figure(figsize=(12, 6))


plt.subplot(2, 1, 1)
plt.plot(df['Data'].iloc[:928], portfolio_values, label='MACD', color='blue')
plt.plot(df['Data'].iloc[:928], baf_values, label='Kup i Zapomnij', color='green')
plt.xlabel('Data')
plt.ylabel('Wartość')
plt.title('Zależność wartości portfela od czasu w zależności od strategii')
plt.legend()
plt.show()




