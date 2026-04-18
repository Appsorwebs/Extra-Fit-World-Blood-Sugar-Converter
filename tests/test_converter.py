import sys

sys.path.insert(0, "..")

from blood_sugar_converter import convert_blood_sugar, get_interpretation


class TestBloodSugarConversion:
    """Test blood sugar conversion functions"""

    def test_mgdl_to_mmoll(self):
        """Test mg/dL to mmol/L conversion"""
        assert convert_blood_sugar(100, "mg/dL", "mmol/L") == 5.6
        assert convert_blood_sugar(180, "mg/dL", "mmol/L") == 10.0
        assert convert_blood_sugar(70, "mg/dL", "mmol/L") == 3.9

    def test_mmoll_to_mgdl(self):
        """Test mmol/L to mg/dL conversion"""
        assert convert_blood_sugar(5.5, "mmol/L", "mg/dL") == 99
        assert convert_blood_sugar(7.0, "mmol/L", "mg/dL") == 126
        assert convert_blood_sugar(3.9, "mmol/L", "mg/dL") == 70

    def test_same_unit(self):
        """Test same unit returns same value"""
        assert convert_blood_sugar(100, "mg/dL", "mg/dL") == 100
        assert convert_blood_sugar(5.5, "mmol/L", "mmol/L") == 5.5

    def test_boundary_values(self):
        """Test boundary values for each range"""
        assert convert_blood_sugar(69, "mg/dL", "mmol/L") == 3.8
        assert convert_blood_sugar(70, "mg/dL", "mmol/L") == 3.9
        assert convert_blood_sugar(99, "mg/dL", "mmol/L") == 5.5
        assert convert_blood_sugar(100, "mg/dL", "mmol/L") == 5.6
        assert convert_blood_sugar(125, "mg/dL", "mmol/L") == 6.9
        assert convert_blood_sugar(126, "mg/dL", "mmol/L") == 7.0


class TestInterpretation:
    """Test blood sugar interpretation"""

    def test_hypoglycemia_mgdl(self):
        """Test low blood sugar in mg/dL"""
        result, status, color = get_interpretation(50, "mg/dL")
        assert "Low" in result
        assert status == "warning"

    def test_normal_mgdl(self):
        """Test normal fasting in mg/dL"""
        result, status, color = get_interpretation(85, "mg/dL")
        assert "Normal" in result
        assert status == "success"

    def test_prediabetes_mgdl(self):
        """Test prediabetes in mg/dL"""
        result, status, color = get_interpretation(110, "mg/dL")
        assert "Prediabetes" in result
        assert status == "warning"

    def test_diabetes_mgdl(self):
        """Test diabetes in mg/dL"""
        result, status, color = get_interpretation(130, "mg/dL")
        assert "Diabetes" in result
        assert status == "error"

    def test_hypoglycemia_mmoll(self):
        """Test low blood sugar in mmol/L"""
        result, status, color = get_interpretation(3.0, "mmol/L")
        assert "Low" in result
        assert status == "warning"

    def test_normal_mmoll(self):
        """Test normal fasting in mmol/L"""
        result, status, color = get_interpretation(5.0, "mmol/L")
        assert "Normal" in result
        assert status == "success"

    def test_prediabetes_mmoll(self):
        """Test prediabetes in mmol/L"""
        result, status, color = get_interpretation(6.0, "mmol/L")
        assert "Prediabetes" in result
        assert status == "warning"

    def test_diabetes_mmoll(self):
        """Test diabetes in mmol/L"""
        result, status, color = get_interpretation(8.0, "mmol/L")
        assert "Diabetes" in result
        assert status == "error"

    def test_boundary_interpretations(self):
        """Test boundary values for interpretation"""
        result, status, color = get_interpretation(69, "mg/dL")
        assert "Low" in result

        result, status, color = get_interpretation(70, "mg/dL")
        assert "Normal" in result

        result, status, color = get_interpretation(99, "mg/dL")
        assert "Normal" in result

        result, status, color = get_interpretation(100, "mg/dL")
        assert "Prediabetes" in result

        result, status, color = get_interpretation(125, "mg/dL")
        assert "Prediabetes" in result

        result, status, color = get_interpretation(126, "mg/dL")
        assert "Diabetes" in result


if __name__ == "__main__":
    import pytest

    pytest.main([__file__, "-v"])
