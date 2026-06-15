import pandas as pd
import plotly.express as px
import scipy.signal as signal

# Wir holen uns eure perfekte Lade-Funktion aus dem alten Code!
from source.read_write_data import read_my_txt

class Ekgdata:
    def __init__(self, ekg_dict):
        self.id = ekg_dict.get("id")
        self.date = ekg_dict.get("date")
        self.result_link = ekg_dict.get("result_link")
        self.df = None
        self.peaks = []
        
        self.load_data()

    def load_data(self):
        try:
            # Hier nutzen wir eure eigene Funktion!
            self.df = read_my_txt(self.result_link)
            # Wir benennen eure Spalten kurz um, damit der Rest vom Code sie versteht
            self.df.rename(columns={"Zeit in ms": "Time", "Messwerte in mV": "Amplitude"}, inplace=True)
        except Exception as e:
            print(f"Fehler beim Laden der EKG Datei {self.result_link}: {e}")

    @classmethod
    def load_by_id(cls, ekg_dict):
        return cls(ekg_dict)

    def find_peaks(self):
        if self.df is not None:
            # Dynamische Peak-Suche anhand eurer Datenhöhe
            mean_amp = self.df['Amplitude'].mean()
            peaks, _ = signal.find_peaks(self.df['Amplitude'], distance=200, height=mean_amp)
            self.peaks = peaks
        return self.peaks

    def estimate_hr(self):
        if len(self.peaks) < 2:
            return 0
        
        time_first_peak = self.df['Time'].iloc[self.peaks[0]]
        time_last_peak = self.df['Time'].iloc[self.peaks[-1]]
        
        time_diff_seconds = (time_last_peak - time_first_peak) / 1000
        num_beats = len(self.peaks) - 1
        
        if time_diff_seconds > 0:
            hr = (num_beats / time_diff_seconds) * 60
            return int(hr)
        return 0

    def plot_time_series(self):
        if self.df is None:
            return None
            
        fig = px.line(self.df, x='Time', y='Amplitude', title='EKG Messung (3 Sekunden Ausschnitt)')
        
        if len(self.peaks) > 0:
            peak_times = self.df['Time'].iloc[self.peaks]
            peak_amps = self.df['Amplitude'].iloc[self.peaks]
            fig.add_scatter(x=peak_times, y=peak_amps, mode='markers', marker=dict(color='red', size=8), name='Peaks')
            
        # Wie in eurem alten Code: Wir zoomen in die ersten 3 Sekunden (3000 ms)
        start_time = self.df['Time'].min()
        end_time = start_time + 3000
        fig.update_layout(xaxis=dict(range=[start_time, end_time]))
            
        return fig