def suavizar(actual, objetivo, alpha=0.35):

    return actual + (objetivo - actual) * alpha


def zona_muerta(actual, objetivo, zona=2):

    if abs(objetivo - actual) < zona:
        return actual

    return objetivo