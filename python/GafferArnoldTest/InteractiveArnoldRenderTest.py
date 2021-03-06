##########################################################################
#
#  Copyright (c) 2016, Image Engine Design Inc. All rights reserved.
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

import os
import unittest

import IECore

import GafferSceneTest
import GafferArnold

@unittest.skipIf( "TRAVIS" in os.environ, "No license available on Travis" )
class InteractiveArnoldRenderTest( GafferSceneTest.InteractiveRenderTest ) :

	def _createInteractiveRender( self ) :

		return GafferArnold.InteractiveArnoldRender()

	def _createConstantShader( self ) :

		shader = GafferArnold.ArnoldShader()
		shader.loadShader( "flat" )
		return shader, shader["parameters"]["color"]

	def _createMatteShader( self ) :

		shader = GafferArnold.ArnoldShader()
		shader.loadShader( "lambert" )
		shader["parameters"]["Kd"].setValue( 1 )
		return shader, shader["parameters"]["Kd_color"]

	def _cameraVisibilityAttribute( self ) :

		return "ai:visibility:camera"

	def _createPointLight( self ) :

		light = GafferArnold.ArnoldLight()

		with IECore.CapturingMessageHandler() as mh :
			light.loadShader( "point_light" )

		self.assertEqual( len( mh.messages ), 4 )
		for m in mh.messages :
			## \todo Remove once we've figured out what to do
			# with these parameters.
			self.assertTrue( "of type \"ARRAY\"" in m.message )

		return light, light["parameters"]["color"]

if __name__ == "__main__":
	unittest.main()
