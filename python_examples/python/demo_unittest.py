# python unittest
# see also https://docs.python.org/2/library/unittest.html
from __future__ import print_function, division
import unittest
from demo_class import Dog, Poodle # to be tested


class TestClassDog(unittest.TestCase):
    """test cases for classes Dog and Poodle"""
    def setUp(self): # this method is called before every test
        self.dog = Dog()
        self.poodle = Poodle(50,"brown")
        
    def tearDown(self): # this method is executed after every test
        del self.dog
        del self.poodle
        
    def testLegs(self):
        self.assertEqual(self.dog.numberOfLegs, 4, "number of legs not 4")
        
    def testPoodleInit(self):
        self.assertEqual(self.poodle.color, "brown", "color of poodle is not brown")
        self.assertEqual(self.poodle.height, 50, "height of poodle is not 50")
        
    def testAccident(self):
        self.poodle.Accident()
        self.assertEqual(self.poodle.numberOfLegs, 3, "number of legs after accident is not 3")
        
    def testSetColorException(self):
        self.assertRaises(ValueError, self.dog.SetColor, 5) # method call self.dog.SetColor(5) should raise a ValueError
        
    def testLessThanOperator(self):
        poodle2 = Poodle(45,"white")
        self.assertTrue(poodle2 < self.poodle, "poodle2 is not smaller than self.poodle")
