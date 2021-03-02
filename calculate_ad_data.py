from math import log, pow

a = (8.91304*pow(10.0,-4.0))
b = (2.04041*pow(10.0,-4.0))
c = (7.4*pow(10.0,-8.0))

def calculate_V(D):
	return (D/51.0)
def calculate_bat_I(D):
	try:
		return ((5.0/6.0)*(D/51.0-2.5))
	except:
		return float('Nan')
def calculate_R(D):
	try:
		return ((-1.0*pow(10.0,5.0)*D)/(D-255.0))
	except:
		return float('Nan')
def calculate_T(D):
	try:
		return ((1.0/(a + b*log(calculate_R(D)) + c*pow(log(calculate_R(D)),3.0))) - 273.15)
	except:
		return float('Nan')
def calculate_solar_I_minus_y_dep(D):
    return (D/260.0)
def calculate_solar_I_plus_y_undep(D):
    return (D/200.0)
def calculate_solar_I_plus_x(D):
    return (D/82.0)
def calculate_solar_I_minus_x(D):
    return (D/82.0)
def calculate_solar_I_plus_y_dep(D):
    return (D/260.0)
def calculate_solar_I_minus_z(D):
    return (D/200.0)
def calculate_txCW_FM_I(D):
    return (D/(51.0*20.5*0.11))
def calculate_rx_modem_I(D):
    return (D/(51.0*20.5*1.0))
def calculate_mis5V_I(D):
	return (D/(51.0*82.5*0.06))
def calculate_mobc5V_I(D):
	return (D/(51.0*82.5*0.06))
def calculate_misbus_I(D):
	return (D/(51.0*8.2*0.1))
