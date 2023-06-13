import tkinter as tk
from functools import partial
from tkinter import *
from matplotlib.backend_bases import NavigationToolbar2
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import struct
import time
import wavio as wv
from tkinter import messagebox
import sounddevice as sound
from scipy.io.wavfile import write 
import sounddevice as sd
import os
from scipy import signal

root = tk.Tk()
root.geometry('1920x1080')
# root.resizable(width=False, height=False)

background = tk.PhotoImage(file="GUI/record_GUI_img/background_new_img.png")
label_background = tk.Label(root, image = background)
label_background.pack()


def start_stream():
    n = True

    def stop_stream():
        n = False
        recorded_audio = 0
        recording=stream
        print("recording=",recording)
        stream.stop_stream()
        # plt.stop()/\
        
        # Save the recorded data as a WAV file
        filename = "recorded_audio.wav"
        filepath = os.path.join(os.getcwd(), filename)
        write(filepath, RATE, recorded_audio)

    record_button = tk.Label(label_background, image = record_img, borderwidth=0, highlightthickness=0)
    record_button.place(x=870, y=410)

    stop_record_button = tk.Button(label_background, image=stop_record_img, borderwidth=0, highlightthickness=0, command = stop_stream)
    stop_record_button.place(x=870, y=650)
    
    CHUNK = 4096  # số mẫu audio trong mỗi chunk
    RATE = 44100  # số mẫu audio trên giây
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)

    # Tạo biến cho miền tần số
    freqs = np.fft.rfftfreq(CHUNK, d=1. / RATE)

    # Khởi tạo figure cho matplotlib

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 8))

    # Thiết lập giá trị trục x, y cho FFT
    ax1.set_title("Frequency domain")
    ax1.set_xlim(40, 400)
    ax1.set_ylim(-20, 40)
    ax1.set_xlabel("")
    ax1.set_ylabel("Magnitude (dB)")
    line_fft, = ax1.plot(freqs, np.zeros(len(freqs)), color='blue')

    # Thiết lập giá trị trục x, y cho HSS
    ax2.set_xlim(40, 400)
    ax2.set_ylim(-20, 200)
    ax2.set_xlabel("Frequency (Hz)")
    ax2.set_ylabel("Magnitude (dB)")
    line_hps, = ax2.plot(freqs, np.zeros(len(freqs)), color='green')

    # Tạo bộ lọc bandpass
    lowcut = 16  # Tần số cắt thấp
    highcut = 20000  # Tần số cắt cao
    fs = RATE  # Tần số lấy mẫu
    order = 2  # Bậc của bộ lọc
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = signal.butter(order, [low, high], btype='band')

    # Create an empty list for storing maximum frequencies
    max_freqs = []

    # Calculate chunks per second
    chunks_per_second = int(RATE / CHUNK)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().place(x=1150,y = 170)
    def update_plot(n):
        while n: 
            print(n)
            data = stream.read(CHUNK)
            y = np.frombuffer(data, dtype=np.int16) / 32768.0

            # Lọc dữ liệu âm thanh bằng bộ lọc bandpass
            filtered_data = signal.lfilter(b, a, y)

            # Chuyển đổi sang miền tần số
            y_frequency = 20 * np.log10(abs(np.fft.rfft(filtered_data)))
            spectrum = abs(np.fft.rfft(filtered_data))

            # Tìm giá trị cực đại FFT
            max_index_fft = np.argmax(y_frequency)
            max_freq_fft = freqs[max_index_fft]
            max_magnitude_fft = y_frequency[max_index_fft]

            # modified HPS (HSS)
            hps = np.copy(spectrum)
            for factor in range(2, 6):
                downsampled = signal.decimate(spectrum, factor, zero_phase=True)
                hps[:len(downsampled)] += downsampled
            fundamental_index = np.argmax(hps)

            # Calculate HPS
            # hps = np.copy(spectrum)
            # for h in range(2, 6):
            #     decimated = np.copy(y)[::h]
            #     spectrum_h = np.fft.rfft(decimated)
            #     hps[:len(spectrum_h)] *= abs(spectrum_h)

            # Tìm fundamental frequency
            fundamental_frequency = 44100 * fundamental_index / len(filtered_data)

            # Cập nhật spectrum trên đồ thị matplotlib FFT
            line_fft.set_ydata(y_frequency)
            ax1.draw_artist(ax1.patch)
            ax1.draw_artist(line_fft)

            # Cập nhật spectrum trên đồ thị matplotlib HPS

            line_hps.set_ydata(hps)
            ax2.draw_artist(ax2.patch)
            ax2.draw_artist(line_hps)

            fig.canvas.blit(ax1.bbox)
            fig.canvas.blit(ax2.bbox)
            fig.canvas.flush_events()

            # Hiển thị giá trị cực đại trên đồ thị

            max_freqs.append(fundamental_frequency)

            if len(max_freqs) > chunks_per_second:
                max_freqs.pop(0)

            average_max_freq = np.mean(max_freqs)
            ax2.set_title(f"Average Fundamental Frequency: {average_max_freq:.2f} Hz")

            # print("FFT", max_freq_fft)

            print("HPS", fundamental_frequency)
            if 81 <= fundamental_frequency <= 83:
                line_hps.set_color('green')
            elif 109 <= fundamental_frequency <= 111:
                line_hps.set_color('green')
            elif 146 <= fundamental_frequency <= 148:
                line_hps.set_color('green')
            elif 195 <= fundamental_frequency <= 197:
                line_hps.set_color('green')
            elif 246 <= fundamental_frequency <= 248:
                line_hps.set_color('green')
            elif 328 <= fundamental_frequency <= 330:
                line_hps.set_color('green')
            else:
                line_hps.set_color('red')

            canvas.draw()
    
            # Schedule the function to be called again
            root.after(1, update_plot(n))
        
    update_plot(n)


# def stop_recording():
#     record_button = tk.Button(label_background, image=record_img, borderwidth=0, highlightthickness=0,command=lambda:start_recording())
#     record_button.place(x=400, y=320)
#     record_button.pack()
#     stop_record_button.pack_forget()




record_img = tk.PhotoImage(file="GUI/record_GUI_img/button/button_record_so_new.png")
stop_record_img = tk.PhotoImage(file="GUI/record_GUI_img/button/button_stop_so_new.png")

# ----------------------------------------------------------------------------
record_button = tk.Button(label_background, image = record_img, borderwidth=0, highlightthickness=0, command = start_stream)
record_button.place(x=870, y=410)














root.mainloop()


