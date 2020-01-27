from datetime import datetime


class SeqCommand(object):
    @staticmethod
    def header_comment(sequence_type="None"):
        now = datetime.now()
        now_string = now.strftime("%d/%m/%Y @%H:%M")
        return (
            f"// Zurich Instruments sequencer program\n"
            f"// sequence type:              {sequence_type}\n"
            f"// automatically generated:    {now_string}\n\n"
        )

    @staticmethod
    def repeat(i):
        if i < 0:
            raise ValueError("Invalid number of repetitions!")
        return f"\nrepeat({int(i)}){{\n\n"

    @staticmethod
    def new_line():
        return "\n"

    @staticmethod
    def comment_line():
        return "//\n"

    @staticmethod
    def wait(i):
        if i < 0:
            raise ValueError("Wait time cannot be negative!")
        if i == 0:
            return ""
        else:
            return f"wait({int(i)});\n"

    @staticmethod
    def wait_wave():
        return "waitWave();\n"

    @staticmethod
    def trigger(value, index=1):
        if value not in [0, 1]:
            raise ValueError("Invalid Trigger Value!")
        if index not in [1, 2]:
            raise ValueError("Invalid Trigger Index!")
        return f"setTrigger({value << (index - 1)});\n"

    @staticmethod
    def count_waveform(i, n):
        return f"// waveform {i+1} / {n}\n"

    @staticmethod
    def play_wave():
        return "playWave(w_1, w_2);\n"

    @staticmethod
    def play_wave_scaled(amp1, amp2):
        if abs(amp1) > 1 or abs(amp2) > 1:
            raise ValueError("Amplitude cannot be larger than 1.0!")
        return f"playWave({amp1}*w_1, {amp2}*w_2);\n"

    @staticmethod
    def play_wave_indexed(i):
        if i < 0:
            raise ValueError("Invalid Waveform Index!")
        return f"playWave(w{i + 1}_1, w{i + 1}_2);\n"

    @staticmethod
    def play_wave_indexed_scaled(amp1, amp2, i):
        if i < 0:
            raise ValueError("Invalid Waveform Index!")
        if abs(amp1) > 1 or abs(amp2) > 1:
            raise ValueError("Amplitude cannot be larger than 1.0!")
        return f"playWave({amp1}*w{i+1}_1, {amp2}*w{i+2}_2);\n"

    @staticmethod
    def init_buffer_indexed(length, i):
        if length < 16 or i < 0:
            raise ValueError("Invalid Values for waveform buffer!")
        if length % 16:
            raise ValueError("Buffer Length has to be multiple of 16!")
        return (
            f"wave w{i + 1}_1 = randomUniform({length});\n"
            f"wave w{i + 1}_2 = randomUniform({length});\n"
        )

    @staticmethod
    def init_gauss(gauss_params):
        length, pos, width = gauss_params
        if length < 16:
            raise ValueError("Invalid Value for length!")
        if length % 16:
            raise ValueError("Length has to be multiple of 16!")
        if not (length > pos and length > width):
            raise ValueError("Length has to be larger than position and width!")
        if not (width > 0):
            raise ValueError("Values cannot be negative!")
        return (
            f"wave w_1 = gauss({length}, {pos}, {width});\n"
            f"wave w_2 = drag({length}, {pos}, {width});\n"
        )

    @staticmethod
    def init_gauss_scaled(amp, gauss_params):
        length, pos, width = gauss_params
        if abs(amp) > 1:
            raise ValueError("Amplitude cannot be larger than 1.0!")
        if length < 16:
            raise ValueError("Invalid Value for length!")
        if length % 16:
            raise ValueError("Length has to be multiple of 16!")
        if not (length > pos and length > width):
            raise ValueError("Length has to be larger than position and width!")
        if not (width > 0):
            raise ValueError("Values cannot be negative!")
        return (
            f"wave w_1 = {amp} * gauss({length}, {pos}, {width});\n"
            f"wave w_2 = {amp} * drag({length}, {pos}, {width});\n"
        )

    @staticmethod
    def init_readout_pulse(length, amps, frequencies, clk_rate=1.8e9):
        assert len(amps) == len(frequencies)
        assert abs(max(amps)) <= 1.0
        n_periods = [length * f / clk_rate for f in frequencies]
        n = len(n_periods)
        s = str()
        for i in range(n):
            s += f"wave w{i+1}_I = 1/{n} * sine({int(length)}, {amps[i]}, 0, {n_periods[i]});\n"
            s += f"wave w{i+1}_Q = 1/{n} * cosine({int(length)}, {amps[i]}, 0, {n_periods[i]});\n"
        s += "\n"
        if n > 1:
            s += (
                f"wave w_1 = add(" + ", ".join([f"w{i+1}_I" for i in range(n)]) + ");\n"
            )
            s += (
                f"wave w_2 = add(" + ", ".join([f"w{i+1}_Q" for i in range(n)]) + ");\n"
            )
        else:
            s += "wave w_1 = w1_I;\n"
            s += "wave w_2 = w1_Q;\n"
        s += "\n"
        return s

    @staticmethod
    def close_bracket():
        return "\n}"

    @staticmethod
    def wait_dig_trigger(index=0):
        if index not in [0, 1, 2]:
            raise ValueError("Invalid Trigger Index!")
        if index == 0:
            return "waitDigTrigger(1);\n"
        else:
            return f"waitDigTrigger({index}, 1);\n"

    @staticmethod
    def init_trigger(target="hdawg"):
        if target == "hdawg":
            return "setTrigger(0);"
        elif target == "uhfqa":
            return "var RO_TRIGGER = AWG_INTEGRATION_ARM + AWG_INTEGRATION_TRIGGER + AWG_MONITOR_TRIGGER;\n"
        else:
            raise Exception("Not a valid target device!!")

    @staticmethod
    def readout_trigger():
        return "setTrigger(RO_TRIGGER);\n"