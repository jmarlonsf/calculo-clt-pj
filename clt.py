class CLT:

    def __init__(self, salario_bruto, num_dependentes, outros_descontos, meses_trabalhado, percent_ppr):
        self.salario_bruto = salario_bruto
        self.num_dependentes = num_dependentes
        self.outros_descontos = outros_descontos
        self.meses_trabalhado = meses_trabalhado
        self.percent_ppr = percent_ppr

    def _calcular_inss(self, salario_bruto):
        # Tabela de alíquotas do INSS
        tabela_inss = {
            1320.00: (0, 0.075),
            2571.29: (1320.00, 0.09),
            3856.94: (2571.29, 0.12),
            7507.49: (3856.94, 0.14)
            # ,
            # float('inf'): (7507.49, 0.14)
        }

        # Cálculo do desconto do INSS
        inss = 0.0
        for faixa, (anterior, aliquota) in tabela_inss.items():
            if faixa >= salario_bruto > anterior:
                inss += round((salario_bruto - anterior) * aliquota, 2)
            elif salario_bruto > faixa:
                inss += round((faixa - anterior) * aliquota, 2)

        return inss

    def _calcular_irrf(self, salario_bruto, inss=0):
        # Tabela de alíquotas do IRRF
        tabela_irrf = {
            2112: (0.0, 0.0),
            2826.65: (0.075, 158.40),
            3751.05: (0.15, 370.40),
            4664.68: (0.225, 651.73),
            float('inf'): (0.275, 884.96)
        }

        # Cálculo do desconto do IRRF
        base_calculo_irrf = salario_bruto - inss - (self.num_dependentes * 189.59) - self.outros_descontos

        irrf = 0.0
        for faixa, (aliquota, parcela_dedutivel) in tabela_irrf.items():
            if base_calculo_irrf <= faixa:
                irrf = round((base_calculo_irrf * aliquota) - parcela_dedutivel, 2)
                break

        return irrf

    def calcular_base(self, salario):

        inss = self._calcular_inss(salario)

        irrf = self._calcular_irrf(salario, inss)

        # Cálculo do FGTS
        fgts = salario * 0.08

        # Cálculo do salário líquido
        salario_liquido = round(salario - inss - irrf, 2)

        return salario_liquido, inss, irrf, fgts

    def calcular_salario(self):
        # Cálculo do salário líquido

        return self.calcular_base(self.salario_bruto)

    def calcular_ferias(self):
        salario = (self.salario_bruto * meses_trabalhados) / 12 + self.salario_bruto / 3

        return self.calcular_base(salario)

    def calcular_prr(self):
        salario = ((self.salario_bruto * self.meses_trabalhado) / 12) * self.percent_ppr
        irrf = self._calcular_irrf(salario_bruto=salario)
        salario = salario - irrf
        return salario, irrf


if __name__ == '__main__':
    print("\n")
    salario_bruto = float(input("Informe o salário bruto: "))
    num_dependentes = int(input("Informe o número de dependentes: "))
    outros_descontos = float(input("Informe outros descontos (opcional): "))
    meses_trabalhados = float(input("Informe quantidade de meses a serem considerados: "))
    percent_ppr = float(input("Informe porcentagem estimada para a PPR: "))
    print("\n")

    clt = CLT(salario_bruto, num_dependentes, outros_descontos, meses_trabalhados, percent_ppr)

    salario_liquido, inss, irrf, fgts = clt.calcular_salario()
    print(f"Salário Líquido: R$ {salario_liquido}")
    print(f"Desconto INSS: R$ {inss}")
    print(f"Desconto IRRF: R$ {irrf}")
    print(f"Valor FGTS: R$ {fgts}")
    print("\n")
    salario_ferias, inss_ferias, irrf_ferias, fgts_ferias = clt.calcular_ferias()
    print(f"Salário Férias: R$ {salario_ferias}")
    print(f"Desconto INSS: R$ {inss_ferias}")
    print(f"Desconto IRRF: R$ {irrf_ferias}")
    print(f"Valor FGTS: R$ {fgts_ferias}")
    print("\n")
    salario_ppr, irrf_ppr = clt.calcular_prr()
    print(f"PPR: R$ {salario_ppr}")
    print(f"Desconto IRRF: R$ {irrf_ppr}")
    print("\n")

    print(f"""Salário Líquido: R$ {salario_liquido}
    em {meses_trabalhados} meses = R$ {salario_liquido * meses_trabalhados}
    + R$ {salario_ferias} (ferias)
    = R$ {round((salario_liquido * meses_trabalhados) + salario_ferias, 2)}
    + R$ {salario_ppr} (ppr)
    = R$ {round((salario_liquido * meses_trabalhados) + salario_ferias + salario_ppr, 2)}""")

    print(f"""Valor FGTS: R$ {fgts} 
    em R$ {meses_trabalhados} meses = R$ {fgts * meses_trabalhados}""")

    print(f"Desconto INSS: R$ {inss} em {meses_trabalhados} meses = {inss * meses_trabalhados}")
    print(f"Desconto IRRF: R$ {irrf} em {meses_trabalhados} meses = {irrf * meses_trabalhados}")
