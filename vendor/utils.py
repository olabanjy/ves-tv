from .models import *


from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from django.core.files import File

from xhtml2pdf import pisa





def create_and_save_contract(template_src, filename, contract_id, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    contract = Contracts.objects.get(id=contract_id)
    print(contract.vendor)
    if not pdf.err:
        with open(filename, 'wb+') as output:
            pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), output)
            contract.contract_file.save(filename, output)
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None