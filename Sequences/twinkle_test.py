
import unittest
from twinkle import StarObject;

class TestStringMethods(unittest.TestCase):

	m_Star = None;
	
	def setUp(self):
		self.m_Star = StarObject(4,6,8,10,int("ff7f3f",16),2,20, 0);
 
	def tearDown(self):
		self.m_Star = None
				
	def test_split(self):
		commands = self.m_Star.handleTick(); self.assertEquals("fill 1,000000,20,1",commands);
		commands = self.m_Star.handleTick(); self.assertEquals("fill 1,000000,20,1",commands);
		
		commands = self.m_Star.handleTick(); self.assertEquals("fill 1,3f1f0f,20,1",commands);
		commands = self.m_Star.handleTick(); self.assertEquals("fill 1,7f3f1f,20,1",commands);
		commands = self.m_Star.handleTick(); self.assertEquals("fill 1,bf5f2f,20,1",commands);
		commands = self.m_Star.handleTick(); self.assertEquals("fill 1,ff7f3f,20,1",commands);
		
		commands = self.m_Star.handleTick(); self.assertEquals("fill 1,ff7f3f,20,1",commands);
		commands = self.m_Star.handleTick(); self.assertEquals("fill 1,ff7f3f,20,1",commands);
		commands = self.m_Star.handleTick(); self.assertEquals("fill 1,ff7f3f,20,1",commands);
		commands = self.m_Star.handleTick(); self.assertEquals("fill 1,ff7f3f,20,1",commands);
		commands = self.m_Star.handleTick(); self.assertEquals("fill 1,ff7f3f,20,1",commands);
		commands = self.m_Star.handleTick(); self.assertEquals("fill 1,ff7f3f,20,1",commands);
		
		commands = self.m_Star.handleTick(); self.assertEquals("fill 1,df6f37,20,1",commands);
		commands = self.m_Star.handleTick(); self.assertEquals("fill 1,bf5f2f,20,1",commands);
		commands = self.m_Star.handleTick(); self.assertEquals("fill 1,9f4f27,20,1",commands);
		commands = self.m_Star.handleTick(); self.assertEquals("fill 1,7f3f1f,20,1",commands);
		commands = self.m_Star.handleTick(); self.assertEquals("fill 1,5f2f17,20,1",commands);
		commands = self.m_Star.handleTick(); self.assertEquals("fill 1,3f1f0f,20,1",commands);
		commands = self.m_Star.handleTick(); self.assertEquals("fill 1,1f0f07,20,1",commands);
		commands = self.m_Star.handleTick(); self.assertEquals("fill 1,000000,20,1",commands);
		
		commands = self.m_Star.handleTick(); self.assertEquals("fill 1,000000,20,1",commands);
		commands = self.m_Star.handleTick(); self.assertEquals("fill 1,000000,20,1",commands);
		commands = self.m_Star.handleTick(); self.assertEquals("fill 1,000000,20,1",commands);
		commands = self.m_Star.handleTick(); self.assertEquals("fill 1,000000,20,1",commands);
		commands = self.m_Star.handleTick(); self.assertEquals("fill 1,000000,20,1",commands);
		commands = self.m_Star.handleTick(); self.assertEquals("fill 1,000000,20,1",commands);
		commands = self.m_Star.handleTick(); self.assertEquals("fill 1,000000,20,1",commands);
		commands = self.m_Star.handleTick(); self.assertEquals("fill 1,000000,20,1",commands);
		commands = self.m_Star.handleTick(); self.assertEquals("fill 1,000000,20,1",commands);
		commands = self.m_Star.handleTick(); self.assertEquals("fill 1,000000,20,1",commands);

		commands = self.m_Star.handleTick(); self.assertEquals("fill 1,3f1f0f,20,1",commands);

if __name__ == '__main__':
	unittest.main()
	
	
