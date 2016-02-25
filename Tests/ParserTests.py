import unittest
from Parser import Parser

class ParserTests(unittest.TestCase):
    def test_parser_returns_query_if_given_single_query(self):
        parser = Parser()
        output = parser.parse("SELECT 1")
        self.assertTrue(len(output) == 1)

    def test_parser_splits_queries_on_semicolon(self):
        parser = Parser()
        output = parser.parse("SELECT 1 ; Select 2")
        self.assertTrue(len(output) == 2)
        self.assertEqual(" Select 2", output[-1].query)

    def test_parser_splits_out_ctes(self):
        parser = Parser()
        output = parser.parse("with test_cte as ( SELECT 1 )  Select 2")
        self.assertEqual(len(output), 2)
        self.assertEqual(output[0].query, "SELECT 1".lower())

    def test_parser_cte_identifies_final_query(self):
        parser = Parser()
        output = parser.parse("with test_cte as ( SELECT 1 )  Select 2")
        self.assertEqual(len(output), 2)
        self.assertEqual(output[1].query, "SELECT 2".lower())

    def test_parser_can_identify_multiple_ctes(self):
        parser = Parser()
        output = parser.parse("with test_cte as ( SELECT 1 ) , test_cte2 as ( SELECT 3 )  Select 2")
        self.assertEqual(len(output), 3)
        self.assertEqual(output[0].query, "SELECT 1".lower())
        self.assertEqual(output[1].query, "SELECT 3".lower())
        self.assertEqual(output[2].query, "SELECT 2".lower())

    def test_parser_can_handle_minimal_whitespace(self):
        parser = Parser()
        output = parser.parse("with test_cte as (SELECT 1),test_cte2 as (SELECT 3 )  Select 2")
        self.assertEqual(len(output), 3)
        self.assertEqual(output[0].query, "SELECT 1".lower())
        self.assertEqual(output[1].query, "SELECT 3".lower())
        self.assertEqual(output[2].query, "SELECT 2".lower())

    def test_parse_identified_cte_names(self):
        parser = Parser()
        output = parser.parse("with test_cte as (SELECT 1),test_cte2 as (SELECT 3 )  Select 2")
        self.assertEqual(output[0].name, "test_cte".lower())
        self.assertEqual(output[1].name, "test_cte2".lower())
        self.assertEqual(output[2].name, "final query".lower())

    def test_parse_identified_dependency(self):
        parser = Parser()
        output = parser.parse("with test_cte as (SELECT 1),test_cte2 as (SELECT 3 )  Select * from test_cte")
        self.assertTrue("test_cte" in output[-1].dependencies)
        
if __name__ == '__main__':
    unittest.main()
