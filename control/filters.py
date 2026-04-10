def limitar_velocidad(actual, objetivo, paso=4):

    if objetivo > actual + paso:
        return actual + paso

    if objetivo < actual - paso:
        return actual - paso

    return objetivo


def zona_muerta(actual, objetivo, zona=3):

    if abs(objetivo - actual) < zona:
        return actual

    return objetivo