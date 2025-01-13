from django.test import TestCase
from main import IraCalculator

class IraCalculatorTest(TestCase):
    def setUp(self):
        """
        Configuração inicial para todos os testes. Instancia o IraCalculator.
        """
        self.ira_calculator = IraCalculator()

    def test_number_of_credits_zero(self):
        """
        Teste com número de créditos igual a 0 (CD1 Verdadeiro), semestre igual a 0 (CD2 Verdadeiro) e menção igual a 'XYZ' (CD3 Verdadeiro).
        """
        disciplines = [{"grade": "XYZ", "number_of_credits": 0, "semester": 0}]
        with self.assertRaisesMessage(ValueError, "O número de créditos da disciplina é menor ou igual a 0."):
            self.ira_calculator.get_ira_value(disciplines)

    def test_number_of_credits_positive(self):
        """
        Teste com número de créditos positivo (CD1 Falso), semestre igual a 6 (CD2 Falso) e menção igual a 'SS' (CD3 Falso).
        """
        disciplines = [{"grade": "SS", "number_of_credits": 4, "semester": 3}]
        result = self.ira_calculator.get_ira_value(disciplines)
        self.assertEqual(result, 5.0)  # IRA esperado: 5.0

    def test_semester_minimum(self):
        """
        Teste com semestre mínimo válido (CD2 Falso), numero de creditos positivo e menção igual a 'MS' .
        """
        disciplines = [{"grade": "MS", "number_of_credits": 3, "semester": 1}]
        result = self.ira_calculator.get_ira_value(disciplines)
        self.assertEqual(result, 4.0)  # IRA esperado: 4.0

    def test_semester_below_minimum(self):
        """
        Teste com semestre abaixo do mínimo (CD2 Verdadeiro).
        """
        disciplines = [{"grade": "MS", "number_of_credits": 3, "semester": 0}]
        with self.assertRaisesMessage(ValueError, "O semestre está fora do intervalo delimitado entre 1 e 6."):
            self.ira_calculator.get_ira_value(disciplines)

    def test_semester_maximum(self):
        """
        Teste com semestre máximo válido (CD2 Falso).
        """
        disciplines = [{"grade": "MM", "number_of_credits": 2, "semester": 6}]
        result = self.ira_calculator.get_ira_value(disciplines)
        self.assertEqual(result, 3.0)  # IRA esperado: 3.0

    def test_semester_above_maximum(self):
        """
        Teste com semestre acima do máximo (CD2 Verdadeiro).
        """
        disciplines = [{"grade": "MM", "number_of_credits": 2, "semester": 7}]
        result = self.ira_calculator.get_ira_value(disciplines)
        self.assertEqual(result, 3.0)  # Semestre ajustado para 6

    def test_valid_grade(self):
        """
        Teste com menção válida (CD3 Falso).
        """
        disciplines = [{"grade": "SS", "number_of_credits": 3, "semester": 3}]
        result = self.ira_calculator.get_ira_value(disciplines)
        self.assertEqual(result, 5.0)  # IRA esperado: 5.0

    def test_invalid_grade(self):
        """
        Teste com menção inválida (CD3 Verdadeiro).
        """
        disciplines = [{"grade": "XYZ", "number_of_credits": 3, "semester": 3}]
        with self.assertRaisesMessage(ValueError, "A menção XYZ não existe."):
            self.ira_calculator.get_ira_value(disciplines)
