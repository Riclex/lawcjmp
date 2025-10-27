from docx import Document

T=r'c:\Users\ricki\Documents\Freelance\Projects\Marlene\gerador\contract_template.docx'

text = '''CONTRATO DE ARRENDAMENTO URBANO

Para fins Habitacionais

ENTRE
     {{senhorio}}
 E
				{{inquilino}}


2025
CONTRATO DE ARRENDAMENTO URBANO
Para fins Habitacionais  
ENTRE:

{{senhorio}}, sociedade registada ao abrigo das leis Angolana, com sede social na Rua {{senhorio_address}} com número contribuinte n.º{{senhorio_nif}}, representada neste acto pelo Sr. {{representative_name}}, na qualidade de Gerente, com poderes para o acto, doravante designado, abreviadamente “SENHORIO”.

E

{{inquilino}}, pessoa singular, portador do {{document_type}} {{document_number}}, emitido em {{document_issue_date}}, válido até {{document_expiry_date}}, NIF {{inquilino_nif}}, adiante abreviadamente designado por ARRENDATÁRIO.

Individualmente designadas por “Parte” e colectivamente por “Partes”

CONSIDERANDO QUE:
O SENHORIO declara ser o dono e legítimo proprietário do {{endereco_imovel}}, na província de Luanda, destinado a habitação de ora em diante simplesmente designado como o “imóvel", conforme Anexos I (Planta);

CLÁUSULA SEGUNDA
  (Vigência)
 O contrato terá o prazo de 1(um) ano com início à {{start_date_written}} à {{end_date_written}}, sendo automaticamente renovável por períodos sucessivos de iguais períodos.

CLÁUSULA TERCEIRA
(Renda e Formas de Pagamento)
As Partes acordam um valor mensal da renda devida pela utilização da fracção é o equivalente AOA {{valor_renda}} de kwanzas), mensal, sobre o valor terá a retenção do imposto, IP equivalente a 15%, e todos impostos determinado por lei, inerentes ao contrato, que estará ao encargo do SENHORIO realizar as retenções.

O pagamento da renda será efectuado {{forma_pagamento}} o equivalente a AOA {{valor_renda}} (--------- de kwanzas), nos primeiros 8 dias úteis. 

Sobre o valor mensal da renda ainda terá de ser pago o montante equivalente á AOA {{valor_caucao}} (----------de kwanzas), correspondente à caução a mesma serve para garantia do bom e pontual cumprimento das obrigações do presente contrato.

CLÁUSULA QUARTA
(Encargos)
A taxa de condomínio a data presente é equivalente à AOA {{taxa_condominio}} (----------------------------- kwanzas), podendo ser alterada nos termos do regulamento interno e aprovação em Assembleia do Condomínio.


Luanda, aos {{contract_date_local}}

P/SENHORIO                                                                              P/ ARRENDATÁRIO 

__________________________                    	____________________________
'''

doc = Document()
for p in text.split('\n\n'):
    doc.add_paragraph(p)

doc.save(T)
print('Template created at', T)
