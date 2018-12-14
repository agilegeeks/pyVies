from __future__ import unicode_literals, print_function

import re
import sys
import zeep
import pprint

VAT_NUMBER_REGEXPS = {
    'AT': re.compile(r'^U\d{8}$', re.IGNORECASE),
    'BE': re.compile(r'^\d{9,10}$'),
    'BG': re.compile(r'^\d{9,10}$'),
    'CY': re.compile(r'^\d{8}[a-z]$', re.IGNORECASE),
    'CZ': re.compile(r'^\d{8,10}$'),
    'DE': re.compile(r'^\d{9}$'),
    'DK': re.compile(r'^\d{8}$'),
    'EE': re.compile(r'^\d{9}$'),
    'ES': re.compile(r'^[\da-z]\d{7}[\da-z]$', re.IGNORECASE),
    'FI': re.compile(r'^\d{8}$'),
    'FR': re.compile(r'^[\da-hj-np-z]{2}\d{9}$', re.IGNORECASE),
    'GB': re.compile(r'^((\d{9})|(\d{12})|(GD\d{3})|(HA\d{3}))$',
                     re.IGNORECASE),
    'GR': re.compile(r'^\d{9}$'),
    'HR': re.compile(r'^\d{11}$'),
    'HU': re.compile(r'^\d{8}$'),
    'IE': re.compile(r'^((\d{7}[a-z])|(\d[a-z]\d{5}[a-z])|(\d{6,7}[a-z]{2}))$',
                     re.IGNORECASE),
    'IT': re.compile(r'^\d{11}$'),
    'LT': re.compile(r'^((\d{9})|(\d{12}))$'),
    'LU': re.compile(r'^\d{8}$'),
    'LV': re.compile(r'^\d{11}$'),
    'MT': re.compile(r'^\d{8}$'),
    'NL': re.compile(r'^\d{9}B\d{2,3}$', re.IGNORECASE),
    'PL': re.compile(r'^\d{10}$'),
    'PT': re.compile(r'^\d{9}$'),
    'RO': re.compile(r'^\d{2,10}$'),
    'SE': re.compile(r'^\d{12}$'),
    'SI': re.compile(r'^\d{8}$'),
    'SK': re.compile(r'^\d{10}$'),
}


class ViesValidationError(Exception):
    """
    Exception thrown by the Vies object when there is a
    validation problem.
    """
    pass


class ViesHTTPError(Exception):
    """
    Exception thrown by the Vies object when there is an
    HTTP error interacting with Vies.
    """
    pass


class ViesError(Exception):
    """
    Base Exception thrown by the Vies object when there is a
    general problem when interacting with Vies service.
    """
    pass


class Vies(object):
    WS_ENDPOINT = 'http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl'


    def __init__(self):
        super(Vies, self).__init__()

    def clean(self, vat_number, vat_country_code=None):
        try:
            vat_number = str(vat_number)
        except:
            ViesValidationError('Invalid VAT number provided')
        vat_number = vat_number.replace(' ', '')

        if vat_country_code is not None:
            try:
                vat_country_code = str(vat_country_code)
            except:
                ViesValidationError('Invalid VAT country provided')
            vat_country_code = vat_country_code.replace(' ', '')
            vat_country_code = vat_country_code.upper()

        # if no vat_country_code provided we try to extract it from vat_number
        else:
            try:
                vat_country_code = vat_number[:2]
            except:
                raise ViesValidationError('Invalid VAT number provided')

            vat_country_code = vat_country_code.upper()
            if vat_country_code== 'EL':
                vat_country_code = 'GR'
            else:
                vat_number = vat_number[2:]

        if vat_country_code not in VAT_NUMBER_REGEXPS.keys():
            raise ViesValidationError('Invalid VAT country')

        if len(vat_number)>2:
            if vat_number[:2].upper() == vat_country_code:
                vat_number = vat_number[2:]

        # validate the vat number against VAT_NUMBER_REGEXPS
        if not VAT_NUMBER_REGEXPS[vat_country_code].match(vat_number):
            raise ViesValidationError('Invalid VAT number')

        return vat_number,vat_country_code

    def request(self, vat_number, vat_country_code=None, extended_info=True):
        result = None

        vat_number,vat_country_code = self.clean(vat_number,vat_country_code)

        # check VIES
        try:
            client = zeep.Client(wsdl=self.WS_ENDPOINT)
        except Exception as e:
            raise ViesHTTPError('VIES service unreachable. %s' % str(e))

        try:
            if extended_info is True:
                result = client.service.checkVatApprox(vat_country_code, vat_number)
            else:
                result = client.service.checkVat(vat_country_code, vat_number)
        except Exception as e:
            raise ViesError('Got error from vies: %s' % str(e))


        return result


def console():

    def print_err(*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)

    if len(sys.argv) < 2:
        print_err("usage: %s <vat_number>\n" % sys.argv[0])
        sys.exit(-255)

    vat_number = sys.argv[1]

    try:
        vies = Vies()
        result = vies.request(vat_number)
    except Exception as e:
        if hasattr(e, 'message'):
            print_err(e.message)
        else:
            print_err(e)
    else:
        pp = pprint.PrettyPrinter(indent=8)
        pp.pprint(result)


if __name__ == '__main__':
    console()