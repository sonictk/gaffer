##########################################################################
#  
#  Copyright (c) 2012, John Haddon. All rights reserved.
#  
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#  
#      * Redistributions of source code must retain the above
#        copyright notice, this list of conditions and the following
#        disclaimer.
#  
#      * Redistributions in binary form must reproduce the above
#        copyright notice, this list of conditions and the following
#        disclaimer in the documentation and/or other materials provided with
#        the distribution.
#  
#      * Neither the name of John Haddon nor the names of
#        any other contributors to this software may be used to endorse or
#        promote products derived from this software without specific prior
#        written permission.
#  
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#  
##########################################################################

import unittest

import IECore

import Gaffer
import GafferScene

class DisplaysTest( unittest.TestCase ) :

	def test( self ) :
	
		p = GafferScene.Plane()
		displays = GafferScene.Displays( inputs = { "in" : p["out"] } )
	
		# check that the scene hierarchy is passed through
	
		self.assertEqual( displays["out"].object( "/" ), None )
		self.assertEqual( displays["out"].transform( "/" ), IECore.M44f() )
		self.assertEqual( displays["out"].bound( "/" ), IECore.Box3f( IECore.V3f( -0.5, -0.5, 0 ), IECore.V3f( 0.5, 0.5, 0 ) ) )
		self.assertEqual( displays["out"].childNames( "/" ), IECore.StringVectorData( [ "plane" ] ) )
		
		self.assertEqual( displays["out"].object( "/plane" ), IECore.MeshPrimitive.createPlane( IECore.Box2f( IECore.V2f( -0.5 ), IECore.V2f( 0.5 ) ) ) )
		self.assertEqual( displays["out"].transform( "/plane" ), IECore.M44f() )
		self.assertEqual( displays["out"].bound( "/plane" ), IECore.Box3f( IECore.V3f( -0.5, -0.5, 0 ), IECore.V3f( 0.5, 0.5, 0 ) ) )
		self.assertEqual( displays["out"].childNames( "/plane" ), None )
		
		# check that we have some displays
		
		display = displays.addDisplay( "beauty.exr", "exr", "rgba" )
		display["parameters"].addParameter( "test", IECore.FloatData( 10 ) )

		displays.addDisplay( "diffuse.exr", "exr", "color aov_diffuse" )
		
		g = displays["out"]["globals"].getValue()
		self.assertEqual( len( g ), 2 )
		self.assertEqual( g[0], IECore.Display( "beauty.exr", "exr", "rgba", { "test" : 10.0 } ) )
		self.assertEqual( g[1], IECore.Display( "diffuse.exr", "exr", "color aov_diffuse" ) )
	
	def testSerialisation( self ) :
	
		s = Gaffer.ScriptNode()
		s["displaysNode"] = GafferScene.Displays()
		display = s["displaysNode"].addDisplay( "beauty.exr", "exr", "rgba" )
		display["parameters"].addParameter( "test", IECore.FloatData( 10 ) )
		
		ss = s.serialise()
		
		s2 = Gaffer.ScriptNode()		
		s2.execute( ss )
		
		g = s2["displaysNode"]["out"]["globals"].getValue()
		self.assertEqual( len( g ), 1 )
		self.assertEqual( g[0], IECore.Display( "beauty.exr", "exr", "rgba", { "test" : 10.0 } ) )
		
if __name__ == "__main__":
	unittest.main()
