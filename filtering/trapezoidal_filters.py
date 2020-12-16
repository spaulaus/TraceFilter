"""
file: trapezoidal_filters.py
brief:
author: S. V. Paulauskas
date: December 14, 2020
"""
from math import exp
from statistics import mean



def calculate_baseline(data, trigger, length):
    offset = trigger - length - 5
    if offset < 0:
        raise ValueError("First trigger happened too early to calculate the baseline!")
    return mean(data[:offset])


def calculate_energy_filter_coefficients(length, decay_constant):
    if decay_constant == 0:
        raise ValueError("Decay constant must be non-zero!")

    beta = exp(-1.0 / decay_constant)

    if beta == TypeError:
        raise beta

    cg = 1 - beta
    ctmp = 1 - pow(beta, length)

    return {'beta': beta, "rise": -(cg / ctmp) * pow(beta, length), "gap": cg, "fall": cg / ctmp}


def calculate_energy_filter_limits(trigger_position, length, gap, data_length):
    min_limit = trigger_position - length - 10
    if min_limit < 0:
        raise ValueError("Trigger happened too early in the trace to calculate the energy!")
    if trigger_position + length + gap > data_length:
        raise ValueError("Trigger happened too late in the trace to calculate the energy!")

    return {"rise": (min_limit, min_limit + length - 1),
            "gap": (min_limit + length, min_limit + length + gap - 1),
            "fall": (min_limit + length + gap, min_limit + 2 * length + gap - 1)}


def calculate_energy(data, baseline, coefficients, limits):
    data_without_baseline = [x - baseline for x in data]
    sum_rise = sum(data_without_baseline[limits['rise'][0]: limits['rise'][1]])
    sum_gap = sum(data_without_baseline[limits['gap'][0]: limits['gap'][1]])
    sum_fall = sum(data_without_baseline[limits['fall'][0]: limits['fall'][1]])

    return coefficients['rise'] * sum_rise + coefficients['gap'] * sum_gap + coefficients[
        'fall'] * sum_fall


def calculate_energy_filter(data, length, gap, baseline, coefficients):
    if not data:
        raise ValueError("Data length cannot be less than 0")

    offset = 2 * length + gap - 1

    if len(data) < offset:
        raise ValueError(f"The data length({len(data)}) is too small for the requested filter "
                         f"size ({offset})!")

    response = [0] * len(data)
    for x in range(offset, len(data)):
        esumL = [0] * len(data)
        for y in range(x - offset, x - offset + length):
            esumL[x] = esumL[x] + data[y] - baseline
        esumG = [0] * len(data)
        for y in range(x - offset + length, x - offset + length + gap):
            esumG[x] = esumG[x] + data[y] - baseline
        esumF = [0] * len(data)
        for y in range(x - offset + length + gap, x - offset + 2 * length + gap):
            esumF[x] = esumF[x] + data[y] - baseline

        response[x] = coefficients['rise'] * esumL[x] + coefficients['gap'] * esumG[x] + \
                      coefficients['fall'] * esumF[x]

    for x in range(0, offset):
        response[x] = response[offset]

    return response


def calculate_trigger_filter(data, length, gap, threshold):
    if not data:
        raise ValueError("Cannot calculate a filter without some data!")

    has_recrossed = False
    triggers = list()
    trigger_filter = list()
    for i in range(0, len(data)):
        if i - 2 * length - gap + 1 >= 0:
            trigger_filter.append((sum(data[i - length + 1: i + 1]) - sum(
                data[i - 2 * length - gap + 1: i - length - gap + 1])) / length)

            if trigger_filter[-1] >= threshold:
                if not triggers:
                    triggers.append(i)
                if has_recrossed:
                    triggers.append(i)
                    has_recrossed = False
            else:
                if triggers:
                    has_recrossed = True
        else:
            trigger_filter.append(0.0)

    if not triggers:
        raise ValueError("No triggers found in the provided data!")

    return triggers, trigger_filter



